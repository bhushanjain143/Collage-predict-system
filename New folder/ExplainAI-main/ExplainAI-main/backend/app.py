from flask import Flask, request, jsonify, session, send_from_directory, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os
import re
import json
import bcrypt
from datetime import datetime

from llm_service import (
    get_ai_public_config,
    run_batch_card_insights,
    run_counselor_chat,
    run_llm_task,
    run_scholarship_apply_guide,
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'explainai-stable-dev-key-2025')

# Allow credentials for session cookies
CORS(app, supports_credentials=True, origins=[
    "http://127.0.0.1:5500", "http://localhost:5500",
    "http://127.0.0.1:5000", "http://localhost:5000",
    "http://127.0.0.1:8000", "http://localhost:8000",
    "null"  # file:// origin during local dev
])

# Database: set DATABASE_URL, or use SQLite under backend/instance/
_backend_dir = os.path.abspath(os.path.dirname(__file__))
_instance_dir = os.path.join(_backend_dir, 'instance')
os.makedirs(_instance_dir, exist_ok=True)
_default_sqlite = 'sqlite:///' + os.path.join(_instance_dir, 'explainai.db').replace('\\', '/')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or _default_sqlite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False

db = SQLAlchemy(app)



def _normalize_identifier(identifier: str) -> str:
    return (identifier or "").strip()


def _is_email(identifier: str) -> bool:
    return bool(re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", identifier))


def _is_phone(identifier: str) -> bool:
    digits = re.sub(r"\D", "", identifier)
    return 10 <= len(digits) <= 15



def _hash_password(password: str) -> str:
    """Hash password using bcrypt — secure, with automatic unique salt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def _verify_password(password: str, hashed: str) -> bool:
    """Check plain password against stored bcrypt hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


# ── Models ─────────────────────────────────────────────────────────────────────

class User(db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    full_name  = db.Column(db.String(200), nullable=False)
    email      = db.Column(db.String(200), unique=True, nullable=False)
    phone      = db.Column(db.String(20), nullable=True)
    password   = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'phone': self.phone or '',
        }


class Cutoff(db.Model):
    __tablename__ = 'cutoffs'
    id                 = db.Column(db.Integer, primary_key=True)
    college_name       = db.Column(db.String(200))
    branch             = db.Column(db.String(300))   # FIX: was 100 — long branch names were silently truncated
    seat_type          = db.Column(db.String(30))
    closing_percentile = db.Column(db.Float)
    year               = db.Column(db.Integer)
    round              = db.Column(db.Integer, default=3)
    city               = db.Column(db.String(500))
    college_type       = db.Column(db.String(500))
    college_code       = db.Column(db.String(20))


# ── UserLike Model ─────────────────────────────────────────────────────────────

class UserLike(db.Model):
    __tablename__ = 'user_likes'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    college_name = db.Column(db.String(200), nullable=False)
    branch       = db.Column(db.String(300), nullable=False)  # FIX: was 100
    liked_at     = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'college_name': self.college_name,
            'branch':       self.branch,
            'liked_at':     self.liked_at.isoformat() if self.liked_at else None,
        }


# ── UserDislike Model ──────────────────────────────────────────────────────────

class UserDislike(db.Model):
    __tablename__ = 'user_dislikes'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    college_name = db.Column(db.String(200), nullable=False)
    branch       = db.Column(db.String(300), nullable=False)  # FIX: was 100
    disliked_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':           self.id,
            'college_name': self.college_name,
            'branch':       self.branch,
            'disliked_at':  self.disliked_at.isoformat() if self.disliked_at else None,
        }


# ── Scholarship Model ──────────────────────────────────────────────────────────

class Scholarship(db.Model):
    __tablename__ = 'scholarships'
    id                  = db.Column(db.Integer, primary_key=True)
    name                = db.Column(db.String(300))
    source              = db.Column(db.String(100))
    portal_url          = db.Column(db.String(500))
    amount_text         = db.Column(db.String(150))
    max_income          = db.Column(db.Integer,   default=999999999)
    min_percentage      = db.Column(db.Float,     default=0)
    categories          = db.Column(db.ARRAY(db.String))
    gender              = db.Column(db.String(15), default='Any')
    domicile_required   = db.Column(db.String(20), default='any')
    disability_required = db.Column(db.Boolean,   default=False)
    minority_required   = db.Column(db.Boolean,   default=False)
    years_eligible      = db.Column(db.ARRAY(db.Integer))
    deadline_open       = db.Column(db.Date)
    deadline_close      = db.Column(db.Date)
    documents           = db.Column(db.ARRAY(db.String))
    is_active           = db.Column(db.Boolean,   default=True)
    is_date_confirmed   = db.Column(db.Boolean,   default=True)  # False = estimated date, not officially announced


# ── UserScholarshipDislike Model ───────────────────────────────────────────────

class UserScholarshipDislike(db.Model):
    __tablename__ = 'user_scholarship_dislikes'
    id             = db.Column(db.Integer, primary_key=True)
    user_id        = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    scholarship_id = db.Column(db.Integer, db.ForeignKey('scholarships.id'), nullable=False)
    disliked_at    = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.UniqueConstraint('user_id', 'scholarship_id'),)


class SavedPrediction(db.Model):
    """Logged-in user's saved counselling runs (shortlist snapshot)."""
    __tablename__ = 'saved_predictions'
    id           = db.Column(db.Integer, primary_key=True)
    user_id      = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title        = db.Column(db.String(200), default='College prediction run')
    payload_json = db.Column(db.Text, nullable=False)
    created_at   = db.Column(db.DateTime, default=datetime.utcnow)

    def to_list_item(self):
        try:
            payload = json.loads(self.payload_json) if self.payload_json else {}
        except json.JSONDecodeError:
            payload = {}
        colleges = payload.get('colleges') or []
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'percentile': payload.get('form', {}).get('percentile'),
            'category': payload.get('form', {}).get('category'),
            'college_count': len(colleges),
        }


# ── Seat type mapping ──────────────────────────────────────────────────────────
# Maps frontend category values → MHT-CET seat type code prefixes
CATEGORY_CODE_MAP = {
    'OPEN': 'OPEN',
    'OBC':  'OBC',
    'SC':   'SC',
    'ST':   'ST',
    'EWS':  'SEBC',   # EWS / SEBC maps to SEBC in the official data
    'SEBC': 'SEBC',
    'VJNT': 'VJ',     # VJ/NT (Vimukta Jati & Nomadic Tribes)
    'NT1':  'NT1',
    'NT2':  'NT2',
    'NT3':  'NT3',
}

# Categories that are eligible for reserved seats only (not OPEN)
_OPEN_ONLY_CATS = {'OPEN',}


def get_eligible_seat_types(category, gender):
    """
    Return ALL seat type codes this student may compete for.

    KEY FIX: SC / ST / OBC / NT / VJ students are eligible for:
      1. Their own reserved category seats  (e.g. GSCS, GSCH, GSCO)
      2. OPEN / General category seats      (e.g. GOPENS, GOPENH, GOPENO)
      3. TFWS (Tuition Fee Waiver Scheme)   — added by caller

    Without this, reserved-category students with low percentiles get zero
    results because the backend was only searching their reserved seat rows,
    completely ignoring the many OPEN-seat rows with lower cutoffs that they
    are legally entitled to fill.

    Suffixes in MHT-CET data:
      H = Home University seats (preference to home-university candidates)
      O = Other University / Outside seats
      S = State-level seats (all Maharashtra)
    """
    cat = category.upper().replace(' ', '').replace('/', '')

    cat_code = CATEGORY_CODE_MAP.get(cat, cat)
    suffixes = ['H', 'O', 'S']
    # G = General (all genders); L = Ladies seats (females can use both G and L)
    prefixes = ['G'] + (['L'] if gender == 'Female' else [])

    # Reserved-category seats for this student
    seat_types = [f"{p}{cat_code}{s}" for p in prefixes for s in suffixes]

    # Reserved-category students are ALSO eligible to compete for OPEN seats
    if cat not in _OPEN_ONLY_CATS:
        open_seats = [f"{p}OPEN{s}" for p in prefixes for s in suffixes]
        seat_types = seat_types + open_seats

    return seat_types


with app.app_context():
    db.create_all()


def get_session_user():
    # Primary: session cookie
    user_id = session.get('user_id')
    # Fallback: X-User-Id header (sent by frontend when file:// blocks cookies)
    if not user_id:
        user_id = request.headers.get('X-User-Id')
    if not user_id:
        return None
    try:
        return db.session.get(User, int(user_id))
    except Exception:
        return None


# ── Static site root (parent of /backend) for single-origin deploys ───────────
_SITE_ROOT = os.path.abspath(os.path.join(_backend_dir, '..'))


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.route('/')
def home():
    index_path = os.path.join(_SITE_ROOT, 'index.html')
    if os.path.isfile(index_path):
        return send_from_directory(_SITE_ROOT, 'index.html')
    return jsonify({
        'message': 'ExplainAI API is running',
        'hint': 'Open index.html from the project root, or deploy with static files beside /backend.',
    })


@app.route('/api/test')
def test():
    return {"message": "Hello from Flask!"}


@app.route('/api/config')
def public_config():
    count_2025 = Cutoff.query.filter(Cutoff.year == 2025).count()
    data_year = 2025 if count_2025 > 0 else 2024
    row_count = Cutoff.query.filter(Cutoff.year == data_year).count()
    ai = get_ai_public_config()
    return jsonify({
        'status': 'success',
        'app_name': 'ExplainAI — MHT-CET college predictor & counselling',
        'data_year': data_year,
        'cutoff_rows_approx': row_count,
        'ai_enabled': ai['ai_enabled'],
        'ai_provider': ai['provider'],
        'ai_tasks': ai['tasks'],
    })


@app.route('/api/ai/explain', methods=['POST'])
def ai_explain():
    data = request.get_json(silent=True) or {}
    task = (data.get('task') or 'explain_list').strip()
    if task not in ('explain_list', 'compare', 'guidance'):
        task = 'explain_list'
    ctx = {
        'percentile': data.get('percentile'),
        'category': data.get('category'),
        'city': data.get('city'),
    }
    colleges = data.get('colleges')
    compare_pair = data.get('compare_pair')
    if not isinstance(colleges, list):
        colleges = []
    if compare_pair is not None and not isinstance(compare_pair, list):
        compare_pair = None
    out = run_llm_task(task, ctx, colleges, compare_pair)
    return jsonify({
        'status': out.get('status', 'ok'),
        'text': out.get('text', ''),
        'provider': out.get('provider'),
        'error': out.get('error'),
    })


@app.route('/api/ai/chat', methods=['POST'])
def ai_counselor_chat():
    data = request.get_json(silent=True) or {}
    percentile = data.get('percentile')
    category = data.get('category')
    city = data.get('city')
    user_question = (data.get('question') or '').strip()
    colleges = data.get('colleges')
    history = data.get('history')
    if not isinstance(colleges, list):
        colleges = []
    if not isinstance(history, list):
        history = []
    history = [h for h in history if isinstance(h, dict) and h.get('role') and h.get('content')]
    out = run_counselor_chat(percentile, category, colleges, user_question, history, city=city)
    return jsonify({
        'status': out.get('status', 'ok'),
        'text': out.get('text', ''),
        'provider': out.get('provider'),
        'error': out.get('error'),
    })


@app.route('/api/ai/card-insights', methods=['POST'])
def ai_card_insights():
    data = request.get_json(silent=True) or {}
    percentile = data.get('percentile')
    category = data.get('category')
    colleges = data.get('colleges')
    if not isinstance(colleges, list):
        colleges = []
    out = run_batch_card_insights(percentile, category, colleges)
    return jsonify({
        'status': out.get('status', 'ok'),
        'text': out.get('text', ''),
        'provider': out.get('provider'),
        'error': out.get('error'),
    })


@app.route('/api/ai/scholarship-guide', methods=['POST'])
def ai_scholarship_guide():
    data = request.get_json(silent=True) or {}
    name = (data.get('name') or '').strip()
    if not name:
        return jsonify({'status': 'error', 'error': 'name is required'}), 400
    url = (data.get('portal_url') or data.get('url') or '').strip()
    documents = data.get('documents')
    if not isinstance(documents, list):
        documents = []
    category = (data.get('category') or '').strip() or 'General'
    out = run_scholarship_apply_guide(name, url, documents, category)
    return jsonify({
        'status': out.get('status', 'ok'),
        'text': out.get('text', ''),
        'provider': out.get('provider'),
        'error': out.get('error'),
    })


@app.route('/api/predictions', methods=['GET'])
def list_predictions():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401
    rows = (
        SavedPrediction.query.filter_by(user_id=user.id)
        .order_by(SavedPrediction.created_at.desc())
        .limit(50)
        .all()
    )
    return jsonify({'status': 'success', 'predictions': [r.to_list_item() for r in rows]})


@app.route('/api/predictions', methods=['POST'])
def save_prediction():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401
    data = request.get_json(silent=True) or {}
    form = data.get('form')
    colleges = data.get('colleges')
    if not isinstance(form, dict) or not isinstance(colleges, list):
        return jsonify({'status': 'error', 'error': 'Invalid body: need form (object) and colleges (array).'}), 400
    title = (data.get('title') or 'College prediction run').strip()[:200]
    payload = {'form': form, 'colleges': colleges[:60]}
    row = SavedPrediction(
        user_id=user.id,
        title=title,
        payload_json=json.dumps(payload, ensure_ascii=False)[:500000],
    )
    db.session.add(row)
    db.session.commit()
    return jsonify({'status': 'success', 'id': row.id})


# ── Register ───────────────────────────────────────────────────────────────────

@app.route('/api/auth/register', methods=['POST'])
def register():
    data      = request.get_json(silent=True) or {}
    full_name = (data.get('full_name', '') or '').strip()
    email     = (data.get('email', '') or '').strip().lower()
    phone     = (data.get('phone', '') or '').strip()
    password  = (data.get('password', '') or '')
    confirm   = (data.get('confirm_password', '') or '')

    if not full_name or len(full_name) < 2:
        return jsonify({'status': 'error', 'field': 'full_name',
                        'error': 'Full name is required (at least 2 characters).'}), 400
    if not _is_email(email):
        return jsonify({'status': 'error', 'field': 'email',
                        'error': 'Enter a valid email address.'}), 400
    if phone and not _is_phone(phone):
        return jsonify({'status': 'error', 'field': 'phone',
                        'error': 'Enter a valid 10-digit phone number.'}), 400
    if len(password) < 8:
        return jsonify({'status': 'error', 'field': 'password',
                        'error': 'Password must be at least 8 characters.'}), 400
    if not re.search(r'[A-Za-z]', password) or not re.search(r'[0-9]', password):
        return jsonify({'status': 'error', 'field': 'password',
                        'error': 'Password must contain both letters and numbers.'}), 400
    if password != confirm:
        return jsonify({'status': 'error', 'field': 'confirm_password',
                        'error': 'Passwords do not match.'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'status': 'error', 'field': 'email',
                        'error': 'An account with this email already exists.'}), 409

    user = User(full_name=full_name, email=email,
                phone=phone or None, password=_hash_password(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({'status': 'success',
                    'message': 'Registration successful. Please login to continue.'})


# ── Login ──────────────────────────────────────────────────────────────────────

@app.route('/api/auth/login', methods=['POST'])
def login():
    data       = request.get_json(silent=True) or {}
    identifier = (data.get('identifier', '') or '').strip().lower()
    password   = (data.get('password', '') or '')

    if not identifier:
        return jsonify({'status': 'error', 'error': 'Email is required.'}), 400
    if not password:
        return jsonify({'status': 'error', 'error': 'Password is required.'}), 400

    user = User.query.filter_by(email=identifier).first()
    if not user:
        return jsonify({'status': 'error', 'error': 'No account found with this email. Please register first.'}), 401
    if not _verify_password(password, user.password):
        return jsonify({'status': 'error', 'error': 'Incorrect password. Please try again.'}), 401

    session.clear()
    session['user_id'] = user.id
    session.permanent = True

    return jsonify({'status': 'success', 'user': user.to_dict()})


# ── Session check ──────────────────────────────────────────────────────────────

@app.route('/api/auth/me', methods=['GET'])
def me():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'unauthenticated'}), 401
    return jsonify({'status': 'success', 'user': user.to_dict()})


# ── Logout ─────────────────────────────────────────────────────────────────────

@app.route('/api/auth/logout', methods=['POST'])
def logout_route():
    session.clear()
    return jsonify({'status': 'success', 'message': 'Logged out.'})


# ── Reset Password ─────────────────────────────────────────────────────────────

@app.route('/api/auth/reset-password', methods=['POST', 'OPTIONS'])
def reset_password():
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data         = request.get_json(silent=True) or {}
    email        = (data.get('email', '') or '').strip().lower()
    new_password = (data.get('new_password', '') or '')

    # Validate email format
    if not _is_email(email):
        return jsonify({'status': 'error', 'error': 'Enter a valid email address.'}), 400

    # Validate password length
    if len(new_password) < 8:
        return jsonify({'status': 'error', 'error': 'Password must be at least 8 characters.'}), 400

    # Check if user exists
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({
            'status': 'not_found',
            'error': 'user_not_found'
        }), 404

    # Update the password
    user.password = _hash_password(new_password)
    db.session.commit()

    return jsonify({
        'status': 'success',
        'message': 'Password reset successfully. Please login with your new password.'
    })


# ── User Likes API ─────────────────────────────────────────────────────────────

@app.route('/api/likes', methods=['POST'])
def save_like():
    """Save a liked college for the logged-in user."""
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in. Please sign in first.'}), 401

    data         = request.get_json(silent=True) or {}
    college_name = (data.get('college_name') or '').strip()
    branch       = (data.get('branch') or '').strip()

    if not college_name or not branch:
        return jsonify({'status': 'error', 'error': 'college_name and branch are required.'}), 400

    # Avoid duplicate likes from same user for same college+branch
    existing = UserLike.query.filter_by(
        user_id=user.id,
        college_name=college_name,
        branch=branch
    ).first()

    if existing:
        return jsonify({'status': 'already_liked', 'message': 'Already liked.'})

    like = UserLike(user_id=user.id, college_name=college_name, branch=branch)
    db.session.add(like)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'College liked!', 'like': like.to_dict()})


@app.route('/api/likes', methods=['DELETE'])
def remove_like():
    """Remove a liked college for the logged-in user."""
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401

    data         = request.get_json(silent=True) or {}
    college_name = (data.get('college_name') or '').strip()
    branch       = (data.get('branch') or '').strip()

    like = UserLike.query.filter_by(
        user_id=user.id,
        college_name=college_name,
        branch=branch
    ).first()

    if not like:
        return jsonify({'status': 'not_found', 'message': 'Like not found.'})

    db.session.delete(like)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'College removed from likes.'})


@app.route('/api/likes', methods=['GET'])
def get_likes():
    """Get all liked colleges for the logged-in user."""
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401

    likes = UserLike.query.filter_by(user_id=user.id).order_by(UserLike.liked_at.desc()).all()
    return jsonify({'status': 'success', 'likes': [l.to_dict() for l in likes], 'total': len(likes)})


# ── User Dislikes API ──────────────────────────────────────────────────────────

@app.route('/api/dislikes', methods=['POST'])
def save_dislike():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in. Please sign in first.'}), 401
    data         = request.get_json(silent=True) or {}
    college_name = (data.get('college_name') or '').strip()
    branch       = (data.get('branch') or '').strip()
    if not college_name or not branch:
        return jsonify({'status': 'error', 'error': 'college_name and branch are required.'}), 400
    # Remove from likes if previously liked
    existing_like = UserLike.query.filter_by(user_id=user.id, college_name=college_name, branch=branch).first()
    if existing_like:
        db.session.delete(existing_like)
    # Avoid duplicate dislikes
    existing = UserDislike.query.filter_by(user_id=user.id, college_name=college_name, branch=branch).first()
    if existing:
        db.session.commit()
        return jsonify({'status': 'already_disliked', 'message': 'Already marked not interested.'})
    dislike = UserDislike(user_id=user.id, college_name=college_name, branch=branch)
    db.session.add(dislike)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Marked as not interested.', 'dislike': dislike.to_dict()})


@app.route('/api/dislikes', methods=['DELETE'])
def remove_dislike():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401
    data         = request.get_json(silent=True) or {}
    college_name = (data.get('college_name') or '').strip()
    branch       = (data.get('branch') or '').strip()
    dislike = UserDislike.query.filter_by(user_id=user.id, college_name=college_name, branch=branch).first()
    if not dislike:
        return jsonify({'status': 'not_found', 'message': 'Dislike not found.'})
    db.session.delete(dislike)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Removed from not interested.'})


@app.route('/api/dislikes', methods=['GET'])
def get_dislikes():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401
    dislikes = UserDislike.query.filter_by(user_id=user.id).order_by(UserDislike.disliked_at.desc()).all()
    return jsonify({'status': 'success', 'dislikes': [d.to_dict() for d in dislikes], 'total': len(dislikes)})


# ── College data APIs ──────────────────────────────────────────────────────────

@app.route('/api/cities')
def cities():
    count_2025 = Cutoff.query.filter(Cutoff.year == 2025).count()
    use_year = 2025 if count_2025 > 0 else 2024
    use_round = db.session.query(db.func.max(Cutoff.round)).filter(Cutoff.year == use_year).scalar() or 3
    rows = db.session.query(Cutoff.city).filter(Cutoff.year == use_year, Cutoff.round == use_round).distinct().order_by(Cutoff.city).all()
    return jsonify({'cities': [r.city for r in rows if r.city]})


@app.route('/api/colleges')
def colleges():
    count_2025 = Cutoff.query.filter(Cutoff.year == 2025).count()
    use_year = 2025 if count_2025 > 0 else 2024
    use_round = db.session.query(db.func.max(Cutoff.round)).filter(Cutoff.year == use_year).scalar() or 3
    q = (request.args.get('q') or '').strip()
    lim = request.args.get('limit', type=int) or 500
    lim = max(1, min(lim, 2000))

    base = db.session.query(Cutoff.college_name, Cutoff.city, Cutoff.college_type).filter(
        Cutoff.year == use_year, Cutoff.round == use_round
    )
    if q:
        base = base.filter(Cutoff.college_name.ilike(f'%{q}%'))
    rows = base.distinct().order_by(Cutoff.college_name).limit(lim).all()
    return jsonify({'colleges': [{'college_name': r.college_name, 'city': r.city, 'college_type': r.college_type} for r in rows]})


def _classify_chance(diff):
    """
    Classify admission chance based on the gap between user's percentile and cutoff.

    diff = user_percentile - cutoff_percentile
      Positive → user is ABOVE cutoff  (good)
      Negative → user is BELOW cutoff  (risky)

    Thresholds:
      High   : diff >= +2.0  (comfortably above — strong chance)
      Medium : diff >= -2.0  (within ±2 pts — borderline, apply with backup)
      Low    : diff <  -2.0  (below cutoff by more than 2 pts — reach option)

    NOTE: We use ±2.0 instead of the old ±0.5/+1.0 because MHT-CET cutoffs
    can shift by 1–3 percentile points year-on-year.  The old narrow band
    classified almost everything as "Low" at lower percentile ranges, making
    the tool useless for SC/ST/OBC students with percentiles below 60.
    """
    if diff >= 0.0:    return "High"     # at or above cutoff = High
    elif diff >= -2.0: return "Medium"   # up to 2 pts below = Medium  
    else:              return "Low"      # more than 2 below = Low


def _build_explanation(percentile, cutoff, diff, seat_type, city, pref_city, chance):
    abs_diff = abs(diff)
    seat_label = seat_type or ''

    if chance == "High":
        verdict = (
            f"Strong chance — your percentile ({percentile:.2f}) is {abs_diff:.2f} pts "
            f"above last year's closing cutoff ({cutoff:.2f}) for the {seat_label} seat."
        )
    elif chance == "Medium":
        if diff >= 0:
            verdict = (
                f"Borderline safe — you are {abs_diff:.2f} pts above cutoff ({cutoff:.2f}). "
                f"Cutoffs can shift slightly year-on-year, so keep safer backups too."
            )
        else:
            verdict = (
                f"Borderline risky — you are {abs_diff:.2f} pts below cutoff ({cutoff:.2f}). "
                f"Admission is possible if this year's cutoff drops. Keep safer backups."
            )
    else:
        verdict = (
            f"Reach option — you are {abs_diff:.2f} pts below last year's cutoff ({cutoff:.2f}). "
            f"Cutoffs do change each year, so it's still worth applying, but don't rely on it."
        )

    if pref_city and city and pref_city.strip().lower() in city.strip().lower():
        verdict += f" City match: {city}."
    return verdict


def _deduplicate(cutoffs, percentile):
    """
    Keep the single best seat-type row per (college, branch) for this student.

    Selection rules (in priority order):
      1. If student's percentile >= cutoff (achievable): prefer the reserved-
         category seat with the HIGHEST cutoff (most selective seat they qualify
         for — avoids "wasting" a reserved seat on a college they'd get via Open).
      2. If the student qualifies for some seats but not others: always prefer
         an achievable seat over an unachievable one.
      3. If no seat is achievable: keep the one whose cutoff is CLOSEST to the
         student's percentile (smallest negative gap = most likely to flip next year).
    """
    best = {}
    for c in cutoffs:
        key = (c.college_name, c.branch)
        existing = best.get(key)
        if existing is None:
            best[key] = c
            continue

        diff_new = percentile - c.closing_percentile
        diff_old = percentile - existing.closing_percentile

        # Both achievable → keep the one with HIGHER cutoff
        # (higher cutoff = more selective = better signal of college quality)
        if diff_new >= 0 and diff_old >= 0:
            if c.closing_percentile > existing.closing_percentile:
                best[key] = c

        # New row achievable, old row is not → always take achievable row
        elif diff_new >= 0 and diff_old < 0:
            best[key] = c

        # Both unachievable → keep the one closest to user's percentile
        # (diff_new > diff_old means diff_new is a smaller negative number = closer)
        elif diff_new < 0 and diff_old < 0:
            if diff_new > diff_old:
                best[key] = c

    return list(best.values())


def _count_eligible(deduped, percentile):
    return sum(1 for c in deduped if c.closing_percentile > 0 and (percentile - c.closing_percentile) >= -15)


def _select_best_colleges(deduped, percentile, total=30):
    MIN_EACH = 3
    if not deduped: return []
    pool_h, pool_m, pool_l = [], [], []
    for c in deduped:
        cutoff = c.closing_percentile
        if cutoff <= 0: continue
        diff = percentile - cutoff
        if diff < -5: continue   # only exclude colleges more than 5 pts below cutoff
        tier = _classify_chance(diff)
        if   tier == 'High':   pool_h.append((c, cutoff, diff))
        elif tier == 'Medium': pool_m.append((c, cutoff, diff))
        else:                  pool_l.append((c, cutoff, diff))
    pool_h.sort(key=lambda x: x[1], reverse=True)
    pool_m.sort(key=lambda x: x[2])
    pool_l.sort(key=lambda x: x[2], reverse=True)
    n = min(total, len(pool_h) + len(pool_m) + len(pool_l))
    if n == 0: return []
    min_each = MIN_EACH if n >= MIN_EACH * 3 else max(1, n // 3)
    slots_h = max(min_each, min(len(pool_h), total - 2 * min_each))
    slots_m = max(min_each, min(len(pool_m), total - slots_h - min_each))
    slots_l = max(min_each, total - slots_h - slots_m)
    slots_h = min(slots_h, len(pool_h)) if pool_h else 0
    slots_m = min(slots_m, len(pool_m)) if pool_m else 0
    slots_l = min(slots_l, len(pool_l)) if pool_l else 0
    if not pool_h: slots_m = min(len(pool_m), slots_m + slots_h); slots_h = 0
    if not pool_m: slots_h = min(len(pool_h), slots_h + slots_m // 2); slots_l = min(len(pool_l), slots_l + slots_m - slots_m // 2); slots_m = 0
    if not pool_l: slots_h = min(len(pool_h), slots_h + slots_l); slots_l = 0
    while slots_h + slots_m + slots_l > total:
        if slots_l > min_each: slots_l -= 1
        elif slots_m > min_each: slots_m -= 1
        elif slots_h > min_each: slots_h -= 1
        else: break
    while slots_h + slots_m + slots_l < total:
        rh = len(pool_h) - slots_h; rm = len(pool_m) - slots_m; rl = len(pool_l) - slots_l
        if rh > 0 and rh >= rm and rh >= rl: slots_h += 1
        elif rm > 0 and rm >= rl: slots_m += 1
        elif rl > 0: slots_l += 1
        else: break
    result = []
    for tier_name, group in [('High', pool_h[:slots_h]), ('Medium', pool_m[:slots_m]), ('Low', pool_l[:slots_l])]:
        for (c, cut, d) in group:
            result.append({'college_name': c.college_name, 'college_code': c.college_code or '',
                            'branch': c.branch, 'city': c.city,
                            'college_type': c.college_type, 'seat_type': c.seat_type,
                            'cutoff_percentile': round(cut, 4), 'diff': round(d, 4), 'chance': tier_name})
    return result


def _run_query(seat_types, pref_city, branches, college_types):
    from sqlalchemy import or_

    # Determine which year to use
    count_2025 = Cutoff.query.filter(Cutoff.year == 2025).count()
    use_year = 2025 if count_2025 > 0 else 2024

    # Find all rounds available for this year
    available_rounds = sorted([
        r[0] for r in
        db.session.query(Cutoff.round).filter(Cutoff.year == use_year).distinct().all()
    ], reverse=True)  # [4, 3, 2, 1] — latest first

    if not available_rounds:
        return []

    # Base filters (city, branch, college type)
    def apply_filters(q):
        if pref_city and pref_city.lower() not in ('any city', 'any', '', 'all cities in maharashtra'):
            # Split city into words and match any word — handles "Pune, Ambegaon" etc.
            city_words = [w.strip() for w in pref_city.replace(',', ' ').split() if len(w.strip()) >= 3]
            if city_words:
                city_filters = [Cutoff.city.ilike(f'%{w}%') for w in city_words]
                q = q.filter(or_(*city_filters))
            else:
                q = q.filter(Cutoff.city.ilike(f'%{pref_city}%'))
        if branches:
            q = q.filter(or_(*[Cutoff.branch.ilike(f'%{b}%') for b in branches]))
        if college_types:
            # Known types the UI can emit. If all are selected, don't filter —
            # this prevents hiding colleges stored as 'Other' in the DB.
            ALL_KNOWN_TYPES = {
                'Government', 'Government-Aided', 'University',
                'Private Autonomous', 'Private', 'Deemed University', 'Other'
            }
            selected_set = set(college_types)
            # Expand Government to include Government-Aided (VJTI etc)
            if 'Government' in selected_set:
                selected_set.add('Government-Aided')
            # If user effectively selected everything, skip the filter entirely
            if selected_set >= ALL_KNOWN_TYPES or selected_set >= (ALL_KNOWN_TYPES - {'Other', 'Deemed University'}):
                pass   # no filter — show all college types
            else:
                q = q.filter(Cutoff.college_type.in_(list(selected_set)))
        return q

    # SMART FALLBACK: for each (college, branch, seat_type) combination,
    # use the latest round that has data for it.
    # This ensures VJ/NT/SC seats are never missing just because
    # they were fully filled in Round 1 and absent in Round 4.
    all_rows = {}  # key=(college_name, branch, seat_type) → row

    for rnd in available_rounds:
        q = Cutoff.query.filter(
            Cutoff.year == use_year,
            Cutoff.round == rnd,
            Cutoff.seat_type.in_(seat_types)
        )
        q = apply_filters(q)
        for row in q.all():
            key = (row.college_name, row.branch, row.seat_type)
            if key not in all_rows:
                # First time we see this combination = latest round that has it
                all_rows[key] = row

    return list(all_rows.values())


@app.route('/api/recommend/colleges', methods=['POST'])
def recommend_colleges():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'status': 'error', 'error': 'Invalid JSON body'}), 400

    percentile    = data.get('percentile')
    category      = data.get('category', 'OPEN').upper()
    gender        = data.get('gender', 'Male')
    pref_city     = (data.get('city', '') or '').strip()
    branches      = data.get('branches', [])
    college_types = data.get('collegeTypes', [])

    if percentile is None:
        return jsonify({'status': 'error', 'error': 'percentile is required'}), 400
    try:
        percentile = float(percentile)
    except (TypeError, ValueError):
        return jsonify({'status': 'error', 'error': 'percentile must be a number'}), 400
    if not (0 <= percentile <= 100):
        return jsonify({'status': 'error', 'error': 'percentile must be between 0 and 100'}), 400

    # ── Build eligible seat types ─────────────────────────────────────────────
    # get_eligible_seat_types already includes OPEN seats for reserved categories.
    # TFWS (Tuition Fee Waiver Scheme) is open to all — always include it.
    all_seat_types = get_eligible_seat_types(category, gender) + ['TFWS']

    # ── Strict query: user's exact filters ───────────────────────────────────
    rows_strict   = _run_query(all_seat_types, pref_city, branches, college_types)
    dedup_strict  = _deduplicate(rows_strict, percentile)
    eligible_strict = _count_eligible(dedup_strict, percentile)
    user_set_type_filter = bool(college_types)

    # If user set a college-type filter and got nothing, tell them why
    if user_set_type_filter and eligible_strict == 0:
        rows_nb = _run_query(all_seat_types, pref_city, [], college_types)
        enb = _count_eligible(_deduplicate(rows_nb, percentile), percentile)
        if enb > 0:
            hint = (
                f"No '{', '.join(college_types)}' colleges match your branch filter. "
                f"{enb} college(s) of that type are available — try removing the branch filter."
            )
        else:
            # Check if the issue is percentile being too low vs no colleges of that type
            rows_any_pct = _run_query(all_seat_types, pref_city, branches, college_types)
            has_rows = len(rows_any_pct) > 0
            if has_rows:
                hint = (
                    f"No '{', '.join(college_types)}' colleges in {pref_city or 'Maharashtra'} "
                    f"match your percentile ({percentile:.2f}). "
                    f"These colleges exist but their cutoffs are higher. "
                    f"Try a different city or college type."
                )
            else:
                hint = (
                    f"No '{', '.join(college_types)}' colleges found"
                    + (f" in {pref_city}" if pref_city else " in Maharashtra")
                    + ". Try selecting a different city or college type."
                )
        return jsonify({'status': 'no_results', 'total': 0, 'data': [], 'hint': hint})

    # ── Progressive filter relaxation if too few results ─────────────────────
    # RULE: If the user selected a city, NEVER show colleges from other cities.
    # City is a hard filter. Only relax branch filter within the same city.
    # If no city selected, relax branch filter freely across Maharashtra.
    filter_note = None
    MINIMUM_NEEDED = 20   # only applies when no city is selected

    if pref_city:
        # City is a hard filter — never override it.
        # Only relax branch filter within this city if branch filter gave zero results.
        if branches and eligible_strict == 0:
            rows_city_any_branch = _run_query(all_seat_types, pref_city, [], college_types)
            dedup_city_any = _deduplicate(rows_city_any_branch, percentile)
            if _count_eligible(dedup_city_any, percentile) > 0:
                raw_cutoffs = dedup_city_any
                filter_note = (
                    f"No colleges in {pref_city} offer your selected branches. "
                    f"Showing all available branches in {pref_city} instead."
                )
            else:
                raw_cutoffs = dedup_strict
        else:
            raw_cutoffs = dedup_strict
    else:
        # No city selected — relax branch filter across Maharashtra if needed
        if eligible_strict >= MINIMUM_NEEDED or user_set_type_filter:
            raw_cutoffs = dedup_strict
        else:
            merged      = list(dedup_strict)
            merged_keys = {(c.college_name, c.branch) for c in dedup_strict}
            relaxed     = False

            for lvl_args in [
                (all_seat_types, '', branches, []),
                (all_seat_types, '', [],       []),
            ]:
                if _count_eligible(merged, percentile) >= MINIMUM_NEEDED:
                    break
                for c in _deduplicate(_run_query(*lvl_args), percentile):
                    key = (c.college_name, c.branch)
                    if key not in merged_keys and c.closing_percentile > 0 \
                            and (percentile - c.closing_percentile) >= -15:
                        merged.append(c)
                        merged_keys.add(key)
                        relaxed = True

            if relaxed:
                filter_note = (
                    f"Fewer than {MINIMUM_NEEDED} colleges matched your branch filters, "
                    f"so we've included additional branches from across Maharashtra."
                )
            raw_cutoffs = merged

    # ── Select & rank best colleges ──────────────────────────────────────────
    results = _select_best_colleges(raw_cutoffs, percentile, total=30)

    if not results:
        if pref_city:
            hint = (
                f"No colleges found in {pref_city} for {category} category "
                f"at {percentile:.2f} percentile. "
                f"Try selecting 'All Cities in Maharashtra' to search statewide."
            )
        else:
            hint = (
                f"No colleges found for {category} category at {percentile:.2f} percentile"
                + ". Please check your inputs or try different filters."
            )
        return jsonify({'status': 'no_results', 'total': 0, 'data': [], 'hint': hint})

    for r in results:
        r['explanation'] = _build_explanation(
            percentile, r['cutoff_percentile'], r['diff'],
            r['seat_type'], r.get('city', ''), pref_city, r['chance']
        )

    # Sort: High first, then Medium, then Low; within each tier by cutoff desc
    results.sort(key=lambda x: (
        {'High': 0, 'Medium': 1, 'Low': 2}.get(x['chance'], 3),
        -x['cutoff_percentile']
    ))

    return jsonify({
        'status': 'success',
        'total': len(results),
        'data': results,
        'filter_note': filter_note
    })


# ── Scholarship Recommendation API ────────────────────────────────────────────

@app.route('/api/recommend/scholarships', methods=['POST'])
def recommend_scholarships():
    data       = request.get_json(silent=True) or {}
    category   = (data.get('category') or 'OPEN').upper().strip()
    income     = int(data.get('income') or 0)
    gender     = (data.get('gender') or 'Male').strip()
    domicile   = (data.get('domicile') or 'maharashtra').strip().lower()
    disability = (data.get('disability') or 'None').strip()
    percentage = float(data.get('percentage') or 0)
    year       = int(data.get('yearOfStudy') or 1)
    minority   = (data.get('minority') or 'None').strip()
    has_disability = disability != 'None'
    is_minority    = minority != 'None'

    # Get user for dislike filtering (optional — works even if not logged in)
    user = get_session_user()
    disliked_ids = set()
    if user:
        disliked_ids = {
            d.scholarship_id for d in
            UserScholarshipDislike.query.filter_by(user_id=user.id).all()
        }

    results = []
    today = datetime.utcnow().date()

    for s in Scholarship.query.filter_by(is_active=True).all():
        # Skip disliked scholarships
        if s.id in disliked_ids:
            continue

        reasons_yes = []
        reasons_no  = []

        # Category check
        if s.categories:
            if 'OPEN' not in s.categories and category not in s.categories:
                reasons_no.append(f"Only for {', '.join(s.categories)} — you are {category}")
            else:
                reasons_yes.append(f"Category {category} is eligible")

        # Income check
        if income > s.max_income:
            reasons_no.append(f"Income ₹{income:,} exceeds limit of ₹{s.max_income:,}")
        else:
            reasons_yes.append(f"Family income ₹{income:,} is within limit")

        # Percentage check
        if percentage < s.min_percentage:
            reasons_no.append(f"Requires {s.min_percentage:.0f}% in 12th — you have {percentage:.0f}%")
        elif s.min_percentage > 0:
            reasons_yes.append(f"Your {percentage:.0f}% meets the {s.min_percentage:.0f}% requirement")

        # Gender check
        if s.gender not in ('Any', gender):
            reasons_no.append(f"Only for {s.gender} students")
        elif s.gender != 'Any':
            reasons_yes.append(f"Open to {gender} students")

        # Disability check
        if s.disability_required and not has_disability:
            reasons_no.append("Requires 40%+ disability certificate")
        elif s.disability_required and has_disability:
            reasons_yes.append("Disability certificate qualifies you")

        # Minority check
        if s.minority_required and not is_minority:
            reasons_no.append("Only for minority community students")
        elif s.minority_required and is_minority:
            reasons_yes.append(f"Minority status ({minority}) qualifies you")

        # Year of study check
        if s.years_eligible and year not in s.years_eligible:
            reasons_no.append(f"Only for year(s) {s.years_eligible} — you are in year {year}")
        elif s.years_eligible:
            reasons_yes.append(f"Year {year} is eligible")

        # Domicile check
        if s.domicile_required not in ('any', domicile):
            reasons_no.append(f"Requires {s.domicile_required} domicile")

        eligible = len(reasons_no) == 0

        # Deadline info
        deadline_text = None
        days_left = None
        deadline_status = 'unknown'
        if s.deadline_close:
            days_left = (s.deadline_close - today).days
            if days_left < 0:
                deadline_text = f"Closed — deadline was {s.deadline_close.strftime('%d %b %Y')}"
                deadline_status = 'closed'
            elif days_left == 0:
                deadline_text = "Last day to apply!"
                deadline_status = 'urgent'
            elif days_left <= 15:
                deadline_text = f"{days_left} days left — apply soon!"
                deadline_status = 'urgent'
            elif days_left <= 45:
                deadline_text = f"{days_left} days left"
                deadline_status = 'open'
            else:
                deadline_text = f"Open until {s.deadline_close.strftime('%d %b %Y')}"
                deadline_status = 'open'
        if s.deadline_open and today < s.deadline_open:
            if not s.is_date_confirmed:
                deadline_text = f"Expected around {s.deadline_open.strftime('%b %Y')} — verify at official portal"
                deadline_status = 'estimated'
            else:
                deadline_text = f"Opens on {s.deadline_open.strftime('%d %b %Y')}"
                deadline_status = 'upcoming'

        results.append({
            'id':              s.id,
            'name':            s.name,
            'source':          s.source,
            'portal_url':      s.portal_url,
            'amount':          s.amount_text,
            'eligible':        eligible,
            'reasons':         reasons_yes if eligible else reasons_no,
            'documents':       s.documents or [],
            'deadline_text':   deadline_text,
            'deadline_status': deadline_status,
            'days_left':       days_left,
        })

    # Eligible first, then not-eligible
    results.sort(key=lambda x: (0 if x['eligible'] else 1, x['name']))
    total_eligible = sum(1 for r in results if r['eligible'])

    return jsonify({
        'status': 'success',
        'data': results,
        'total_eligible': total_eligible
    })


# ── Scholarship Dislike API ────────────────────────────────────────────────────

@app.route('/api/scholarship/dislike', methods=['POST'])
def dislike_scholarship():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401
    data = request.get_json(silent=True) or {}
    scholarship_id = data.get('scholarship_id')
    if not scholarship_id:
        return jsonify({'status': 'error', 'error': 'scholarship_id required.'}), 400
    existing = UserScholarshipDislike.query.filter_by(
        user_id=user.id, scholarship_id=scholarship_id).first()
    if existing:
        return jsonify({'status': 'already_disliked'})
    d = UserScholarshipDislike(user_id=user.id, scholarship_id=scholarship_id)
    db.session.add(d)
    db.session.commit()
    return jsonify({'status': 'success', 'message': 'Scholarship removed from your list.'})


@app.route('/api/scholarship/dislike', methods=['DELETE'])
def undo_dislike_scholarship():
    user = get_session_user()
    if not user:
        return jsonify({'status': 'error', 'error': 'Not logged in.'}), 401
    data = request.get_json(silent=True) or {}
    scholarship_id = data.get('scholarship_id')
    d = UserScholarshipDislike.query.filter_by(
        user_id=user.id, scholarship_id=scholarship_id).first()
    if d:
        db.session.delete(d)
        db.session.commit()
    return jsonify({'status': 'success'})


@app.route('/<path:relpath>')
def serve_public(relpath):
    """Serve script.js, styles, images from project root when using one Flask process."""
    if relpath.startswith('api/'):
        abort(404)
    safe = os.path.normpath(os.path.join(_SITE_ROOT, relpath))
    root = os.path.abspath(_SITE_ROOT)
    if not safe.startswith(root):
        abort(404)
    if os.path.isfile(safe):
        return send_from_directory(os.path.dirname(safe), os.path.basename(safe))
    abort(404)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)