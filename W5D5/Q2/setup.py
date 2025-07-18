#!/usr/bin/env python3
"""
Setup script for Quick Commerce Price Comparison Platform
"""

import os
import sys
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_gemini_api_key():
    """Check if Gemini API key is set in .env file or environment"""
    
    # First check if .env file exists
    if os.path.exists('.env'):
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            print("✅ GEMINI_API_KEY found in .env file")
            return True
        else:
            print("❌ .env file exists but GEMINI_API_KEY not found in it")
    else:
        print("❌ .env file not found")
    
    # Check environment variable as fallback
    api_key = os.getenv('GEMINI_API_KEY')
    if api_key:
        print("✅ GEMINI_API_KEY found in environment variables")
        return True
    
    print("\n📋 To set up your Gemini API key:")
    print("1. Get your API key from: https://makersuite.google.com/app/apikey")
    print("2. Copy the example file: cp env.example .env")
    print("3. Edit .env and replace 'your_gemini_api_key_here' with your actual API key")
    print("\n💡 Or create .env file directly:")
    print("   echo 'GEMINI_API_KEY=your_actual_api_key' > .env")
    print("\n🔒 The .env file is already added to .gitignore for security")
    
    return False

def install_requirements():
    """Install Python requirements"""
    try:
        print("📦 Installing Python requirements...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_database():
    """Setup SQLite database"""
    try:
        print("🗄️ Setting up SQLite database...")
        subprocess.check_call([sys.executable, "database_setup.py"])
        print("✅ Database setup completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup database: {e}")
        return False

def test_system():
    """Test the system components"""
    try:
        print("🧪 Testing system components...")
        subprocess.check_call([sys.executable, "query_agent.py"])
        print("✅ System test completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ System test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Quick Commerce Price Comparison Platform Setup")
    print("=" * 60)
    
    success = True
    
    # Check Python version
    success &= check_python_version()
    
    # Check API key
    success &= check_gemini_api_key()
    
    if not success:
        print("\n❌ Setup prerequisites not met. Please fix the issues above.")
        return False
    
    # Install requirements
    success &= install_requirements()
    
    # Setup database
    success &= setup_database()
    
    # Test system
    success &= test_system()
    
    if success:
        print("\n🎉 Setup completed successfully!")
        print("\n🚀 Ready to start the application:")
        print("   python3 app.py")
        print("\n🌐 Then open: http://localhost:5000")
        print("\n📊 Sample queries to try:")
        print("   • Which app has cheapest onions right now?")
        print("   • Show products with 30%+ discount on Blinkit")
        print("   • Compare fruit prices between Zepto and Instamart")
        print("   • Find best deals for ₹1000 grocery list")
    else:
        print("\n❌ Setup failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 