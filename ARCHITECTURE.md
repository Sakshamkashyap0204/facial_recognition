# Criminal Record Detection System - Architecture

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│                   (Web Browser)                              │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    FLASK APPLICATION                         │
│                       (app.py)                               │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Register   │  │    Check     │  │   Webcam     │     │
│  │   Criminal   │  │   Criminal   │  │    Check     │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
┌──────────────────┐ ┌──────────────┐ ┌──────────────┐
│   database.py    │ │recognition.py│ │  OpenCV/CV2  │
│                  │ │              │ │              │
│ - MongoDB Ops    │ │ - Face Rec   │ │ - Image Proc │
│ - CRUD           │ │ - Encoding   │ │ - Drawing    │
│ - Caching        │ │ - Matching   │ │ - Capture    │
└──────────────────┘ └──────────────┘ └──────────────┘
            │               │
            ▼               ▼
┌─────────────────────────────────────────────────────────────┐
│                      MONGODB DATABASE                        │
│                      (criminal_db)                           │
│                                                              │
│  Collection: criminals                                       │
│  ┌────────────────────────────────────────────────────┐    │
│  │ - name (unique)                                     │    │
│  │ - crime, crime_details                              │    │
│  │ - status, location, nationality                     │    │
│  │ - face_encoding (128-D array)                       │    │
│  │ - image_path                                        │    │
│  │ - created_at                                        │    │
│  └────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Data Flow

### 1. Register Criminal Flow
```
User Input (Form + Image)
    ↓
Flask Route (/register_criminal)
    ↓
Extract Face Encoding (face_recognition)
    ↓
Store in MongoDB (database.py)
    ↓
Reload Cache (recognition.py)
    ↓
Success Message
```

### 2. Check Criminal Flow (Upload)
```
User Upload Image
    ↓
Flask Route (/check_criminal)
    ↓
Load Image (OpenCV)
    ↓
Extract Encoding (face_recognition)
    ↓
Compare with Cached Encodings (recognition.py)
    ↓
Match Found?
    ├─ YES → Fetch Full Record from MongoDB
    └─ NO  → Return "Unknown Face"
    ↓
Draw Results (OpenCV)
    ↓
Display Results Page
```

### 3. Webcam Check Flow
```
User Clicks "Start Webcam"
    ↓
Browser Captures Video Stream
    ↓
User Clicks "Capture"
    ↓
Convert to Base64
    ↓
AJAX POST to /webcam_check
    ↓
Decode Image (Flask)
    ↓
Extract Encoding (face_recognition)
    ↓
Compare with Database (recognition.py)
    ↓
Draw Results (OpenCV)
    ↓
Return JSON Response
    ↓
Display Results (JavaScript)
```

### 4. Dataset Import Flow
```
Run import_criminal_dataset.py
    ↓
Read Images from Dataset Folder
    ↓
For Each Image:
    ├─ Extract Name from Filename
    ├─ Load Image (face_recognition)
    ├─ Generate Face Encoding
    ├─ Check if Already Exists
    └─ Store in MongoDB
    ↓
Import Complete
```

### 5. Seed Data Flow
```
Run seed_criminal_data.py
    ↓
For Each Criminal in CRIMINAL_DATA:
    ├─ Check if Exists in Database
    ├─ Update with Detailed Information
    └─ Save to MongoDB
    ↓
Seeding Complete
```

## Component Interaction

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │ HTTP Request
       ▼
┌─────────────┐
│    Flask    │◄──────┐
└──────┬──────┘       │
       │              │
       ├──────────────┤
       │              │
       ▼              │
┌─────────────┐       │
│ recognition │       │
│    .py      │       │
└──────┬──────┘       │
       │              │
       │ Get Encodings│
       ▼              │
┌─────────────┐       │
│ database.py │───────┘
└──────┬──────┘
       │ Query
       ▼
┌─────────────┐
│   MongoDB   │
└─────────────┘
```

## File Organization

```
face_recognition/
│
├── Core Application
│   ├── app.py                  # Main Flask app
│   ├── database.py             # MongoDB operations
│   └── recognition.py          # Face recognition logic
│
├── Setup Scripts
│   ├── import_criminal_dataset.py
│   ├── seed_criminal_data.py
│   ├── quickstart.py
│   └── test_system.py
│
├── Templates
│   ├── index.html              # Main UI
│   ├── result.html             # Results display
│   └── criminals.html          # Database view
│
├── Data Directories
│   ├── uploads/                # Uploaded images
│   ├── static/results/         # Result images
│   └── Dataset of Mugshots/    # Criminal dataset
│
└── Documentation
    ├── README_CRIMINAL_SYSTEM.md
    ├── SETUP_INSTRUCTIONS.md
    ├── IMPLEMENTATION_COMPLETE.md
    ├── CHECKLIST.md
    └── ARCHITECTURE.md (this file)
```

## Technology Stack

```
┌─────────────────────────────────────────┐
│           Frontend Layer                 │
│  HTML5 │ CSS3 │ JavaScript │ Canvas API │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          Application Layer               │
│         Flask (Python 3.8+)              │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│         Processing Layer                 │
│  face_recognition │ OpenCV │ NumPy      │
└─────────────────────────────────────────┘
                    │
┌─────────────────────────────────────────┐
│          Database Layer                  │
│         MongoDB (NoSQL)                  │
└─────────────────────────────────────────┘
```

## Performance Optimization

```
┌──────────────────────────────────────┐
│     Application Startup              │
└──────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│  Load All Encodings from MongoDB    │
│  (One-time operation)                │
└──────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│  Cache in Memory                     │
│  (Global variables)                  │
└──────────────────────────────────────┘
                │
                ▼
┌──────────────────────────────────────┐
│  Fast Recognition                    │
│  (No database queries)               │
│  < 1 second response                 │
└──────────────────────────────────────┘
```

## Security Considerations

```
Input Validation
    ├─ File type checking
    ├─ File size limits
    ├─ Filename sanitization
    └─ Form data validation

Database Security
    ├─ MongoDB authentication (optional)
    ├─ Connection encryption
    └─ Input sanitization

Application Security
    ├─ Flask secret key
    ├─ CSRF protection
    └─ Error message safety
```

## Scalability

```
Current: Single Server
    ├─ In-memory caching
    ├─ Single MongoDB instance
    └─ Synchronous processing

Future: Distributed
    ├─ Redis for caching
    ├─ MongoDB replica set
    ├─ Load balancer
    └─ Async processing
```

---

**Architecture Status**: ✅ Implemented
**Performance**: ✅ Optimized
**Scalability**: ✅ Ready for expansion
