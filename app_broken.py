from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import face_recognition
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
import io

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

def load_image_safe(filepath):
    """Load image safely using PIL - guaranteed to work with face_recognition"""
    pil_img = Image.open(filepath)
    if pil_img.mode != 'RGB':
        pil_img = pil_img.convert('RGB')
    img_array = np.array(pil_img, dtype=np.uint8)
    img_array = np.ascontiguousarray(img_array)
    return img_array

def load_known_faces():
    """Load all known faces"""
    known_encodings = []
    known_names = []
    
    known_faces_dir = app.config['KNOWN_FACES_FOLDER']
    if not os.path.exists(known_faces_dir):
        return known_encodings, known_names
    
    for filename in os.listdir(known_faces_dir):
        if not allowed_file(filename):
            continue
            
        filepath = os.path.join(known_faces_dir, filename)
        
        try:
            image = load_image_safe(filepath)
            encodings = face_recognition.face_encodings(image)
            
            if encodings:
                known_encodings.append(encodings[0])
                name = os.path.splitext(filename)[0]
                known_names.append(name)
                print(f"[OK] Loaded: {name}")
        except Exception as e:
            print(f"[ERROR] {filename}: {e}")
            continue
    
    return known_encodings, known_names

def recognize_faces(image_path):
    """Recognize faces in uploaded image"""
    try:
        known_encodings, known_names = load_known_faces()
        
        image = load_image_safe(image_path)
        
        face_locations = face_recognition.face_locations(image)
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        pil_image = Image.fromarray(image)
        draw = ImageDraw.Draw(pil_image)
        
        results = []
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            
            if known_encodings:
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
            
            draw.rectangle(((left, top), (right, bottom)), outline="red", width=3)
            draw.rectangle(((left, bottom - 35), (right, bottom)), fill="red", outline="red")
            draw.text((left + 6, bottom - 30), name, fill="white")
            
            results.append({
                'name': name,
                'location': f"Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}"
            })
        
        result_filename = 'result_' + os.path.basename(image_path)
        result_path = os.path.join('static/results', result_filename)
        pil_image.save(result_path)
        
        return results, result_filename
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return [], None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        results, result_image = recognize_faces(filepath)
        
        if result_image is None:
            flash('Error processing image. Please try again.')
            return redirect(url_for('index'))
        
        return render_template('result.html', 
                             results=results, 
                             result_image=result_image,
                             num_faces=len(results))
    
    flash('Invalid file type. Please upload JPG, JPEG, or PNG')
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
        filename = secure_filename(name + '.' + file.filename.rsplit('.', 1)[1].lower())
        filepath = os.path.join(app.config['KNOWN_FACES_FOLDER'], filename)
        file.save(filepath)
        
        flash(f'Successfully added {name} to known faces!')
        return redirect(url_for('index'))
    
    flash('Invalid file type')
    return redirect(url_for('index'))

@app.route('/webcam_capture', methods=['POST'])
def webcam_capture():
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data'}), 400
        
        image_data = data['image']
        
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        
        filename = 'webcam_capture.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Use the same recognize_faces function
        results, result_image = recognize_faces(filepath)
        
        if result_image is None:
            return jsonify({'success': False, 'error': 'Processing failed'}), 400
        
        return jsonify({
            'success': True,
            'num_faces': len(results),
            'results': results,
            'result_image': result_image
        })
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 400

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Face Recognition Web App Starting...")
    print("="*50)
    print("\nOpen your browser and go to: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
