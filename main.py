
from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__, static_folder='static')
# UPLOAD_FOLDER = 'uploads'
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')


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