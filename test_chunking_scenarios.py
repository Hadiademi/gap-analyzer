"""
Test script to demonstrate chunking behavior with different control formats
"""

# Simulate the chunking logic
def split_docx_by_structure_simulation():
    """
    Simulating how the chunker handles different scenarios
    """
    
    print("=" * 80)
    print("SCENARIO 1: Controls WITH Heading (Current IT Risk Controls)")
    print("=" * 80)
    
    document_with_heading = [
        ("Heading 2", "Section 1: Access Control"),
        ("List Bullet", "C-01 | User Authentication"),
        ("Normal", "All users must authenticate using MFA"),
        ("Normal", "Biometric verification is required"),
        ("List Bullet", "C-02 | Password Policy"),
        ("Normal", "Passwords must be at least 12 characters"),
        ("Heading 2", "Section 2: Data Security"),
        ("List Bullet", "C-03 | Encryption at Rest"),
        ("Normal", "All sensitive data must be encrypted"),
    ]
    
    chunks_with_heading = []
    current_main_title = None
    current_subtitle = None
    current_content = []
    
    for style, text in document_with_heading:
        if style == 'Heading 2':
            if current_subtitle and current_content:
                chunks_with_heading.append([current_main_title, current_subtitle, current_content])
                current_content = []
            current_main_title = text
            current_subtitle = None
            
        elif style == 'List Bullet':
            if current_subtitle and current_content:
                chunks_with_heading.append([current_main_title, current_subtitle, current_content])
                current_content = []
            current_subtitle = text
            
        else:  # Normal
            current_content.append(text)
    
    # Save last chunk
    if current_subtitle and current_content:
        chunks_with_heading.append([current_main_title, current_subtitle, current_content])
    
    print(f"\nTotal chunks: {len(chunks_with_heading)}\n")
    for i, chunk in enumerate(chunks_with_heading, 1):
        print(f"Chunk {i}:")
        print(f"  Main Title: {chunk[0]}")
        print(f"  Subtitle: {chunk[1]}")
        print(f"  Content: {chunk[2]}")
        print()
    
    print("\n" + "=" * 80)
    print("SCENARIO 2: Controls WITHOUT Heading (Just a list)")
    print("=" * 80)
    
    document_without_heading = [
        ("List Bullet", "C-01 | User Authentication"),
        ("Normal", "All users must authenticate using MFA"),
        ("Normal", "Biometric verification is required"),
        ("List Bullet", "C-02 | Password Policy"),
        ("Normal", "Passwords must be at least 12 characters"),
        ("List Bullet", "C-03 | Encryption at Rest"),
        ("Normal", "All sensitive data must be encrypted"),
    ]
    
    chunks_without_heading = []
    current_main_title = None
    current_subtitle = None
    current_content = []
    
    for style, text in document_without_heading:
        if style == 'Heading 2':
            if current_subtitle and current_content:
                chunks_without_heading.append([current_main_title, current_subtitle, current_content])
                current_content = []
            current_main_title = text
            current_subtitle = None
            
        elif style == 'List Bullet':
            if current_subtitle and current_content:
                chunks_without_heading.append([current_main_title or "General", current_subtitle, current_content])
                current_content = []
            current_subtitle = text
            
        else:  # Normal
            current_content.append(text)
    
    # Save last chunk
    if current_subtitle and current_content:
        chunks_without_heading.append([current_main_title or "General", current_subtitle, current_content])
    
    print(f"\nTotal chunks: {len(chunks_without_heading)}\n")
    for i, chunk in enumerate(chunks_without_heading, 1):
        print(f"Chunk {i}:")
        print(f"  Main Title: {chunk[0]}")
        print(f"  Subtitle: {chunk[1]}")
        print(f"  Content: {chunk[2]}")
        print()
    
    print("\n" + "=" * 80)
    print("SCENARIO 3: Controls as Bold Text (Alternative format)")
    print("=" * 80)
    
    document_bold_controls = [
        ("Bold", "C-01 | User Authentication"),
        ("Normal", "All users must authenticate using MFA"),
        ("Normal", "Biometric verification is required"),
        ("Bold", "C-02 | Password Policy"),
        ("Normal", "Passwords must be at least 12 characters"),
        ("Bold", "C-03 | Encryption at Rest"),
        ("Normal", "All sensitive data must be encrypted"),
    ]
    
    chunks_bold = []
    current_main_title = None
    current_subtitle = None
    current_content = []
    
    for style, text in document_bold_controls:
        if style == 'Heading 2':
            if current_subtitle and current_content:
                chunks_bold.append([current_main_title, current_subtitle, current_content])
                current_content = []
            current_main_title = text
            current_subtitle = None
            
        elif style == 'List Bullet' or style == 'Bold':
            if current_subtitle and current_content:
                chunks_bold.append([current_main_title or "General", current_subtitle, current_content])
                current_content = []
            current_subtitle = text
            
        else:  # Normal
            current_content.append(text)
    
    # Save last chunk
    if current_subtitle and current_content:
        chunks_bold.append([current_main_title or "General", current_subtitle, current_content])
    
    print(f"\nTotal chunks: {len(chunks_bold)}\n")
    for i, chunk in enumerate(chunks_bold, 1):
        print(f"Chunk {i}:")
        print(f"  Main Title: {chunk[0]}")
        print(f"  Subtitle: {chunk[1]}")
        print(f"  Content: {chunk[2]}")
        print()

if __name__ == "__main__":
    split_docx_by_structure_simulation()

