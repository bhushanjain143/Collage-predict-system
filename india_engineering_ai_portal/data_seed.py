"""Sample college–branch rows aligned with AI_ML_College_Portal_v2.md (indicative data)."""
from __future__ import annotations

COLLEGES: list[dict] = []

def add(
    *,
    college_name: str,
    city: str,
    state: str,
    college_type: str,
    branch: str,
    branch_code: str,
    cutoff_exam: str,
    cutoff_general: str,
    cutoff_score: float,
    fees_per_year: int,
    placement_percent: float,
    avg_package_lpa: float,
    highest_package_lpa: float,
    scholarship: str,
    nirf_rank: int | None = None,
    website: str = "",
) -> None:
    COLLEGES.append(
        {
            "id": len(COLLEGES) + 1,
            "college_name": college_name,
            "city": city,
            "state": state,
            "college_type": college_type,
            "branch": branch,
            "branch_code": branch_code,
            "cutoff_exam": cutoff_exam,
            "cutoff_general": cutoff_general,
            "cutoff_score": cutoff_score,
            "fees_per_year": fees_per_year,
            "placement_percent": placement_percent,
            "avg_package_lpa": avg_package_lpa,
            "highest_package_lpa": highest_package_lpa,
            "scholarship": scholarship,
            "nirf_rank": nirf_rank,
            "website": website,
        }
    )


# --- IIT sample rows (JEE Advanced style as rough percentile proxy for UI sorting) ---
for row in [
    ("IIT Bombay", "Mumbai", "Maharashtra", "CSE", "Top 100 rank", 99.9, 230200, 92, 22, 120, 3),
    ("IIT Bombay", "Mumbai", "Maharashtra", "Electrical Engineering", "Top 300 rank", 99.7, 230200, 88, 18, 80, 3),
    ("IIT Bombay", "Mumbai", "Maharashtra", "Mechanical Engineering", "Top 700 rank", 99.4, 230200, 85, 14, 60, 3),
    ("IIT Delhi", "New Delhi", "Delhi", "CSE", "Top 100 rank", 99.85, 217000, 93, 23, 150, 2),
    ("IIT Delhi", "New Delhi", "Delhi", "Mathematics & Computing", "Top 200 rank", 99.75, 217000, 90, 21, 100, 2),
    ("IIT Madras", "Chennai", "Tamil Nadu", "CSE", "Top 150 rank", 99.8, 212100, 91, 21, 100, 1),
    ("IIT Kanpur", "Kanpur", "Uttar Pradesh", "CSE", "Top 200 rank", 99.7, 212600, 90, 20, 120, 4),
    ("IIT Kharagpur", "Kharagpur", "West Bengal", "CSE", "Top 250 rank", 99.65, 148700, 89, 19, 95, 6),
    ("IIT Hyderabad", "Hyderabad", "Telangana", "CSE", "Top 600 rank", 99.5, 225000, 86, 17, 80, 8),
    ("IIT Roorkee", "Roorkee", "Uttarakhand", "CSE", "Top 350 rank", 99.55, 222700, 88, 18, 90, 5),
    ("IIT Guwahati", "Guwahati", "Assam", "CSE", "Top 700 rank", 99.35, 216000, 85, 16, 75, 7),
    ("IIT BHU Varanasi", "Varanasi", "Uttar Pradesh", "CSE", "Top 900 rank", 99.2, 142000, 83, 14, 65, 14),
    ("IIT (ISM) Dhanbad", "Dhanbad", "Jharkhand", "CSE", "Top 1000 rank", 99.15, 200000, 81, 13, 58, 12),
]:
    name, city, st, br, cg, cs, fee, pl, ap, hp, nr = row
    add(
        college_name=name,
        city=city,
        state=st,
        college_type="IIT",
        branch=f"B.Tech {br}" if br == "CSE" else f"B.Tech {br}",
        branch_code="CSE" if br == "CSE" else br[:4].upper(),
        cutoff_exam="JEE Advanced",
        cutoff_general=cg,
        cutoff_score=cs,
        fees_per_year=fee,
        placement_percent=pl,
        avg_package_lpa=ap,
        highest_package_lpa=hp,
        scholarship="Merit-cum-Means, SC/ST Fee Waiver (verify at institute)",
        nirf_rank=nr,
        website="https://www.iitb.ac.in" if "Bombay" in name else "",
    )

# --- NIT (JEE Main percentile proxy) ---
for row in [
    ("NIT Trichy", "Tiruchirappalli", "Tamil Nadu", "CSE", 99.5, 156750, 88, 16, 60, 10),
    ("NIT Trichy", "Tiruchirappalli", "Tamil Nadu", "Electronics & Communication Engg.", 99.0, 156750, 84, 13, 50, 10),
    ("NIT Warangal", "Warangal", "Telangana", "CSE", 99.4, 151300, 87, 15, 55, 21),
    ("NIT Surathkal", "Surathkal", "Karnataka", "CSE", 99.3, 168000, 86, 15, 52, 12),
    ("NIT Calicut", "Kozhikode", "Kerala", "CSE", 99.0, 144400, 85, 14, 50, 23),
    ("NIT Rourkela", "Rourkela", "Odisha", "CSE", 98.8, 152580, 84, 13, 48, 16),
    ("NIT Allahabad (MNNIT)", "Prayagraj", "Uttar Pradesh", "CSE", 98.5, 150000, 83, 13, 46, 47),
    ("NIT Jaipur (MNIT)", "Jaipur", "Rajasthan", "CSE", 98.4, 155000, 82, 12, 44, 35),
    ("NIT Bhopal (MANIT)", "Bhopal", "Madhya Pradesh", "CSE", 98.2, 148000, 81, 12, 42, 53),
    ("NIT Nagpur (VNIT)", "Nagpur", "Maharashtra", "CSE", 98.0, 158000, 80, 12, 42, 41),
    ("NIT Delhi", "New Delhi", "Delhi", "CSE", 97.5, 146000, 78, 10, 38, 51),
    ("NIT Srinagar", "Srinagar", "Jammu and Kashmir", "CSE", 93.0, 120000, 70, 7, 25, 58),
]:
    name, city, st, br, cs, fee, pl, ap, hp, nr = row
    add(
        college_name=name,
        city=city,
        state=st,
        college_type="NIT",
        branch=f"B.Tech {br}",
        branch_code="CSE" if br == "CSE" else "ECE",
        cutoff_exam="JEE Main",
        cutoff_general=f"{cs}+ percentile (indicative)",
        cutoff_score=cs,
        fees_per_year=fee,
        placement_percent=pl,
        avg_package_lpa=ap,
        highest_package_lpa=hp,
        scholarship="Merit-cum-Means, SC/ST (verify)",
        nirf_rank=nr,
    )

# --- IIIT ---
for row in [
    ("IIIT Hyderabad", "Hyderabad", "Telangana", "CSE", 99.8, 450000, 92, 22, 100),
    ("IIIT Allahabad", "Prayagraj", "Uttar Pradesh", "IT", 99.2, 180000, 85, 14, 55),
    ("IIIT Allahabad", "Prayagraj", "Uttar Pradesh", "CSE", 99.4, 180000, 86, 15, 58),
    ("IIIT Bangalore", "Bangalore", "Karnataka", "CSE", 99.0, 400000, 88, 18, 70),
    ("IIIT Delhi", "New Delhi", "Delhi", "CSE", 99.0, 350000, 87, 17, 65),
    ("IIIT Gwalior (ABV-IIITM)", "Gwalior", "Madhya Pradesh", "IT", 98.0, 175000, 81, 12, 44),
    ("IIIT Pune", "Pune", "Maharashtra", "CSE", 98.5, 220000, 82, 12, 45),
    ("IIIT Lucknow", "Lucknow", "Uttar Pradesh", "IT", 97.0, 200000, 78, 10, 36),
    ("IIIT Nagpur", "Nagpur", "Maharashtra", "CSE", 96.5, 158000, 75, 9, 30),
    ("IIIT Vadodara", "Vadodara", "Gujarat", "CSE", 96.8, 165000, 76, 9, 32),
]:
    name, city, st, br, cs, fee, pl, ap, hp = row
    add(
        college_name=name,
        city=city,
        state=st,
        college_type="IIIT",
        branch=f"B.Tech {br}",
        branch_code=br,
        cutoff_exam="JEE Main",
        cutoff_general=f"{cs}+ percentile (indicative)",
        cutoff_score=cs,
        fees_per_year=fee,
        placement_percent=pl,
        avg_package_lpa=ap,
        highest_package_lpa=hp,
        scholarship="Merit / institutional (verify)",
    )

# --- Private & state reputed ---
for row in [
    ("BITS Pilani", "Pilani", "Rajasthan", "CSE", 98.5, 525000, 95, 24, 120),
    ("VIT Vellore", "Vellore", "Tamil Nadu", "CSE", 95.0, 217000, 82, 11, 44),
    ("COEP Technological University", "Pune", "Maharashtra", "CSE", 99.0, 180000, 84, 12, 50),
    ("PICT Pune", "Pune", "Maharashtra", "CSE", 98.5, 150000, 83, 11, 46),
    ("VIT Pune", "Pune", "Maharashtra", "CSE", 98.0, 160000, 80, 10, 40),
    ("DTU Delhi", "New Delhi", "Delhi", "CSE", 99.6, 162000, 83, 12, 48),
    ("NSUT Delhi", "New Delhi", "Delhi", "CSE", 99.5, 165000, 82, 11, 44),
    ("Jadavpur University", "Kolkata", "West Bengal", "CSE", 98.5, 25000, 83, 11, 44),
    ("RV College of Engineering", "Bangalore", "Karnataka", "CSE", 99.0, 190000, 83, 12, 50),
]:
    name, city, st, br, cs, fee, pl, ap, hp = row
    is_govt = any(
        x in name for x in ("Jadavpur", "DTU", "NSUT", "COEP", "IGDTUW")
    )
    add(
        college_name=name,
        city=city,
        state=st,
        college_type="Govt" if is_govt else "Private",
        branch=f"B.Tech {br}",
        branch_code="CSE",
        cutoff_exam="BITSAT / MHT-CET / JEE / State exam (see cutoff_general)",
        cutoff_general="Varies — indicative score for demo",
        cutoff_score=cs,
        fees_per_year=fee,
        placement_percent=pl,
        avg_package_lpa=ap,
        highest_package_lpa=hp,
        scholarship="Merit, TFWS, SC/ST — verify at college",
    )
