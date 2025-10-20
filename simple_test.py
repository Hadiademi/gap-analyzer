#!/usr/bin/env python3
"""
Simple test script for Gap Analyzer without emojis
"""

import os
import sys

def test_basic_setup():
    """Test basic setup"""
    print("Testing basic setup...")
    
    # Test 1: Check if we can import basic modules
    try:
        import pandas as pd
        print("OK Pandas imported successfully")
    except ImportError as e:
        print(f"ERROR Pandas import failed: {e}")
        return False
    
    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"ERROR Streamlit import failed: {e}")
        return False
    
    # Test 2: Check if data files exist
    required_files = [
        "Data/Finma_EN/splitted/finma2017.xlsx",
        "Data/Finma_EN/splitted/finma2023.xlsx",
        "Data/Finma_EN/splitted/finma2008.xlsx",
        "Data/Finma_EN/splitted/finma_optional.xlsx"
    ]
    
    print("\nChecking data files...")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"ERROR {file_path} missing")
            return False
    
    # Test 3: Check embeddings
    print("\nChecking embeddings...")
    try:
        df = pd.read_excel('Data/Finma_EN/splitted/finma2017.xlsx')
        if 'Embedding' in df.columns:
            non_null = df['Embedding'].notna().sum()
            print(f"✓ FINMA 2017: {non_null}/{len(df)} embeddings")
        else:
            print("ERROR No Embedding column in finma2017.xlsx")
            return False
    except Exception as e:
        print(f"ERROR Error reading finma2017.xlsx: {e}")
        return False
    
    # Test 4: Check if main app file exists
    print("\nChecking main application...")
    if os.path.exists("Rhizon.py"):
        print("✓ Main application file exists")
    else:
        print("ERROR Main application file missing")
        return False
    
    return True

def main():
    """Main test function"""
    print("=" * 50)
    print("Gap Analyzer Simple Test")
    print("=" * 50)
    
    success = test_basic_setup()
    
    print("\n" + "=" * 50)
    if success:
        print("✓ All basic tests passed!")
        print("\nYou can now:")
        print("1. Set up your API key in .env file")
        print("2. Run: streamlit run Rhizon.py")
        print("3. Open browser to http://localhost:8501")
    else:
        print("ERROR Some tests failed. Please check the errors above.")
    
    return success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
