"""
Gap Analysis Module using Claude API (Anthropic)
This module performs real-time gap analysis between uploaded documents and regulatory requirements
"""

from docx import Document as dx
import pandas as pd
import numpy as np
from langchain_chroma import Chroma
from langchain.schema.document import Document
from modules.model.open_source_llm import create_embeddings, get_llm
import streamlit as st
import os
import ast

# Initialize embeddings and LLM
embeddings = create_embeddings()
llm = get_llm()


def parse_embedding(embedding_str):
    """Parse embedding string to numpy array"""
    try:
        if isinstance(embedding_str, str):
            return np.array(ast.literal_eval(embedding_str))
        elif isinstance(embedding_str, (list, np.ndarray)):
            return np.array(embedding_str)
        else:
            return None
    except Exception as e:
        print(f"Error parsing embedding: {e}")
        return None


def split_docx_by_structure(file_path):
    """
    Universal document chunker that works with multiple document structures
    Handles both List Paragraph style (Concept Risk) and Heading styles (IT Risk Controls)
    """
    doc = dx(file_path)
    content = []
    current_main_title = None
    current_subtitle = None
    current_content = []
    index = 1
    
    for paragraph in doc.paragraphs:
        style_name = paragraph.style.name
        text = paragraph.text.strip()
        
        if not text:
            continue
            
        # Main titles - List Paragraph style or Heading 2
        if style_name == 'List Paragraph' or style_name == 'Heading 2':
            # Save previous section if exists
            if current_main_title:
                content.append([
                    current_main_title,
                    current_subtitle or "",
                    current_content
                ])
            
            # Start new main section
            if style_name == 'List Paragraph':
                current_main_title = f"{index}. {text}"
                index += 1
            else:
                current_main_title = text
            
            current_subtitle = None
            current_content = []
            
        # Subtitles - Bold text or List Bullet
        elif (any(run.bold for run in paragraph.runs) or 
              style_name == 'List Bullet' or 
              style_name == 'Heading 3'):
            # Save previous subsection if exists
            if current_subtitle and current_content:
                content.append([
                    current_main_title or "General",
                    current_subtitle,
                    current_content
                ])
                current_content = []
            
            current_subtitle = text
            
        # Regular content
        else:
            if text:
                current_content.append(text)
    
    # Save last section
    if current_main_title:
        content.append([
            current_main_title,
            current_subtitle or "",
            current_content
        ])
    
    return content


def create_vectorstore(db_directory, split_content):
    """Create ChromaDB vector store from document chunks"""
    documents = []
    
    for item in split_content:
        title = item[0]
        subtitle = item[1]
        content_list = item[2]
        
        # Combine content
        full_content = "\n".join(content_list) if content_list else ""
        
        # Create metadata
        metadata = {
            "title": title,
            "subtitle": subtitle
        }
        
        # Create page content
        page_content = f"Title: {title}"
        if subtitle:
            page_content += f"\nSubTitle: {subtitle}"
        page_content += f"\n{full_content}"
        
        # Create document
        doc = Document(
            page_content=page_content,
            metadata=metadata
        )
        documents.append(doc)
    
    # Create vector store - use a unique directory each time to avoid conflicts
    import time
    import uuid
    unique_db_directory = f"{db_directory}_{uuid.uuid4().hex[:8]}"
    
    vectorstore = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=unique_db_directory
    )
    
    return vectorstore


def build_gap_prompt(retrieved_docs, article):
    """Build professional prompt for comprehensive gap analysis with direct table output"""
    concept_text = ''
    for item in retrieved_docs:
        concept_text += '\n' + item.page_content
    
    concept_text = concept_text.replace("Title: ", 'Section: ').replace(' SubTitle:', ' SubSection:')
    
    prompt = f"""You are an expert in market conduct regulation for banks and a senior regulatory compliance consultant conducting a professional gap analysis between a company's internal documentation and regulatory requirements.

**YOUR TASK:**
Analyze the regulatory article below and identify EVERY requirement. For each requirement, evaluate whether the company's concept document adequately addresses it. Output your findings DIRECTLY in table format.

**ANALYSIS CRITERIA:**
- "Yes" = Requirement is FULLY addressed with specific controls, procedures, or evidence
- "Partial" = Requirement is mentioned but lacks sufficient detail, procedures, or implementation guidance
- "No" = Requirement is NOT addressed or missing entirely

**OUTPUT FORMAT:**
Create a table with EXACTLY these columns (use | as separator):
Requirement | Covered | Reference | Comment

**COLUMN SPECIFICATIONS:**
1. **Requirement**: Clear description of what the regulatory article requires (30-60 words). Be specific about WHAT must be done.
2. **Covered**: Only use "Yes", "Partial", or "No"
3. **Reference**: Exact section/subsection name from company document where requirement is addressed. Use "-" if not covered.
4. **Comment**: DETAILED professional assessment (MINIMUM 30 words, aim for 40 words) explaining:
   - For "Yes": Describe HOW the requirement is met, WHICH controls/procedures/evidence exist, and WHERE in the document they are documented. Include specific details about implementation.
   - For "Partial": Explain in detail WHAT aspects are covered, reference specific sections, then clearly describe WHAT specific elements/details/procedures are missing or inadequate. Provide recommendations.
   - For "No": Describe WHAT specific controls/procedures/documentation need to be implemented, WHY they are required by regulation, and provide actionable recommendations for compliance.

**QUALITY STANDARDS:**
- Comments MUST be detailed and comprehensive (minimum 30 words each)
- Be specific and actionable in all assessments
- Always reference exact sections from the company document
- Identify missing elements with specific details
- Write in professional business language suitable for executive review
- Provide actionable recommendations where gaps exist
- Each requirement must be on a separate row
- NEVER use short phrases - always write full explanatory sentences

**REGULATORY ARTICLE TO ANALYZE:**
{article}

**COMPANY CONCEPT DOCUMENT:**
{concept_text}

**OUTPUT YOUR GAP ANALYSIS TABLE BELOW (start immediately with data rows, no headers needed):**"""
    
    return prompt


# Removed build_table_prompt - now using direct table output in build_gap_prompt


def extract_table_from_text(margin, article, table_response):
    """Extract table data from LLM response with improved parsing"""
    rows = []
    
    # Split response into lines
    lines = table_response.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or '|' not in line:
            continue
        
        # Skip header lines (case insensitive)
        line_lower = line.lower()
        if ('requirement' in line_lower and 'covered' in line_lower) or \
           ('---' in line or '===' in line or '___' in line):
            continue
        
        # Split by | and handle cases with more than 4 parts (comment might contain |)
        parts = line.split('|')
        
        if len(parts) >= 4:
            requirement = parts[0].strip()
            covered = parts[1].strip()
            reference = parts[2].strip()
            
            # Join remaining parts as comment (in case comment contains |)
            comment = '|'.join(parts[3:]).strip()
            
            # Skip empty requirements
            if not requirement or len(requirement) < 5:
                continue
            
            # Normalize coverage values
            covered_normalized = covered
            if covered.lower() in ['yes', 'y', 'full', 'fully covered']:
                covered_normalized = 'Yes'
            elif covered.lower() in ['partial', 'partially', 'p', 'partly']:
                covered_normalized = 'Partial'
            elif covered.lower() in ['no', 'n', 'missing', 'not covered']:
                covered_normalized = 'No'
            
            rows.append([
                margin,                    # Article number
                article[:300],             # Article content (300 chars for context)
                requirement,               # Requirement description
                covered_normalized,        # Coverage status (Yes/Partial/No)
                reference if reference != '-' else '',  # Reference in document
                comment                    # Detailed comment
            ])
    
    return rows


def perform_gap_analysis(uploaded_file, regulation_file, regulation_name):
    """
    Main function to perform gap analysis
    
    Args:
        uploaded_file: Streamlit uploaded file object (company document)
        regulation_file: Path to regulation Excel file
        regulation_name: Name of the regulation
        
    Returns:
        DataFrame with gap analysis results
    """
    
    # Save uploaded file temporarily
    temp_file_path = f"temp_uploaded_document.docx"
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Parse uploaded document
    status_text.text("Parsing uploaded document...")
    split_content = split_docx_by_structure(temp_file_path)
    progress_bar.progress(10)
    
    # Step 2: Create vector store
    status_text.text("Creating document embeddings...")
    db_directory = "vectorestores/chroma_db_temp_upload"
    vectorstore = create_vectorstore(db_directory, split_content)
    vectorstore_directory = vectorstore._persist_directory  # Store the actual directory path
    progress_bar.progress(30)
    
    # Step 3: Load regulation data
    status_text.text(f"Loading {regulation_name} regulation...")
    df_regulation = pd.read_excel(regulation_file)
    df_regulation['Embedding'] = df_regulation['Embedding'].apply(parse_embedding)
    progress_bar.progress(40)
    
    # Step 4: Perform gap analysis
    status_text.text("Analyzing gaps with Claude AI...")
    
    headers = ['Article', 'Article Content', 'Requirement', 'Covered', 'Reference in Document', 'Comment']
    all_rows = []
    
    total_articles = len(df_regulation)
    
    for index, row in df_regulation.iterrows():
        # Extract article information
        title = str(row.get('Title', ''))
        sub_title = str(row.get('SubTitle', ''))
        sub_subtitle = str(row.get('Sub_Subtitle', ''))
        margin = str(row.get('Margin', ''))
        text = row.get('Text', '')
        embedded_item = row.get('Embedding', None)
        
        # Skip abrogated articles
        if text == 'Abrogated' or text == 'abrogated':
            continue
        
        # Build full article text
        full_text = ''
        if title and title not in ['None', 'nan', '']:
            full_text = title
        if sub_title and sub_title not in ['None', 'nan', '']:
            full_text = full_text + '\n' + sub_title if full_text else sub_title
        if sub_subtitle and sub_subtitle not in ['None', 'nan', '']:
            full_text = full_text + '\n' + sub_subtitle if full_text else sub_subtitle
        full_text = full_text + '\n' + text if full_text else text
        
        # Similarity search
        if embedded_item is not None:
            try:
                results = vectorstore.similarity_search_by_vector(
                    embedding=embedded_item.tolist() if isinstance(embedded_item, np.ndarray) else embedded_item,
                    k=4
                )
                
                # Build gap analysis prompt (direct table output)
                gap_prompt = build_gap_prompt(results, full_text)
                
                # Get gap analysis from Claude (single call - returns table directly)
                # Use higher max_tokens for detailed comments with retry logic
                max_retries = 3
                for attempt in range(max_retries):
                    try:
                        table_response = llm.ask_llm(gap_prompt, temperature=0.2, max_tokens=3000)
                        break  # Success, exit retry loop
                    except Exception as e:
                        if attempt < max_retries - 1:
                            import time
                            time.sleep(2)  # Wait 2 seconds before retry
                            continue
                        else:
                            raise e  # Re-raise the exception on final attempt
                
                # Extract table data
                cur_table_data = extract_table_from_text(margin, full_text, table_response)
                all_rows.extend(cur_table_data)
                
                # Progress tracking only - no individual article messages
                
            except Exception as e:
                st.warning(f"Error analyzing article {margin}: {str(e)}")
                continue
        
        # Update progress
        progress = 40 + int((index + 1) / total_articles * 50)
        progress_bar.progress(min(progress, 90))
        status_text.text(f"Analyzing article {index + 1}/{total_articles}...")
    
    # Step 5: Create DataFrame
    status_text.text("Generating Excel report...")
    df_results = pd.DataFrame(all_rows, columns=headers)
    progress_bar.progress(100)
    
    # Clean up
    status_text.empty()
    progress_bar.empty()
    
    # Remove temp files
    if os.path.exists(temp_file_path):
        os.remove(temp_file_path)
    
    # Clean up vector store - just close the connection, keep the files
    try:
        # Close the vectorstore connection
        if 'vectorstore' in locals():
            try:
                vectorstore._client.reset()
            except:
                pass
        
        # Note: We keep the vectorstore files for potential reuse or debugging
        # They are stored in unique directories so they won't conflict
        pass
    except Exception as e:
        pass  # Ignore cleanup errors
    
    return df_results

