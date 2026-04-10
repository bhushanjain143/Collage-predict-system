# Optimized production image for the Streamlit UI + pipeline tooling.
# Build:  docker build -t mahacet-fe .
# Run UI: docker run -p 8501:8501 -e PYTHONPATH=/app mahacet-fe

FROM python:3.11-slim-bookworm AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    MAHA_LOG_LEVEL=WARNING

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Byte-compile for slightly faster cold imports (safe for this app)
RUN python -m compileall -q config cleaner model scraper app || true

EXPOSE 8501

CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true"]
