import os
from click import prompt
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app, auth

app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('.\matterionic-firebase-adminsdk-4hp7s-8ed55c1481.json')
default_app = initialize_app(cred)
db = firestore.client()
port = int(os.environ.get('PORT', 8080))

# Get Users register
@app.route('/users', methods=['GET'])
def getUsers():
    users = dict()
    for user in auth.list_users().iterate_all():
        users[f'{user.email}'] = user.uid
    return jsonify(users), 200

# Get invoices
@app.route('/invoice', methods=['GET'])
def getInvoices():
    todo_id = request.args.get('id')
    todo_ref = db.collection(u'users').document(todo_id).collection(u'invoices')
    try:
        all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        return jsonify(all_todos), 200
    except Exception:
        return render_template('data_error.html')

# Get sales
@app.route('/sale', methods=['GET'])
def getSales():
    todo_id = request.args.get('id')
    todo_ref = db.collection(u'users').document(todo_id).collection(u'sales')
    try:
        all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        return jsonify(all_todos), 200
    except Exception:
        return render_template('data_error.html')
    
# Get employees
@app.route('/employee/<id>', methods=['GET'])
def getEmployees(id):
    todo_ref = db.collection(u'users').document(id).collection(u'employees')
    try:
        all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        return jsonify(all_todos), 200
    except Exception:
        return render_template('data_error.html')
    
# Delete Register User
@app.route('/delete', methods=['GET'])
def delete():
    id = request.args.get('id')
    try:
        auth.delete_user(id)
        return jsonify({"success": True}), 200
    except Exception:
        return jsonify({"success": False}), 400
    

# Page not found
def page_not_found(error):
    data={
        'error':error
    }
    return render_template('404.html',data=data), 404

# Main
if __name__ == '__main__':
    app.register_error_handler(404,page_not_found)
    app.run(debug=True,threaded=True, host='0.0.0.0', port=port)