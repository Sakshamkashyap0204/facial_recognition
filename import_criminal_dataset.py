"""
Import Criminal Dataset from Mugshots folder
Automatically extract names and face encodings
"""
import os
import face_recognition
from database import insert_criminal, criminal_exists
import cv2
import numpy as np

# No dataset configured - waiting for new criminal dataset
DATASET_PATH = None  # Update this when you have the dataset

def extract_name_from_filename(filename):
    """Convert filename to proper name format"""
    name = os.path.splitext(filename)[0]
    name = name.replace('_', ' ').replace('-', ' ')
    name = ' '.join(word.capitalize() for word in name.split())
    return name

def import_dataset():
    """Import all criminal images from dataset"""
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset path not found: {DATASET_PATH}")
        return
    
    imported = 0
    skipped = 0
    errors = 0
    
    print("Starting dataset import...")
    
    for filename in os.listdir(DATASET_PATH):
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue
        
        filepath = os.path.join(DATASET_PATH, filename)
        criminal_name = extract_name_from_filename(filename)
        
        # Check if already exists
        if criminal_exists(criminal_name):
            print(f"Skipped (exists): {criminal_name}")
            skipped += 1
            continue
        
        try:
            # Load image
            image = face_recognition.load_image_file(filepath)
            
            # Get face encoding
            encodings = face_recognition.face_encodings(image)
            
            if not encodings:
                print(f"No face found: {filename}")
                errors += 1
                continue
            
            # Use first face
            encoding = encodings[0].tolist()
            
            # Create criminal record
            criminal_data = {
                'name': criminal_name,
                'aliases': [],
                'crime': 'Unknown',
                'crime_details': 'Details to be updated',
                'years_in_prison': 'Unknown',
                'status': 'Unknown',
                'nationality': 'Unknown',
                'location': 'Unknown',
                'description': 'Imported from dataset',
                'image_path': filepath,
                'face_encoding': encoding
            }
            
            insert_criminal(criminal_data)
            print(f"Imported: {criminal_name}")
            imported += 1
            
        except Exception as e:
            print(f"Error processing {filename}: {e}")
            errors += 1
    
    print(f"\n=== Import Complete ===")
    print(f"Imported: {imported}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")

if __name__ == "__main__":
    import_dataset()
