
from flask import Flask, render_template, request, redirect, url_for, session
from flask_session import Session
import os
import pickle
import sqlite3





app = Flask(__name__, static_folder='static')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['STATIC_FOLDER']="./static"
Session(app)


@app.route('/')
def index():
    if not session.get("admin"):
        session["admin"]=True
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/fees')
def fees():
    return render_template('fees.html')

@app.route('/times')
def times():
    return render_template('times.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/student')
def student():
    return render_template('student.html')

@app.route('/teacher', endpoint="teacher")
def teacher():
    if session.get("teacher"):
        return render_template('teacher.html')
    else:
        return redirect('/teacher-login')

@app.route('/teacher-login', methods=['GET', 'POST'], endpoint="teacher-login")
def teacher_login():
    error = None
    session["teacher"]=None
    if request.method == 'POST':
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            query="SELECT t_id, password FROM teacher"
            cursor.execute(query)
            teacher_login_dict=dict(cursor.fetchall())
        username, password = int(request.form["username"]), request.form["password"]
        if username not in teacher_login_dict:
            error = 'Invalid Username. Please try again.'
        elif password != teacher_login_dict[username]:
            error = 'Incorrect Password. Please try again.'
        else:
            session["teacher"]=username
            return redirect(url_for('teacher'))
    return render_template('teacher_login.html', error=error)

@app.route('/teacher/details', methods=['GET', 'POST'], endpoint="teacher-details")
def teacher_details():
    if session.get("teacher"):
        return render_template('teacher_details.html')
    else:
        return redirect('/teacher-login')
    
@app.route('/teacher/hw', methods=['GET', 'POST'], endpoint="teacher-hw")
def teacher_hw():
    if session.get("teacher"):
        return render_template('teacher_hw.html')
    else:
        return redirect('/teacher-login')
    
@app.route('/teacher/attendance', methods=['GET', 'POST'], endpoint="teacher-attendance")
def teacher_attendance():
    if session.get("teacher"):
        return render_template('teacher_attendance.html')
    else:
        return redirect('/teacher-login')


@app.route('/admin', endpoint="admin")
def admin():
    if session.get("admin"):
        return render_template('admin.html')
    else:
        return redirect('/admin-login')


@app.route('/announcements')
def admin_announce():
    with sqlite3.connect("school.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM announcements WHERE NOT announcement_title ='' and announcement_id IS NOT NULL")
        output=cursor.fetchall()
    return render_template('announcements.html', output=output)


@app.route('/admin/sql', methods=['GET', 'POST'], endpoint="admin-sql")
def admin_sql():
    output=None
    if session.get("admin"):
        if request.method == 'POST':
            try:
                with sqlite3.connect("school.db") as conn:
                    cursor = conn.cursor()
                    query=request.form["query"]
                    print(query)
                    cursor.execute(query)
                    output=cursor.fetchall()
            except ZeroDivisionError:
                output="Error!"
        return render_template('admin_sql.html', output=output)
    else:
        return redirect('/admin-login')
    
@app.route('/admin/announce', methods=['GET', 'POST'], endpoint="admin-announce")
def admin_announce():
    if session.get("admin"):
        if request.method == 'POST':
            try:
                print("lablablablablablablablab")
                with sqlite3.connect("school.db") as conn:
                    cursor = conn.cursor()
                    announcement_title=request.form["title"]
                    announcement_text=request.form["announcement"]
                    announcer=request.form["announcer"]
                    if announcer=="":
                        announcer="Principal"
                    query = f"INSERT INTO announcements (announcement_id, announcement_title, announcement_text, announcer) VALUES((SELECT MAX(announcement_id) FROM announcements)+1, '{announcement_title}', '{announcement_text}', '{announcer}')"
                    # query = f"INSERT INTO announcements (announcement_id, announcement_title, announcement_text, announcer) VALUES(1, '{announcement_title}', '{announcement_text}', {announcer})"
                
                    print(query)
                    cursor.execute(query)   
                        
            except ZeroDivisionError:
                output="Error!"   
        return render_template('admin_announce.html')
    else:
        return redirect('/admin-login')

@app.route('/admin-login', methods=['GET', 'POST'], endpoint="admin-login")
def admin_login():
    error = None
    session["admin"]=False
    if request.method == 'POST':
        with open("./misc/admin_id.bin", "rb") as f:
            admin_login_dict = pickle.load(f)
        if request.form['username'] != admin_login_dict["id"] or request.form['password'] != admin_login_dict["password"]:
            print(session["admin"])
            error = 'Invalid Credentials. Please try again.'
        else:
            session["admin"]=True
            return redirect(url_for('admin'))
    return render_template('admin_login.html', error=error)

if __name__ == "__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    app.run(debug=True)       

