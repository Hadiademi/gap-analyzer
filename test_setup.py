#!/usr/bin/env python3
"""
Test script to verify the open source setup is working correctly
"""

import os
import sys
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_imports():
    """Test if all required packages can be imported"""
    print("Testing imports...")
    
    try:
        from modules.model.open_source_llm import create_embeddings, create_openai_llm, create_anthropic_llm
        print("   ✅ Open source LLM module imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import open source LLM module: {e}")
        return False
    
    try:
        from modules.embed_open_source import embed_articles
        print("   ✅ Open source embeddings module imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import embeddings module: {e}")
        return False
    
    try:
        import streamlit as st
        print("   ✅ Streamlit imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import Streamlit: {e}")
        return False
    
    try:
        from sentence_transformers import SentenceTransformer
        print("   ✅ Sentence Transformers imported successfully")
    except ImportError as e:
        print(f"   ❌ Failed to import Sentence Transformers: {e}")
        return False
    
    return True

def test_embeddings():
    """Test embeddings functionality"""
    print("\nTesting embeddings...")
    
    try:
        from modules.model.open_source_llm import create_embeddings
        embeddings = create_embeddings()
        
        # Test embedding generation
        test_text = "This is a test document for compliance analysis."
        embedding = embeddings.embed_query(test_text)
        
        if len(embedding) > 0:
            print(f"   ✅ Generated embedding with {len(embedding)} dimensions")
            return True
        else:
            print("   ❌ Generated empty embedding")
            return False
            
    except Exception as e:
        print(f"   ❌ Embeddings test failed: {e}")
        return False

def test_llm_setup():
    """Test LLM setup (without making actual API calls)"""
    print("\nTesting LLM setup...")
    
    # Check environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    
    if openai_key:
        print("   ✅ OpenAI API key found")
        try:
            from modules.model.open_source_llm import create_openai_llm
            llm = create_openai_llm()
            print("   ✅ OpenAI LLM instance created successfully")
            return True
        except Exception as e:
            print(f"   ❌ OpenAI LLM setup failed: {e}")
            return False
    elif anthropic_key:
        print("   ✅ Anthropic API key found")
        try:
            from modules.model.open_source_llm import create_anthropic_llm
            llm = create_anthropic_llm()
            print("   ✅ Anthropic LLM instance created successfully")
            return True
        except Exception as e:
            print(f"   ❌ Anthropic LLM setup failed: {e}")
            return False
    else:
        print("   ⚠️  No API keys found. Please set OPENAI_API_KEY or ANTHROPIC_API_KEY")
        return False

def test_data_files():
    """Test if required data files exist"""
    print("\nTesting data files...")
    
    required_files = [
        "Data/Finma_EN/splitted/finma2017.xlsx",
        "Data/Finma_EN/splitted/finma2023.xlsx",
        "Data/Document/Concept_Risk and Governance_EN.docx"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path} exists")
        else:
            print(f"   ❌ {file_path} not found")
            all_exist = False
    
    return all_exist

def test_chromadb():
    """Test ChromaDB functionality"""
    print("\nTesting ChromaDB...")
    
    try:
        from langchain_chroma import Chroma
        from modules.model.open_source_llm import create_embeddings
        
        embeddings = create_embeddings()
        
        # Create a test vector store
        test_docs = ["Test document 1", "Test document 2"]
        vectorstore = Chroma.from_texts(
            texts=test_docs,
            embedding=embeddings,
            persist_directory="./test_chroma"
        )
        
        # Test similarity search
        results = vectorstore.similarity_search("test", k=1)
        
        if results:
            print("   ✅ ChromaDB test successful")
            # Clean up test directory
            import shutil
            shutil.rmtree("./test_chroma", ignore_errors=True)
            return True
        else:
            print("   ❌ ChromaDB similarity search failed")
            return False
            
    except Exception as e:
        print(f"   ❌ ChromaDB test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting Gap Analyzer Open Source Setup Test\n")
    
    tests = [
        ("Imports", test_imports),
        ("Embeddings", test_embeddings),
        ("LLM Setup", test_llm_setup),
        ("Data Files", test_data_files),
        ("ChromaDB", test_chromadb)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"   ❌ {test_name} test crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:20} {status}")
        if result:
            passed += 1
    
    print("="*50)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("\nAll tests passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run 'python generate_embeddings.py' to generate embeddings")
        print("2. Run 'streamlit run Rhizon.py' to start the application")
        print("3. Or use 'docker-compose up --build' for Docker deployment")
    else:
        print(f"\n⚠️  {total - passed} tests failed. Please check the errors above.")
        print("\n🔧 Common solutions:")
        print("- Install missing dependencies: pip install -r requirements.txt")
        print("- Set up API keys in .env file")
        print("- Ensure all data files are present")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
