?"""
Student Record System - Flask Backend
Project 1 of 300-Day AI/ML Roadmap
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

class Student:
    school = "Tech Academy"
    total_students = 0

    def __init__(self, name, marks, section="A"):
        self.name = name
        self.marks = marks
        self.section = section
        Student.total_students += 1

    def __str__(self):
        return f"{self.name} [{self.get_avg():.1f}]"

    def get_avg(self):
        return sum(self.marks) / len(self.marks)

    def to_dict(self):
        avg = round(self.get_avg(), 2)
        return {
            "name": self.name,
            "marks": self.marks,
            "avg": avg,
            "grade": get_grade(avg),
            "status": "Pass" if avg >= 40 else "Fail",
            "section": self.section,
        }

_students = [
    Student("Sneha",  [95, 88, 92], section="A"),
    Student("Uday",   [85, 90, 78], section="A"),
    Student("Ravi",   [70, 65, 80], section="A"),
    Student("Priya",  [50, 45, 55], section="B"),
    Student("Arjun",  [30, 35, 28], section="B"),
    Student("Meera",  [92, 96, 89], section="A"),
]
Student.total_students = len(_students)

def get_grade(avg):
    if avg >= 90: return "A"
    elif avg >= 75: return "B"
    elif avg >= 60: return "C"
    elif avg >= 40: return "D"
    else:          return "F"

def create_student(name, marks, section="A"):
    s = Student(name, marks, section)
    _students.append(s)
    return s

def find_by_name(students, name):
    for s in students:
        if s.name.lower() == name.lower().strip():
            return s
    return None

def get_topper(students):
    return max(students, key=lambda x: x.get_avg())

def sort_by_grade(students):
    return sorted(students, key=lambda x: x.get_avg(), reverse=True)

def merge_sections(section_a, section_b):
    merged = section_a + section_b
    seen = set()
    result = []
    for s in merged:
        if s.name.lower() not in seen:
            result.append(s)
            seen.add(s.name.lower())
    return sorted(result, key=lambda s: s.get_avg(), reverse=True)

def generate_report(students):
    sorted_s = sorted(students, key=lambda s: s.get_avg(), reverse=True)
    report = []
    for rank, s in enumerate(sorted_s, start=1):
        avg = round(s.get_avg(), 2)
        report.append({
            "rank": rank,
            "name": s.name,
            "avg": avg,
            "grade": get_grade(avg),
            "status": "Pass" if avg >= 40 else "Fail",
            "section": s.section,
        })
    return report

def export_data(students):
    lines = ["Name,Average,Grade,Status,Section"]
    for s in sorted(students, key=lambda s: s.get_avg(), reverse=True):
        avg = round(s.get_avg(), 2)
        lines.append(f"{s.name},{avg},{get_grade(avg)},{'Pass' if avg >= 40 else 'Fail'},{s.section}")
    return "\n".join(lines)

def compare_students(s1, s2):
    avg1 = round(s1.get_avg(), 2)
    avg2 = round(s2.get_avg(), 2)
    if avg1 > avg2:
        return f"{s1.name} ({avg1}) > {s2.name} ({avg2})"
    elif avg1 < avg2:
        return f"{s2.name} ({avg2}) > {s1.name} ({avg1})"
    else:
        return f"{s1.name} and {s2.name} are equal ({avg1})"

@app.route("/api/students", methods=["GET"])
def api_get_students():
    section = request.args.get("section")
    students = _students if not section else [s for s in _students if s.section == section]
    return jsonify([s.to_dict() for s in sort_by_grade(students)])

@app.route("/api/students", methods=["POST"])
def api_add_student():
    data = request.json
    name = data.get("name", "").strip()
    marks = data.get("marks", [])
    section = data.get("section", "A")
    if not name:
        return jsonify({"error": "Name is required"}), 400
    if not marks or not isinstance(marks, list):
        return jsonify({"error": "Marks must be a non-empty list"}), 400
    if find_by_name(_students, name):
        return jsonify({"error": f"Student '{name}' already exists"}), 409
    student = create_student(name, marks, section)
    return jsonify(student.to_dict()), 201

@app.route("/api/students/<name>", methods=["PUT"])
def api_update_student(name):
    student = find_by_name(_students, name)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    data = request.json
    new_marks = data.get("marks")
    if not new_marks:
        return jsonify({"error": "New marks required"}), 400
    student.marks = new_marks
    return jsonify(student.to_dict())

@app.route("/api/students/<name>", methods=["DELETE"])
def api_delete_student(name):
    student = find_by_name(_students, name)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    _students.remove(student)
    Student.total_students -= 1
    return jsonify({"message": f"Student '{name}' deleted"})

@app.route("/api/stats", methods=["GET"])
def api_stats():
    if not _students:
        return jsonify({"count": 0})
    avgs = [s.get_avg() for s in _students]
    grades = [get_grade(a) for a in avgs]
    grade_counts = {g: grades.count(g) for g in ["A", "B", "C", "D", "F"]}
    sections = list(set(s.section for s in _students))
    section_counts = {sec: len([s for s in _students if s.section == sec]) for sec in sections}
    return jsonify({
        "count": len(_students),
        "avg_of_avgs": round(sum(avgs) / len(avgs), 2),
        "highest": round(max(avgs), 2),
        "lowest": round(min(avgs), 2),
        "pass_count": sum(1 for a in avgs if a >= 40),
        "fail_count": sum(1 for a in avgs if a < 40),
        "grade_distribution": grade_counts,
        "section_distribution": section_counts,
        "topper": get_topper(_students).name,
    })

@app.route("/api/topper", methods=["GET"])
def api_topper():
    if not _students:
        return jsonify({"error": "No students"}), 404
    return jsonify(get_topper(_students).to_dict())

@app.route("/api/compare", methods=["GET"])
def api_compare():
    name1 = request.args.get("a")
    name2 = request.args.get("b")
    s1 = find_by_name(_students, name1)
    s2 = find_by_name(_students, name2)
    if not s1 or not s2:
        return jsonify({"error": "One or both students not found"}), 404
    return jsonify({"result": compare_students(s1, s2)})

@app.route("/api/report", methods=["GET"])
def api_report():
    section = request.args.get("section")
    students = _students if not section else [s for s in _students if s.section == section]
    return jsonify(generate_report(students))

@app.route("/api/export", methods=["GET"])
def api_export():
    section = request.args.get("section")
    students = _students if not section else [s for s in _students if s.section == section]
    csv_text = export_data(students)
    return Response(
        csv_text,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=student_report.csv"}
    )

@app.route("/api/merge", methods=["GET"])
def api_merge():
    sec_a = [s for s in _students if s.section == "A"]
    sec_b = [s for s in _students if s.section == "B"]
    merged = merge_sections(sec_a, sec_b)
    return jsonify([s.to_dict() for s in merged])

if __name__ == "__main__":
    app.run(debug=True, port=5000)

