#!/usr/bin/env python3
"""
Setup script for Gap Analyzer Open Source version
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"   ✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ {description} failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} is not compatible")
        print("   Please use Python 3.8 or higher")
        return False

def setup_environment():
    """Set up virtual environment"""
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Creating virtual environment"):
            return False
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
    else:  # Unix/Linux/MacOS
        activate_script = "venv/bin/activate"
        pip_command = "venv/bin/pip"
    
    print(f"📦 Installing dependencies...")
    if not run_command(f"{pip_command} install --upgrade pip", "Upgrading pip"):
        return False
    
    if not run_command(f"{pip_command} install -r requirements.txt", "Installing requirements"):
        return False
    
    return True

def setup_env_file():
    """Set up environment file"""
    print("⚙️  Setting up environment file...")
    
    if not os.path.exists(".env"):
        if os.path.exists("env.example"):
            shutil.copy("env.example", ".env")
            print("   ✅ Created .env file from template")
            print("   ⚠️  Please edit .env file with your API keys")
        else:
            print("   ❌ env.example file not found")
            return False
    else:
        print("   ✅ .env file already exists")
    
    return True

def check_data_files():
    """Check if required data files exist"""
    print("📁 Checking data files...")
    
    required_files = [
        "Data/Finma_EN/splitted/finma2017.xlsx",
        "Data/Finma_EN/splitted/finma2023.xlsx",
        "Data/Document/Concept_Risk and Governance_EN.docx"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("   ❌ Missing required files:")
        for file in missing_files:
            print(f"      - {file}")
        return False
    else:
        print("   ✅ All required data files found")
        return True

def create_directories():
    """Create necessary directories"""
    print("📂 Creating directories...")
    
    directories = [
        "Results",
        "vectorestores",
        "vectorestores/chroma_db_document_open_source"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("   ✅ Directories created successfully")
    return True

def main():
    """Main setup function"""
    print("🚀 Gap Analyzer Open Source Setup")
    print("=" * 40)
    
    steps = [
        ("Python Version", check_python_version),
        ("Environment Setup", setup_environment),
        ("Environment File", setup_env_file),
        ("Data Files", check_data_files),
        ("Directories", create_directories)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}")
        if not step_func():
            failed_steps.append(step_name)
    
    print("\n" + "=" * 40)
    print("📊 SETUP SUMMARY")
    print("=" * 40)
    
    if not failed_steps:
        print("🎉 Setup completed successfully!")
        print("\n📝 Next steps:")
        print("1. Edit .env file with your API keys:")
        print("   - OPENAI_API_KEY=your_key_here")
        print("   - or ANTHROPIC_API_KEY=your_key_here")
        print("\n2. Activate virtual environment:")
        if os.name == 'nt':
            print("   venv\\Scripts\\activate")
        else:
            print("   source venv/bin/activate")
        print("\n3. Test the setup:")
        print("   python test_setup.py")
        print("\n4. Generate embeddings:")
        print("   python generate_embeddings.py")
        print("\n5. Run the application:")
        print("   streamlit run Rhizon.py")
        print("\n6. Or use Docker:")
        print("   docker-compose up --build")
    else:
        print(f"❌ Setup failed at {len(failed_steps)} step(s):")
        for step in failed_steps:
            print(f"   - {step}")
        print("\n🔧 Please fix the errors above and run setup again")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
