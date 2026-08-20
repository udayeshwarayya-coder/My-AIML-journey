"""
Day 8 Backend — Employee Payroll System
Your job: Fill in each TODO below using your practice.py functions.
Read the guide file for exact instructions on what to write where.

TO RUN:
  pip install flask flask-cors
  python app.py
  Then open frontend/index.html in your browser.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

# ── Import your classes and functions from practice.py ──
from practice import (
    Employee, Manager, Intern,      # Days 5-7 classes
    department_summary,             # Day 8 Task 1
    highest_earner,                 # Day 8 Task 2
    payroll_report,                 # Day 8 Task 3
)

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# In-memory list — holds Employee / Manager / Intern objects
employees = []


# ════════════════════════════════════════════════════════
# TASK 1 — GET /api/employees
# Returns all employees as JSON.
# Function to use: emp.get_details()  ← Day 5
# ════════════════════════════════════════════════════════
@app.route('/api/employees', methods=['GET'])
def get_employees():
    # TODO: return all employees using get_details()
    return jsonify([emp.get_details() for emp in employees])


# ════════════════════════════════════════════════════════
# TASK 2 — POST /api/employees
# Adds a new employee from JSON body.
# Functions to use: Employee / Manager / Intern __init__  ← Day 5
# Body: { name, emp_id, type, department, base_salary,
#         team_size?, stipend?, college? }
# ════════════════════════════════════════════════════════
@app.route('/api/employees', methods=['POST'])
def add_employee():
    # TODO: read JSON, create correct object, append to employees
    data=request.get_json(force=True,silent=True)
    if not data: return jsonify({"error":"invalid jason"}),400
    name=data.get("name","").strip()    
    emp_id=data.get("emp_id","").strip()
    base_salary=int(data.get("base_salary",0))
    department=data.get("department","General")
    emp_type=data.get("type","Employee")
    if not name or not emp_id:
        return jsonify({"error":"name and emp_id are required"}),400
    if any (e.emp_id==emp_id for e in employees):
        return jsonify({"error":"emp_id already exists"}),409
    if emp_type=='Manager':
        emp=Manager(name,emp_id,base_salary,department,team_size=int(data.get("team_size",0)))
    elif emp_type=='Intern':
        emp=Intern(name,emp_id,0,department,stipend=data.get("stipend",0),college=data.get("college","unknow"))
    else:
        emp = Employee(name, emp_id, base_salary, department)
    employees.append(emp)
    return jsonify(emp.get_details()),201

# ════════════════════════════════════════════════════════
# TASK 3 — DELETE /api/employees/<emp_id>
# Removes employee by ID.
# Concept: emp_id comparison  ← Day 7 __eq__
# ════════════════════════════════════════════════════════
@app.route('/api/employees/<emp_id>', methods=['DELETE'])
def remove_employee(emp_id):
    # TODO: filter employees list, return 404 if not found
    global employees
    new_list = [e for e in employees if e.emp_id != emp_id]
    if len(new_list) == len(employees):
        return jsonify({"error": "Not found"}), 404
    employees = new_list
    return jsonify({"message": "Removed"}), 200


# ════════════════════════════════════════════════════════
# TASK 4 — GET /api/employees/<emp_id>
# Returns one employee by ID.
# Function to use: emp.get_details()  ← Day 5
# ════════════════════════════════════════════════════════
@app.route('/api/employees/<emp_id>', methods=['GET'])
def get_employee(emp_id):
    # TODO: find emp, return get_details() or 404
    emp = next((e for e in employees if e.emp_id == emp_id), None)
    if not emp:
        return jsonify({"error": "Not found"}), 404
    return jsonify(emp.get_details())


# ════════════════════════════════════════════════════════
# TASK 5 — GET /api/employees/<emp_id>/pay
# Returns base salary + calculated pay.
# Functions to use:
#   emp.base_salary   ← Day 5 calculate_base_pay()
#   emp.calculate_pay ← Day 6 @property override
# ════════════════════════════════════════════════════════
@app.route('/api/employees/<emp_id>/pay', methods=['GET'])
def get_employee_pay(emp_id):
    # TODO: return { emp_id, name, type, base_salary, total_pay }
    emp=next((e for e in employees if e.emp_id==emp_id),None)
    if not emp:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        'emp_id':emp.emp_id,
        'name': emp.name,
        'type': type(emp).__name__,
        "base_salary": emp.base_salary,
        "total_pay":   emp.calculate_pay,
    })


# ════════════════════════════════════════════════════════
# TASK 6 — GET /api/employees/<emp_id>/team-info
# Returns Manager team info.
# Function to use: emp.get_team_info()  ← Day 5 Manager method
# Return 400 if not a Manager.
# ════════════════════════════════════════════════════════
@app.route('/api/employees/<emp_id>/team-info', methods=['GET'])
def get_team_info(emp_id):
    # TODO: check isinstance(emp, Manager), call get_team_info()
    emp=next((e for e in employees if e.emp_id==emp_id),None)
    if not emp:
        return jsonify({"error": "Not found"}),404
    if not isinstance(emp,Manager):
        return jsonify({"error": "Not a Manager"}),400
    return jsonify({
        "emp_id":    emp.emp_id,
        "name":      emp.name,
        "team_info": emp.get_team_info(),
        "team_size": emp.team_size,
        "team_bonus": emp.team_size * 5000,
        "total_pay": emp.calculate_pay,
    })


# ════════════════════════════════════════════════════════
# TASK 7 — GET /api/employees/<emp_id>/intern-info
# Returns Intern college + stipend info.
# Function to use: emp.get_intern_info()  ← Day 5 Intern method
# Return 400 if not an Intern.
# ════════════════════════════════════════════════════════
@app.route('/api/employees/<emp_id>/intern-info', methods=['GET'])
def get_intern_info(emp_id):
    # TODO: check isinstance(emp, Intern), call get_intern_info()
    emp=next((e for e in employees if e.emp_id==emp_id),None)
    if not emp:
        return jsonify({"error":"Not found"}),404
    if not isinstance(emp,Intern):
        return jsonify({"error":"Not an Intern"}),400
    return jsonify({
        "emp_id":emp.emp_id,
        "name":emp.name,
        "intern_info": emp.get_intern_info(),
        "college":    emp.college,
        "stipend":    emp.stipend,
    })


# ════════════════════════════════════════════════════════
# TASK 8 — GET /api/departments
# Returns department summary.
# Function to use: department_summary()  ← Day 8 Task 1
# ════════════════════════════════════════════════════════
@app.route('/api/departments', methods=['GET'])
def get_departments():
    # TODO: call department_summary(employees) and return it
    return jsonify(department_summary(employees))


# ════════════════════════════════════════════════════════
# TASK 9 — GET /api/top-earner
# Returns the highest paid employee.
# Functions to use:
#   highest_earner()  ← Day 8 Task 2
#   uses __gt__       ← Day 7 dunder (max() calls it)
# ════════════════════════════════════════════════════════
@app.route('/api/top-earner', methods=['GET'])
def get_top_earner():
    # TODO: call highest_earner(employees), return get_details()
    #       return {} if no employees
    if not employees:
        return jsonify({"error":"no employees added"})
    top=highest_earner(employees)
    return jsonify(top.get_details())


# ════════════════════════════════════════════════════════
# TASK 10 — GET /api/report
# Returns full payroll report.
# Function to use: payroll_report()  ← Day 8 Task 3
# ════════════════════════════════════════════════════════
@app.route('/api/report', methods=['GET'])
def get_report():
    # TODO: call payroll_report(employees) and return it
    #       return {} if no employees
    if not employees:
        return jsonify({})
    return jsonify(payroll_report(employees))


# ════════════════════════════════════════════════════════
# TASK 11 — GET /api/run-payroll
# Returns a pay slip line for every employee.
# Concept: emp.calculate_pay for each  ← Day 6 run_payroll()
# Response: { "payslips": [ {name, emp_id, type, pay, line}, ... ] }
# ════════════════════════════════════════════════════════
@app.route('/api/run-payroll', methods=['GET'])
def run_payroll_endpoint():
    # TODO: loop employees, build payslips list using calculate_pay
    if not employees:
        return jsonify({"payslips": []})
    payslips = []
    for emp in employees:
        payslips.append({
            "name":   emp.name,
            "emp_id": emp.emp_id,
            "type":   type(emp).__name__,
            "pay":    emp.calculate_pay,
            "line":   f"Payslip -> {emp.name} [{emp.emp_id}]: Rs.{emp.calculate_pay:,}",
        })
    return jsonify({"payslips": payslips})


# ════════════════════════════════════════════════════════
# TASK 12 — GET /api/compare?id1=E001&id2=M001
# Compares two employees using ALL Day 7 dunders.
# Dunders to use: __eq__, __lt__, __gt__, __add__, __len__, __bool__
# Get query params: request.args.get('id1'), request.args.get('id2')
# ════════════════════════════════════════════════════════
@app.route('/api/compare', methods=['GET'])
def compare_employees():
    # TODO: get id1, id2 from query params
    #       find both employees
    #       return dict using: ==, <, >, +, len(), bool()
    id1 = request.args.get('id1', '')
    id2 = request.args.get('id2', '')
    emp1 = next((e for e in employees if e.emp_id == id1), None)
    emp2 = next((e for e in employees if e.emp_id == id2), None)
    if not emp1:
        return jsonify({"error": f"No employee '{id1}'"}), 404
    if not emp2:
        return jsonify({"error": f"No employee '{id2}'"}), 404

    return jsonify({
        "employee_1":      {"name": emp1.name, "pay": emp1.calculate_pay},
        "employee_2":      {"name": emp2.name, "pay": emp2.calculate_pay},
        "are_equal":       emp1 == emp2,           # __eq__
        "emp1_earns_less": emp1 <  emp2,           # __lt__
        "emp1_earns_more": emp1 >  emp2,           # __gt__
        "combined_pay":    emp1 +  emp2,           # __add__
        "emp1_len":        len(emp1),              # __len__
        "emp2_len":        len(emp2),              # __len__
        "emp1_is_active":  bool(emp1),             # __bool__
        "emp2_is_active":  bool(emp2),             # __bool__
        "higher_earner":   emp1.name if emp1 > emp2 else emp2.name,
    })


# ════════════════════════════════════════════════════════
# TASK 13 — GET /api/summary
# Returns overall company summary.
# Concept: isinstance() checks  ← Day 5 bonus employees_summary()
# ════════════════════════════════════════════════════════
@app.route('/api/summary', methods=['GET'])
def get_summary():
    # TODO: return { company, total_employees, total_base_payroll,
    #                managers:[], interns:[], employees:[] }
    #       use isinstance(emp, Manager) to filter
    return jsonify({
        "company":             Employee.company,
        "total_employees":     len(employees),
        "total_base_payroll":  sum(emp.base_salary for emp in employees),
        "managers":  [emp.name for emp in employees if isinstance(emp, Manager)],
        "interns":   [emp.name for emp in employees if isinstance(emp, Intern)],
        "employees": [emp.name for emp in employees if type(emp).__name__ == 'Employee'],
    })


if __name__ == '__main__':
    print("PayrollPro API - http://localhost:5000")
    print("Endpoints: /api/employees, /api/departments, /api/top-earner")
    print("           /api/report, /api/run-payroll, /api/compare, /api/summary")
    app.run(debug=True, port=5000)
