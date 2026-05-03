import json
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY")

students = {
    "student1": {
        "name": "Student 1",
        "major": "Computer Science",
        "transcript": [
            {"course_name": "Operating Systems", "grade": "A", "absences": 4},
            {"course_name": "Database Systems", "grade": "A+", "absences": 1},
            {"course_name": "Software Engineering", "grade": "B+", "absences": 0},
            {"course_name": "AI Fundamentals", "grade": "NG", "absences": 0},
            {"course_name": "Machine Learning Intro", "grade": "NG", "absences": 1}
        ]
    },
    "student2": {
        "name": "Student 2",
        "major": "Mechanical Engineering",
        "transcript": [
            {"course_name": "Robotics II", "grade": "D+", "absences": 0},
            {"course_name": "Fluid Mechanics", "grade": "D", "absences": 1},
            {"course_name": "Control Systems", "grade": "D+", "absences": 0},
            {"course_name": "Mechatronics", "grade": "D", "absences": 0},
            {"course_name": "AI in Robotics", "grade": "C+", "absences": 0}
        ]
    },
    "student3": {
        "name": "Student 3",
        "major": "Computer Science",
        "transcript": [
            {"course_name": "Algorithms", "grade": "A", "absences": 1},
            {"course_name": "Linear Algebra", "grade": "A+", "absences": 0},
            {"course_name": "Statistics", "grade": "C", "absences": 4},
            {"course_name": "Operating Systems", "grade": "NG", "absences": 0},
            {"course_name": "Database Systems", "grade": "NG", "absences": 0}
        ]
    }
}

import json
import os
from openai import OpenAI

client = OpenAI(api_key="OPENAI_API_KEY") 

def generate_recommendations(student):
    prompt = f"""
You are an academic advisor in MentorVerse.

Analyze this student's transcript and generate exactly 3 academic recommendations.

Rules:
- Recommendations must be specific to the student's grades and absences.
- Do not give generic advice.
- Keep each recommendation short.
- Return only a JSON array of 3 strings.

Student data:
{json.dumps(student, indent=2)}
"""

    response = client.responses.create(
        model="gpt-5",
        input=prompt
    )

    return json.loads(response.output_text) 

results = {}

for student_id, student_data in students.items():
    print(f"Generating recommendations for {student_id}...")
    results[student_id] = generate_recommendations(student_data)

with open("recommendations.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("✅ Saved to recommendations.json")