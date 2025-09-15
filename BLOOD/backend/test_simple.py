#!/usr/bin/env python3
import sys
import os

# Add the current directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from app import create_app
    from config import Config
    print("✓ Imports successful")
    
    app = create_app()
    print("✓ App creation successful")
    
    with app.app_context():
        print("✓ App context successful")
        print(f"✓ Database: {Config.MONGODB_DB}")
        print(f"✓ Host: {Config.MONGODB_URI}")
        
    print("🎉 All basic tests passed!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()