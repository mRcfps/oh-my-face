import os

import face_recognition
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config['BASE_DIR'] = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(app.config['BASE_DIR'], 'uploads')


@app.route('/')
def index():
    return render_template('index.html')


def allowed_file(filename):
    """Check if a file is a picture by its name."""
    return filename.endswith(('.png', 'jpg', 'jpeg'))


@app.route('/judge', methods=['POST'])
def judge():
    face_file = request.files['face']
    photo_file = request.files['photo']

    if allowed_file(face_file.filename) and allowed_file(photo_file.filename):
        # Both images are valid, so save them to upload folder
        face_filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            face_file.filename)
        photo_filepath = os.path.join(
            app.config['UPLOAD_FOLDER'],
            photo_file.filename)
        face_file.save(face_filepath)
        photo_file.save(photo_filepath)

        # Load image files into numpy arrays
        face_image = face_recognition.load_image_file(face_filepath)
        photo_image = face_recognition.load_image_file(photo_filepath)

        face_encoding = face_recognition.face_encodings(face_image)[0]
        photo_encoding = face_recognition.face_encodings(photo_image)[0]
        results = face_recognition.compare_faces([face_encoding], photo_encoding)

        return render_template('result.html', result=results[0])
    else:
        return 400, "Image file required."
