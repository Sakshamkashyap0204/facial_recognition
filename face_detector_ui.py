import face_recognition
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog
import numpy as np

def select_and_process_image():
    # Open file picker
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    print("Select an image file...")
    file_path = filedialog.askopenfilename(
        title="Select an image with faces",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp"), ("All files", "*.*")]
    )
    
    if not file_path:
        print("No file selected!")
        return
    
    print(f"\nProcessing: {file_path}")
    
    # Load and process image
    image = face_recognition.load_image_file(file_path)
    
    print("Finding faces...")
    face_locations = face_recognition.face_locations(image)
    print(f"✓ Found {len(face_locations)} face(s)")
    
    if len(face_locations) == 0:
        print("No faces detected in this image.")
        return
    
    # Get face encodings
    face_encodings = face_recognition.face_encodings(image, face_locations)
    print(f"✓ Generated {len(face_encodings)} face encoding(s)")
    
    # Draw boxes on faces
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)
    
    for i, (top, right, bottom, left) in enumerate(face_locations, 1):
        draw.rectangle(((left, top), (right, bottom)), outline="red", width=3)
        print(f"  Face {i}: Top={top}, Left={left}, Bottom={bottom}, Right={right}")
    
    # Show result
    pil_image.show()
    print("\n✓ Done! Image displayed with face boxes.")

if __name__ == "__main__":
    print("=" * 50)
    print("Face Recognition - Image Selector")
    print("=" * 50)
    select_and_process_image()
