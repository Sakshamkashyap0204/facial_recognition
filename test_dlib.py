import numpy as np
import dlib

# Test dlib directly
print("Testing dlib...")
print(f"dlib version: {dlib.__version__}")

# Create a simple test image
test_image = np.zeros((100, 100, 3), dtype=np.uint8)
test_image[:] = [255, 0, 0]  # Red image

print(f"Test image shape: {test_image.shape}")
print(f"Test image dtype: {test_image.dtype}")
print(f"Test image is C-contiguous: {test_image.flags['C_CONTIGUOUS']}")

# Try to use dlib face detector
detector = dlib.get_frontal_face_detector()
print("Face detector created successfully")

try:
    faces = detector(test_image, 1)
    print(f"✓ dlib works! Found {len(faces)} faces (expected 0 in blank image)")
except Exception as e:
    print(f"✗ dlib error: {e}")
    print("\nYour dlib is broken. Need to reinstall.")
