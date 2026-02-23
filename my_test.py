import face_recognition
from PIL import Image
import numpy as np

# Load your image (change this path to your image)
# Put your image in the examples folder and change the filename below
image_path = "examples/your_image.jpg"  # ← Change 'your_image.jpg' to your actual filename
image = face_recognition.load_image_file(image_path)

# Find faces
face_locations = face_recognition.face_locations(image)
print(f"Found {len(face_locations)} face(s)")

# Get face encodings (for recognition)
face_encodings = face_recognition.face_encodings(image, face_locations)
print(f"Generated {len(face_encodings)} face encoding(s)")

# Draw boxes on faces
pil_image = Image.fromarray(image)
from PIL import ImageDraw
draw = ImageDraw.Draw(pil_image)

for (top, right, bottom, left) in face_locations:
    draw.rectangle(((left, top), (right, bottom)), outline="red", width=3)

pil_image.show()
print("Done!")
