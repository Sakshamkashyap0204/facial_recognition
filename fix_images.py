"""  
Script to validate and fix all images in known_faces folder
Converts all images to proper RGB JPEG format
"""
import cv2
import os
import numpy as np
import sys
import io

# Fix encoding for Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def fix_known_faces():
    known_faces_dir = 'known_faces'
    
    if not os.path.exists(known_faces_dir):
        print("known_faces folder not found!")
        return
    
    files = os.listdir(known_faces_dir)
    print(f"Found {len(files)} files in known_faces folder\n")
    
    for filename in files:
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            print(f"[SKIP] {filename} - not an image")
            continue
        
        filepath = os.path.join(known_faces_dir, filename)
        print(f"\n[PROCESSING] {filename}")
        
        try:
            # Load image
            img = cv2.imread(filepath)
            
            if img is None:
                print(f"  ❌ Could not load - file may be corrupted")
                continue
            
            print(f"  ✓ Loaded - shape: {img.shape}, dtype: {img.dtype}")
            
            # Check if it's already BGR (3 channels)
            if len(img.shape) != 3 or img.shape[2] != 3:
                print(f"  ❌ Invalid format - not a 3-channel image")
                continue
            
            # Convert to RGB
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Ensure uint8
            img_rgb = np.ascontiguousarray(img_rgb, dtype=np.uint8)
            
            # Convert back to BGR for saving
            img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
            
            # Save as JPEG with proper format
            name_without_ext = os.path.splitext(filename)[0]
            new_filename = f"{name_without_ext}.jpg"
            new_filepath = os.path.join(known_faces_dir, new_filename)
            
            # Save with high quality
            cv2.imwrite(new_filepath, img_bgr, [cv2.IMWRITE_JPEG_QUALITY, 95])
            
            print(f"  ✓ Saved as: {new_filename}")
            
            # If original was PNG, delete it
            if filename.lower().endswith('.png') and filename != new_filename:
                os.remove(filepath)
                print(f"  ✓ Removed original PNG: {filename}")
            
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            continue
    
    print("\n" + "="*60)
    print("Image validation and conversion complete!")
    print("="*60)
    print("\nAll images are now in proper RGB JPEG format.")
    print("Restart your Flask app and try again.")

if __name__ == "__main__":
    fix_known_faces()
