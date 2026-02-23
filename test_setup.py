"""
Test script to verify face recognition setup
"""
import sys

def test_imports():
    """Test if all required packages are installed"""
    print("Testing imports...")
    
    try:
        import flask
        print("✓ Flask installed")
    except ImportError:
        print("✗ Flask not installed - Run: pip install Flask")
        return False
    
    try:
        import face_recognition
        print("✓ face_recognition installed")
    except ImportError:
        print("✗ face_recognition not installed - Run: pip install face_recognition")
        return False
    
    try:
        import numpy
        print("✓ NumPy installed")
    except ImportError:
        print("✗ NumPy not installed - Run: pip install numpy")
        return False
    
    try:
        from PIL import Image
        print("✓ Pillow installed")
    except ImportError:
        print("✗ Pillow not installed - Run: pip install Pillow")
        return False
    
    return True

def test_folders():
    """Test if required folders exist"""
    import os
    print("\nTesting folders...")
    
    folders = ['uploads', 'known_faces', 'static/results', 'templates']
    all_exist = True
    
    for folder in folders:
        if os.path.exists(folder):
            print(f"✓ {folder}/ exists")
        else:
            print(f"✗ {folder}/ missing - Will be created automatically")
            all_exist = False
    
    return True  # Not critical, will be created

def test_templates():
    """Test if template files exist"""
    import os
    print("\nTesting templates...")
    
    templates = ['templates/index.html', 'templates/result.html']
    all_exist = True
    
    for template in templates:
        if os.path.exists(template):
            print(f"✓ {template} exists")
        else:
            print(f"✗ {template} missing")
            all_exist = False
    
    return all_exist

def test_app():
    """Test if app.py exists and is valid"""
    import os
    print("\nTesting app.py...")
    
    if os.path.exists('app.py'):
        print("✓ app.py exists")
        return True
    else:
        print("✗ app.py missing")
        return False

def main():
    print("="*50)
    print("Face Recognition Setup Test")
    print("="*50)
    print()
    
    tests = [
        ("Imports", test_imports),
        ("Folders", test_folders),
        ("Templates", test_templates),
        ("Application", test_app)
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"✗ Error in {name}: {e}")
            results.append((name, False))
    
    print("\n" + "="*50)
    print("Test Summary")
    print("="*50)
    
    all_passed = True
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print()
    if all_passed:
        print("✓ All tests passed! You can run: python app.py")
    else:
        print("✗ Some tests failed. Please fix the issues above.")
        print("\nQuick fix:")
        print("  pip install -r requirements.txt")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
