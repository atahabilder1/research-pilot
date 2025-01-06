"""Text chunking strategies for document processing."""

import logging
from typing import List, Dict
import re

logger = logging.getLogger(__name__)


class SemanticChunker:
    """Chunk text semantically for better embedding quality."""

    def __init__(
        self,
        chunk_size: int = 512,
        chunk_overlap: int = 50,
        separators: List[str] = None,
    ):
        """Initialize chunker.

        Args:
            chunk_size: Target size for chunks (in characters)
            chunk_overlap: Overlap between chunks
            separators: List of separators for splitting (in priority order)
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.separators = separators or [
            "\n\n",  # Paragraph breaks
            "\n",    # Line breaks
            ". ",    # Sentences
            " ",     # Words
        ]

    def chunk_text(self, text: str, metadata: Dict = None) -> List[Dict]:
        """Chunk text into semantic units.

        Args:
            text: Text to chunk
            metadata: Optional metadata to attach to each chunk

        Returns:
            List of chunks with metadata
        """
        logger.info(f"Chunking text of length {len(text)}")

        chunks = []
        current_chunk = ""
        chunk_id = 0

        # Split by paragraphs first
        paragraphs = re.split(r'\n\n+', text)

        for paragraph in paragraphs:
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # If paragraph is too long, split it further
            if len(paragraph) > self.chunk_size:
                sub_chunks = self._split_long_text(paragraph)
                for sub_chunk in sub_chunks:
                    chunks.append(self._create_chunk(
                        sub_chunk,
                        chunk_id,
                        metadata
                    ))
                    chunk_id += 1
            else:
                # Try to combine with current chunk
                if len(current_chunk) + len(paragraph) <= self.chunk_size:
                    current_chunk += "\n\n" + paragraph if current_chunk else paragraph
                else:
                    # Save current chunk and start new one
                    if current_chunk:
                        chunks.append(self._create_chunk(
                            current_chunk,
                            chunk_id,
                            metadata
                        ))
                        chunk_id += 1

                    current_chunk = paragraph

        # Don't forget the last chunk
        if current_chunk:
            chunks.append(self._create_chunk(
                current_chunk,
                chunk_id,
                metadata
            ))

        logger.info(f"Created {len(chunks)} chunks")
        return chunks

    def _split_long_text(self, text: str) -> List[str]:
        """Split long text using separators.

        Args:
            text: Text to split

        Returns:
            List of text chunks
        """
        chunks = []
        remaining = text

        while len(remaining) > self.chunk_size:
            # Find best split point
            split_idx = self.chunk_size

            for separator in self.separators:
                # Look for separator near chunk boundary
                search_start = max(0, self.chunk_size - 100)
                search_end = min(len(remaining), self.chunk_size + 100)
                search_text = remaining[search_start:search_end]

                idx = search_text.rfind(separator)
                if idx != -1:
                    split_idx = search_start + idx + len(separator)
                    break

            # Extract chunk with overlap
            chunk = remaining[:split_idx].strip()
            if chunk:
                chunks.append(chunk)

            # Move to next chunk with overlap
            overlap_start = max(0, split_idx - self.chunk_overlap)
            remaining = remaining[overlap_start:]

        # Add final chunk
        if remaining.strip():
            chunks.append(remaining.strip())

        return chunks

    def _create_chunk(
        self,
        text: str,
        chunk_id: int,
        metadata: Dict = None
    ) -> Dict:
        """Create chunk dictionary.

        Args:
            text: Chunk text
            chunk_id: Chunk identifier
            metadata: Additional metadata

        Returns:
            Chunk dictionary
        """
        chunk = {
            "chunk_id": chunk_id,
            "text": text,
            "char_count": len(text),
            "word_count": len(text.split()),
        }

        if metadata:
            chunk.update(metadata)

        return chunk

    def chunk_by_sentences(self, text: str, sentences_per_chunk: int = 5) -> List[str]:
        """Chunk text by sentences.

        Args:
            text: Text to chunk
            sentences_per_chunk: Number of sentences per chunk

        Returns:
            List of text chunks
        """
        # Simple sentence splitting
        sentences = re.split(r'(?<=[.!?])\s+', text)
        chunks = []

        for i in range(0, len(sentences), sentences_per_chunk):
            chunk = " ".join(sentences[i:i + sentences_per_chunk])
            chunks.append(chunk)

        return chunks
