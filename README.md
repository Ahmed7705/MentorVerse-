<h1 align="center">
  <br>
  🎓 MentorVerse
  <br>
</h1>

<h4 align="center">A smart academic advising platform connecting students with their advisors — built with Flask & MongoDB.</h4>

<p align="center">
  <img src="https://img.shields.io/badge/Python-Flask-blue?style=for-the-badge&logo=flask" />
  <img src="https://img.shields.io/badge/Database-MongoDB-green?style=for-the-badge&logo=mongodb" />
  <img src="https://img.shields.io/badge/Frontend-HTML%20%7C%20CSS%20%7C%20JS-orange?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Status-In%20Development-yellow?style=for-the-badge" />
</p>

---

## 📌 About MentorVerse

**MentorVerse** is a graduation project web application designed to bridge the gap between university students and their academic advisors. The platform allows students to track their academic journey and enables advisors to monitor student performance — all in one place.

---

## ✨ Features

### 👩‍🎓 Student Portal
- 📊 **Dashboard** — Overview of academic status and quick access to all features
- 📋 **Transcript** — View full academic transcript and grades
- 🗓️ **Schedule** — View weekly class schedule
- 🔔 **Notifications** — Receive important alerts and updates
- ⚙️ **Settings** — Manage profile and account preferences

### 👩‍🏫 Advisor Portal
- 👥 **Students List** — View and manage assigned students
- 📈 **Performance Cards** — Quick performance overview for each student
- 📉 **Detailed Performance** — In-depth academic performance analytics
- 🔔 **Notifications** — Stay informed with student activity updates
- ⚙️ **Settings** — Manage advisor profile

### 🔐 Authentication System
- Secure **Register / Login** for both students and advisors
- **Forgot Password** with OTP verification via email
- Role-based access control (Student / Advisor / Admin)

---

## 🛠️ Tech Stack

| Layer       | Technology                     |
|-------------|-------------------------------|
| Backend     | Python (Flask)                |
| Database    | MongoDB (PyMongo)             |
| Frontend    | HTML5, CSS3, JavaScript       |
| Auth        | Werkzeug (Password Hashing)   |
| Email OTP   | smtplib (Gmail SMTP)          |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- MongoDB (running locally on port `27017`)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/iirawan-d/MentorVerse-.git
cd MentorVerse-

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the application
python app.py
```

Then open your browser and go to: **http://127.0.0.1:5000**

---

## 📁 Project Structure

```
MentorVerse/
│
├── app.py                  # Main Flask application & routes
├── requirements.txt        # Python dependencies
│
├── templates/              # HTML templates (Jinja2)
│   ├── Home-page.html
│   ├── login-page.html
│   ├── register-page.html
│   ├── student-dashboard-page.html
│   ├── advisor-students-list-page.html
│   └── ...
│
├── static/                 # Static assets
│   └── (CSS, JS, Images)
│
└── README.md
```

---

## 👩‍💻 Team

This project was developed as a **Graduation Project** at **Jazan University**.

| Name | Role | GitHub |
|------|------|--------|
| Rawan | Developer | [@iirawan-d](https://github.com/iirawan-d) |

---

## 📄 License

This project is for academic purposes only.

---

<p align="center">Made with ❤️ by the MentorVerse Team</p>
