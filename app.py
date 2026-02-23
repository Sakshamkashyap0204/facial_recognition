from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from deepface import DeepFace
import os
from werkzeug.utils import secure_filename
import cv2
import base64
import numpy as np

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['KNOWN_FACES_FOLDER'] = 'known_faces'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['KNOWN_FACES_FOLDER'], exist_ok=True)
os.makedirs('static/results', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def recognize_faces(image_path):
    """Recognize faces using DeepFace"""
    try:
        img = cv2.imread(image_path)
        
        # Find faces
        faces = DeepFace.extract_faces(image_path, detector_backend='opencv', enforce_detection=False)
        
        results = []
        known_faces_dir = app.config['KNOWN_FACES_FOLDER']
        
        for face_data in faces:
            name = "Unknown"
            facial_area = face_data['facial_area']
            
            # Try to match with known faces
            if os.path.exists(known_faces_dir) and os.listdir(known_faces_dir):
                try:
                    result = DeepFace.find(image_path, db_path=known_faces_dir, enforce_detection=False, silent=True)
                    if result and len(result) > 0 and len(result[0]) > 0:
                        matched_path = result[0].iloc[0]['identity']
                        name = os.path.splitext(os.path.basename(matched_path))[0]
                except:
                    pass
            
            # Draw rectangle
            x, y, w, h = facial_area['x'], facial_area['y'], facial_area['w'], facial_area['h']
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
            cv2.rectangle(img, (x, y+h-35), (x+w, y+h), (0, 0, 255), -1)
            cv2.putText(img, name, (x+6, y+h-6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            results.append({'name': name, 'location': f"X: {x}, Y: {y}, W: {w}, H: {h}"})
        
        result_filename = 'result_' + os.path.basename(image_path)
        result_path = os.path.join('static/results', result_filename)
        cv2.imwrite(result_path, img)
        
        return results, result_filename
    except Exception as e:
        print(f"Error: {e}")
        return [], None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        results, result_image = recognize_faces(filepath)
        
        if result_image is None:
            flash('Error processing image')
            return redirect(url_for('index'))
        
        return render_template('result.html', results=results, result_image=result_image, num_faces=len(results))
    
    flash('Invalid file type')
    return redirect(url_for('index'))

@app.route('/add_known_face', methods=['POST'])
def add_known_face():
    if 'file' not in request.files or 'name' not in request.form:
        flash('Please provide both image and name')
        return redirect(url_for('index'))
    
    file = request.files['file']
    name = request.form['name'].strip()
    
    if file.filename == '' or name == '':
        flash('Please provide both image and name')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(name + '.jpg')
        filepath = os.path.join(app.config['KNOWN_FACES_FOLDER'], filename)
        file.save(filepath)
        
        flash(f'Added {name}!')
        return redirect(url_for('index'))
    
    flash('Invalid file')
    return redirect(url_for('index'))

@app.route('/webcam_capture', methods=['POST'])
def webcam_capture():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image'}), 400
        
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'webcam_capture.jpg')
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        results, result_image = recognize_faces(filepath)
        
        if result_image is None:
            return jsonify({'success': False, 'error': 'Failed'}), 400
        
        return jsonify({'success': True, 'num_faces': len(results), 'results': results, 'result_image': result_image})
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Face Recognition with DeepFace")
    print("="*50)
    print("\nhttp://127.0.0.1:5000\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
