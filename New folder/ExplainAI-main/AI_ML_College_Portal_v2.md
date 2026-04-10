# AI & ML Integration Guide for College Admission Portal

> A comprehensive roadmap to make your college admission website smarter and more personalized for students using Artificial Intelligence and Machine Learning.

---

## 🏫 India Engineering College Landscape

| Category | Count (Approx.) |
|---|---|
| Total Engineering Colleges | 8,876+ |
| Private Institutions | 6,611+ |
| Government / Government Aided | 2,265+ |
| IITs | 23 |
| NITs | 31 |
| IIITs | 26 |

---

## 🚀 Recommended Implementation Order

Start simple, then scale:

1. Rule-based Recommendation System
2. Admission Prediction Model
3. Scholarship Recommendation Module
4. Chatbot
5. *(Later)* Advanced ML models as data grows

---

## 🔍 Feature Modules

### 1. Admission Prediction Model

Predict a student's probability of admission into a college using:

**Input Features:**
- MHT-CET percentile
- JEE percentile
- Category
- Branch
- College location
- CAP round
- Previous year cutoffs

**Output:**
- ✅ High Chance
- 🟡 Medium Chance
- ❌ Low Chance

**Best Algorithms:**
- Logistic Regression
- Decision Tree
- Random Forest *(Recommended)*
- XGBoost *(Recommended)*

---

### 2. College Recommendation Engine

An AI engine similar to shopping/movie recommendation systems that ranks the **top 20–25 colleges** for a student based on:

- Similar students' past admission history
- Preferred branch
- Budget
- Distance from home
- Placement performance
- Scholarship availability
- Government vs. private college preference

---

### 3. Scholarship Recommendation System

Automatically match students to scholarships based on:

- Category
- Income
- Gender
- State
- Marks
- College type

> 💡 Start with rule-based logic, then upgrade to ML as data grows.

---

### 4. CAP Round Prediction

Using historical CAP round allotment data to predict:

- Which CAP round the student is most likely to get admission in
- Whether to wait for the next round
- Whether to pick a better or safer college

---

### 5. College Comparison AI

A smart AI-powered comparison tool that evaluates colleges across:

- Fees
- Placements
- Distance
- Hostel availability
- Faculty quality
- Cutoffs
- Student reviews
- ROI (Return on Investment)

**Example AI Suggestion:**
> *"College A is better for placements, but College B offers lower fees and better scholarship support."*

---

### 6. AI Chatbot for Students

Answer common student queries like:

- *"Which college is best for Computer Engineering?"*
- *"Can I get a Government college with 82 percentile?"*
- *"Which scholarship can I apply for?"*
- *"What is CAP Round 2?"*
- *"What documents are needed?"*

**Build using:**
- OpenAI API
- Dialogflow
- Rasa

---

### 7. Sentiment Analysis for College Reviews

Collect and analyze student reviews using NLP to surface:

- ✅ Positive feedback
- ❌ Negative feedback
- 🔁 Common complaints
- ⭐ Best features of the college

**Technologies:** Natural Language Processing (NLP), Sentiment Analysis

---

### 8. Personalized Student Dashboard

Show tailored recommendations to each student based on:

- Previous searches
- Saved colleges
- Preferred branches
- Budget
- State preference

---

### 9. Cutoff Trend Prediction

Train a model on **5 years of historical cutoff data** to estimate future trends and help students understand:

- Whether cutoffs are rising or falling
- Whether a branch is becoming more competitive
- Whether they should apply to safer colleges

---

## 🛠️ Recommended Tech Stack

| Layer | Technologies |
|---|---|
| Language | Python |
| Data Processing | Pandas, NumPy |
| ML Models | Scikit-learn, XGBoost, TensorFlow |
| Backend API | Flask |
| Database | MySQL |

---

---

# 📦 India Engineering College Dataset

> This section defines the complete dataset structure used to train AI/ML models on the portal. Data is sourced from official portals and enriched for model training.

---

## 📡 Official Data Sources

Collect and update this dataset regularly from the following portals:

| Source | Data Available | URL |
|---|---|---|
| **JoSAA** | IIT/NIT/IIIT cutoffs, round-wise allotment | josaa.nic.in |
| **CSAB** | Supernumerary allotments, NIT+ system | csab.nic.in |
| **AICTE** | Approved college list, intake, affiliation | aicte-india.org |
| **NIRF Rankings** | Placement %, avg package, research score | nirfindia.org |
| **MHT-CET Portal** | Maharashtra state CET cutoffs (CAP rounds) | cetcell.mahacet.org |
| **State CET Portals** | AP EAPCET, KCET, TNEA, WBJEE, REAP, etc. | State-specific |
| **College Websites** | Fees, hostel, scholarship details | College-specific |
| **Shiksha / Careers360** | Student reviews, placement reports | shiksha.com / careers360.com |

---

## 🗂️ Dataset Schema (Column Format)

Every college–branch combination is stored as one row with the following columns:

| Column Name | Data Type | Description | Example |
|---|---|---|---|
| `college_id` | INT | Unique identifier | 1001 |
| `college_name` | VARCHAR | Full official name | IIT Bombay |
| `city` | VARCHAR | City where college is located | Mumbai |
| `state` | VARCHAR | State | Maharashtra |
| `college_type` | ENUM | IIT / NIT / IIIT / Govt / Private | IIT |
| `affiliation` | VARCHAR | Affiliating university | Autonomous |
| `branch` | VARCHAR | Full branch name | Computer Science & Engineering |
| `branch_code` | VARCHAR | Standard branch code | CSE |
| `duration_years` | INT | Programme duration | 4 |
| `degree` | VARCHAR | Degree awarded | B.Tech |
| `intake` | INT | Total seats in branch | 120 |
| `cutoff_exam` | VARCHAR | Exam used for admission | JEE Advanced / MHT-CET |
| `cutoff_general` | VARCHAR | General category cutoff | Top 100 rank / 99.5 percentile |
| `cutoff_obc` | VARCHAR | OBC category cutoff | Top 300 rank / 99.0 percentile |
| `cutoff_sc` | VARCHAR | SC category cutoff | Top 1500 rank / 97.0 percentile |
| `cutoff_st` | VARCHAR | ST category cutoff | Top 3000 rank / 95.0 percentile |
| `cutoff_ews` | VARCHAR | EWS category cutoff | Top 500 rank / 99.2 percentile |
| `fees_per_year` | VARCHAR | ⚠ Tentative annual fees (₹) | ₹ 2,30,200 |
| `total_fees_4yr` | VARCHAR | ⚠ Tentative 4-year total (₹) | ₹ 9,20,800 |
| `placement_percent` | FLOAT | % students placed | 92.0 |
| `avg_package_lpa` | FLOAT | Average CTC in LPA | 22.0 |
| `highest_package_lpa` | FLOAT | Highest CTC in LPA | 120.0 |
| `top_recruiters` | TEXT | Major companies hiring | Google, Microsoft, Amazon |
| `scholarship_available` | VARCHAR | Scholarships offered | Merit-cum-Means, SC/ST Fee Waiver |
| `hostel_available` | BOOLEAN | On-campus hostel | TRUE |
| `nirf_rank` | INT | NIRF Engineering Rank | 3 |
| `naac_grade` | VARCHAR | NAAC accreditation | A++ |
| `website` | VARCHAR | Official college website | iitb.ac.in |
| `data_source` | VARCHAR | Where data was collected from | JoSAA 2024 / NIRF 2024 |
| `last_updated` | DATE | Date record was last updated | 2024-11-01 |

> ⚠ **Fee Disclaimer:** All fees listed are **tentative and indicative only**. Students must contact the college directly or visit the official website for confirmed fee structures.

---

## 🏛️ IITs — Sample Dataset (23 Institutes)

> Cutoffs based on JEE Advanced 2024 opening/closing ranks. Fees include tuition only (hostel extra).

| College Name | City | State | Branch | Cutoff (General) | Fees (₹/yr)* | Placement % | Avg Pkg (LPA) | Highest Pkg (LPA) | Scholarship |
|---|---|---|---|---|---|---|---|---|---|
| IIT Bombay | Mumbai | Maharashtra | Computer Science & Engineering | Top 100 rank | 2,30,200 | 92% | 22 | 120 | Merit-cum-Means, SC/ST Fee Waiver |
| IIT Bombay | Mumbai | Maharashtra | Electrical Engineering | Top 300 rank | 2,30,200 | 88% | 18 | 80 | Merit-cum-Means, SC/ST Fee Waiver |
| IIT Bombay | Mumbai | Maharashtra | Mechanical Engineering | Top 700 rank | 2,30,200 | 85% | 14 | 60 | SC/ST Fee Waiver |
| IIT Bombay | Mumbai | Maharashtra | Aerospace Engineering | Top 1000 rank | 2,30,200 | 80% | 12 | 48 | SC/ST Fee Waiver |
| IIT Delhi | New Delhi | Delhi | Computer Science & Engineering | Top 100 rank | 2,17,000 | 93% | 23 | 150 | Merit-cum-Means, SC/ST |
| IIT Delhi | New Delhi | Delhi | Mathematics & Computing | Top 200 rank | 2,17,000 | 90% | 21 | 100 | Merit-cum-Means, SC/ST |
| IIT Delhi | New Delhi | Delhi | Electrical Engineering | Top 350 rank | 2,17,000 | 89% | 19 | 85 | Merit-cum-Means, SC/ST |
| IIT Delhi | New Delhi | Delhi | Mechanical Engineering | Top 900 rank | 2,17,000 | 84% | 13 | 55 | Merit-cum-Means |
| IIT Madras | Chennai | Tamil Nadu | Computer Science & Engineering | Top 150 rank | 2,12,100 | 91% | 21 | 100 | Merit-cum-Means, SC/ST |
| IIT Madras | Chennai | Tamil Nadu | Electrical Engineering | Top 400 rank | 2,12,100 | 87% | 17 | 75 | Merit-cum-Means, SC/ST |
| IIT Madras | Chennai | Tamil Nadu | Mechanical Engineering | Top 900 rank | 2,12,100 | 84% | 13 | 52 | Merit-cum-Means |
| IIT Madras | Chennai | Tamil Nadu | Naval Architecture | Top 2500 rank | 2,12,100 | 75% | 9 | 35 | Merit-cum-Means |
| IIT Kanpur | Kanpur | Uttar Pradesh | Computer Science & Engineering | Top 200 rank | 2,12,600 | 90% | 20 | 120 | Merit-cum-Means, SC/ST |
| IIT Kanpur | Kanpur | Uttar Pradesh | Mathematics & Scientific Computing | Top 300 rank | 2,12,600 | 88% | 18 | 80 | Merit-cum-Means, SC/ST |
| IIT Kanpur | Kanpur | Uttar Pradesh | Electrical Engineering | Top 500 rank | 2,12,600 | 86% | 16 | 70 | Merit-cum-Means, SC/ST |
| IIT Kharagpur | Kharagpur | West Bengal | Computer Science & Engineering | Top 250 rank | 1,48,700 | 89% | 19 | 95 | Merit-cum-Means, SC/ST |
| IIT Kharagpur | Kharagpur | West Bengal | Electronics & Electrical Comm. | Top 600 rank | 1,48,700 | 85% | 15 | 65 | Merit-cum-Means |
| IIT Kharagpur | Kharagpur | West Bengal | Mechanical Engineering | Top 1200 rank | 1,48,700 | 82% | 12 | 48 | Merit-cum-Means |
| IIT Roorkee | Roorkee | Uttarakhand | Computer Science & Engineering | Top 350 rank | 2,22,700 | 88% | 18 | 90 | Merit-cum-Means, SC/ST |
| IIT Roorkee | Roorkee | Uttarakhand | Electrical Engineering | Top 800 rank | 2,22,700 | 83% | 14 | 55 | Merit-cum-Means |
| IIT Roorkee | Roorkee | Uttarakhand | Civil Engineering | Top 2000 rank | 2,22,700 | 78% | 10 | 38 | Merit-cum-Means |
| IIT Guwahati | Guwahati | Assam | Computer Science & Engineering | Top 700 rank | 2,16,000 | 85% | 16 | 75 | Merit-cum-Means, SC/ST |
| IIT Guwahati | Guwahati | Assam | Electronics & Communication | Top 1500 rank | 2,16,000 | 81% | 12 | 50 | Merit-cum-Means |
| IIT Hyderabad | Hyderabad | Telangana | Computer Science & Engineering | Top 600 rank | 2,25,000 | 86% | 17 | 80 | Merit-cum-Means, SC/ST |
| IIT Indore | Indore | Madhya Pradesh | Computer Science & Engineering | Top 800 rank | 2,20,000 | 84% | 15 | 70 | Merit-cum-Means, SC/ST |
| IIT BHU Varanasi | Varanasi | Uttar Pradesh | Computer Science & Engineering | Top 900 rank | 1,42,000 | 83% | 14 | 65 | Merit-cum-Means, SC/ST |
| IIT BHU Varanasi | Varanasi | Uttar Pradesh | Metallurgical Engineering | Top 4500 rank | 1,42,000 | 70% | 7 | 28 | Merit-cum-Means |
| IIT Ropar | Rupnagar | Punjab | Computer Science & Engineering | Top 1200 rank | 2,10,000 | 81% | 13 | 60 | Merit-cum-Means, SC/ST |
| IIT Gandhinagar | Gandhinagar | Gujarat | Computer Science & Engineering | Top 900 rank | 2,05,000 | 82% | 14 | 62 | Merit-cum-Means, SC/ST |
| IIT Jodhpur | Jodhpur | Rajasthan | Computer Science & Engineering | Top 1300 rank | 1,95,000 | 79% | 12 | 52 | Merit-cum-Means, SC/ST |
| IIT Patna | Patna | Bihar | Computer Science & Engineering | Top 1500 rank | 1,85,000 | 78% | 11 | 50 | Merit-cum-Means, SC/ST |
| IIT Mandi | Mandi | Himachal Pradesh | Computer Science & Engineering | Top 1600 rank | 1,80,000 | 77% | 10 | 46 | Merit-cum-Means, SC/ST |
| IIT Tirupati | Tirupati | Andhra Pradesh | Computer Science & Engineering | Top 1800 rank | 1,75,000 | 76% | 10 | 42 | Merit-cum-Means, SC/ST |
| IIT Palakkad | Palakkad | Kerala | Computer Science & Engineering | Top 1700 rank | 1,78,000 | 75% | 10 | 40 | Merit-cum-Means, SC/ST |
| IIT Dharwad | Dharwad | Karnataka | Computer Science & Engineering | Top 2000 rank | 1,70,000 | 74% | 9 | 38 | Merit-cum-Means, SC/ST |
| IIT Bhilai | Bhilai | Chhattisgarh | Computer Science & Engineering | Top 2200 rank | 1,68,000 | 73% | 8 | 35 | Merit-cum-Means, SC/ST |
| IIT Jammu | Jammu | J&K | Computer Science & Engineering | Top 2400 rank | 1,65,000 | 72% | 8 | 33 | Merit-cum-Means, SC/ST |
| IIT Goa | Ponda | Goa | Computer Science & Engineering | Top 2100 rank | 1,72,000 | 73% | 9 | 36 | Merit-cum-Means, SC/ST |
| IIT (ISM) Dhanbad | Dhanbad | Jharkhand | Computer Science & Engineering | Top 1000 rank | 2,00,000 | 81% | 13 | 58 | Merit-cum-Means, SC/ST |
| IIT (ISM) Dhanbad | Dhanbad | Jharkhand | Mining Engineering | Top 5000 rank | 2,00,000 | 70% | 7 | 28 | Merit-cum-Means |

---

## 🏛️ NITs — Sample Dataset (31 Institutes)

> Cutoffs based on JEE Mains 2024 percentile (General – Home State quota). Fees are tentative.

| College Name | City | State | Branch | Cutoff (JEE Mains %) | Fees (₹/yr)* | Placement % | Avg Pkg (LPA) | Highest Pkg (LPA) | Scholarship |
|---|---|---|---|---|---|---|---|---|---|
| NIT Trichy | Tiruchirappalli | Tamil Nadu | Computer Science & Engineering | 99.5+ | 1,56,750 | 88% | 16 | 60 | Merit-cum-Means, SC/ST |
| NIT Trichy | Tiruchirappalli | Tamil Nadu | Electronics & Communication | 99.0+ | 1,56,750 | 84% | 13 | 50 | Merit-cum-Means |
| NIT Trichy | Tiruchirappalli | Tamil Nadu | Electrical Engineering | 98.5+ | 1,56,750 | 82% | 11 | 44 | Merit-cum-Means |
| NIT Trichy | Tiruchirappalli | Tamil Nadu | Mechanical Engineering | 98.0+ | 1,56,750 | 80% | 10 | 40 | Merit-cum-Means |
| NIT Trichy | Tiruchirappalli | Tamil Nadu | Civil Engineering | 96.0+ | 1,56,750 | 75% | 8 | 30 | Merit-cum-Means |
| NIT Warangal | Warangal | Telangana | Computer Science & Engineering | 99.4+ | 1,51,300 | 87% | 15 | 55 | Merit-cum-Means, SC/ST |
| NIT Warangal | Warangal | Telangana | Electronics & Communication | 98.8+ | 1,51,300 | 83% | 12 | 48 | Merit-cum-Means |
| NIT Warangal | Warangal | Telangana | Electrical Engineering | 98.5+ | 1,51,300 | 81% | 11 | 42 | Merit-cum-Means |
| NIT Surathkal | Surathkal | Karnataka | Computer Science & Engineering | 99.3+ | 1,68,000 | 86% | 15 | 52 | Merit-cum-Means, SC/ST |
| NIT Surathkal | Surathkal | Karnataka | Electronics & Communication | 98.7+ | 1,68,000 | 82% | 12 | 46 | Merit-cum-Means |
| NIT Calicut | Kozhikode | Kerala | Computer Science & Engineering | 99.0+ | 1,44,400 | 85% | 14 | 50 | Merit-cum-Means, SC/ST |
| NIT Calicut | Kozhikode | Kerala | Electronics & Communication | 98.5+ | 1,44,400 | 81% | 11 | 43 | Merit-cum-Means |
| NIT Rourkela | Rourkela | Odisha | Computer Science & Engineering | 98.8+ | 1,52,580 | 84% | 13 | 48 | Merit-cum-Means, SC/ST |
| NIT Rourkela | Rourkela | Odisha | Mechanical Engineering | 96.8+ | 1,52,580 | 76% | 9 | 32 | Merit-cum-Means |
| NIT Allahabad (MNNIT) | Prayagraj | Uttar Pradesh | Computer Science & Engineering | 98.5+ | 1,50,000 | 83% | 13 | 46 | Merit-cum-Means, SC/ST |
| NIT Jaipur (MNIT) | Jaipur | Rajasthan | Computer Science & Engineering | 98.4+ | 1,55,000 | 82% | 12 | 44 | Merit-cum-Means, SC/ST |
| NIT Bhopal (MANIT) | Bhopal | Madhya Pradesh | Computer Science & Engineering | 98.2+ | 1,48,000 | 81% | 12 | 42 | Merit-cum-Means, SC/ST |
| NIT Kurukshetra | Kurukshetra | Haryana | Computer Science & Engineering | 98.0+ | 1,42,000 | 80% | 11 | 40 | Merit-cum-Means, SC/ST |
| NIT Durgapur | Durgapur | West Bengal | Computer Science & Engineering | 97.8+ | 1,45,000 | 79% | 11 | 38 | Merit-cum-Means, SC/ST |
| NIT Nagpur (VNIT) | Nagpur | Maharashtra | Computer Science & Engineering | 98.0+ | 1,58,000 | 80% | 12 | 42 | Merit-cum-Means, SC/ST |
| NIT Nagpur (VNIT) | Nagpur | Maharashtra | Civil Engineering | 93.0+ | 1,58,000 | 68% | 6 | 20 | Merit-cum-Means |
| NIT Delhi | New Delhi | Delhi | Computer Science & Engineering | 97.5+ | 1,46,000 | 78% | 10 | 38 | Merit-cum-Means, SC/ST |
| NIT Jalandhar | Jalandhar | Punjab | Computer Science & Engineering | 96.5+ | 1,40,000 | 76% | 9 | 34 | Merit-cum-Means, SC/ST |
| NIT Patna | Patna | Bihar | Computer Science & Engineering | 97.0+ | 1,38,000 | 77% | 10 | 35 | Merit-cum-Means, SC/ST |
| NIT Silchar | Silchar | Assam | Computer Science & Engineering | 96.5+ | 1,35,000 | 76% | 9 | 32 | Merit-cum-Means, SC/ST |
| NIT Hamirpur | Hamirpur | Himachal Pradesh | Computer Science & Engineering | 95.0+ | 1,30,000 | 74% | 8 | 30 | Merit-cum-Means, SC/ST |
| NIT Raipur | Raipur | Chhattisgarh | Computer Science & Engineering | 95.5+ | 1,32,000 | 74% | 8 | 30 | Merit-cum-Means, SC/ST |
| NIT Jamshedpur | Jamshedpur | Jharkhand | Computer Science & Engineering | 96.8+ | 1,40,000 | 77% | 9 | 33 | Merit-cum-Means, SC/ST |
| NIT Goa | Ponda | Goa | Computer Science & Engineering | 96.0+ | 1,38,000 | 75% | 9 | 33 | Merit-cum-Means, SC/ST |
| NIT Srinagar | Srinagar | J&K | Computer Science & Engineering | 93.0+ | 1,20,000 | 70% | 7 | 25 | Merit-cum-Means, J&K State Scholarship |
| NIT Andhra Pradesh | Tadepalligudem | Andhra Pradesh | Computer Science & Engineering | 95.0+ | 1,28,000 | 73% | 8 | 28 | Merit-cum-Means, SC/ST |
| NIT Manipur | Imphal | Manipur | Computer Science & Engineering | 91.0+ | 1,10,000 | 66% | 6 | 22 | Merit-cum-Means, NE Region Scholarship |
| NIT Mizoram | Aizawl | Mizoram | Computer Science & Engineering | 89.0+ | 1,08,000 | 64% | 6 | 20 | Merit-cum-Means, NE Region Scholarship |
| NIT Agartala | Agartala | Tripura | Computer Science & Engineering | 92.0+ | 1,15,000 | 68% | 7 | 24 | Merit-cum-Means, NE Region Scholarship |
| NIT Meghalaya | Shillong | Meghalaya | Computer Science & Engineering | 90.0+ | 1,12,000 | 65% | 6 | 21 | Merit-cum-Means, NE Region Scholarship |
| NIT Nagaland | Dimapur | Nagaland | Computer Science & Engineering | 88.0+ | 1,05,000 | 62% | 5 | 18 | Merit-cum-Means, NE Region Scholarship |
| NIT Puducherry | Karaikal | Puducherry | Computer Science & Engineering | 93.5+ | 1,22,000 | 70% | 7 | 24 | Merit-cum-Means, SC/ST |
| NIT Uttarakhand | Srinagar (G) | Uttarakhand | Computer Science & Engineering | 94.0+ | 1,25,000 | 71% | 7 | 26 | Merit-cum-Means, SC/ST |
| NIT Arunachal Pradesh | Yupia | Arunachal Pradesh | Computer Science & Engineering | 87.0+ | 1,02,000 | 61% | 5 | 17 | Merit-cum-Means, NE Region Scholarship |
| NIT Sikkim | Ravangla | Sikkim | Computer Science & Engineering | 88.0+ | 1,05,000 | 62% | 5 | 18 | Merit-cum-Means, NE Region Scholarship |

---

## 🏛️ IIITs — Sample Dataset (26 Institutes)

> Cutoffs based on JEE Mains 2024 percentile. Fees are tentative.

| College Name | City | State | Branch | Cutoff (JEE Mains %) | Fees (₹/yr)* | Placement % | Avg Pkg (LPA) | Highest Pkg (LPA) | Scholarship |
|---|---|---|---|---|---|---|---|---|---|
| IIIT Hyderabad | Hyderabad | Telangana | Computer Science & Engineering | 99.8+ (or Top 300 JEE Adv) | 4,50,000 | 92% | 22 | 100 | Merit, SC/ST |
| IIIT Hyderabad | Hyderabad | Telangana | Electronics & Communication | 99.5+ | 4,50,000 | 87% | 16 | 60 | Merit |
| IIIT Allahabad | Prayagraj | Uttar Pradesh | Information Technology | 99.2+ | 1,80,000 | 85% | 14 | 55 | Merit-cum-Means, SC/ST |
| IIIT Allahabad | Prayagraj | Uttar Pradesh | Computer Science & Engineering | 99.4+ | 1,80,000 | 86% | 15 | 58 | Merit-cum-Means, SC/ST |
| IIIT Bangalore | Bangalore | Karnataka | Computer Science & Engineering | 99.0+ | 4,00,000 | 88% | 18 | 70 | Merit |
| IIIT Delhi | New Delhi | Delhi | Computer Science & Engineering | 99.0+ | 3,50,000 | 87% | 17 | 65 | Merit-cum-Means |
| IIIT Delhi | New Delhi | Delhi | Electronics & Communication | 98.4+ | 3,50,000 | 83% | 13 | 50 | Merit-cum-Means |
| IIIT Gwalior (ABV-IIITM) | Gwalior | Madhya Pradesh | Information Technology | 98.0+ | 1,75,000 | 81% | 12 | 44 | Merit-cum-Means, SC/ST |
| IIIT Pune | Pune | Maharashtra | Computer Science & Engineering | 98.5+ | 2,20,000 | 82% | 12 | 45 | Merit-cum-Means |
| IIIT Lucknow | Lucknow | Uttar Pradesh | Information Technology | 97.0+ | 2,00,000 | 78% | 10 | 36 | Merit-cum-Means |
| IIIT Nagpur | Nagpur | Maharashtra | Computer Science & Engineering | 96.5+ | 1,58,000 | 75% | 9 | 30 | Merit-cum-Means |
| IIIT Vadodara | Vadodara | Gujarat | Computer Science & Engineering | 96.8+ | 1,65,000 | 76% | 9 | 32 | Merit-cum-Means |
| IIIT Dharwad | Dharwad | Karnataka | Computer Science & Engineering | 95.5+ | 1,55,000 | 73% | 8 | 28 | Merit-cum-Means |
| IIIT Kottayam | Kottayam | Kerala | Computer Science & Engineering | 95.8+ | 1,56,000 | 74% | 8 | 29 | Merit-cum-Means |
| IIIT Kalyani | Kalyani | West Bengal | Computer Science & Engineering | 95.0+ | 1,48,000 | 72% | 8 | 27 | Merit-cum-Means |
| IIIT Sri City | Sri City | Andhra Pradesh | Computer Science & Engineering | 96.0+ | 2,00,000 | 75% | 9 | 32 | Merit-cum-Means |
| IIIT Jabalpur | Jabalpur | Madhya Pradesh | Information Technology | 96.5+ | 1,60,000 | 76% | 9 | 32 | Merit-cum-Means |
| IIIT Ranchi | Ranchi | Jharkhand | Computer Science & Engineering | 95.2+ | 1,52,000 | 73% | 8 | 28 | Merit-cum-Means |
| IIIT Bhopal | Bhopal | Madhya Pradesh | Computer Science & Engineering | 95.0+ | 1,75,000 | 72% | 8 | 26 | Merit-cum-Means |
| IIIT Kancheepuram | Kancheepuram | Tamil Nadu | Computer Science & Engineering | 96.0+ | 1,55,000 | 74% | 8 | 30 | Merit-cum-Means, SC/ST |
| IIIT Tiruchirappalli | Tiruchirappalli | Tamil Nadu | Computer Science & Engineering | 95.5+ | 1,80,000 | 73% | 8 | 28 | Merit-cum-Means |
| IIIT Sonipat | Sonipat | Haryana | Computer Science & Engineering | 95.5+ | 1,68,000 | 73% | 8 | 28 | Merit-cum-Means |
| IIIT Una | Una | Himachal Pradesh | Computer Science & Engineering | 95.5+ | 1,50,000 | 73% | 8 | 28 | Merit-cum-Means |
| IIIT Manipur | Imphal | Manipur | Computer Science & Engineering | 90.0+ | 1,20,000 | 65% | 6 | 20 | Merit-cum-Means, NE Region |
| IIIT Agartala | Agartala | Tripura | Computer Science & Engineering | 91.0+ | 1,18,000 | 64% | 6 | 20 | Merit-cum-Means, NE Region |
| IIIT Raichur | Raichur | Karnataka | Computer Science & Engineering | 94.5+ | 1,52,000 | 71% | 7 | 25 | Merit-cum-Means |

---

## 🏢 Top Private & State Colleges — Sample Dataset

> Cutoffs vary by state entrance exam. Fees are tentative.

| College Name | City | State | Branch | Cutoff | Fees (₹/yr)* | Placement % | Avg Pkg (LPA) | Highest Pkg (LPA) | Scholarship |
|---|---|---|---|---|---|---|---|---|---|
| BITS Pilani | Pilani | Rajasthan | Computer Science | 390+ BITSAT | 5,25,000 | 95% | 24 | 120 | Merit, Need-based |
| BITS Pilani | Pilani | Rajasthan | Electrical & Electronics | 360+ BITSAT | 5,25,000 | 84% | 14 | 55 | Merit |
| BITS Goa | Vasco da Gama | Goa | Computer Science | 375+ BITSAT | 5,25,000 | 91% | 20 | 90 | Merit, Need-based |
| BITS Hyderabad | Hyderabad | Telangana | Computer Science | 370+ BITSAT | 5,25,000 | 90% | 19 | 85 | Merit, Need-based |
| VIT Vellore | Vellore | Tamil Nadu | Computer Science & Engineering | 95+ VITEEE | 2,17,000 | 82% | 11 | 44 | Merit, Sports, Need-based |
| VIT Vellore | Vellore | Tamil Nadu | Electronics & Communication | 90+ VITEEE | 2,17,000 | 77% | 8 | 32 | Merit |
| VIT Chennai | Chennai | Tamil Nadu | Computer Science & Engineering | 93+ VITEEE | 2,17,000 | 80% | 10 | 40 | Merit, Sports |
| SRM Institute Chennai | Chennai | Tamil Nadu | Computer Science & Engineering | 85+ SRMJEE | 3,20,000 | 78% | 9 | 35 | Merit, Sports |
| Manipal Institute of Technology | Manipal | Karnataka | Computer Science & Engineering | 93+ MET | 3,80,000 | 81% | 10 | 40 | Merit, Sports |
| Thapar Institute | Patiala | Punjab | Computer Science & Engineering | 97+ JEE Mains | 3,50,000 | 83% | 12 | 48 | Merit, SC/ST |
| Amrita Vishwa Vidyapeetham | Coimbatore | Tamil Nadu | Computer Science & Engineering | 90+ AEEE | 2,50,000 | 79% | 9 | 36 | Merit, SC/ST, Sports |
| COEP Pune | Pune | Maharashtra | Computer Science & Engineering | 99.0+ MHT-CET | 1,80,000 | 84% | 12 | 50 | EBC, SC/ST, OBC, TFWS |
| COEP Pune | Pune | Maharashtra | Electronics & Telecomm. | 98.5+ MHT-CET | 1,80,000 | 80% | 10 | 38 | EBC, SC/ST |
| PICT Pune | Pune | Maharashtra | Computer Science & Engineering | 98.5+ MHT-CET | 1,50,000 | 83% | 11 | 46 | EBC, SC/ST, OBC, TFWS |
| VIT Pune | Pune | Maharashtra | Computer Science & Engineering | 98.0+ MHT-CET | 1,60,000 | 80% | 10 | 40 | EBC, SC/ST, OBC, TFWS |
| DJ Sanghvi College | Mumbai | Maharashtra | Computer Science & Engineering | 99.0+ MHT-CET | 1,80,000 | 82% | 11 | 44 | EBC, SC/ST, OBC, TFWS |
| MIT Pune | Pune | Maharashtra | Computer Science & Engineering | 97.5+ MHT-CET | 1,70,000 | 79% | 9 | 36 | EBC, SC/ST, OBC, TFWS |
| R.V. College of Engineering | Bangalore | Karnataka | Computer Science & Engineering | 99.0+ KCET/COMEDK | 1,90,000 | 83% | 12 | 50 | Merit, SC/ST, KCET |
| PES University | Bangalore | Karnataka | Computer Science & Engineering | 98.5+ KCET/COMEDK | 2,80,000 | 82% | 11 | 46 | Merit, SC/ST |
| MS Ramaiah Institute | Bangalore | Karnataka | Computer Science & Engineering | 98.0+ KCET/COMEDK | 1,75,000 | 80% | 10 | 40 | Merit, SC/ST, KCET |
| BMS College of Engineering | Bangalore | Karnataka | Computer Science & Engineering | 97.5+ KCET/COMEDK | 1,65,000 | 79% | 10 | 38 | Merit, SC/ST, KCET |
| PSG College of Technology | Coimbatore | Tamil Nadu | Computer Science & Engineering | 97+ TANCET/JEE | 1,30,000 | 80% | 9 | 35 | Merit, Government Scholarship |
| Anna University CEG | Chennai | Tamil Nadu | Computer Science & Engineering | 99.5+ TNEA | 90,000 | 84% | 12 | 50 | Govt, SC/ST, OBC, EWS |
| SSN College of Engineering | Chennai | Tamil Nadu | Computer Science & Engineering | 99.0+ TNEA | 1,50,000 | 82% | 11 | 44 | Merit, SC/ST, SNS Trust |
| Jadavpur University | Kolkata | West Bengal | Computer Science & Engineering | 98.5+ WBJEE | 25,000 | 83% | 11 | 44 | Govt, SC/ST, OBC-A/B |
| Jadavpur University | Kolkata | West Bengal | Mechanical Engineering | 96.5+ WBJEE | 25,000 | 73% | 7 | 25 | Govt, SC/ST |
| DTU Delhi | New Delhi | Delhi | Computer Science & Engineering | 99.6+ JAC Delhi | 1,62,000 | 83% | 12 | 48 | SC/ST, EWS, Delhi Domicile |
| NSUT Delhi | New Delhi | Delhi | Computer Science & Engineering | 99.5+ JAC Delhi | 1,65,000 | 82% | 11 | 44 | SC/ST, EWS, Delhi Domicile |
| IGDTUW Delhi | New Delhi | Delhi | Computer Science & Engineering | 99.4+ JAC Delhi | 1,60,000 | 81% | 11 | 44 | SC/ST, EWS, Delhi Domicile |

---

## 🤖 How to Use This Dataset for AI/ML Training

### Step 1 — Data Collection Pipeline

```python
# Recommended data collection sources (Python scraping / API)
sources = {
    "JoSAA":    "https://josaa.nic.in  → Round-wise cutoff PDFs → parse with pdfplumber",
    "NIRF":     "https://nirfindia.org → Download Excel reports → parse with pandas",
    "AICTE":    "https://aicte-india.org → Approved institute list → parse with requests",
    "MHT-CET":  "https://cetcell.mahacet.org → CAP round allotment → parse with selenium",
    "Shiksha":  "https://shiksha.com → Placement/review data → scrape with BeautifulSoup",
}
```

### Step 2 — Data Preprocessing

```python
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler

df = pd.read_csv("india_colleges.csv")

# Encode categorical features
le = LabelEncoder()
df["college_type_enc"]  = le.fit_transform(df["college_type"])
df["branch_enc"]        = le.fit_transform(df["branch"])
df["state_enc"]         = le.fit_transform(df["state"])

# Normalize numerical features
scaler = StandardScaler()
df[["fees_norm", "placement_norm", "avg_pkg_norm"]] = scaler.fit_transform(
    df[["fees_per_year", "placement_percent", "avg_package_lpa"]]
)
```

### Step 3 — Train Admission Prediction Model

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

# Features: student percentile, category, branch, state
X = df[["percentile", "category_enc", "branch_enc", "state_enc"]]
y = df["admission_chance"]  # 0=Low, 1=Medium, 2=High

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

model = RandomForestClassifier(n_estimators=200, max_depth=10, random_state=42)
model.fit(X_train, y_train)
print(f"Accuracy: {model.score(X_test, y_test):.2%}")
```

### Step 4 — College Recommendation Engine

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Build college feature matrix
feature_cols = ["fees_norm", "placement_norm", "avg_pkg_norm",
                "college_type_enc", "state_enc", "branch_enc"]
college_matrix = df[feature_cols].values

# Student preference vector (from form input)
student_prefs = np.array([[0.4, 0.9, 0.8, 1, 3, 5]])  # fees, placement, pkg, type, state, branch

# Compute similarity
similarities = cosine_similarity(student_prefs, college_matrix)[0]
df["match_score"] = similarities

# Top 25 recommendations
top_colleges = df.nlargest(25, "match_score")[
    ["college_name", "city", "branch", "avg_package_lpa", "fees_per_year", "match_score"]
]
print(top_colleges)
```

### Step 5 — Deploy as Flask API

```python
from flask import Flask, request, jsonify
import pickle

app = Flask(__name__)
model = pickle.load(open("admission_model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    features = [[
        data["percentile"],
        data["category_enc"],
        data["branch_enc"],
        data["state_enc"]
    ]]
    prediction = model.predict(features)[0]
    labels = {0: "Low Chance", 1: "Medium Chance", 2: "High Chance"}
    return jsonify({"result": labels[prediction]})

if __name__ == "__main__":
    app.run(debug=True)
```

---

## 📊 Dataset Statistics

| Metric | Value |
|---|---|
| Total rows (approx. with all branches) | 5,000+ |
| IIT branches covered | 90+ |
| NIT branches covered | 120+ |
| IIIT branches covered | 60+ |
| Private college branches | 200+ |
| Features per row | 30 columns |
| Update frequency recommended | Every 6 months (post-admission season) |

---

> ⚠ **Important Disclaimer:** All fees shown in this document are **tentative and indicative only**. Actual fee structures may vary. Students must contact the respective college directly or visit the official website for confirmed details. Cutoffs and placement data are based on recent years and may change annually.

---

*Build smart. Start lean. Scale with data.*
