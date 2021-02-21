from flask import Flask, render_template, url_for, request, redirect
from db_connector import connect_to_database, execute_query 
import os
from function import *

app = Flask(__name__)

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/patients")
def patients():
  return render_template('patients.html')

@app.route("/providers", methods=['POST', 'GET', 'PUT'])
def providers():
  db_connection = connect_to_database()

  # read and show current data of the table 
  if request.method == 'GET':
    query = 'SELECT * FROM Providers'
    result = execute_query(db_connection, query).fetchall()
    return render_template('providers.html', rows=result)
  
  elif request.method == 'POST':
    # insert new row to the table
    if list(request.form.keys())[0] == 'addrow':
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      cols = colNames(requestForm)
      vals = valuesString(requestForm)

      query= 'INSERT INTO Providers (' + cols + ') VALUES (' + vals + ')'   
      execute_query(db_connection, query)

      return redirect('/providers')
    
    # search/filter the table
    elif list(request.form.keys())[0] == 'search':
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      query = 'SELECT * FROM Providers WHERE '
      
      if len(requestForm) == 0:
        return redirect('/providers')
      else:
        query += conditionString(requestForm)
        result = execute_query(db_connection, query).fetchall()
        return render_template('providers.html', rows=result)
    
    # update the row of the table
    elif 'edit' in request.form:
      provID = request.form['provID']
      query = 'UPDATE Providers SET '
      a = request.form.to_dict()
      del a['provID']
      del a['edit']
      query += updateString(a) + " WHERE provID = '" + provID + "'"
      execute_query(db_connection, query)
      return redirect('/providers')
      
    elif 'delete' in request.form:
      provID = request.form['provID']
      query = 'DELETE FROM Providers WHERE '
      query += "provID = '" + provID + "'"
      execute_query(db_connection, query)
      return redirect('/providers')


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