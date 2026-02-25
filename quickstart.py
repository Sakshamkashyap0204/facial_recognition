"""
Quick Start Script for Criminal Record Detection System
Runs all setup steps automatically
"""
import subprocess
import sys

def run_command(command, description):
    """Run a command and print status"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print('='*60)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        print(f"✓ {description} - SUCCESS")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} - FAILED")
        print(e.stderr)
        return False

def main():
    print("\n" + "="*60)
    print("Criminal Record Detection System - Quick Start")
    print("="*60)
    
    steps = [
        ("python import_criminal_dataset.py", "Step 1: Importing Criminal Dataset"),
        ("python seed_criminal_data.py", "Step 2: Seeding Criminal Data"),
    ]
    
    for command, description in steps:
        if not run_command(command, description):
            print(f"\n⚠️  Warning: {description} failed, but continuing...")
    
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print("\nStarting Flask Application...")
    print("Open browser: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop\n")
    
    # Start Flask app
    subprocess.run("python app.py", shell=True)

if __name__ == "__main__":
    main()
