from click import password_option
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import mysql.connector
import pandas as pd


app = Flask(__name__)

class User:
    def __init__(self, id, user, password):
        self.id = id
        self.user = user
        self.password = password

users = []
users.append(User(id = 1, user = 'cs3311_admin', password = 'password'))

app.config['SECRET_KEY'] = 'SecretKey'


#app.config['SQLALCHEMTY_DATABASE_URI'] = 'mysql://root:""@localhost/cs3311'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#db = SQLAlchemy(app)

#class Data(db.model):
#    id = db.Column(db.Integer)
#DB_HOST = '127.0.0.1'
#DB_NAME = 'CS3311'
#DB_USER = 'cs3311_admin'
#DB_PASS = 'password'
config = {
    'user': 'root',
    'password': '1100279464',
    'host': '127.0.0.1',
    'database': 'CS3311'
}

insert_query = {
    'projects': ("INSERT INTO projects "
            "(Project, State, Budget_Period_Start, Budget_Period_End, Reporting_Period) "
            "VALUES (%(Project)s, %(State)s, %(Budget_Period_Start)s, %(Budget_Period_End)s, %(Reporting_Period)s);"),
    'activities': ("INSERT INTO activities "
            "(ProjectID, Activity, Description, Outcome, Output, Timeline, Statistics, Status, Successes, Challenges, CDC_Support_Needed, Parent_File) "
            "VALUES (%(ProjectID)s, %(Activity)s, %(Description)s, %(Outcome)s, %(Output)s, %(Timeline)s, %(Statistics)s, %(Status)s, %(Successes)s, %(Challenges)s, %(CDC_Support_Needed)s, %(Parent_File)s);")
}

cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        user = [name for name in users if name.id == session['user_id']][0]
        g.user = user
    else:
        g.user = None
        

@app.route('/')
def entry():
    return redirect(url_for('login'))

@app.route('/login', methods = ["GET", "POST"])
def login():
    session.pop('user_id', None)
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']
        user = [name for name in users if name.user == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('Index'))
        return redirect(url_for('login'))

    return(render_template('login.html'))

@app.route("/activities")
def Index():
    if not g.user:
        return redirect(url_for('login'))
    s = "Select * FROM cs3311.activities"
    cursor.execute(s)
    list_activities = cursor.fetchall()
    return render_template("Index.html", activities = list_activities)
    

@app.route('/insert', methods = ['POST'])
def insert():
    if request.method =='POST':
        activity = request.form['Activity']
        description = request.form['Description']
        outcome = request.form['Outcome']
        output = request.form['Output']
        timeline = request.form['Timeline']
        statistics = request.form['Statistics']
        status = request.form['Status']
        successes = request.form['Successes']
        challenges = request.form['Challenges']
        CDC_Support_Needed = request.form['CDC_Support_Needed']
        Parent_File = request.form['Parent_File']

        table_activities = 'activities'

        data_activities = [{
            'ActivityID': 3,
            'ProjectID': 3,
            'Activity': activity,
            'Description': description,
            'Outcome': outcome,
            'Output' : output,
            'Timeline': timeline,
            'Statistics': statistics,
            'Status': status,
            'Successes': successes,
            'Challenges': challenges,
            'CDC_Support_Needed': CDC_Support_Needed,
            'Parent_File' : Parent_File
        }]

        if table_activities in insert_query:
            cursor.executemany(insert_query[table_activities], data_activities)
            cnx.commit()
        
        flash("Activity Inserted Successfully")

        return redirect(url_for('Index'))

@app.route('/projects')
def change():
    if not g.user:
        return redirect(url_for('login'))
    s = "Select * FROM cs3311.projects"
    cursor.execute(s)
    list_projects = cursor.fetchall()
    return render_template("index_project.html", projects = list_projects)


@app.route('/update', methods = ['GET', 'POST'])
def update():
    if request.method == 'POST':
        id = request.form.get('ActivityID')
        query = "Select * FROM cs3311.activities WHERE ActivityID = %s"
        #value = (int(id),)
        #value = (int(id))
        #cursor.execute(s)
        cursor.execute(query, (id, ))
        rel_activities = cursor.fetchall()
        print(rel_activities)
        activityID = rel_activities[0][0]
        print(activityID)

        activity = request.form['Activity']
        description = request.form['Description']
        outcome = request.form['Outcome']
        output = request.form['Output']
        timeline = request.form['Timeline']
        statistics = request.form['Statistics']
        status = request.form['Status']
        successes = request.form['Successes']
        challenges = request.form['Challenges']
        CDC_Support_Needed = request.form['CDC_Support_Needed']
        Parent_File = request.form['Parent_File']

        sql = """
        UPDATE activities
        SET Activity = %s,
            Description = %s,
            Outcome = %s,
            Output = %s,
            Timeline = %s,
            Statistics = %s,
            Status = %s,
            Successes = %s,
            Challenges = %s,
            CDC_Support_Needed = %s,
            Parent_File = %s
        WHERE ActivityID = %s
        """        
        cursor.execute(sql, (str(activity), str(description), str(outcome), str(output), str(timeline), str(statistics), 
                        str(status), str(successes), str(challenges), str(CDC_Support_Needed), str(Parent_File), activityID))
        cnx.commit()

        flash("Activity Updated Successfully")

        return redirect(url_for('Index'))

@app.route('/delete/<ActivityID>/', methods = ['GET', 'POST'])
def delete(ActivityID):
    sql = "DELETE FROM activities WHERE ActivityID = %s"
    cursor.execute(sql, (ActivityID,))
    cnx.commit()
    flash("Activity Deleted")
    return redirect(url_for('Index'))

@app.route('/upload')
def upload():
    if not g.user:
        return redirect(url_for('login'))
    return render_template("upload.html")

@app.route('/upload', methods=['POST']) 
def upload_file():
    if request.method == "POST":
        if 'files[]' not in request.files:
            flash('Files Not Available')
            return redirect(url_for('upload'))
        files = request.files.getlist('files[]')
        for file in files:
            #x1 = pd.ExcelFile(file, engine = "openpyxl")
            #print(x1)
            x2 = pd.read_excel(file, engine='openpyxl')
            print(x2)
            x2 = x2.to_html()
            print(x2)

            #data_xls = pd.read_excel(file, engine='openpyxl')
            #print(data_xls)
            #document = secure_filename(file.filename)
        flash("File(s) Uploaded Succesfully")

    ##f = request.files['file']
    #f = request.files['file']
    #f.save(secure_filename(f.filename))
    
    return redirect(url_for('upload'))


if(__name__) == "__main__":
    app.run(host='localhost', port=1000, debug=True)
