# Research Pilot

> An AI research assistant that helps you discover, analyze, and synthesize academic papers faster.

Research Pilot automates the tedious parts of literature review. Point it at a research question, and it searches multiple databases, processes papers, and helps you understand what's been done in your field.

## What it does

- **Multi-source search**: Finds papers from arXiv and Semantic Scholar based on your query
- **Smart filtering**: Ranks papers by relevance and citation count
- **PDF processing**: Extracts and chunks text for analysis
- **GPU acceleration**: Uses your NVIDIA GPU to generate embeddings quickly
- **Web interface**: Clean Streamlit UI for searching and browsing papers

## Quick Start

```bash
# Clone and install
git clone https://github.com/yourusername/research-pilot.git
cd research-pilot
pip install -r requirements.txt

# Run the web app
streamlit run app.py
```

Open `http://localhost:8501` and start searching!

## Example Usage

**Python API:**

```python
from src.data_sources import ArxivClient

client = ArxivClient()
papers = client.search("attention mechanisms", max_results=10)

for paper in papers:
    print(f"{paper.title} - {paper.citation_count} citations")
```

**Web Interface:**

<img src="https://via.placeholder.com/800x400?text=Screenshot+Coming+Soon" width="100%" alt="Research Pilot Screenshot">

Just type your research question and hit search. The app finds relevant papers and shows you titles, abstracts, and citation counts.

## How It Works

1. **Search**: Queries arXiv and Semantic Scholar APIs simultaneously
2. **Filter**: Ranks results by relevance and removes duplicates
3. **Process**: Downloads PDFs and extracts text using PyMuPDF
4. **Embed**: Generates vector embeddings on GPU (5000+ docs/sec on A6000)
5. **Display**: Shows results in an easy-to-browse interface

## Requirements

- Python 3.10+
- NVIDIA GPU with CUDA support (optional but recommended)
- 8GB+ RAM
- Internet connection for API access

## Tech Stack

- **Search APIs**: arXiv, Semantic Scholar
- **ML**: PyTorch + sentence-transformers
- **Frontend**: Streamlit
- **PDF**: PyMuPDF
- **GPU**: CUDA 11.8+

## Project Structure

```
research-pilot/
├── app.py                  # Streamlit web interface
├── src/
│   ├── data_sources/       # arXiv and Semantic Scholar clients
│   ├── parsers/            # PDF text extraction
│   ├── embeddings/         # GPU-accelerated embedding generation
│   └── ...
├── examples/               # Usage examples
├── docs/                   # Additional documentation
└── configs/                # Configuration files
```

## Configuration

Copy `.env.example` to `.env` and add your API keys:

```bash
# Optional: for higher rate limits
SEMANTIC_SCHOLAR_API_KEY=your_key_here

# For future LLM features
ANTHROPIC_API_KEY=your_claude_key
OPENAI_API_KEY=your_openai_key
```

## Development Status

**Working:**
- ✅ Multi-source paper search
- ✅ PDF text extraction
- ✅ GPU-accelerated embeddings
- ✅ Web interface

**In Progress:**
- 🚧 Vector database integration
- 🚧 RAG-based paper synthesis
- 🚧 Citation graph visualization

**Planned:**
- 📋 Automated literature reviews
- 📋 Export to Zotero/Mendeley
- 📋 Email digests for new papers

## Performance

On an NVIDIA A6000 (48GB):
- Embedding generation: 5000-7000 chunks/sec
- Paper search: 2-5 seconds
- Full research cycle: 5-10 minutes for 20 papers

CPU mode also works but is slower (200-500 chunks/sec).

## Limitations

- Only searches arXiv and Semantic Scholar (PubMed coming soon)
- English papers only for now
- Requires internet connection for search
- GPU recommended for large-scale embedding generation

## Contributing

Found a bug or have a feature idea? Open an issue on GitHub.

Pull requests welcome, especially for:
- Adding new paper sources (PubMed, CORE, etc.)
- Improving PDF parsing accuracy
- Better relevance ranking algorithms

## License

MIT License - feel free to use this for your own research.

## Author

Built by Anik Tahabilder | January-May 2024

This started as a side project to speed up my own lit reviews. Hope it helps you too!

## Acknowledgments

- [arXiv](https://arxiv.org/) for the open access API
- [Semantic Scholar](https://www.semanticscholar.org/) for paper metadata
- [Hugging Face](https://huggingface.co/) for transformer models
