
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

@app.route('/student', endpoint="student")
def student():
    if session.get("student"):
        return render_template('student.html')
    else:
        return redirect('/student-login')

@app.route('/student-login', methods=['GET', 'POST'], endpoint="student-login")
def student_login():
    error = None
    session["student"]=None
    if request.method == 'POST':
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            query="SELECT s_id, password FROM student"
            cursor.execute(query)
            student_login_dict=dict(cursor.fetchall())
        username, password = int(request.form["username"]), request.form["password"]
        if username not in student_login_dict:
            error = 'Invalid Username. Please try again.'
        elif password != student_login_dict[username]:
            error = 'Incorrect Password. Please try again.'
        else:
            session["student"]=username
            return redirect(url_for('student'))
    return render_template('student_login.html', error=error)

@app.route('/student/details', methods=['GET', 'POST'], endpoint="student-details")
def student_details():
    if session.get("student"):
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            query=f"SELECT s_id, name, class, dob, email FROM student WHERE s_id= {session.get("student")}"
            cursor.execute(query)
            student_details_query = cursor.fetchall()
        return render_template('student_details.html', student_details=student_details_query)
    else:
        return redirect('/student-login')
    
@app.route('/student/hw', methods=['GET', 'POST'], endpoint="student-hw")
def student_hw():
    if session.get("student"):
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            query=f"SELECT l.hw_title, l.hw_text, l.post_date, l.due_date, l.subject, l.class, r.t_id, name FROM homework l INNER JOIN teacher r ON l.t_id= r.t_id WHERE l.class=(SELECT class FROM student WHERE s_id = {session.get("student")})"    
            cursor.execute(query)
            student_hw = cursor.fetchall()
        return render_template('student_hw.html', student_hw=student_hw)
    else:
        return redirect('/student-login')
    
@app.route('/student/marks', methods=['GET', 'POST'], endpoint="student-marks")
def student_marks():
    if session.get("student"):
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            query=f"SELECT exam_type, subject, marks, total FROM marks WHERE s_id = {session.get("student")}"    
            cursor.execute(query)
            student_marks = cursor.fetchall()
            print(student_marks)
            student_marks_dict=dict()
            for i in student_marks:
                if i[0] not in student_marks_dict:
                    student_marks_dict[i[0]]=[list(i[1:])]
                else:
                    student_marks_dict[i[0]]=student_marks_dict[i[0]]+[list(i[1:])]
            print(student_marks_dict)
        return render_template('student_marks.html', student_marks_dict=student_marks_dict)
    else:
        return redirect('/student-login')
    

@app.route('/student/attendance', methods=['GET', 'POST'], endpoint="student-attendance")
def student_attendance():
    if session.get("student"):
        return render_template('student_attendance.html')
    else:
        return redirect('/student-login')


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
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            query=f"SELECT t_id, name, subject, class, email FROM teacher WHERE t_id= {session.get("teacher")}"
            cursor.execute(query)
            teacher_details_query = cursor.fetchall()
        return render_template('teacher_details.html', teacher_details=teacher_details_query)
    else:
        return redirect('/teacher-login')
    
@app.route('/teacher/hw', methods=['GET', 'POST'], endpoint="teacher-hw")
def teacher_hw():
    if session.get("teacher"):
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            # print(request.form.get("title"))
            hw_title, hw_text, due_date, hw_subject, hw_class = request.form.get("title"), request.form.get("text"), request.form.get("date"), request.form.get("subject"), request.form.get("class")
            if hw_title and hw_class:
                query=f"INSERT INTO homework (hw_title, hw_text, due_date, subject, class, t_id) VALUES ('{hw_title}', '{hw_text}', '{due_date}', '{hw_subject}', '{hw_class}', {session.get("teacher")})"
                cursor.execute(query)
                conn.commit()
            query=f"SELECT hw_title, hw_text, post_date, due_date, subject, class FROM homework WHERE t_id={session.get("teacher")}"    
            cursor.execute(query)
            teacher_hw = cursor.fetchall()
        return render_template('teacher_hw.html', teacher_hw=teacher_hw)
    
    else:
        return redirect('/teacher-login')

@app.route('/teacher/marks', methods=['GET', 'POST'], endpoint="teacher-marks")
def teacher_marks():
    exam_options=["Unit Test", "Mid Term", "Pre-Boards", "Finals"]
    if session.get("teacher"):
        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            # print(request.form.get("title"))
            student_id, subject, marks, total, exam_type = request.form.get("s_id"), request.form.get("subject"), request.form.get("marks"), request.form.get("total"), request.form.get("type")
            query="SELECT s_id, subject, exam_type FROM marks"
            cursor.execute(query)
            if student_id and subject and marks and total and exam_type:
                student_id, marks, total =int(student_id), int(marks), int(total)
                x=cursor.fetchone()
                if x==(student_id, subject, exam_type):
                    query=f"UPDATE marks SET marks={marks}, total={total} WHERE s_id={student_id} AND subject='{subject}' AND exam_type='{exam_type}' "
                else:
                    query=f"INSERT INTO marks (s_id, subject, marks, total, exam_type) VALUES ({student_id}, '{subject}', {marks}, {total}, '{exam_type}')"
                cursor.execute(query)
        return render_template('teacher_marks.html', exam_options=exam_options)
    else:
        return redirect('/teacher-login')

 
@app.route('/teacher/attendance', methods=['GET', 'POST'], endpoint="teacher-attendance")
def teacher_attendance():
    date_received=homeroom=False
    teacher_class=None
    student_list=[]
    if session.get("teacher"):

        with sqlite3.connect("school.db") as conn:
            cursor=conn.cursor()
            cursor.execute(f"SELECT homeroom, class FROM teacher where t_id={session.get("teacher")}")
            data=cursor.fetchone()
            print(data)
            homeroom=bool(data[0])
            teacher_class=data[1]
        if homeroom:
            cursor=conn.cursor()
            date_received=request.form.get("date")
            if date_received:
                with sqlite3.connect("school.db") as conn:
                    query=f"SELECT s_id, name FROM student WHERE class=(SELECT class FROM teacher WHERE t_id={session.get("teacher")})"
                    cursor=conn.cursor()
                    cursor.execute(query)
                    student_list=cursor.fetchall()
                print(request.form.getlist('present'))
                print(request.form.getlist('id'))
                # print(amounts, item_ids)
                print("La")
                # for item_id, idx in enumerate(item_ids):
                #     print(False)
                #     amount = amounts[idx]
                #     print(item_id, amount)
                    # do something with item_id and amount
                    # cursor.execute(query)
                    # attendance=query

        return render_template('teacher_attendance.html', student_list=student_list, teacher_class=teacher_class, homeroom=homeroom, date_received=date_received)
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
            except:
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
                        
            except:
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

