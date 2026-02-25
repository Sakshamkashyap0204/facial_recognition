# 🚨 Criminal Record Detection System

Advanced Face Recognition System with MongoDB Integration for Law Enforcement

## 🎯 Features

✅ **MongoDB Database Integration** - Store criminal records with face encodings  
✅ **Auto Dataset Import** - Automatically import criminal mugshots  
✅ **Criminal Registration** - Add new criminals with full details  
✅ **Image Upload Detection** - Check criminals from uploaded images  
✅ **Webcam Real-time Detection** - Live criminal identification  
✅ **Unknown Face Handling** - Gracefully handle unrecognized faces  
✅ **Full Criminal Records** - Display complete criminal information  
✅ **Performance Optimized** - Cached encodings for fast recognition  

## 📋 System Requirements

- Python 3.8+
- MongoDB 4.0+
- Webcam (for real-time detection)
- 4GB RAM minimum
- Windows/Linux/Mac

## 🚀 Quick Start

### 1. Install MongoDB
```bash
# Download from: https://www.mongodb.com/try/download/community
# Start MongoDB service
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Quick Start
```bash
python quickstart.py
```

This will:
- Import criminal dataset
- Seed criminal data
- Start Flask application

### 4. Open Browser
```
http://127.0.0.1:5000
```

## 📁 Project Structure

```
face_recognition/
├── app.py                          # Main Flask application
├── database.py                     # MongoDB connection & operations
├── recognition.py                  # Face recognition logic
├── import_criminal_dataset.py      # Dataset import script
├── seed_criminal_data.py           # Seed criminal information
├── quickstart.py                   # Quick start script
├── templates/
│   ├── index.html                 # Main interface
│   ├── result.html                # Results display
│   └── criminals.html             # Criminal database view
├── Dataset of Mugshots/           # Criminal images dataset
├── uploads/                        # Uploaded images
└── static/results/                # Result images
```

## 💾 Database Schema

```javascript
{
    "_id": ObjectId,
    "name": String,              // Criminal name
    "aliases": [String],         // Known aliases
    "crime": String,             // Type of crime
    "crime_details": String,     // Detailed description
    "years_in_prison": String,   // Sentence duration
    "status": String,            // alive, dead, imprisoned, fugitive
    "nationality": String,       // Nationality
    "location": String,          // Last known location
    "description": String,       // Additional info
    "image_path": String,        // Path to mugshot
    "face_encoding": Array,      // 128-D face encoding
    "created_at": Date          // Registration date
}
```

## 🎮 Usage

### Register New Criminal

1. Navigate to "Register Criminal" section
2. Fill in criminal details:
   - Name (required)
   - Crime type
   - Crime details
   - Years in prison
   - Status
   - Nationality
   - Location
   - Description
3. Upload clear photo
4. Click "Register Criminal"

### Check Criminal Record (Upload)

1. Go to "Check Criminal" section
2. Upload image
3. Click "Check Criminal Record"
4. View results:
   - If match: Full criminal record displayed
   - If no match: "UNKNOWN FACE" message

### Check Criminal Record (Webcam)

1. Scroll to "Webcam Check" section
2. Click "Start Webcam"
3. Allow camera access
4. Click "Capture & Check"
5. View instant results

### View All Criminals

1. Click "View All Criminals" button
2. Browse entire criminal database

## 🔧 Manual Setup

### Step 1: Import Dataset
```bash
python import_criminal_dataset.py
```

Imports all images from:
```
Dataset of Mugshots/Testing_images_real_time_scenario_more_than_one_faces/
```

Extracts:
- Criminal name from filename
- Face encoding from image
- Stores in MongoDB

### Step 2: Seed Criminal Data
```bash
python seed_criminal_data.py
```

Updates records with detailed information for:
- Abu Salem
- Chhota Rajan
- Dawood Ibrahim
- Haji Mastan
- Harshad Mehta
- Lawrence Bishnoi
- Muthappa
- Osama
- Rehman Dakait
- Veerappan
- Vijay Mallya
- Vikas Dubey

### Step 3: Run Application
```bash
python app.py
```

## 🎯 Recognition Flow

```
Image Input (Upload/Webcam)
    ↓
Extract Face Encoding
    ↓
Compare with MongoDB Encodings
    ↓
Match Found?
    ├─ YES → Display Full Criminal Record
    └─ NO  → Display "UNKNOWN FACE"
```

## 📊 Performance

- **Recognition Speed**: < 1 second
- **Accuracy**: 99%+ (using face_recognition library)
- **Concurrent Users**: Supports multiple simultaneous checks
- **Database**: Cached encodings for fast lookup

## 🛡️ Security Features

- Face encoding stored (not raw images)
- MongoDB authentication support
- Secure file uploads
- Input validation
- Error handling

## 🔍 Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
mongod --version

# Start MongoDB
net start MongoDB  # Windows
sudo systemctl start mongod  # Linux
```

### No Face Detected
- Use clear, well-lit images
- Ensure face is visible and not obscured
- Try different angle or lighting

### Import Dataset Failed
- Verify dataset path exists
- Check image file formats (jpg, jpeg, png)
- Ensure proper file permissions

### Webcam Not Working
- Check browser permissions
- Close other apps using camera
- Try different browser

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main page |
| `/register_criminal` | POST | Register new criminal |
| `/check_criminal` | POST | Check criminal from upload |
| `/webcam_check` | POST | Check criminal from webcam |
| `/criminals` | GET | List all criminals |

## 🎨 Technologies Used

- **Backend**: Flask (Python)
- **Database**: MongoDB
- **Face Recognition**: face_recognition (dlib)
- **Computer Vision**: OpenCV
- **Frontend**: HTML5, CSS3, JavaScript
- **Image Processing**: Pillow, NumPy

## 📦 Dependencies

```
Flask>=3.0.0
pymongo>=4.6.0
face_recognition>=1.3.0
opencv-python>=4.8.0
numpy>=1.24.0
Pillow>=10.0.0
werkzeug>=3.0.0
```

## 🚧 Known Limitations

- Requires clear frontal face images
- Performance depends on dataset size
- Lighting conditions affect accuracy
- Single face per criminal in database

## 🔮 Future Enhancements

- [ ] Multi-face per criminal support
- [ ] Advanced search filters
- [ ] Export reports (PDF)
- [ ] User authentication
- [ ] Audit logs
- [ ] REST API
- [ ] Mobile app
- [ ] Real-time video stream processing

## 📄 License

This project is for educational and demonstration purposes only.

## ⚠️ Disclaimer

This system is designed for educational purposes. Ensure compliance with local laws and regulations regarding facial recognition technology and data privacy.

## 👨‍💻 Author

Criminal Record Detection System
Advanced Face Recognition for Law Enforcement

---

**⭐ Star this project if you find it useful!**
