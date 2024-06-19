from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
