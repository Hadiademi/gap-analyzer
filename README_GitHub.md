# 🎯 AI-Powered Gap Analyzer

A sophisticated regulatory compliance gap analysis tool that uses AI to compare company documents against regulatory requirements and generate detailed Excel reports.

## ✨ Features

- **🤖 AI-Powered Analysis**: Uses Anthropic Claude 3 Haiku for intelligent gap analysis
- **📄 Document Processing**: Supports DOCX files with intelligent chunking
- **🔍 Semantic Search**: Open-source embeddings with Sentence Transformers
- **📊 Excel Reports**: Professional gap analysis reports with detailed comments
- **🎨 Modern UI**: Beautiful Streamlit interface with professional styling
- **🔧 Open Source**: No vendor lock-in, fully customizable

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Anthropic API key

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Hadiademi/gap-analyzer.git
cd gap-analyzer
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp env.example .env
# Edit .env and add your Anthropic API key
```

5. **Run the application**
```bash
streamlit run Rhizon.py
```

## 📋 How It Works

### 1. Document Upload
- Upload your company policy document (.docx)
- System automatically chunks the document by structure

### 2. Regulation Selection
- Choose from available regulations (FINMA, etc.)
- Select specific regulation to analyze against

### 3. AI Analysis
- Document chunks are converted to embeddings
- Semantic search finds relevant sections
- Claude AI analyzes gaps and requirements

### 4. Report Generation
- Detailed Excel report with:
  - Requirements analysis
  - Coverage status (Yes/Partial/No)
  - Professional comments (50+ words each)
  - Actionable recommendations

## 🏗️ Architecture

```
Document (.docx) → Chunking → Embeddings → Vector Store
                                           ↓
Regulation (Excel) → Similarity Search → AI Analysis → Excel Report
```

## 🛠️ Technologies Used

- **Frontend**: Streamlit
- **AI/LLM**: Anthropic Claude 3 Haiku
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB
- **Document Processing**: python-docx
- **Data Processing**: Pandas, NumPy
- **Styling**: Custom CSS

## 📁 Project Structure

```
gap-analyzer/
├── modules/
│   ├── model/
│   │   └── open_source_llm.py      # LLM and embeddings
│   ├── gap_analyzer_claude.py      # Main analysis logic
│   ├── improved_chunker.py         # Document chunking
│   └── UI/                         # User interface components
├── pages/
│   ├── gap_analyzer.py             # Gap analysis page
│   └── regulatory_repo.py          # Repository page
├── Data/
│   └── Finma_EN/                   # Regulation data
├── Rhizon.py                       # Main Streamlit app
└── requirements.txt                # Dependencies
```

## 🔧 Configuration

### Environment Variables
```bash
ANTHROPIC_API_KEY=your_api_key_here
ANTHROPIC_MODEL=claude-3-haiku-20240307
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
```

### Supported Regulations
- FINMA Operational Risk (RS 2023/1)
- FINMA Operational Risk (RS 2008/21)
- FINMA Operational Risk (RS 2017/1)
- FINMA Optional Risk

## 📊 Sample Output

The tool generates detailed Excel reports with:
- **Requirement**: Clear description of regulatory requirement
- **Covered**: Yes/Partial/No status
- **Reference**: Exact document section
- **Comment**: Detailed professional assessment (50+ words)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 👨‍💻 Author

**Hadia Demi** - [@Hadiademi](https://github.com/Hadiademi)

## 🙏 Acknowledgments

- Anthropic for Claude AI
- Streamlit for the web framework
- Sentence Transformers for embeddings
- ChromaDB for vector storage

---

⭐ **Star this repository if you find it helpful!**
