# Gap Analyzer - Open Source AI Compliance Tool

An AI-powered regulatory compliance gap analysis tool built with Streamlit that analyzes company documents against regulatory frameworks (like FINMA regulations) to identify compliance gaps and generate detailed reports.

## 🚀 Features

- **Regulatory Repository**: Browse and view different regulatory frameworks
- **AI Gap Analysis**: Upload company documents and analyze against regulations
- **Open Source Stack**: Uses Sentence Transformers for embeddings and OpenAI/Anthropic for LLM
- **Excel Reports**: Generate formatted compliance reports with color-coded status
- **Modern UI**: Clean Streamlit interface with custom styling

## 🛠️ Technology Stack

### Open Source Components
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2, all-mpnet-base-v2, etc.)
- **Vector Store**: ChromaDB
- **Document Processing**: LangChain, python-docx, pdfminer
- **Web Framework**: Streamlit

### LLM Providers (Choose One)
- **OpenAI**: GPT-4, GPT-3.5-turbo
- **Anthropic**: Claude-3-Sonnet, Claude-3-Haiku

## 📦 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd Gap_Analyzer-main
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
   # Edit .env with your API keys
   ```

5. **Generate embeddings**
   ```bash
   python generate_embeddings.py
   ```

6. **Run the application**
   ```bash
   streamlit run Rhizon.py
   ```

### Docker Deployment

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**
   ```bash
   docker build -t gap-analyzer .
   docker run -p 8501:8501 --env-file .env gap-analyzer
   ```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Choose your LLM provider
LLM_PROVIDER=openai  # or "anthropic"

# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

# Anthropic Configuration (Alternative)
ANTHROPIC_API_KEY=your_anthropic_api_key_here
ANTHROPIC_MODEL=claude-3-sonnet-20240229

# Embeddings Model
EMBEDDINGS_MODEL=all-MiniLM-L6-v2
```

### Available Embedding Models
- `all-MiniLM-L6-v2` (Default, fast and efficient)
- `all-mpnet-base-v2` (Better quality, slower)
- `paraphrase-multilingual-MiniLM-L12-v2` (Multilingual support)

## 🌐 Deployment Options

### 1. Railway (Recommended)
- Connect your GitHub repository
- Set environment variables in Railway dashboard
- Automatic deployments on push

### 2. Render
- Connect your repository
- Set environment variables
- Configure build command: `pip install -r requirements.txt`
- Start command: `streamlit run Rhizon.py --server.port=$PORT --server.address=0.0.0.0`

### 3. Heroku
- Add `Procfile`: `web: streamlit run Rhizon.py --server.port=$PORT --server.address=0.0.0.0`
- Add `runtime.txt`: `python-3.11.7`
- Deploy via Git

### 4. Vercel (Streamlit Support)
- Use Vercel's Python runtime
- Configure build settings for Streamlit

## 📊 Usage

1. **Start the application** and navigate to the main page
2. **Choose "Regulatory Repository"** to browse available regulations
3. **Choose "Gap Analyzer"** to perform analysis:
   - Upload your company document (.docx)
   - Select a regulatory framework
   - Click "GAP-Analyzer" to generate the report
   - Download the formatted Excel report

## 📁 Project Structure

```
Gap_Analyzer-main/
├── modules/
│   ├── model/
│   │   ├── open_source_llm.py      # Open source LLM and embeddings
│   │   └── bedrock.py              # Legacy AWS Bedrock (deprecated)
│   ├── embed_open_source.py        # Open source embeddings
│   ├── analyzer_open_source.py     # Main analysis logic
│   └── prompts/
│       └── gap_finder_prompt.py    # AI prompts for analysis
├── pages/
│   ├── gap_analyzer.py             # Main analysis page
│   └── regulatory_repo.py          # Regulatory repository page
├── Data/
│   └── Finma_EN/splitted/          # Regulatory data and embeddings
├── Results/                        # Generated reports
├── Rhizon.py                       # Main Streamlit app
├── generate_embeddings.py          # Script to generate embeddings
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose setup
└── requirements.txt                # Python dependencies
```

## 🔄 Migration from AWS Bedrock

This version replaces AWS Bedrock with open source alternatives:

- **Embeddings**: AWS Bedrock Titan → Sentence Transformers
- **LLM**: AWS Bedrock Claude → OpenAI API or Anthropic API
- **Cost**: Significantly reduced costs
- **Control**: Full control over models and data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Review the GitHub issues
3. Create a new issue with detailed information

## 🎯 Roadmap

- [ ] Support for more regulatory frameworks
- [ ] Multi-language document support
- [ ] Advanced reporting features
- [ ] API endpoints for integration
- [ ] Batch processing capabilities
