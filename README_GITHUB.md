# Facial Recognition System with Webcam

A real-time face recognition web application built with Flask, DeepFace, TensorFlow, and OpenCV.

## Features

✅ **Real-time Webcam Capture** - Capture photos directly from your browser  
✅ **Face Detection** - Automatically detect faces in images  
✅ **Face Recognition** - Identify known faces from your database  
✅ **Web Interface** - Easy-to-use web UI  
✅ **Multiple Face Support** - Detect and recognize multiple people  
✅ **Unknown Detection** - Identifies faces not in database  

## Tech Stack

- **Backend**: Flask (Python)
- **Face Recognition**: DeepFace
- **Deep Learning**: TensorFlow, Keras
- **Computer Vision**: OpenCV
- **Frontend**: HTML5, JavaScript, CSS3

## Installation

### Prerequisites
- Python 3.8+
- Webcam (for real-time capture)

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Sakshamkashyap0204/facial_recognition.git
cd facial_recognition
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python app.py
```

4. **Open browser**
```
http://127.0.0.1:5000
```

## Usage

### 1. Add Known Faces
- Enter person's name
- Upload a clear photo
- Click "Add to Known Faces"

### 2. Upload Image for Recognition
- Click "Choose Image"
- Select an image file
- Click "Recognize Faces"

### 3. Use Webcam
- Click "Start Webcam"
- Allow camera access
- Click "Capture & Recognize"
- View results instantly!

## Project Structure

```
facial_recognition/
├── app.py                  # Main Flask application
├── templates/
│   ├── index.html         # Main page
│   └── result.html        # Results page
├── static/
│   └── results/           # Processed images
├── known_faces/           # Database of known faces
├── uploads/               # Temporary uploads
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Requirements

```
deepface
tensorflow
tf-keras
opencv-python
Flask
numpy
Pillow
```

## How It Works

1. **Image Capture**: Browser captures webcam frame or user uploads image
2. **Face Detection**: DeepFace detects all faces in the image
3. **Face Recognition**: Compares detected faces with known faces database
4. **Results Display**: Shows annotated image with names and bounding boxes

## Screenshots

### Main Interface
Upload images or use webcam to recognize faces

### Results
View detected faces with names and confidence scores

## Technologies

- **DeepFace**: State-of-the-art face recognition
- **TensorFlow**: Deep learning framework
- **OpenCV**: Computer vision library
- **Flask**: Web framework
- **HTML5 Canvas**: Webcam capture

## Features in Detail

### Face Detection
- Uses DeepFace with multiple backend options
- Detects multiple faces simultaneously
- Works with various angles and lighting

### Face Recognition
- Compares faces using deep learning
- High accuracy recognition
- Handles unknown faces gracefully

### Web Interface
- Responsive design
- Real-time webcam access
- Instant results display

## Troubleshooting

**Webcam not working?**
- Check browser permissions
- Ensure no other app is using the camera
- Try refreshing the page

**No faces detected?**
- Ensure good lighting
- Face the camera directly
- Use clear, high-quality images

**Recognition not accurate?**
- Add more photos of the person
- Use clear, well-lit photos
- Ensure face is clearly visible

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Author

**Saksham Kashyap**
- GitHub: [@Sakshamkashyap0204](https://github.com/Sakshamkashyap0204)

## Acknowledgments

- DeepFace library for face recognition
- TensorFlow team for deep learning framework
- OpenCV community for computer vision tools
- Flask team for web framework

---

⭐ Star this repo if you find it helpful!
