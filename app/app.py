import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from firebase_admin import credentials, firestore, initialize_app

app = Flask(__name__)
CORS(app)

# Initialize Firestore DB
cred = credentials.Certificate('.\matterionic-firebase-adminsdk-4hp7s-8ed55c1481.json')
default_app = initialize_app(cred)
db = firestore.client()
port = int(os.environ.get('PORT', 8080))

# Invoices
@app.route('/invoice', methods=['GET'])
def getInvoices():
    todo_id = request.args.get('id')
    todo_ref = db.collection(u'users').document(todo_id).collection(u'invoices')
    try:
        all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        return jsonify(all_todos), 200
    except Exception as e:
        return render_template('data_error.html')

# Sales
@app.route('/sale', methods=['GET'])
def getSales():
    todo_id = request.args.get('id')
    todo_ref = db.collection(u'users').document(todo_id).collection(u'sales')
    try:
        all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        return jsonify(all_todos), 200
    except Exception as e:
        return render_template('data_error.html')
    
# Employees
@app.route('/employee/<id>', methods=['GET'])
def getEmployees(id):
    todo_ref = db.collection(u'users').document(id).collection(u'employees')
    try:
        all_todos = [doc.to_dict() for doc in todo_ref.stream()]
        return jsonify(all_todos), 200
    except Exception as e:
        return render_template('data_error.html')

# Statistics
@app.route('/statics', methods=['GET'])
def statics():
    return render_template('statics.html'), 200

# Administration
@app.route('/administration', methods=['GET'])
def administration():
    return render_template('administration.html'), 200

# Page Not Found
def page_not_found(error):
    data={
        'error':error
    }
    return render_template('404.html',data=data), 404

if __name__ == '__main__':
    app.register_error_handler(404,page_not_found)
    app.run(debug=True,threaded=True, host='0.0.0.0', port=port)