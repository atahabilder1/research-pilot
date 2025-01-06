"""PDF parsing and text extraction."""

import logging
from pathlib import Path
from typing import Optional, Dict, List
import fitz  # PyMuPDF
import re

logger = logging.getLogger(__name__)


class PDFParser:
    """Parse and extract text from PDF files."""

    def __init__(self):
        """Initialize PDF parser."""
        pass

    def extract_text(self, pdf_path: Path) -> str:
        """Extract all text from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text
        """
        logger.info(f"Extracting text from: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)
            text = ""

            for page_num in range(len(doc)):
                page = doc[page_num]
                text += page.get_text()

            doc.close()

            # Clean up text
            text = self._clean_text(text)

            logger.info(
                f"Extracted {len(text)} characters from {len(doc)} pages"
            )
            return text

        except Exception as e:
            logger.error(f"Error extracting text from {pdf_path}: {e}")
            raise

    def extract_with_metadata(self, pdf_path: Path) -> Dict:
        """Extract text and metadata from PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with text, metadata, and page information
        """
        logger.info(f"Extracting text and metadata from: {pdf_path}")

        try:
            doc = fitz.open(pdf_path)

            # Extract metadata
            metadata = doc.metadata
            pages_text = []

            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = page.get_text()
                pages_text.append({
                    "page_number": page_num + 1,
                    "text": self._clean_text(page_text),
                })

            doc.close()

            return {
                "metadata": metadata,
                "total_pages": len(doc),
                "pages": pages_text,
                "full_text": "\n\n".join([p["text"] for p in pages_text]),
            }

        except Exception as e:
            logger.error(f"Error extracting from {pdf_path}: {e}")
            raise

    def extract_sections(self, pdf_path: Path) -> List[Dict]:
        """Extract text organized by sections (heuristic-based).

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of sections with titles and content
        """
        text = self.extract_text(pdf_path)
        sections = []

        # Simple heuristic: lines that are all caps or numbered
        section_pattern = re.compile(
            r"^(?:\d+\.?\s+)?([A-Z][A-Z\s]{3,50})$", re.MULTILINE
        )

        matches = list(section_pattern.finditer(text))

        for i, match in enumerate(matches):
            title = match.group(1).strip()
            start = match.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            content = text[start:end].strip()

            sections.append({
                "title": title,
                "content": content,
                "start_pos": start,
                "end_pos": end,
            })

        # If no sections found, treat entire text as one section
        if not sections:
            sections = [{
                "title": "Full Text",
                "content": text,
                "start_pos": 0,
                "end_pos": len(text),
            }]

        logger.info(f"Extracted {len(sections)} sections")
        return sections

    def _clean_text(self, text: str) -> str:
        """Clean extracted text.

        Args:
            text: Raw text

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove page numbers (simple heuristic)
        text = re.sub(r'\n\d+\n', '\n', text)

        # Fix common OCR issues
        text = text.replace('ﬁ', 'fi')
        text = text.replace('ﬂ', 'fl')

        return text.strip()

    def get_page_count(self, pdf_path: Path) -> int:
        """Get number of pages in PDF.

        Args:
            pdf_path: Path to PDF file

        Returns:
            Number of pages
        """
        try:
            doc = fitz.open(pdf_path)
            count = len(doc)
            doc.close()
            return count
        except Exception as e:
            logger.error(f"Error getting page count for {pdf_path}: {e}")
            return 0
