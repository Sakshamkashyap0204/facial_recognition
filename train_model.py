"""
Train model on criminal dataset organized in folders
Each folder = criminal name, contains their images
"""
import os
import face_recognition
from database import insert_criminal, criminal_exists, get_all_criminals
import numpy as np

DATASET_PATH = r"C:\Users\stran\OneDrive\Desktop\major\clone of imgprocess\face_recognition\Dataset of Mugshots"

def train_on_dataset():
    """Train on folder-based criminal dataset"""
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset path not found: {DATASET_PATH}")
        return
    
    imported = 0
    skipped = 0
    errors = 0
    
    print("Starting training on criminal dataset...\n")
    
    # Get all criminal folders
    for criminal_folder in os.listdir(DATASET_PATH):
        folder_path = os.path.join(DATASET_PATH, criminal_folder)
        
        if not os.path.isdir(folder_path):
            continue
        
        criminal_name = criminal_folder.strip()
        
        # Check if already exists
        if criminal_exists(criminal_name):
            print(f"Skipped (exists): {criminal_name}")
            skipped += 1
            continue
        
        print(f"Processing: {criminal_name}")
        
        # Collect all encodings from multiple images
        all_encodings = []
        image_count = 0
        
        for image_file in os.listdir(folder_path):
            if not image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.avif')):
                continue
            
            image_path = os.path.join(folder_path, image_file)
            
            try:
                # Load and encode face
                image = face_recognition.load_image_file(image_path)
                encodings = face_recognition.face_encodings(image)
                
                if encodings:
                    all_encodings.append(encodings[0])
                    image_count += 1
                    
            except Exception as e:
                print(f"  Error with {image_file}: {e}")
                errors += 1
        
        if not all_encodings:
            print(f"  No faces found for {criminal_name}")
            errors += 1
            continue
        
        # Average all encodings for better accuracy
        avg_encoding = np.mean(all_encodings, axis=0).tolist()
        
        # Create criminal record
        criminal_data = {
            'name': criminal_name,
            'aliases': [],
            'crime': 'To be updated',
            'crime_details': 'Details to be updated',
            'years_in_prison': 'Unknown',
            'status': 'Active',
            'nationality': 'Unknown',
            'location': 'Unknown',
            'description': f'Trained on {image_count} images',
            'image_path': folder_path,
            'face_encoding': avg_encoding
        }
        
        insert_criminal(criminal_data)
        print(f"  Trained on {image_count} images - SUCCESS\n")
        imported += 1
    
    print(f"\n=== Training Complete ===")
    print(f"Imported: {imported}")
    print(f"Skipped: {skipped}")
    print(f"Errors: {errors}")
    print(f"\nTotal criminals in database: {len(get_all_criminals())}")

if __name__ == "__main__":
    train_on_dataset()
