"""arXiv API client for searching and downloading papers."""

import logging
from typing import List, Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime
import arxiv
from pathlib import Path

logger = logging.getLogger(__name__)


@dataclass
class Paper:
    """Represents a research paper."""

    id: str
    title: str
    authors: List[str]
    abstract: str
    published: datetime
    updated: datetime
    pdf_url: str
    categories: List[str]
    primary_category: str
    comment: Optional[str] = None
    journal_ref: Optional[str] = None
    doi: Optional[str] = None
    citation_count: int = 0
    source: str = "arxiv"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "abstract": self.abstract,
            "published": self.published.isoformat(),
            "updated": self.updated.isoformat(),
            "pdf_url": self.pdf_url,
            "categories": self.categories,
            "primary_category": self.primary_category,
            "comment": self.comment,
            "journal_ref": self.journal_ref,
            "doi": self.doi,
            "citation_count": self.citation_count,
            "source": self.source,
        }


class ArxivClient:
    """Client for interacting with arXiv API."""

    def __init__(self, max_results: int = 100):
        """Initialize arXiv client.

        Args:
            max_results: Maximum number of results per query
        """
        self.max_results = max_results
        self.client = arxiv.Client()

    def search(
        self,
        query: str,
        max_results: Optional[int] = None,
        sort_by: arxiv.SortCriterion = arxiv.SortCriterion.Relevance,
        sort_order: arxiv.SortOrder = arxiv.SortOrder.Descending,
    ) -> List[Paper]:
        """Search arXiv for papers.

        Args:
            query: Search query
            max_results: Override default max results
            sort_by: Sort criterion
            sort_order: Sort order

        Returns:
            List of Paper objects
        """
        logger.info(f"Searching arXiv for: {query}")

        max_results = max_results or self.max_results

        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=sort_by,
            sort_order=sort_order,
        )

        papers = []
        try:
            for result in self.client.results(search):
                paper = self._convert_result(result)
                papers.append(paper)
        except Exception as e:
            logger.error(f"Error searching arXiv: {e}")
            raise

        logger.info(f"Found {len(papers)} papers on arXiv")
        return papers

    def _convert_result(self, result: arxiv.Result) -> Paper:
        """Convert arxiv.Result to Paper object."""
        return Paper(
            id=result.entry_id.split("/")[-1],
            title=result.title,
            authors=[author.name for author in result.authors],
            abstract=result.summary,
            published=result.published,
            updated=result.updated,
            pdf_url=result.pdf_url,
            categories=result.categories,
            primary_category=result.primary_category,
            comment=result.comment,
            journal_ref=result.journal_ref,
            doi=result.doi,
        )

    def download_pdf(self, paper: Paper, output_dir: Path) -> Path:
        """Download PDF for a paper.

        Args:
            paper: Paper object
            output_dir: Directory to save PDF

        Returns:
            Path to downloaded PDF
        """
        output_dir.mkdir(parents=True, exist_ok=True)

        # Sanitize filename
        filename = f"{paper.id.replace('/', '_')}.pdf"
        output_path = output_dir / filename

        if output_path.exists():
            logger.info(f"PDF already exists: {output_path}")
            return output_path

        logger.info(f"Downloading PDF: {paper.title}")

        try:
            # Find the paper and download
            search = arxiv.Search(id_list=[paper.id])
            result = next(self.client.results(search))
            result.download_pdf(dirpath=str(output_dir), filename=filename)
            logger.info(f"Downloaded PDF to: {output_path}")
            return output_path
        except Exception as e:
            logger.error(f"Error downloading PDF for {paper.id}: {e}")
            raise

    def get_paper_by_id(self, arxiv_id: str) -> Optional[Paper]:
        """Get a single paper by arXiv ID.

        Args:
            arxiv_id: arXiv paper ID

        Returns:
            Paper object or None if not found
        """
        logger.info(f"Fetching paper: {arxiv_id}")

        try:
            search = arxiv.Search(id_list=[arxiv_id])
            result = next(self.client.results(search))
            return self._convert_result(result)
        except StopIteration:
            logger.warning(f"Paper not found: {arxiv_id}")
            return None
        except Exception as e:
            logger.error(f"Error fetching paper {arxiv_id}: {e}")
            raise
