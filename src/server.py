from flask import Flask, request, jsonify
import os
import cv2

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def detect_faces(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    return faces

def predict():
    image = cv2.imread(r'./uploads/uploaded_image.jpg')
    faces = detect_faces(image)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    cv2.imshow('Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files and request.data:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'uploaded_image.jpg')
        with open(file_path, 'wb') as f:
            f.write(request.data)
        return "File uploaded successfully", 200

    if 'file' in request.files:
        file = request.files['file']
        if file.filename == '':
            return "No selected file", 400

        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            return "File uploaded successfully", 200

@app.route('/uploads', methods=['GET'])
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
