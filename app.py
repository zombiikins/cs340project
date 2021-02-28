from flask import Flask, render_template, url_for, request, redirect
from db_connector import connect_to_database, execute_query 
import os
from function import *

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/", methods=["GET", "POST"])
def index():
  with connect_to_database() as db_connection: 
    # read and show current data of the table 
    if request.method == "GET":
      query = "SELECT * FROM Claims"
      result = execute_query(db_connection, query).fetchall()
      return render_template("index.html", claims=result)

    elif request.method == "POST":
      # Add new row to table
      if "addrow" in request.form:
        a = request.form.to_dict()
        requestForm = delEmptyColumn(a)
        columns = colNames(requestForm)
        values = valuesString(requestForm)

        query = "INSERT INTO Claims (" + columns + ") VALUES (" + values + ")"
        execute_query(db_connection, query)

        query = "SELECT * FROM Claims"

        # Return results for display on the page
        results = execute_query(db_connection, query)
        claims = results.fetchall()
        return render_template('index.html', claims=claims)

      # Implement search on claims
      elif "search" in request.form:
        query = "SELECT * FROM Claims"
        query += " WHERE "
        a = request.form.to_dict()
        requestForm = delEmptyColumn(a)
        query += conditionString(requestForm)
        # Return results for display on the page
        results = execute_query(db_connection, query)
        claims = results.fetchall()
        return render_template('index.html', claims=claims)

      # update claim information
      elif 'edit' in request.form:
        claimid = request.form['claimid']
        query = "update claims set "
        a = request.form.to_dict()
        del a['claimid']
        del a['edit']
        query += updatestring(a) + " where claimid = '" + claimid + "'"
        execute_query(db_connection, query)
        return redirect('/')

      # delete claim record
      elif "delete" in request.form:
        claimid = request.form["claimid"]
        query = "delete from claims where claimid = '"
        query += claimid + "'"
        execute_query(db_connection, query)
        return redirect('/')   

      else:
       raise RuntimeError("Request not found") 

@app.route("/patients", methods=["GET", "POST"])
def patients():
  with connect_to_database() as db_connection: 
    # read and show current data of the table 
    if request.method == "GET":
      query = "SELECT * FROM Patients"
      result = execute_query(db_connection, query).fetchall()
      return render_template("patients.html", patients=result)
    
    elif request.method == "POST":
      if "addrow" in request.form:
        # add the new row
        a = request.form.to_dict()
        requestForm = delEmptyColumn(a)
        columns = colNames(requestForm)
        values = valuesString(requestForm)

        query = "INSERT INTO Patients (" + columns + ") VALUES (" + values + ")"
        execute_query(db_connection, query)

        query = "SELECT * FROM Patients"
        # Return results for display on the page
        results = execute_query(db_connection, query)
        patients = results.fetchall()
        return render_template('patients.html', patients=patients)

      # Implement search on patients
      elif "search" in request.form:
        query = "SELECT * FROM Patients"
        query += " WHERE "
        a = request.form.to_dict()
        requestForm = delEmptyColumn(a)
        query += conditionString(requestForm)
        # Return results for display on the page
        results = execute_query(db_connection, query)
        patients = results.fetchall()
        return render_template('patients.html', patients=patients)
    
      # See providers related to patient
      elif 'seeProvider' in request.form:
        provID = request.form['patientID']
        query = "SELECT * FROM PatientsProviders WHERE patID = '"
        query += provID + "'"
        patQuery = "SELECT * FROM Patients"
        provQuery = "SELECT * FROM Providers"
        result = execute_query(db_connection, query).fetchall()
        patResult = execute_query(db_connection, patQuery).fetchall()
        provResult = execute_query(db_connection, provQuery).fetchall()
        return render_template('patientsProviders.html', rows = result, patients = patResult, providers = provResult)

      # Update patient information
      elif 'edit' in request.form:
        patientID = request.form['patientID']
        query = "UPDATE Patients SET "
        a = request.form.to_dict()
        del a['patientID']
        del a['edit']
        query += updateString(a) + " WHERE patientID = '" + patientID + "'"
        execute_query(db_connection, query)
        return redirect('/patients')

      # Delete patient record
      elif "delete" in request.form:
        patientID = request.form["patientID"]
        query = "DELETE FROM Patients WHERE patientID = '"
        query += patientID + "'"
        execute_query(db_connection, query)
        return redirect('/patients')   

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
    
    # See patients related to provider
    elif 'seePatient' in request.form:
      provID = request.form['provID']
      query = "SELECT * FROM PatientsProviders WHERE provID = '"
      query += provID + "'"
      patQuery = "SELECT * FROM Patients"
      provQuery = "SELECT * FROM Providers"
      result = execute_query(db_connection, query).fetchall()
      patResult = execute_query(db_connection, patQuery).fetchall()
      provResult = execute_query(db_connection, provQuery).fetchall()
      return render_template('patientsProviders.html', rows = result, patients = patResult, providers = provResult)
    
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
      

@app.route("/patientsProviders", methods=["POST","GET"])
def patientsProviders():
  with connect_to_database() as db_connection: 
    # Read and show current data
    if request.method == "GET":
      query = "SELECT * FROM PatientsProviders"
      patQuery = "SELECT * FROM Patients"
      provQuery = "SELECT * FROM Providers"
      result = execute_query(db_connection, query).fetchall()
      patResult = execute_query(db_connection, patQuery).fetchall()
      provResult = execute_query(db_connection, provQuery).fetchall()
      return render_template('patientsProviders.html', rows = result, patients = patResult, providers = provResult)

    elif request.method == "POST":
      if "addrow" in request.form.keys():
        # add the new row
        a = request.form.to_dict()
        requestForm = delEmptyColumn(a)
        columns = colNames(requestForm)
        values = valuesString(requestForm)

        query = "INSERT INTO PatientsProviders (" + columns + ") VALUES (" + values + ")"
        execute_query(db_connection, query)
        return redirect("/patientsProviders")

      # Implement search on patients
      elif "search" in request.form.keys():
        query = "SELECT * FROM PatientsProviders WHERE "
        a = request.form.to_dict()
        requestForm = delEmptyColumn(a)
        query += conditionString(requestForm)
    
        # Return results for display on the page
        results = execute_query(db_connection, query)
        patProvs = results.fetchall()
        return render_template('patientsProviders.html', rows=patProvs)

      # update patientProvider information
      elif 'edit' in request.form:
        patProvID = request.form['patProvID']
        query = "UPDATE PatientsProviders SET "
        a = request.form.to_dict()
        del a['patProvID']
        del a['edit']
        query += updateString(a) + " where patProvID = '" + patProvID + "'"
        execute_query(db_connection, query)
        return redirect('/patientsProviders')

      # delete patientProvider record
      elif "delete" in request.form:
        patProvID = request.form["patProvID"]
        query = "DELETE FROM PatientsProviders WHERE PatProvID = '"
        query += patProvID + "'"
        execute_query(db_connection, query)
        return redirect('/patientsProviders')

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
      checkQuery = 'SELECT EXISTS(SELECT * FROM ProvidersFacilities WHERE '
      a = request.form.to_dict()
      requestForm = delEmptyColumn(a)
      checkQuery += conditionString(requestForm)+')'
      check = execute_query(db_connection, checkQuery).fetchall()
      check = list(check)[0][0]

      # check if the relationship already existed
      if(not int(check)):
        cols = colNames(requestForm)
        vals = valuesString(requestForm)

        query= 'INSERT INTO ProvidersFacilities (' + cols + ') VALUES (' + vals + ')'   
        execute_query(db_connection, query)

        return redirect('/facilitiesProviders')
      else:
        message = 'The relationship already existed. Please try another.'
        return render_template('facilitiesProviders.html', message=message)

    
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
