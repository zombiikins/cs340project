from flask import Flask, render_template, url_for, request, redirect
from db_connector import connect_to_database, execute_query 
import os

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/patients")
def patients():
  return render_template('patients.html')

@app.route("/providers", methods=['POST', 'GET'])
def providers():
  db_connection = connect_to_database()
  if request.method == 'GET':
    query = 'SELECT * FROM Providers'
    result = execute_query(db_connection, query).fetchall()
    return render_template('providers.html', rows=result)
  
  elif request.method == 'POST':
    print(list(request.form.keys())[0])

@app.route("/facilities")
def facilities():
  return render_template('facilities.html')

@app.route("/patientsProviders")
def patientsProviders():
  return render_template('patientsProviders.html')

@app.route("/facilitiesProviders")
def facilitiesProviders():
  return render_template('facilitiesProviders.html')

  
if __name__ == "__main__":
  port = int(os.environ.get('PORT', 6276)) 
  app.run(port=port, debug=True)