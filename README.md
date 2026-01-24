# WellSure: AI-Powered Healthcare Companion

WellSure is a comprehensive healthcare platform that combines **AI-driven symptom diagnosis** with a complete **telemedicine system**. Users can check symptoms, get instant disease predictions, book appointments with specialists, and manage prescriptions—all in one place.

![WellSure Dashboard](static/img/dashboard_preview.png)

## 🚀 Live Demo
**[https://wellsure-an0b.onrender.com](https://wellsure-an0b.onrender.com)**  
*Note: Hosted on Render Free Tier. Initial load may take ~50 seconds due to cold start.*

---

## ✨ Features

### 🤖 AI Diagnosis Engine
- **Rules-Based & ML Analysis**: Checks user symptoms against a medical dataset to predict potential conditions (e.g., Flu, Migraine, COVID-19).
- **Instant Reports**: Generates a downloadable PDF report with:
    - Predicted Disease & Confidence Level
    - Description & Precautions
    - Recommended Medication & Diet
    - Specialized Workout Plans
- **Emergency Detection**: Flags critical keywords (e.g., "chest pain", "breathing difficulty") and advises immediate care.

### 🏥 Telemedicine & Appointments
- **Doctor Discovery**: Find doctors by specialization (Cardiologist, Dermatologist, etc.) or location.
- **Appointment Booking**: Schedule visits instantly with payments handled via Stripe (simulated).
- **Teleconsultation**: Doctor-Patient video call integration (via meeting links).
- **Digital Prescriptions**: Doctors can upload prescriptions directly to the patient's dashboard.

### 👥 User Roles
- **Patients**: Check symptoms, book appointments, view history, rate doctors.
- **Doctors**: Manage schedule, view appointments, upload prescriptions, update profile.
- **Admins**: Manage users, doctors, specializations, and view system logs.

---

## 🛠️ Technology Stack

- **Backend**: Python (Flask)
- **Database**: PostgreSQL (Hosted on Supabase)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap 5)
- **Deployment**: Render (Web Service)
- **AI/ML**: Scikit-learn, Pandas, NumPy (Rules-based fallback for low-resource environments)
- **Tools**: Gunicorn, Psycopg2, ReportLab (PDF Gen)

---

## ⚙️ Local Installation

### Prerequisites
- Python 3.9+
- PostgreSQL Database (Local or Cloud)

### Steps
1. **Clone the Repo**
   ```bash
   git clone https://github.com/UtsavYadav1/WellSure.git
   cd WellSure
   ```

2. **Install Dependencies**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements_render.txt
   ```

3. **Configure Environment**
   Create a `.env` file in the root directory:
   ```env
   # PostgreSQL Connection String
   DATABASE_URL=postgresql://user:password@localhost:5432/wellsure_db
   
   # Security
   SECRET_KEY=your_secret_key_here
   
   # Optional: Google OAuth
   GOOGLE_CLIENT_ID=your_client_id
   GOOGLE_CLIENT_SECRET=your_client_secret
   ```

4. **Initialize Database**
   You can use the provided SQL scripts or Python helpers:
   ```bash
   # Run schema setup (Manual or via tool)
   # Import schema_postgres.sql into your database
   ```

5. **Run the App**
   ```bash
   python main.py
   ```
   Visit `http://localhost:8000`

---

## ☁️ Deployment (Render + Supabase)

This project is configured for seamless deployment on Render.

1. **Database**: Create a Postgres database on Supabase.
2. **Service**: Create a **Web Service** on Render connected to this repo.
3. **Environment**:
   - `Runtime`: Python 3
   - `Build Command`: `pip install -r requirements_render.txt`
   - `Start Command`: `gunicorn main:app`
   - `PYTHON_VERSION`: `3.9.18`
4. **Variables**: Add `DATABASE_URL` from Supabase to Render Environment variables.

---

## 📂 Project Structure

```
WellSure/
├── main.py                 # Application Entry Point (Routes & Logic)
├── database.py             # PostgreSQL Connection Handler
├── rules_engine.py         # Symptom Analysis Logic
├── templates/              # HTML Pages (Jinja2)
├── static/                 # CSS, JS, Images, Uploads
│   ├── css/
│   ├── js/
│   └── uploads/            # Prescriptions & Reports
├── requirements.txt        # Dependencies
├── render.yaml             # Render Deployment Config
└── ...
```

---

## 🛡️ License
This project is open-source and available under the **MIT License**.

Built with ❤️ by **Utsav Yadav**.
