# Hi there 👋, I'm Shaik Asif

🚀 About Me

🎓 Student at K.S.R.M. College of Engineering

💼 Currently working as a Full-Stack Developer Intern at Teclusion.ai

💻 Passionate about Software Development, Artificial Intelligence, and Building Real-World Applications.

🌱 Currently learning Machine Learning, Advanced Full-Stack Development, Cloud Technologies, and Data Structures & Algorithms.

🔭 Working on industry projects during my internship along with personal and academic projects.

⚡ Skilled in building responsive web applications using modern technologies and continuously improving my problem-solving skills.

🎯 Career Goal: Become a highly skilled Full-Stack Developer and AI Engineer, creating scalable software solutions powered by AI.

---

## 🛠️ Tech Stack

### Languages
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![C](https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white)

### Web Development
![HTML5](https://img.shields.io/badge/HTML-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

### Tools
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)

---

## 📊 GitHub Stats

![GitHub Stats](https://github-readme-stats.vercel.app/api?username=[YOUR_USERNAME]&show_icons=true&theme=tokyonight)

![Top Languages](https://github-readme-stats.vercel.app/api/top-langs/?username=[YOUR_USERNAME]&layout=compact&theme=tokyonight)

---

## 🔥 GitHub Streak

![GitHub Streak](https://streak-stats.demolab.com?user=asifshaik48626-cloud&theme=tokyonight)

---

## 🌟 Featured Projects

### 📌 https://tennis-pi-rouge.vercel.app/
Brief description of your project.

### 📌 Project 2
Brief description of your project.

### 📌 Project 3
Brief description of your project.

---

## 📫 Connect With Me

- GitHub: 
- LinkedIn: https://linkedin.com/in/[YOUR_LINKEDIN]
- Email: asifshaik48626@gmail.com

---

### 💡 Quote

> "Code. Learn. Build. Repeat."

⭐ Thanks for visiting my profile!

---

# 🏥 MediSphere AI — Multilingual Clinical Intelligence & Doctor-Assisted Guidance

MediSphere AI is a robust clinical decision-support and patient-guidance platform built with safety-first deterministic overrides and multilingual integration.

## 🚀 Key Features
- **Deterministic Safety Firewall**: Bypasses AI generation for emergency warning signs (e.g., chest pain, infant fever, stiff neck, slurred speech) to prevent delayed critical care.
- **Three-Column Care Summary**: Dynamically organizes patient-appropriate movements, complementary wellness options, and medications.
- **CDC/WHO Guideline Retrieval**: Queries standard clinical guidelines and attaches Grade A/B evidence citations to generated care plans.
- **Interactive Multi-Step Intake**: Guides patients through specialized Fever and Headache symptom intakes.
- **Structured OCR Prescription Extraction**: Uploads documents and extracts medicine properties, strength, and frequency records dynamically.
- **Clinical Review Workspace**: Clinician interface for doctors to review patient cases, edit recommendations, and sign off or reject care summaries.

---

## 🛠️ Repository Architecture

```
Medisphere-Ai/
├── backend/
│   ├── app/
│   │   ├── models/        # 17 SQLAlchemy Relational Schemas
│   │   ├── routers/       # Auth, Intakes, Safety, Guidelines, Reports, OCR uploads
│   │   ├── services/      # Deterministic Safety Engine, WHO/CDC Guidelines Lookup
│   │   ├── utils/         # PBKDF2 Password Hashing
│   │   ├── seed.py        # Database catalog & credential seeder
│   │   └── main.py        # FastAPI Application Engine
│   └── requirements.txt   # Python Dependencies
│
└── frontend/
    ├── src/
    │   ├── components/    # Navigation, Layout, UrgencyBadge, ThreeColumnResults
    │   ├── context/       # Auth Session Management
    │   ├── pages/         # Landing Page, Login, Patient Intake, Doctor Workspace
    │   └── App.tsx        # Route Guards & Route Configuration
    ├── tailwind.config.js # Premium UI/UX Design System
    └── package.json       # React bundler config
```

---

## ⚡ Setup & Run Instructions

### 1. Run the Monolith Backend
Activate the local Python virtual environment and seed clinical databases:
```bash
# Navigate to the backend directory
cd backend

# Activate virtual environment
source .venv/bin/activate

# Seed default test users and catalog details
python -m app.seed

# Run the FastAPI server
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
*The Swagger API documentation will be live at `http://127.0.0.1:8000/docs`.*

### 2. Default Test Credentials
- **Patient User**: `patient@medisphere.com` / `password123`
- **Doctor User**: `doctor@medisphere.com` / `password123`

### 3. Launch the Frontend
Compile and bundle the React web page assets:
```bash
cd frontend
npm install
npm run dev
```
*The web interface will open at `http://localhost:3000` (automatically proxying backend requests to port 8000).*

