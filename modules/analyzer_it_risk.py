from docx import Document as dx
import pandas as pd
import re
import os
from langchain.schema.document import Document

def split_it_risk_document(file_path):
    """
    Split IT Risk Controls document by its specific structure
    """
    doc = dx(file_path)
    
    content = []
    current_section = None
    current_control = None
    current_data = []
    
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if not text:
            continue
        
        style = paragraph.style.name
        
        # Detect main sections (Heading 2)
        if style == 'Heading 2':
            # Save previous control if exists
            if current_control and current_data:
                content.append([current_section, current_control, current_data])
                current_data = []
            
            current_section = text
            current_control = None
            print(f"Section: {current_section}")
            
        # Detect controls (List Bullet with C-XX pattern)
        elif style == 'List Bullet' or (text.startswith('C-') and '|' in text):
            # Save previous control if exists
            if current_control and current_data:
                content.append([current_section, current_control, current_data])
                current_data = []
            
            current_control = text.replace('**', '').strip()
            print(f"  Control: {current_control}")
            
        # Normal content belongs to current control
        elif current_control and style == 'Normal':
            if text:
                current_data.append(text)
    
    # Save last control
    if current_control and current_data:
        content.append([current_section, current_control, current_data])
    
    return content

def create_vectorstore_it_risk(db_directory, split_content, embeddings):
    """
    Create vector store for IT Risk Controls document
    """
    from langchain_chroma import Chroma
    
    to_embed_docs = []
    doc_num = 1
    
    for row in split_content:
        if row[2]:  # If has content
            section = row[0] if row[0] else "General"
            control = row[1] if row[1] else "No Control"
            joined_content = '\n'.join(row[2])
            
            # Build full text
            content = f"Section: {section}\nControl: {control}\n{joined_content}"
            
            print(f"Creating document {doc_num}: {control[:50]}...")
            to_embed_docs.append(Document(
                page_content=content,
                metadata={
                    'id': doc_num,
                    'section': section,
                    'control': control
                }
            ))
            doc_num += 1
    
    # Create ChromaDB vector store
    if not os.path.isdir(db_directory):
        os.makedirs(db_directory)
    
    vectorstore = Chroma(
        collection_name="it_risk_controls",
        embedding_function=embeddings,
        persist_directory=db_directory,
    )
    vectorstore.add_documents(to_embed_docs)
    
    return vectorstore

if __name__ == "__main__":
    # Test the new chunking
    file_path = "Data/Document/IT_Risk_Controls_for_Banks.docx"
    split_content = split_it_risk_document(file_path)
    
    print(f"\n{'='*60}")
    print(f"Total chunks created: {len(split_content)}")
    print(f"{'='*60}")
    
    # Show first 3 chunks
    for i, chunk in enumerate(split_content[:3]):
        print(f"\nChunk {i+1}:")
        print(f"  Section: {chunk[0]}")
        print(f"  Control: {chunk[1]}")
        print(f"  Content lines: {len(chunk[2])}")
        print(f"  First line: {chunk[2][0][:80] if chunk[2] else 'N/A'}...")
