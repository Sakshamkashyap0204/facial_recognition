"""
Emergency fix: Clear known_faces and test system
"""
import os
import shutil

def clear_known_faces():
    known_faces_dir = 'known_faces'
    
    # Backup existing files
    backup_dir = 'known_faces_backup'
    if os.path.exists(known_faces_dir):
        if os.path.exists(backup_dir):
            shutil.rmtree(backup_dir)
        shutil.copytree(known_faces_dir, backup_dir)
        print(f"Backed up known_faces to {backup_dir}")
        
        # Clear known_faces
        for file in os.listdir(known_faces_dir):
            filepath = os.path.join(known_faces_dir, file)
            if os.path.isfile(filepath):
                os.remove(filepath)
        print("Cleared known_faces folder")
    
    print("\n" + "="*60)
    print("INSTRUCTIONS:")
    print("="*60)
    print("1. Start Flask: python app.py")
    print("2. Go to http://127.0.0.1:5000")
    print("3. Use 'Step 1: Add Known Faces' to upload NEW images")
    print("4. Then test webcam or upload")
    print("\nYour old images are backed up in known_faces_backup/")
    print("="*60)

if __name__ == "__main__":
    response = input("This will clear known_faces folder. Continue? (yes/no): ")
    if response.lower() == 'yes':
        clear_known_faces()
    else:
        print("Cancelled")
