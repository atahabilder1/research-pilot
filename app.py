"""Research Pilot - Streamlit Web Interface."""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_sources import ArxivClient, SemanticScholarClient
from parsers import PDFParser
from embeddings import EmbeddingEncoder

st.set_page_config(
    page_title="Research Pilot",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
.main-header {
    font-size: 3rem;
    font-weight: bold;
    text-align: center;
    margin-bottom: 2rem;
}
.stButton>button {
    width: 100%;
}
</style>
""", unsafe_allow_html=True)


def main():
    """Main application."""

    # Header
    st.markdown('<h1 class="main-header">🔬 Research Pilot</h1>', unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align: center; font-size: 1.2rem;'>"
        "AI-powered research assistant for academic paper discovery and analysis"
        "</p>",
        unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")

        source = st.selectbox(
            "Data Source",
            ["arXiv", "Semantic Scholar", "Both"],
            index=0
        )

        max_results = st.slider(
            "Max Papers",
            min_value=5,
            max_value=50,
            value=10,
            step=5
        )

        st.divider()

        st.header("📊 System Info")
        try:
            import torch
            if torch.cuda.is_available():
                st.success(f"✅ GPU: {torch.cuda.get_device_name(0)}")
                st.info(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
            else:
                st.warning("⚠️ No GPU detected (using CPU)")
        except:
            st.warning("⚠️ PyTorch not available")

    # Main content
    tab1, tab2, tab3 = st.tabs(["🔍 Search", "📚 Library", "ℹ️ About"])

    with tab1:
        st.header("Search Research Papers")

        query = st.text_area(
            "What would you like to research?",
            placeholder="Example: Recent advances in transformer architectures for computer vision",
            height=100
        )

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            search_button = st.button("🔍 Search Papers", type="primary")

        with col2:
            example_button = st.button("Try Example")

        if example_button:
            query = "Attention mechanisms in vision transformers"
            st.rerun()

        if search_button and query:
            with st.spinner("Searching for papers..."):
                try:
                    papers = []

                    if source in ["arXiv", "Both"]:
                        arxiv_client = ArxivClient()
                        arxiv_papers = arxiv_client.search(query, max_results=max_results//2 if source == "Both" else max_results)
                        papers.extend(arxiv_papers)
                        st.success(f"Found {len(arxiv_papers)} papers on arXiv")

                    if source in ["Semantic Scholar", "Both"]:
                        try:
                            s2_client = SemanticScholarClient()
                            s2_papers = s2_client.search(query, limit=max_results//2 if source == "Both" else max_results)
                            papers.extend(s2_papers)
                            st.success(f"Found {len(s2_papers)} papers on Semantic Scholar")
                        except Exception as e:
                            st.warning(f"Semantic Scholar search failed: {e}")

                    if papers:
                        st.subheader(f"📝 Found {len(papers)} Papers")

                        for i, paper in enumerate(papers[:max_results]):
                            with st.expander(f"{i+1}. {paper.title}"):
                                st.markdown(f"**Authors:** {', '.join(paper.authors[:5])}{' et al.' if len(paper.authors) > 5 else ''}")
                                st.markdown(f"**Published:** {paper.published.strftime('%Y-%m-%d')}")
                                st.markdown(f"**Source:** {paper.source}")
                                if paper.citation_count > 0:
                                    st.markdown(f"**Citations:** {paper.citation_count}")

                                st.markdown("**Abstract:**")
                                st.write(paper.abstract[:500] + "..." if len(paper.abstract) > 500 else paper.abstract)

                                col_pdf, col_cite = st.columns(2)
                                with col_pdf:
                                    if paper.pdf_url:
                                        st.markdown(f"[📄 PDF]({paper.pdf_url})")
                                with col_cite:
                                    st.markdown(f"[🔗 Details](https://arxiv.org/abs/{paper.id})")

                    else:
                        st.warning("No papers found. Try a different query.")

                except Exception as e:
                    st.error(f"Error searching papers: {e}")

    with tab2:
        st.header("📚 Paper Library")
        st.info("Coming soon: Manage your saved papers and collections")

        st.markdown("""
        **Planned features:**
        - Save papers to collections
        - Generate literature reviews
        - Citation graph visualization
        - Export to BibTeX/Markdown
        """)

    with tab3:
        st.header("About Research Pilot")

        st.markdown("""
        **Research Pilot** is an AI-powered research assistant that automates academic research workflows.

        ### Features
        - 🔍 Multi-source paper search (arXiv, Semantic Scholar)
        - 📄 PDF processing and text extraction
        - 🧠 GPU-accelerated embedding generation
        - 🤖 LangGraph-based agentic workflows (coming soon)
        - 📊 Citation network visualization (coming soon)
        - 📝 Automated literature reviews (coming soon)

        ### Technology Stack
        - **Frontend:** Streamlit
        - **ML:** PyTorch, sentence-transformers
        - **APIs:** arXiv, Semantic Scholar
        - **Vector DB:** Qdrant (planned)
        - **LLM:** Claude/OpenAI APIs (planned)

        ### GPU Acceleration
        This application is optimized for NVIDIA GPUs with CUDA support.
        """)

        st.divider()

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Author:** Anik Tahabilder")
            st.markdown("**Version:** 0.1.0 (MVP)")
        with col2:
            st.markdown("[📖 Documentation](docs/README.md)")
            st.markdown("[🐙 GitHub](https://github.com/yourusername/research-pilot)")


if __name__ == "__main__":
    main()
