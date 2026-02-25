"""
Criminal Record Detection System
Flask Application with MongoDB Integration
"""
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
import face_recognition
import cv2
import base64
import numpy as np
from PIL import Image, ImageDraw
from database import insert_criminal, get_all_criminals, criminal_exists, get_criminal_by_name, update_criminal, delete_criminal
from recognition import recognize_face, reload_encodings

app = Flask(__name__)
app.secret_key = 'criminal_detection_secret_key'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static/results', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_criminal', methods=['POST'])
def register_criminal():
    """Register new criminal in database"""
    try:
        # Get form data
        name = request.form.get('name', '').strip()
        crime = request.form.get('crime', '').strip()
        crime_details = request.form.get('crime_details', '').strip()
        years_in_prison = request.form.get('years_in_prison', '').strip()
        status = request.form.get('status', '').strip()
        nationality = request.form.get('nationality', '').strip()
        location = request.form.get('location', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('Name is required')
            return redirect(url_for('index'))
        
        # Check if already exists
        if criminal_exists(name):
            flash(f'Criminal {name} already exists in database')
            return redirect(url_for('index'))
        
        # Get uploaded file
        if 'image' not in request.files:
            flash('Image is required')
            return redirect(url_for('index'))
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(f"{name.replace(' ', '_')}.jpg")
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extract face encoding
            image = face_recognition.load_image_file(filepath)
            encodings = face_recognition.face_encodings(image)
            
            if not encodings:
                flash('No face detected in image')
                os.remove(filepath)
                return redirect(url_for('index'))
            
            encoding = encodings[0].tolist()
            
            # Create criminal record
            criminal_data = {
                'name': name,
                'aliases': [],
                'crime': crime or 'Unknown',
                'crime_details': crime_details or 'N/A',
                'years_in_prison': years_in_prison or 'Unknown',
                'status': status or 'Unknown',
                'nationality': nationality or 'Unknown',
                'location': location or 'Unknown',
                'description': description or 'N/A',
                'image_path': filepath,
                'face_encoding': encoding
            }
            
            insert_criminal(criminal_data)
            reload_encodings()  # Reload cache
            
            flash(f'Criminal {name} registered successfully!')
            return redirect(url_for('index'))
        
        flash('Invalid file type')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/check_criminal', methods=['POST'])
def check_criminal():
    """Check criminal from uploaded image"""
    try:
        if 'image' not in request.files:
            flash('No file uploaded')
            return redirect(url_for('index'))
        
        file = request.files['image']
        
        if file.filename == '':
            flash('No file selected')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Recognize face
            result = recognize_face(image_path=filepath)
            
            # Draw results on image
            image = cv2.imread(filepath)
            
            for face_data in result.get('faces', []):
                top, right, bottom, left = face_data['face_location']
                
                if face_data['found']:
                    color = (0, 255, 0)  # Green for known
                    label = face_data['name']
                else:
                    color = (0, 0, 255)  # Red for unknown
                    label = "UNKNOWN"
                
                cv2.rectangle(image, (left, top), (right, bottom), color, 2)
                cv2.rectangle(image, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
                cv2.putText(image, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            result_filename = 'result_' + filename
            result_path = os.path.join('static/results', result_filename)
            cv2.imwrite(result_path, image)
            
            return render_template('result.html', result=result, result_image=result_filename)
        
        flash('Invalid file type')
        return redirect(url_for('index'))
        
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

@app.route('/webcam_check', methods=['POST'])
def webcam_check():
    """Check criminal from webcam capture"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({'success': False, 'error': 'No image data'}), 400
        
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        image_bytes = base64.b64decode(image_data)
        
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'webcam_capture.jpg')
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Recognize face
        result = recognize_face(image_path=filepath)
        
        # Draw results on image
        image = cv2.imread(filepath)
        
        for face_data in result.get('faces', []):
            top, right, bottom, left = face_data['face_location']
            
            if face_data['found']:
                color = (0, 255, 0)  # Green
                label = face_data['name']
            else:
                color = (0, 0, 255)  # Red
                label = "UNKNOWN"
            
            cv2.rectangle(image, (left, top), (right, bottom), color, 2)
            cv2.rectangle(image, (left, bottom - 35), (right, bottom), color, cv2.FILLED)
            cv2.putText(image, label, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
        
        result_filename = 'result_webcam.jpg'
        result_path = os.path.join('static/results', result_filename)
        cv2.imwrite(result_path, image)
        
        return jsonify({
            'success': True,
            'result': result,
            'result_image': result_filename
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/criminals')
def list_criminals():
    """List all criminals in database"""
    criminals = get_all_criminals()
    return render_template('criminals.html', criminals=criminals)

@app.route('/edit_criminal/<name>')
def edit_criminal(name):
    """Edit criminal details"""
    criminal = get_criminal_by_name(name)
    if not criminal:
        flash('Criminal not found')
        return redirect(url_for('list_criminals'))
    return render_template('edit_criminal.html', criminal=criminal)

@app.route('/update_criminal/<name>', methods=['POST'])
def update_criminal_route(name):
    """Update criminal details"""
    try:
        updates = {
            'crime': request.form.get('crime', '').strip(),
            'crime_details': request.form.get('crime_details', '').strip(),
            'years_in_prison': request.form.get('years_in_prison', '').strip(),
            'status': request.form.get('status', '').strip(),
            'nationality': request.form.get('nationality', '').strip(),
            'location': request.form.get('location', '').strip(),
            'description': request.form.get('description', '').strip()
        }
        
        update_criminal(name, updates)
        reload_encodings()  # Reload cache with updated data
        flash(f'Criminal {name} updated successfully!')
        return redirect(url_for('list_criminals'))
        
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('edit_criminal', name=name))

@app.route('/delete_criminal/<name>', methods=['POST'])
def delete_criminal_route(name):
    """Delete criminal from database"""
    try:
        delete_criminal(name)
        reload_encodings()
        flash(f'Criminal {name} deleted successfully!')
        return redirect(url_for('list_criminals'))
    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('list_criminals'))

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Criminal Record Detection System")
    print("="*60)
    print("\nhttp://127.0.0.1:5000\n")
    
    # Load encodings on startup
    from recognition import load_encodings_from_db
    load_encodings_from_db()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
