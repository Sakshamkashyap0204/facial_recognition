# Quick Start Guide - Webcam Face Recognition

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Verify installation:**
```bash
python -c "import face_recognition; print('Face recognition installed successfully!')"
```

## Running the Application

1. **Start the Flask server:**
```bash
python app.py
```

2. **Open your browser:**
Navigate to: `http://127.0.0.1:5000`

3. **You should see:**
```
==================================================
Face Recognition Web App Starting...
==================================================

Open your browser and go to: http://127.0.0.1:5000

Press CTRL+C to stop the server
```

## Using the Webcam Feature

### Quick Demo (3 Steps):

**Step 1: Add a Known Face**
- Enter your name (e.g., "John")
- Upload a clear photo of yourself
- Click "Add to Known Faces"

**Step 2: Test Webcam**
- Scroll to "Step 3: Use Webcam"
- Click "Start Webcam"
- Allow camera access when prompted

**Step 3: Capture & Recognize**
- Click "Capture & Recognize"
- See your name appear on the detected face!

## Folder Structure
```
face_recognition/
├── app.py                  # Main Flask application
├── templates/
│   ├── index.html         # Main page with webcam feature
│   └── result.html        # Results page
├── known_faces/           # Store known face images here
├── uploads/               # Temporary uploaded images
└── static/
    └── results/           # Processed images with annotations
```

## Tips for Best Results

✅ **Good Lighting** - Face the light source
✅ **Clear Face** - Remove glasses/masks if possible
✅ **Direct Angle** - Face the camera straight on
✅ **Close Distance** - Be 2-3 feet from camera
✅ **High Quality** - Use good resolution images for known faces

## Common Issues

**Issue: "No faces detected"**
- Solution: Improve lighting, move closer, face camera directly

**Issue: "Unknown Person" detected**
- Solution: Add the person's photo to known_faces first

**Issue: Webcam not starting**
- Solution: Check browser permissions, close other apps using camera

**Issue: Wrong person recognized**
- Solution: Add more photos of the correct person, adjust tolerance

## Advanced Configuration

Edit `app.py` to customize:

```python
# Change tolerance (lower = stricter matching)
matches = face_recognition.compare_faces(
    known_encodings, 
    face_encoding, 
    tolerance=0.6  # Change this (0.0-1.0)
)

# Change image quality
image.save(filepath, quality=95)  # 1-100

# Change max upload size
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

## Next Steps

- Add multiple people to known_faces
- Test with group photos
- Try different lighting conditions
- Experiment with tolerance values
- Deploy to production server

## Support

For issues or questions:
1. Check WEBCAM_FEATURE.md for detailed documentation
2. Review the main README.md
3. Check face_recognition library docs: https://face-recognition.readthedocs.io

Enjoy your face recognition system! 🎉
