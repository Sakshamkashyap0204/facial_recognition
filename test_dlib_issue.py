from PIL import Image
import numpy as np
import face_recognition

# Test with a simple image
print("Creating test image...")
img = Image.new('RGB', (100, 100), color='red')
img.save('test_img.jpg')

print("Loading with PIL...")
pil_img = Image.open('test_img.jpg')
print(f"PIL mode: {pil_img.mode}")

print("Converting to numpy...")
arr = np.array(pil_img, dtype=np.uint8)
print(f"Array shape: {arr.shape}, dtype: {arr.dtype}")
print(f"Contiguous: {arr.flags['C_CONTIGUOUS']}")

print("Testing face_recognition...")
try:
    locations = face_recognition.face_locations(arr)
    print(f"SUCCESS! Found {len(locations)} faces")
except Exception as e:
    print(f"ERROR: {e}")
    
    # Try with explicit copy
    print("\nTrying with explicit copy...")
    arr2 = np.ascontiguousarray(arr.copy(), dtype=np.uint8)
    print(f"Array2 shape: {arr2.shape}, dtype: {arr2.dtype}")
    print(f"Contiguous: {arr2.flags['C_CONTIGUOUS']}")
    
    try:
        locations = face_recognition.face_locations(arr2)
        print(f"SUCCESS with copy! Found {len(locations)} faces")
    except Exception as e2:
        print(f"STILL ERROR: {e2}")
