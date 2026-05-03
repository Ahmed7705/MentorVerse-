from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from bson.objectid import ObjectId
import smtplib
import random
import json
import os
from openai import OpenAI


app = Flask(__name__, template_folder="templates", static_folder="static", static_url_path="/")
app.secret_key = "62a758d4-460c-4220-b277-693f0502d1da"

client_ai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=1000)
db = client["MentorVerseDB"]
reset_pins = {}

students = db["students"]
advisors = db["advisors"]


def student_required():
    return "user_id" in session and session.get("role") == "student"


def advisor_required():
    return "user_id" in session and session.get("role") == "advisor"


def get_logged_user():
    if "user_id" not in session:
        return None

    user_id = session["user_id"]

    if session.get("role") == "student":
        return students.find_one({"_id": ObjectId(user_id)})
    else:
        return advisors.find_one({"_id": ObjectId(user_id)})


def get_student_for_recommendations():
    if session.get("role") == "student":
        return get_logged_user()

    student_id = request.args.get("student_id")

    if student_id:
        try:
            student = students.find_one({"_id": ObjectId(student_id)})
            if student:
                return student
        except:
            pass

        student = students.find_one({"student_id": student_id})
        if student:
            return student

    return students.find_one()


def build_student_data(user=None):
    if not user:
        return {
            "student_name": "Student",
            "current_term": "Current Term",
            "next_term": "Next Term",
            "courses": ["AI Fundamentals", "Operating Systems", "Database Systems"],
            "credit_hours": 15,
            "absences": 8,
            "previous_semesters_performance": "stable",
            "current_term_performance": "declining"
        }

    return {
        "student_name": user.get("firstName", "Student"),
        "current_term": user.get("current_term", "Current Term"),
        "next_term": user.get("next_term", "Next Term"),
        "courses": user.get("courses", []),
        "credit_hours": user.get("credit_hours", 0),
        "absences": user.get("absences", 0),
        "previous_semesters_performance": user.get("previous_semesters_performance", "not available"),
        "current_term_performance": user.get("current_term_performance", "not available")
    }


def fallback_recommendations(audience):
    if audience == "student":
        return [
            "Improve your attendance this term and keep your course load balanced next term.",
            "Use your previous performance to plan better study habits for the current term.",
            "Focus on demanding courses and manage your weekly study time carefully."
        ]

    return [
        "Monitor the student's attendance and discuss a balanced course load for next term.",
        "Review the student’s current performance compared with previous semesters.",
        "Recommend short follow-up meetings to support progress in demanding courses."
    ]


def generate_ai_recommendations(student_data, audience):
    try:
        prompt = f"""
You are an academic advising assistant in MentorVerse.

Generate exactly 3 short academic recommendations for the {audience}.

Rules:
- Each recommendation must be one short sentence only.
- Use absences, courses, credit hours, previous semesters performance, and current term performance.
- Do not focus on grades.
- Mention next term planning when useful.
- Student recommendations should speak directly to the student.
- Advisor recommendations should guide the advisor about the student.
- Return only a JSON array of 3 strings.

Student data:
{json.dumps(student_data, indent=2)}
"""

        response = client_ai.responses.create(
            model="gpt-4.1-mini",
            input=prompt
        )

        text = response.output[0].content[0].text.strip()
        return json.loads(text)

    except Exception as e:
        print("AI recommendation error:", e)
        return fallback_recommendations(audience)

@app.route("/get-recommendations")
def get_recommendations():
    try:
        student = get_student_for_recommendations()
    except Exception as e:
        print("MongoDB connection error:", e)
        student = None

    student_data = build_student_data(student)

    student_recs = generate_ai_recommendations(student_data, "student")
    advisor_recs = generate_ai_recommendations(student_data, "advisor")

    return jsonify({
        "student": {
            "data_used": student_data,
            "student_recommendations": student_recs,
            "advisor_recommendations": advisor_recs
        }
    })
@app.route("/")
def home():
    return "API work"


@app.route("/Home-page/")
def home_page():
    return render_template("Home-page.html")


@app.route("/faq-page/")
def faq_page():
    return render_template("faq-page.html")


@app.route("/contact-us-page/")
def contact_us_page():
    return render_template("contact-us-page.html")


@app.route("/about-us-page/")
def about_us_page():
    return render_template("about-us-page.html")


@app.route("/error-page/")
def error_page():
    return render_template("error-page.html")


@app.route("/login-page/", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        role = request.form.get("role")

        if role == "advisor":
            user = advisors.find_one({"email": email})
        else:
            user = students.find_one({"email": email})

        if not user:
            flash("User not found")
            return redirect(url_for("login_page"))

        if not check_password_hash(user["password"], password):
            flash("Incorrect password")
            return redirect(url_for("login_page"))

        session["user_id"] = str(user["_id"])
        session["email"] = user["email"]
        session["role"] = user["role"]

        if role == "student":
            return redirect(url_for("student_dashboard_page"))
        else:
            return redirect(url_for("advisor_students_list_page"))

    return render_template("login-page.html")


@app.route("/register-page/", methods=["GET", "POST"])
def register_page():
    if request.method == "POST":
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        email = request.form.get("email")
        university_id = request.form.get("universityID")
        password = request.form.get("password")
        role = request.form.get("role")

        if not firstname or not lastname or not email or not university_id or not password:
            flash("Please fill all fields")
            return redirect(url_for("register_page"))

        existing_student = students.find_one({
            "$or": [{"email": email}, {"student_id": university_id}]
        })

        existing_advisor = advisors.find_one({
            "$or": [{"email": email}, {"advisor_id": university_id}]
        })

        if existing_student or existing_advisor:
            flash("User already exists")
            return redirect(url_for("register_page"))

        if role == "advisor":
            user = {
                "aid": "ad",
                "firstName": firstname,
                "lastName": lastname,
                "email": email,
                "advisor_id": university_id,
                "password": generate_password_hash(password),
                "advisor_students": [],
                "role": role,
                "office": "Building A, Room 101",
                "bio": "Academic advisor in MentorVerse.",
                "gender": "Female"
            }
            advisors.insert_one(user)

        else:
            user = {
                "firstName": firstname,
                "lastName": lastname,
                "email": email,
                "student_id": university_id,
                "password": generate_password_hash(password),
                "role": role,

                "current_term": "Current Term",
                "next_term": "Next Term",
                "courses": ["AI Fundamentals", "Operating Systems", "Database Systems"],
                "credit_hours": 15,
                "absences": 8,
                "previous_semesters_performance": "stable",
                "current_term_performance": "declining",

                "transcript": [],
                "schedule": []
            }
            students.insert_one(user)

        return redirect(url_for("login_page"))

    return render_template("register-page.html")


@app.route("/forgot-password-page/", methods=["GET", "POST"])
def forgot_password_page():
    step = session.get("step", "email")

    if request.method == "POST":
        if step == "email":
            email = request.form.get("email")
            user = students.find_one({"email": email})

            if not user:
                flash("No account found with this email")
                return redirect(url_for("forgot_password_page"))

            pin = str(random.randint(1000, 9999))
            reset_pins[email] = pin
            print("OTP (for testing):", pin)

            flash("Verification code sent to your email")
            session["reset_email"] = email
            session["step"] = "otp"
            return redirect(url_for("forgot_password_page"))

        elif step == "otp":
            entered_pin = request.form.get("pin")
            email = session.get("reset_email")

            if reset_pins.get(email) != entered_pin:
                flash("Invalid verification code")
                return redirect(url_for("forgot_password_page"))

            session["step"] = "reset"
            return redirect(url_for("forgot_password_page"))

        elif step == "reset":
            email = session.get("reset_email")
            password = request.form.get("password")

            students.update_one(
                {"email": email},
                {"$set": {"password": generate_password_hash(password)}}
            )

            reset_pins.pop(email, None)
            session.clear()

            flash("Password updated successfully")
            return redirect(url_for("login_page"))

    return render_template("forgot-password-page.html", step=session.get("step", "email"))


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("login_page"))


@app.route("/student-dashboard-page/", methods=["GET", "POST"])
def student_dashboard_page():
    if "user_id" not in session:
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("student-dashboard-page.html", user=user)


@app.route("/student-transcript-page/")
def student_transcript_page():
    if not student_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("student-transcript-page.html", transcript=user.get("transcript", []))


@app.route("/student-schedule-page/")
def student_schedule_page():
    if not student_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("student-schedule-page.html", schedule=user.get("schedule", []))


@app.route("/student-notification-page/")
def student_notification_page():
    if not student_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("student-notification-page.html", user=user)


@app.route("/student-settings-page/")
def student_settings_page():
    if not student_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("student-settings-page.html", user=user)


@app.route("/advisor-students-list-page/")
def advisor_students_list_page():
    if not advisor_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    students_list = list(students.find())

    return render_template(
        "advisor-students-list-page.html",
        user=user,
        students=students_list
    )


@app.route("/advisor-student-performance-cards/")
def advisor_student_performance_cards():
    if not advisor_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("advisor-student-performance-cards.html", user=user)


@app.route("/advisor-student-performance-page/")
def advisor_student_performance_page():
    if not advisor_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("advisor-student-performance-page.html", user=user)


@app.route("/advisor-notification-page/")
def advisor_notification_page():
    if not advisor_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("advisor-notification-page.html", user=user)


@app.route("/advisor-settings-page/")
def advisor_settings_page():
    if not advisor_required():
        return redirect(url_for("login_page"))

    user = get_logged_user()
    return render_template("advisor-settings-page.html", user=user)


@app.route("/admin-page/")
def admin_page():
    return render_template("admin-page.html")


if __name__ == "__main__":
    app.run(debug=True)