from flask import Flask, render_template, url_for, request, redirect
from db_connector import connect_to_database, execute_query 
import os
from function import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/patients", methods=["GET", "POST"])
def patients():
  with connect_to_database() as db_connection: 
    if request.method == "POST":
      if "addfname" in request.form.keys():
        # add the new guy
        query = "INSERT INTO Patients (firstName, lastName, age, gender, phoneNumber, email) VALUES (%s, %s, %b, %s, %s, %s)"
        results = execute_query(db_connection, query, (
          request.form["addfname"], request.form["addlname"], request.form["addage"], 
          request.form["addgender"].upper(), request.form["addpnum"], request.form["addemail"]))
        
    query = "SELECT * FROM Patients"

    if request.method == "POST" and list(request.form.keys())[0] == "search":
      query += " WHERE "
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      query += conditionString(requestForm)
    
    print(query)

    results = execute_query(db_connection, query)
    patients = results.fetchall()
    return render_template('patients.html', patients=patients)
        

@app.route("/providers", methods=['POST', 'GET'])
def providers():
  db_connection = connect_to_database()

  # read and show current data of the table 
  if request.method == 'GET':
    query = 'SELECT * FROM Providers'
    result = execute_query(db_connection, query).fetchall()
    return render_template('providers.html', rows=result)
  
  elif request.method == 'POST':
    # insert new row to the table
    if 'addrow' in request.form:
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      cols = colNames(requestForm)
      vals = valuesString(requestForm)

      query= 'INSERT INTO Providers (' + cols + ') VALUES (' + vals + ')'   
      execute_query(db_connection, query)

      return redirect('/providers')
    
    # search/filter the table
    elif 'search' in request.form:
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

    # delete the row of the table  
    elif 'delete' in request.form:
      provID = request.form['provID']
      query = 'DELETE FROM Providers WHERE '
      query += "provID = '" + provID + "'"
      execute_query(db_connection, query)
      return redirect('/providers')


@app.route("/facilities", methods=['POST', 'GET'])
def facilities():
  db_connection = connect_to_database()

  # read and show current data of the table 
  if request.method == 'GET':
    query = 'SELECT * FROM Facilities'
    result = execute_query(db_connection, query).fetchall()
    return render_template('facilities.html', rows=result)
  
  elif request.method == 'POST':
    # insert new row to the table
    if 'addrow' in request.form:
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      cols = colNames(requestForm)
      vals = valuesString(requestForm)

      query= 'INSERT INTO Facilities (' + cols + ') VALUES (' + vals + ')'   
      execute_query(db_connection, query)

      return redirect('/facilities')
    
    # search/filter the table
    elif 'search' in request.form:
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      query = 'SELECT * FROM Facilities WHERE '
      
      if len(requestForm) == 0:
        return redirect('/facilities')
      else:
        query += conditionString(requestForm)
        result = execute_query(db_connection, query).fetchall()
        return render_template('facilities.html', rows=result)
    
    # update the row of the table
    elif 'edit' in request.form:
      facilityID = request.form['facilityID']
      query = 'UPDATE Facilities SET '
      a = request.form.to_dict()
      del a['facilityID']
      del a['edit']
      query += updateString(a) + " WHERE facilityID = '" + facilityID + "'"
      execute_query(db_connection, query)
      return redirect('/facilities')

    # delete the row of the table  
    elif 'delete' in request.form:
      facilityID = request.form['facilityID']
      query = 'DELETE FROM Facilities WHERE '
      query += "facilityID = '" + facilityID + "'"
      execute_query(db_connection, query)
      return redirect('/facilities')

    # see related providers by the selected facility
    elif 'seeProvider' in request.form:
      facilityID = request.form['facilityID']
      query = "SELECT * FROM ProvidersFacilities WHERE facilityID = '"
      query += facilityID + "'"
      pQuery = 'SELECT provID FROM Providers'
      fQuery = 'SELECT facilityID from Facilities'
      result = execute_query(db_connection, query).fetchall()
      pResult = execute_query(db_connection, pQuery).fetchall()
      fResult = execute_query(db_connection, fQuery).fetchall()
      return render_template('facilitiesProviders.html', rows=result, pid=pResult,
      fid=fResult)
      

@app.route("/patientsProviders")
def patientsProviders():
  return render_template('patientsProviders.html')

@app.route("/facilitiesProviders", methods=['POST', 'GET'])
def facilitiesProviders():
  db_connection = connect_to_database()

  # read and show current data of the table 
  if request.method == 'GET':
    query = 'SELECT * FROM ProvidersFacilities'
    pQuery = 'SELECT provID FROM Providers'
    fQuery = 'SELECT facilityID from Facilities'
    result = execute_query(db_connection, query).fetchall()
    pResult = execute_query(db_connection, pQuery).fetchall()
    fResult = execute_query(db_connection, fQuery).fetchall()
    return render_template('facilitiesProviders.html', rows=result, pid=pResult,
     fid=fResult)
  
  elif request.method == 'POST':
    # insert new row to the table
    if 'addrow' in request.form:
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      cols = colNames(requestForm)
      vals = valuesString(requestForm)

      query= 'INSERT INTO ProvidersFacilities (' + cols + ') VALUES (' + vals + ')'   
      execute_query(db_connection, query)

      return redirect('/facilitiesProviders')
    
    # search/filter the table
    elif 'search' in request.form:
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      query = 'SELECT * FROM ProvidersFacilities WHERE '
      
      if len(requestForm) == 0:
        return redirect('/facilitiesProviders')
      else:
        query += conditionString(requestForm)
        pQuery = 'SELECT provID FROM Providers'
        fQuery = 'SELECT facilityID from Facilities'
        result = execute_query(db_connection, query).fetchall()
        pResult = execute_query(db_connection, pQuery).fetchall()
        fResult = execute_query(db_connection, fQuery).fetchall()
        return render_template('facilitiesProviders.html', rows=result, pid=pResult,
        fid=fResult)
    
    # update the row of the table
    elif 'edit' in request.form:
      provFacID = request.form['provFacID']
      query = 'UPDATE ProvidersFacilities SET '
      a = request.form.to_dict()
      del a['provFacID']
      del a['edit']
      query += updateString(a) + " WHERE provFacID = '" + provFacID + "'"
      execute_query(db_connection, query)
      return redirect('/facilitiesProviders')

    # delete the row of the table  
    elif 'delete' in request.form:
      provFacID = request.form['provFacID']
      query = 'DELETE FROM ProvidersFacilities WHERE '
      query += "provFacID = '" + provFacID + "'"
      execute_query(db_connection, query)
      return redirect('/facilitiesProviders') 

  
if __name__ == "__main__":
  port = int(os.environ.get('PORT', 6276)) 
  app.run(port=port, debug=True)