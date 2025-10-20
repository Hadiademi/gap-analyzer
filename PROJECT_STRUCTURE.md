# 📁 Project Structure & Active Files

## 🟢 ACTIVE FILES (Currently in Use)

### Main Application
```
Rhizon.py                           ← Entry point (Streamlit main app)
├── pages/
│   ├── gap_analyzer.py             ← Gap analysis page (ACTIVE)
│   └── regulatory_repo.py          ← Regulatory repository page (ACTIVE)
```

### Core Modules (ACTIVE)
```
modules/
├── gap_analyzer_claude.py          ← ✅ MAIN GAP ANALYSIS MODULE
│   ├── split_docx_by_structure()   ← Universal chunking (ONE METHOD)
│   ├── create_vectorstore()        ← ChromaDB vector store
│   ├── build_gap_prompt()          ← LLM prompt builder
│   ├── extract_table_from_text()   ← Parse LLM response
│   └── perform_gap_analysis()      ← Main entry point
│
├── design_excel.py                 ← Excel report formatting
│
├── model/
│   └── open_source_llm.py          ← ✅ LLM & Embeddings (Anthropic + Sentence Transformers)
│       ├── OpenSourceEmbeddings    ← all-MiniLM-L6-v2
│       ├── AnthropicLLM            ← Claude 3 Haiku
│       └── get_llm()               ← LLM factory
│
├── UI/
│   ├── general.py                  ← UI components
│   ├── regulation_list.py          ← Regulation dropdown
│   └── dropdown_styling.py         ← CSS styling
│
└── prompts/
    └── gap_finder_prompt.py        ← Prompt templates
```

### Data Files (ACTIVE)
```
Data/
├── Finma_EN/splitted/
│   ├── finma2023_open_source_embeddings.xlsx  ← ✅ RS 2023/1 (384-dim embeddings)
│   ├── finma2017.xlsx                         ← ✅ RS 2017/1
│   ├── finma2008.xlsx                         ← ✅ RS 2008/21
│   └── finma_optional_open_source_embeddings.xlsx ← ✅ RS Optional
│
└── Document/
    ├── Concept_Risk and Governance_EN.docx    ← Test document 1
    └── IT_Risk_Controls_for_Banks.docx        ← Test document 2
```

---

## 🟡 BACKUP FILES (Not Currently in Use)

### Legacy Bedrock Files (AWS)
```
modules/
├── analyzer.py                     ← ⚠️ OLD: Bedrock-based analyzer
├── embed.py                        ← ⚠️ OLD: Bedrock embeddings
└── model/
    └── bedrock.py                  ← ⚠️ OLD: AWS Bedrock integration
```

**Status:** Deprecated. Kept for reference. System now uses open-source alternatives.

### Alternative Chunking Implementations
```
modules/
├── improved_chunker.py             ← ⚠️ BACKUP: Two-method chunking with detection
│   ├── detect_document_type()      ← Document type detection
│   ├── split_docx_by_bold_titles() ← Concept Risk specific
│   └── split_it_risk_controls()    ← IT Risk specific
│
├── universal_chunker.py            ← ⚠️ BACKUP: Alternative universal chunking
│
├── analyzer_open_source.py         ← ⚠️ OLD: First open-source migration
└── analyzer_it_risk.py             ← ⚠️ OLD: IT Risk Controls test
```

**Status:** Development/testing files. Current system uses `gap_analyzer_claude.py` with universal chunking.

### Legacy Embeddings (Bedrock)
```
Data/Finma_EN/splitted/
├── embedding_2008.xlsx             ← ⚠️ OLD: Bedrock embeddings (1536-dim)
├── embedding_2017.xlsx             ← ⚠️ OLD: Bedrock embeddings
├── embedding_2023.xlsx             ← ⚠️ OLD: Bedrock embeddings
├── finma2023.xlsx                  ← ⚠️ OLD: Bedrock embeddings
└── finma_optional.xlsx             ← ⚠️ OLD: Bedrock embeddings (no embeddings)
```

**Status:** Deprecated. Use `*_open_source_embeddings.xlsx` files instead.

---

## 🔄 CURRENT ARCHITECTURE

### Pipeline Flow
```
1. User Upload (DOCX)
   └── pages/gap_analyzer.py
       └── perform_gap_analysis()
           └── modules/gap_analyzer_claude.py

2. Document Chunking
   └── split_docx_by_structure()      ← UNIVERSAL METHOD
       ├── Detects: List Paragraph OR Heading 2 → Main Title
       ├── Detects: Bold OR List Bullet OR Heading 3 → Subtitle
       └── Else: Normal Content

3. Embedding Generation
   └── modules/model/open_source_llm.py
       └── OpenSourceEmbeddings (all-MiniLM-L6-v2)
           └── 384-dimensional vectors

4. Vector Store
   └── ChromaDB (vectorestores/chroma_db_temp_upload_*)

5. Regulation Loading
   └── Excel file (e.g., finma2023_open_source_embeddings.xlsx)
       └── Pre-computed 384-dim embeddings

6. Similarity Search
   └── For each regulation article:
       └── Find top 4 most similar document chunks

7. LLM Analysis
   └── Anthropic Claude 3 Haiku
       └── Gap analysis with detailed comments

8. Excel Report
   └── modules/design_excel.py
       └── Formatted gap analysis report
```

---

## 📊 WHY UNIVERSAL CHUNKING?

### Current Approach: ONE Method for ALL Documents
```python
# gap_analyzer_claude.py: split_docx_by_structure()

✅ Simpler codebase (one function)
✅ No detection overhead
✅ Works for mixed/hybrid documents
✅ Easier maintenance
✅ Robust fallback ("General" for documents without headings)
```

### Alternative Approach: TWO Methods with Detection
```python
# improved_chunker.py: detect_document_type() + specialized methods

✅ More specific to each document type
✅ Can optimize granularity separately
✅ Better for very different structures
❌ More complex code
❌ Requires detection logic
❌ Harder to maintain
```

**Decision:** Use universal method for simplicity and robustness. The alternative is kept as backup for reference.

---

## 🎯 KEY TAKEAWAYS

1. **Active Module:** `modules/gap_analyzer_claude.py` is the only active chunking/analysis module
2. **Universal Chunking:** Uses ONE method that handles both Concept Risk and IT Risk Controls
3. **Open Source:** All embeddings use Sentence Transformers (384-dim), not AWS Bedrock
4. **LLM:** Anthropic Claude 3 Haiku via direct API calls
5. **Backup Files:** Legacy and alternative implementations are kept for reference but not imported

---

## 📝 FOR DEVELOPERS

### To Understand the System
1. Start with: `Rhizon.py` (entry point)
2. Then read: `pages/gap_analyzer.py` (UI logic)
3. Core logic: `modules/gap_analyzer_claude.py` (main pipeline)
4. LLM/Embeddings: `modules/model/open_source_llm.py`

### To Test Chunking
```bash
# Test the backup/alternative chunking (standalone)
python modules/improved_chunker.py

# Test active system (requires Streamlit)
streamlit run Rhizon.py
```

### To Add New Document Types
Modify `split_docx_by_structure()` in `gap_analyzer_claude.py` to add new style detection:
```python
if style_name == 'List Paragraph' or style_name == 'Heading 2' or style_name == 'YOUR_NEW_STYLE':
    # Handle new main title style
```

---

**Last Updated:** October 2025  
**Active Version:** Universal Chunking with Claude 3 Haiku  
**Status:** Production Ready

