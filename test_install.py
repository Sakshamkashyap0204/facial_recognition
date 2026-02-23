import sys
print("Python path:")
for p in sys.path:
    print(f"  {p}")

print("\nTrying to import face_recognition_models...")
try:
    import face_recognition_models
    print("✓ face_recognition_models imported successfully")
    print(f"  Location: {face_recognition_models.__file__}")
    print(f"  Model location: {face_recognition_models.face_recognition_model_location()}")
except Exception as e:
    print(f"✗ Failed to import: {e}")

print("\nTrying to import dlib...")
try:
    import dlib
    print("✓ dlib imported successfully")
except Exception as e:
    print(f"✗ Failed to import: {e}")

print("\nTrying to import face_recognition...")
try:
    import face_recognition
    print("✓ face_recognition imported successfully")
except Exception as e:
    print(f"✗ Failed to import: {e}")
