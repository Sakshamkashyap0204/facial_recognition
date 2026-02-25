"""
Face Recognition Module with MongoDB Integration
"""
import face_recognition
import numpy as np
from database import get_all_encodings
import cv2

# Cache for encodings
_cached_encodings = None
_cached_names = None
_cached_records = None

def load_encodings_from_db():
    """Load all encodings from MongoDB and cache them"""
    global _cached_encodings, _cached_names, _cached_records
    
    encodings, names, records = get_all_encodings()
    
    # Convert to numpy arrays
    _cached_encodings = [np.array(enc) for enc in encodings]
    _cached_names = names
    _cached_records = records
    
    print(f"Loaded {len(_cached_encodings)} criminal encodings from database")
    return _cached_encodings, _cached_names, _cached_records

def get_cached_encodings():
    """Get cached encodings or load if not cached"""
    global _cached_encodings, _cached_names, _cached_records
    
    if _cached_encodings is None:
        load_encodings_from_db()
    
    return _cached_encodings, _cached_names, _cached_records

def recognize_face(image_path=None, image_array=None):
    """
    Recognize face from image path or array
    Returns criminal record if match found, else None
    """
    try:
        # Load image
        if image_path:
            image = face_recognition.load_image_file(image_path)
        elif image_array is not None:
            image = image_array
        else:
            return None
        
        # Get face locations and encodings
        face_locations = face_recognition.face_locations(image)
        
        if not face_locations:
            return {
                'found': False,
                'message': 'No face detected in image',
                'faces': []
            }
        
        face_encodings = face_recognition.face_encodings(image, face_locations)
        
        # Get cached encodings
        known_encodings, known_names, known_records = get_cached_encodings()
        
        if not known_encodings:
            return {
                'found': False,
                'message': 'No criminals in database',
                'faces': []
            }
        
        results = []
        
        for face_encoding, face_location in zip(face_encodings, face_locations):
            # Compare with known faces
            matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(known_encodings, face_encoding)
            
            if True in matches:
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    # Match found
                    criminal_record = known_records[best_match_index]
                    
                    results.append({
                        'found': True,
                        'name': criminal_record['name'],
                        'crime': criminal_record.get('crime', 'Unknown'),
                        'crime_details': criminal_record.get('crime_details', 'N/A'),
                        'status': criminal_record.get('status', 'Unknown'),
                        'location': criminal_record.get('location', 'Unknown'),
                        'nationality': criminal_record.get('nationality', 'Unknown'),
                        'description': criminal_record.get('description', 'N/A'),
                        'years_in_prison': criminal_record.get('years_in_prison', 'Unknown'),
                        'image_path': criminal_record.get('image_path', ''),
                        'confidence': float(1 - face_distances[best_match_index]),
                        'face_location': face_location
                    })
                else:
                    # Unknown face
                    results.append({
                        'found': False,
                        'name': 'Unknown Face',
                        'status': 'No record found in database',
                        'face_location': face_location
                    })
            else:
                # Unknown face
                results.append({
                    'found': False,
                    'name': 'Unknown Face',
                    'status': 'No record found in database',
                    'face_location': face_location
                })
        
        return {
            'found': any(r['found'] for r in results),
            'faces': results,
            'total_faces': len(results)
        }
        
    except Exception as e:
        print(f"Recognition error: {e}")
        return {
            'found': False,
            'message': f'Error: {str(e)}',
            'faces': []
        }

def reload_encodings():
    """Force reload encodings and records from database"""
    global _cached_encodings, _cached_names, _cached_records
    _cached_encodings = None
    _cached_names = None
    _cached_records = None
    return load_encodings_from_db()
