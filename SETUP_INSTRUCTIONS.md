# Criminal Record Detection System - Setup Instructions

## Prerequisites
- Python 3.8+
- MongoDB installed and running
- Webcam (for real-time detection)

## Installation Steps

### 1. Install MongoDB
Download and install MongoDB from: https://www.mongodb.com/try/download/community

Start MongoDB service:
```bash
# Windows
net start MongoDB

# Linux/Mac
sudo systemctl start mongod
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Import Criminal Dataset
```bash
python import_criminal_dataset.py
```

This will:
- Read all images from Dataset folder
- Extract criminal names from filenames
- Generate face encodings
- Store in MongoDB

### 4. Seed Criminal Data
```bash
python seed_criminal_data.py
```

This will update criminal records with detailed information for known criminals.

### 5. Run the Application
```bash
python app.py
```

Open browser: http://127.0.0.1:5000

## Features

### 1. Register Criminal
- Add new criminals to database
- Upload photo
- Enter crime details
- System extracts face encoding automatically

### 2. Check Criminal (Upload)
- Upload image
- System identifies criminals
- Shows full criminal record
- Displays "UNKNOWN" if not in database

### 3. Check Criminal (Webcam)
- Real-time face detection
- Instant criminal identification
- Live results display

### 4. View All Criminals
- Browse entire criminal database
- See all registered criminals

## Database Schema

```
criminal_db
  └── criminals
      ├── name (String, unique)
      ├── aliases (Array)
      ├── crime (String)
      ├── crime_details (String)
      ├── years_in_prison (String)
      ├── status (String)
      ├── nationality (String)
      ├── location (String)
      ├── description (String)
      ├── image_path (String)
      ├── face_encoding (Array)
      └── created_at (Date)
```

## File Structure

```
face_recognition/
├── app.py                      # Main Flask application
├── database.py                 # MongoDB connection
├── recognition.py              # Face recognition logic
├── import_criminal_dataset.py  # Dataset import script
├── seed_criminal_data.py       # Seed criminal data
├── templates/
│   ├── index.html             # Main page
│   ├── result.html            # Results page
│   └── criminals.html         # Criminal list
├── uploads/                    # Uploaded images
├── static/results/            # Result images
└── Dataset of Mugshots/       # Criminal dataset
```

## Usage

### Register New Criminal
1. Go to "Register Criminal" section
2. Fill in criminal details
3. Upload photo
4. Click "Register Criminal"

### Check Criminal Record
1. Go to "Check Criminal" section
2. Upload image OR use webcam
3. System will identify and show:
   - Criminal name
   - Crime details
   - Status
   - Location
   - Full record

### Unknown Face Handling
- If face not in database: Shows "UNKNOWN FACE"
- No crash or errors
- Clear message displayed

## Performance
- Encodings cached in memory
- Fast recognition (< 1 second)
- Supports multiple faces in single image

## Troubleshooting

**MongoDB Connection Error:**
- Ensure MongoDB is running
- Check connection string in database.py

**No Face Detected:**
- Use clear, well-lit images
- Face should be clearly visible
- Try different angle

**Import Dataset Failed:**
- Check dataset path
- Ensure images are valid
- Check file permissions

## Security Notes
- This is for educational/demonstration purposes
- Use proper authentication in production
- Secure MongoDB connection
- Implement access controls
