# Webcam Face Recognition Feature

## Overview
This feature allows you to capture images directly from your webcam and recognize faces in real-time.

## How to Use

### Step 1: Start the Application
```bash
python app.py
```
Open your browser and navigate to: `http://127.0.0.1:5000`

### Step 2: Add Known Faces (Optional)
1. Enter the person's name in the text field
2. Click "Choose Photo" and select a clear image of the person
3. Click "Add to Known Faces"
4. Repeat for all people you want to recognize

### Step 3: Use Webcam Recognition
1. Scroll to "Step 3: Use Webcam" section
2. Click "Start Webcam" button
3. Allow browser to access your webcam when prompted
4. Position yourself in front of the camera
5. Click "Capture & Recognize" to take a photo
6. The system will automatically:
   - Detect all faces in the image
   - Compare them with known faces
   - Display results with bounding boxes and names
7. Click "Retake" if you want to capture another photo

## Features

✅ **Real-time Webcam Access** - Direct camera access from browser
✅ **Instant Recognition** - Immediate face detection and recognition
✅ **Visual Feedback** - Bounding boxes and labels on detected faces
✅ **Multiple Faces** - Detects and recognizes multiple people simultaneously
✅ **Unknown Detection** - Identifies faces not in the known database
✅ **Retake Option** - Easy to capture multiple photos

## Technical Details

### Technologies Used
- **Frontend**: HTML5, JavaScript, Canvas API, MediaDevices API
- **Backend**: Flask (Python)
- **Face Recognition**: face_recognition library (dlib)
- **Image Processing**: PIL, NumPy

### How It Works
1. Browser captures video stream from webcam using `getUserMedia()`
2. JavaScript captures frame from video and converts to base64
3. Image sent to Flask backend via AJAX POST request
4. Backend processes image using face_recognition library
5. Faces detected and compared with known encodings
6. Results returned as JSON with names and locations
7. Frontend displays annotated image with results

### API Endpoint
**POST** `/webcam_capture`
- **Input**: JSON with base64 encoded image
- **Output**: JSON with detection results
```json
{
  "success": true,
  "num_faces": 2,
  "results": [
    {
      "name": "John Doe",
      "location": "Top: 100, Left: 150, Bottom: 300, Right: 350"
    }
  ],
  "result_image": "result_webcam_capture.jpg"
}
```

## Browser Compatibility
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support (requires HTTPS in production)
- Opera: ✅ Full support

## Security Notes
- Webcam access requires user permission
- Images are processed server-side
- Captured images saved in `uploads/` folder
- Results saved in `static/results/` folder

## Troubleshooting

**Webcam not working?**
- Ensure browser has permission to access camera
- Check if another application is using the webcam
- Try refreshing the page

**No faces detected?**
- Ensure good lighting
- Face the camera directly
- Move closer to the camera
- Ensure face is not obscured

**Recognition not accurate?**
- Add more photos of the person to known_faces
- Use clear, well-lit photos
- Adjust tolerance in code (default: 0.6)
