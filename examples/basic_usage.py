"""Example: Basic usage of Research Pilot components."""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from data_sources import ArxivClient, SemanticScholarClient
from parsers import PDFParser, SemanticChunker
from embeddings import EmbeddingEncoder


def example_search_arxiv():
    """Example: Search arXiv for papers."""
    print("\n=== Example 1: Search arXiv ===")

    client = ArxivClient()
    papers = client.search(
        query="attention mechanisms in vision transformers",
        max_results=5
    )

    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(paper.authors[:3])}")
        print(f"   Published: {paper.published.strftime('%Y-%m-%d')}")
        print(f"   Abstract: {paper.abstract[:200]}...")


def example_search_semantic_scholar():
    """Example: Search Semantic Scholar."""
    print("\n=== Example 2: Search Semantic Scholar ===")

    client = SemanticScholarClient()
    papers = client.search(
        query="transformers for NLP",
        limit=5,
        year="2023-2024"
    )

    print(f"\nFound {len(papers)} papers:")
    for i, paper in enumerate(papers, 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Citations: {paper.citation_count}")
        print(f"   Year: {paper.published.year}")


def example_pdf_parsing():
    """Example: Parse PDF file."""
    print("\n=== Example 3: PDF Parsing ===")

    # This requires a PDF file to exist
    pdf_path = Path("./data/papers/example.pdf")

    if not pdf_path.exists():
        print(f"\nSkipping: {pdf_path} does not exist")
        print("Download a paper first using ArxivClient.download_pdf()")
        return

    parser = PDFParser()
    text = parser.extract_text(pdf_path)

    print(f"\nExtracted {len(text)} characters")
    print(f"Preview: {text[:300]}...")


def example_text_chunking():
    """Example: Chunk text for embedding."""
    print("\n=== Example 4: Text Chunking ===")

    sample_text = """
    Transformers have revolutionized natural language processing. The attention
    mechanism allows models to weigh the importance of different words.

    Recent advances include vision transformers, which apply the same principles
    to image understanding. These models have achieved state-of-the-art results
    on various benchmarks.

    The key innovation is the self-attention mechanism, which computes attention
    weights between all pairs of tokens in the input sequence.
    """

    chunker = SemanticChunker(chunk_size=200, chunk_overlap=50)
    chunks = chunker.chunk_text(sample_text)

    print(f"\nCreated {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks, 1):
        print(f"\nChunk {i}:")
        print(f"  Text: {chunk['text'][:100]}...")
        print(f"  Length: {chunk['char_count']} chars, {chunk['word_count']} words")


def example_embeddings():
    """Example: Generate embeddings."""
    print("\n=== Example 5: Embedding Generation ===")

    encoder = EmbeddingEncoder()

    texts = [
        "Transformers use self-attention mechanisms",
        "Vision transformers apply attention to image patches",
        "BERT is a transformer-based language model"
    ]

    print("\nGenerating embeddings...")
    embeddings = encoder.encode(texts, show_progress=True)

    print(f"\nGenerated embeddings:")
    print(f"  Shape: {embeddings.shape}")
    print(f"  Dimension: {encoder.get_embedding_dim()}")

    # Show memory usage if GPU
    memory = encoder.get_memory_usage()
    if memory:
        print(f"\nGPU Memory:")
        print(f"  Allocated: {memory['allocated_gb']:.2f} GB")
        print(f"  Reserved: {memory['reserved_gb']:.2f} GB")


def main():
    """Run all examples."""
    print("=" * 60)
    print("Research Pilot - Basic Usage Examples")
    print("=" * 60)

    # Run examples
    example_search_arxiv()
    example_search_semantic_scholar()
    example_pdf_parsing()
    example_text_chunking()
    example_embeddings()

    print("\n" + "=" * 60)
    print("Examples complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
