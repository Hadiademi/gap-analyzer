from docx import Document as dx
import sys

def analyze_document_structure(file_path):
    """
    Analyze the structure of a DOCX document
    """
    print(f"Analyzing document: {file_path}")
    print("=" * 60)
    
    doc = dx(file_path)
    
    print(f"\nTotal paragraphs: {len(doc.paragraphs)}")
    print("\nDocument Structure Analysis:")
    print("=" * 60)
    
    list_paragraph_count = 0
    bold_paragraph_count = 0
    normal_paragraph_count = 0
    
    for i, paragraph in enumerate(doc.paragraphs[:30]):  # First 30 paragraphs
        text = paragraph.text.strip()
        if not text:
            continue
            
        style = paragraph.style.name
        has_bold = any(run.bold for run in paragraph.runs)
        
        # Categorize
        if style == 'List Paragraph':
            list_paragraph_count += 1
            category = "[LIST PARAGRAPH]"
        elif has_bold:
            bold_paragraph_count += 1
            category = "[BOLD]"
        else:
            normal_paragraph_count += 1
            category = "[NORMAL]"
        
        print(f"\n{i+1}. {category}")
        print(f"   Style: {style}")
        print(f"   Text: {text[:80]}{'...' if len(text) > 80 else ''}")
    
    print("\n" + "=" * 60)
    print("SUMMARY:")
    print("=" * 60)
    print(f"List Paragraphs: {list_paragraph_count}")
    print(f"Bold Paragraphs: {bold_paragraph_count}")
    print(f"Normal Paragraphs: {normal_paragraph_count}")
    
    print("\n" + "=" * 60)
    print("CHUNKING PIPELINE COMPATIBILITY:")
    print("=" * 60)
    
    if list_paragraph_count > 0:
        print("OK List Paragraphs detected - will be used as main titles")
    else:
        print("WARNING No List Paragraphs found - may need adjustment")
    
    if bold_paragraph_count > 0:
        print("OK Bold text detected - will be used as subtitles")
    else:
        print("WARNING No bold text found - subtitles may not be detected")
    
    if normal_paragraph_count > 0:
        print("OK Normal text detected - will be used as content")
    
    return {
        'list_paragraphs': list_paragraph_count,
        'bold_paragraphs': bold_paragraph_count,
        'normal_paragraphs': normal_paragraph_count
    }

if __name__ == "__main__":
    file_path = "Data/Document/IT_Risk_Controls_for_Banks.docx"
    analyze_document_structure(file_path)
