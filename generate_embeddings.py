#!/usr/bin/env python3
"""
Script to generate embeddings for FINMA regulations using open source sentence transformers
"""

import os
import sys
import pandas as pd
from modules.embed_open_source import embed_articles

def main():
    """
    Generate embeddings for all FINMA regulation files
    """
    print("🚀 Starting embedding generation with open source models...")
    
    # List of regulation files to process
    regulation_files = [
        'Data/Finma_EN/splitted/finma2017.xlsx',
        'Data/Finma_EN/splitted/finma2023.xlsx', 
        'Data/Finma_EN/splitted/finma2008.xlsx',
        'Data/Finma_EN/splitted/finma_optional.xlsx'
    ]
    
    for file_path in regulation_files:
        if os.path.exists(file_path):
            print(f"\n📄 Processing {file_path}...")
            
            try:
                # Load data
                df = pd.read_excel(file_path)
                print(f"   Loaded {len(df)} rows")
                
                # Generate embeddings
                embeddings_df = embed_articles(df)
                
                # Save embeddings
                output_file = file_path.replace('.xlsx', '_open_source_embeddings.xlsx')
                embeddings_df.to_excel(output_file, index=False)
                print(f"   ✅ Saved embeddings to {output_file}")
                
            except Exception as e:
                print(f"   ❌ Error processing {file_path}: {e}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print("\n🎉 Embedding generation completed!")
    print("\n📝 Next steps:")
    print("1. Update your analyzer to use the new embedding files")
    print("2. Test the gap analysis with the new embeddings")
    print("3. Deploy your application")

if __name__ == "__main__":
    main()
