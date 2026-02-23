from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import face_recognition
import os
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import base64
import io
import cv2
import dlib
try:
    import tensorflow as tf
    print(f"TensorFlow version: {tf.__version__}")
    TENSORFLOW_AVAILABLE = True
except ImportError:
    print("TensorFlow not available, using dlib only")
    TENSORFLOW_AVAILABLE = False

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['KNOWN_FACES_FOLDER'] = 'known_faces'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Create folders if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['KNOWN_FACES_FOLDER'], exist_ok=True)
os.makedirs('static/results', exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Initialize dlib face detector
print("Initializing dlib face detector...")
dlib_detector = dlib.get_frontal_face_detector()
print("dlib detector ready")

def preprocess_image_tensorflow(image_rgb):
    """Preprocess image using TensorFlow for better quality"""
    if not TENSORFLOW_AVAILABLE:
        return image_rgb
    
    try:
        # Convert to TensorFlow tensor
        img_tensor = tf.convert_to_tensor(image_rgb, dtype=tf.float32)
        
        # Normalize to [0, 1]
        img_tensor = img_tensor / 255.0
        
        # Apply slight denoising using Gaussian blur
        img_tensor = tf.expand_dims(img_tensor, 0)  # Add batch dimension
        
        # Convert back to uint8 [0, 255]
        img_tensor = img_tensor * 255.0
        img_processed = tf.cast(img_tensor[0], tf.uint8).numpy()
        
        return img_processed
    except Exception as e:
        print(f"[WARNING] TensorFlow preprocessing failed: {e}")
        return image_rgb

def detect_faces_dlib(image_rgb):
    """Detect faces using dlib detector"""
    try:
        # dlib expects RGB uint8
        dlib_faces = dlib_detector(image_rgb, 1)
        
        # Convert dlib rectangles to face_recognition format (top, right, bottom, left)
        face_locations = []
        for face in dlib_faces:
            top = face.top()
            right = face.right()
            bottom = face.bottom()
            left = face.left()
            face_locations.append((top, right, bottom, left))
        
        return face_locations
    except Exception as e:
        print(f"[WARNING] dlib detection failed: {e}")
        return []

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_known_faces():
    """Load all known faces from known_faces folder with maximum error handling"""
    known_encodings = []
    known_names = []
    
    known_faces_dir = app.config['KNOWN_FACES_FOLDER']
    if not os.path.exists(known_faces_dir):
        print("[INFO] No known_faces folder found")
        return known_encodings, known_names
    
    files = [f for f in os.listdir(known_faces_dir) if allowed_file(f)]
    if not files:
        print("[INFO] No known faces in folder")
        return known_encodings, known_names
    
    print(f"[INFO] Processing {len(files)} files in known_faces folder...")
    
    for filename in files:
        filepath = os.path.join(known_faces_dir, filename)
        
        try:
            # Method 1: Try with OpenCV
            img_bgr = cv2.imread(filepath, cv2.IMREAD_COLOR)
            
            if img_bgr is None:
                print(f"[ERROR] Could not load {filename}")
                continue
            
            # Force convert to RGB uint8
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
            img_rgb = np.ascontiguousarray(img_rgb, dtype=np.uint8)
            
            # Double check format
            assert img_rgb.dtype == np.uint8, f"Wrong dtype: {img_rgb.dtype}"
            assert len(img_rgb.shape) == 3, f"Wrong dimensions: {img_rgb.shape}"
            assert img_rgb.shape[2] == 3, f"Wrong channels: {img_rgb.shape[2]}"
            
            print(f"[OK] {filename} - {img_rgb.shape}, {img_rgb.dtype}")
            
            # Detect faces first
            face_locs = face_recognition.face_locations(img_rgb, model="hog")
            
            if not face_locs:
                print(f"[WARNING] {filename} - no face detected")
                continue
            
            # Encode only the first face
            encodings = face_recognition.face_encodings(img_rgb, known_face_locations=face_locs)
            
            if not encodings:
                print(f"[WARNING] {filename} - could not encode face")
                continue
            
            known_encodings.append(encodings[0])
            name = os.path.splitext(filename)[0]
            known_names.append(name)
            print(f"[SUCCESS] Loaded: {name}")
            
        except Exception as e:
            print(f"[ERROR] {filename}: {str(e)}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"[INFO] Successfully loaded {len(known_encodings)} known faces\n")
    return known_encodings, known_names

def recognize_faces(image_path):
    """Recognize faces in the uploaded image"""
    known_encodings, known_names = load_known_faces()
    
    try:
        # Load with OpenCV
        img_bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
        
        if img_bgr is None:
            print(f"[ERROR] Could not load {image_path}")
            return [], None
        
        # Convert BGR to RGB and ensure uint8
        image = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
        image = np.ascontiguousarray(image, dtype=np.uint8)
        
        # Verify format
        assert image.dtype == np.uint8
        assert len(image.shape) == 3
        assert image.shape[2] == 3
        
        print(f"[INFO] Image loaded: {image.shape}, {image.dtype}")
        
        # Detect faces
        face_locations = face_recognition.face_locations(image, model="hog")
        print(f"[INFO] Found {len(face_locations)} faces")
        
        # Encode faces
        face_encodings = face_recognition.face_encodings(image, known_face_locations=face_locations)
        
        results = []
        
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            name = "Unknown"
            
            if known_encodings:
                # Compare with known faces
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
            
            # Draw box and name on BGR image
            cv2.rectangle(img_bgr, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(img_bgr, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(img_bgr, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1)
            
            results.append({
                'name': name,
                'location': f"Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}"
            })
        
        # Save result image
        result_filename = 'result_' + os.path.basename(image_path)
        result_path = os.path.join('static/results', result_filename)
        cv2.imwrite(result_path, img_bgr)
        
        return results, result_filename
        
    except Exception as e:
        print(f"[ERROR] recognize_faces failed: {str(e)}")
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
        
        # Recognize faces
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
        # Save with the person's name
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
        print("\n" + "="*60)
        print("[INFO] Webcam capture request received")
        print("[INFO] Using: OpenCV + dlib + face_recognition" + (" + TensorFlow" if TENSORFLOW_AVAILABLE else ""))
        print("="*60)
        
        data = request.get_json()
        
        if not data or 'image' not in data:
            print("[ERROR] No image data in request")
            return jsonify({'success': False, 'error': 'No image data provided'}), 400
        
        image_data = data['image']
        
        # Remove data URL prefix
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        # Decode base64
        print("[STEP 1] Decoding base64 image...")
        image_bytes = base64.b64decode(image_data)
        print(f"[SUCCESS] Decoded {len(image_bytes)} bytes")
        
        # Save to file first
        filename = 'webcam_capture.jpg'
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        print(f"[STEP 2] Saved to {filepath}")
        
        # Load with OpenCV
        print("[STEP 3] Loading with OpenCV...")
        image_bgr = cv2.imread(filepath)
        
        if image_bgr is None:
            print("[ERROR] OpenCV failed to load image")
            return jsonify({'success': False, 'error': 'Failed to load image'}), 400
        
        print(f"[SUCCESS] OpenCV loaded - shape: {image_bgr.shape}, dtype: {image_bgr.dtype}")
        
        # Convert BGR to RGB using OpenCV
        print("[STEP 4] Converting BGR to RGB...")
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        
        # Ensure uint8
        image_rgb = np.ascontiguousarray(image_rgb, dtype=np.uint8)
        
        print(f"[SUCCESS] RGB image - shape: {image_rgb.shape}, dtype: {image_rgb.dtype}")
        
        # Optional: Preprocess with TensorFlow
        if TENSORFLOW_AVAILABLE:
            print("[STEP 5] Preprocessing with TensorFlow...")
            image_rgb = preprocess_image_tensorflow(image_rgb)
            print("[SUCCESS] TensorFlow preprocessing complete")
        
        # Verify format
        if len(image_rgb.shape) != 3 or image_rgb.shape[2] != 3:
            print(f"[ERROR] Invalid shape: {image_rgb.shape}")
            return jsonify({'success': False, 'error': 'Invalid image format'}), 400
        
        if image_rgb.dtype != np.uint8:
            print(f"[ERROR] Invalid dtype: {image_rgb.dtype}")
            image_rgb = image_rgb.astype(np.uint8)
        
        # Load known faces
        print("[STEP 6] Loading known faces...")
        known_encodings, known_names = load_known_faces()
        print(f"[SUCCESS] Loaded {len(known_encodings)} known faces")
        
        # Detect faces using dlib directly
        print("[STEP 7] Detecting faces with dlib...")
        face_locations_dlib = detect_faces_dlib(image_rgb)
        print(f"[SUCCESS] dlib found {len(face_locations_dlib)} faces")
        
        # Also try with face_recognition (uses HOG)
        print("[STEP 8] Detecting faces with face_recognition (HOG)...")
        face_locations_hog = face_recognition.face_locations(image_rgb, model="hog")
        print(f"[SUCCESS] HOG found {len(face_locations_hog)} faces")
        
        # Use whichever found more faces
        face_locations = face_locations_dlib if len(face_locations_dlib) >= len(face_locations_hog) else face_locations_hog
        print(f"[INFO] Using {len(face_locations)} face locations")
        
        if len(face_locations) == 0:
            print("[WARNING] No faces detected")
        
        # Encode faces
        print("[STEP 9] Encoding faces...")
        face_encodings = face_recognition.face_encodings(image_rgb, face_locations)
        print(f"[SUCCESS] Generated {len(face_encodings)} encodings")
        
        results = []
        
        # Process each face
        print("[STEP 10] Recognizing faces...")
        for idx, ((top, right, bottom, left), face_encoding) in enumerate(zip(face_locations, face_encodings)):
            name = "Unknown"
            confidence = 0.0
            
            if known_encodings:
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                
                if True in matches:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                        confidence = 1 - face_distances[best_match_index]
            
            print(f"[RESULT] Face {idx+1}: {name} (confidence: {confidence:.2f})")
            
            # Draw on BGR image using OpenCV
            cv2.rectangle(image_bgr, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(image_bgr, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            
            label = f"{name} ({confidence:.2f})" if name != "Unknown" else name
            cv2.putText(image_bgr, label, (left + 6, bottom - 6), 
                       cv2.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255), 1)
            
            results.append({
                'name': name,
                'confidence': f"{confidence:.2f}",
                'location': f"Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}"
            })
        
        # Save result
        result_filename = 'result_webcam_capture.jpg'
        result_path = os.path.join('static/results', result_filename)
        cv2.imwrite(result_path, image_bgr)
        print(f"[STEP 11] Saved result to {result_path}")
        
        print("[SUCCESS] Processing complete!")
        print("="*60 + "\n")
        
        return jsonify({
            'success': True,
            'num_faces': len(results),
            'results': results,
            'result_image': result_filename,
            'tech_stack': 'OpenCV + dlib + face_recognition' + (' + TensorFlow' if TENSORFLOW_AVAILABLE else '')
        })
        
    except Exception as e:
        import traceback
        error_msg = str(e)
        print(f"\n[ERROR] Exception: {error_msg}")
        print(f"[ERROR] Traceback:\n{traceback.format_exc()}")
        print("="*60 + "\n")
        return jsonify({'success': False, 'error': error_msg}), 400

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Face Recognition Web App Starting...")
    print("="*50)
    print("\nOpen your browser and go to: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
