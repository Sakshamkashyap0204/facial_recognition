from PIL import Image
import face_recognition

# Load the jpg file into a numpy array
import os
import numpy as np
script_dir = os.path.dirname(os.path.abspath(__file__))
image = face_recognition.load_image_file(os.path.join(script_dir, "biden.jpg"))

# Ensure image is in correct format (8-bit RGB)
if len(image.shape) == 2:
    image = np.stack([image] * 3, axis=-1)
elif image.shape[2] == 4:
    image = image[:, :, :3]

# Convert to uint8 if needed
if image.dtype != np.uint8:
    if image.max() <= 1.0:
        image = (image * 255).astype(np.uint8)
    else:
        image = image.astype(np.uint8)

# Find all the faces in the image using the default HOG-based model.
# This method is fairly accurate, but not as accurate as the CNN model and not GPU accelerated.
# See also: find_faces_in_picture_cnn.py
face_locations = face_recognition.face_locations(image)

print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

    # Print the location of each face in this image
    top, right, bottom, left = face_location
    print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

    # You can access the actual face itself like this:
    face_image = image[top:bottom, left:right]
    pil_image = Image.fromarray(face_image)
    pil_image.show()
