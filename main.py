
from flask import Flask, render_template, request, redirect, url_for
import os
from wtforms import Form, BooleanField, StringField, PasswordField, validators
import db_main

class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])

app = Flask(__name__, static_folder='static')
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
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

@app.route('/teacher')
def teacher():
    return render_template('teacher.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form_data = {"id": request.form.get('id'), "password": request.form.get('password')}
    if db_main.verify_admin(form_data):
        print("aa")
        redirect(url_for("/"))
    return render_template('admin_login.html')


# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if 'file' not in request.files:
#         return render_template('image-upload.html')
#     file = request.files['file']
#     if file.filename == '':
#         return render_template('image-upload.html')
#     if file:
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'trueocr.png'))
#         return redirect('/image-to-video')
    
# @app.route('/image-upload')
# def image_upload():
#     return render_template('image-upload.html')

# @app.route('/image-to-video')
# def image_to_video():
#     return render_template('image-to-video.html')

if __name__ == "__main__":
    app.run(debug=True)       

