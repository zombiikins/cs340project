from flask import Flask, render_template, url_for
import db_connector as db

app = Flask(__name__)
db_connection = db.connect_to_database()

@app.route("/")
def index():
  return render_template('index.html')

@app.route("/patients")
def patients():
  return render_template('patients.html')

@app.route("/providers")
def providers():
  return render_template('providers.html')

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