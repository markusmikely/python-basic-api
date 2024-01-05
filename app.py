import json
from flask import Flask, jsonify, request
app = Flask(__name__)

employees = [
    { 'id': 1, 'name': 'Ashley' }, 
    { 'id': 2, 'name': 'Kate' }, 
    { 'id': 3, 'name': 'Joe' }
]

nextEmployeeId = 4

@app.route('/employees', methods=["GET"])
def get_employees():
    return jsonify(employees)

@app.route('/employees/<int:id>', methods=["GET"])
def get_employee_by_id(id):
    employee = get_employee(id)
    if employee is None:
        return jsonify({'error': 'Employee does not exist'}), 404
    
    return jsonify(employees)

def get_employee(id):
    employee = next((e for e in employees if e['id'] == id), None)
    print('Employee:', employee)
    print('Employees:', employees)
    return employee

def employee_is_valid(employee):
    # print(employee.keys())
    if not isinstance(employee, dict):
        print('not dict')
        return False
    
    if employee is None:
        print('not found')
        return False

    for key in employee.keys():
        if key != "name":
            print('name not exist')
            return False
    return True
    
@app.route('/employees', methods=['POST'])
def create_employee():
    global nextEmployeeId
    
    try:
        # Check if the request has JSON data
        employee = request.get_json()

        
        if not employee:
            print("DEBUG: No JSON data provided in the request.")
            return jsonify({'error': 'No JSON data provided in the request.'}), 400
    
        print(f"DEBUG: Request JSON data received: {employee}")

        # Validate the structure of the employee data
        if not employee_is_valid(employee):
            print("DEBUG: Invalid employee properties.")
            return jsonify({'error': 'Invalid employee properties.'}), 400
    
        employee['id'] = nextEmployeeId
        nextEmployeeId += 1
        employees.append(employee)

        return '', 201, {'location': f'/employees/{employee["id"]}'}
    except json.JSONDecodeError:
        print("DEBUG: Invalid JSON format in the request data.")
        return jsonify({'error': 'Invalid JSON format in the request data.'}), 400

@app.route('/employees/<int:id>', methods=['PUT'])
def update_employee(id: int):
    employee = get_employee(id)
    
    if employee is None:
        return jsonify({ 'error', 'Employ does not exist'}), 404
    
    updated_employee:dict = request.get_json()
    print(employee_is_valid(updated_employee))
    if not employee_is_valid(updated_employee):
        return jsonify({ 'error': 'Invalid employee properties'}), 400
    
    employee.update(updated_employee)

    return jsonify(employee)

@app.route('/employees/<int:id>', methods=["DELETE"])
def delete_employee(id: int):
    global employees
    employee = get_employee(id)
    if employee is None:
        return jsonify({ 'error', 'Employee does not exist'}), 404
    
    employees = [e for e in employees if e['id'] != id]
    return jsonify(employee), 200

if __name__ == '__main__':
    app.run(port=5000)