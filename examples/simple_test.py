#!/usr/bin/env python
# -*- coding: utf-8 -*-
import face_recognition
import os
from PIL import Image
import numpy as np

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Load the jpg file
image_path = os.path.join(script_dir, "obama_small.jpg")
print(f"Loading image: {image_path}")

# Load image using PIL first to ensure correct format
pil_image = Image.open(image_path)
pil_image = pil_image.convert('RGB')
image = np.array(pil_image, dtype=np.uint8)

print(f"Image shape: {image.shape}")
print(f"Image dtype: {image.dtype}")

# Find all the faces in the image
print("Finding faces...")
face_locations = face_recognition.face_locations(image)

print(f"I found {len(face_locations)} face(s) in this photograph.")

for face_location in face_locations:
    top, right, bottom, left = face_location
    print(f"A face is located at pixel location Top: {top}, Left: {left}, Bottom: {bottom}, Right: {right}")
