"""Semantic Scholar API client for paper search and metadata."""

import logging
import time
from typing import List, Optional, Dict, Any
import requests
from tenacity import retry, stop_after_attempt, wait_exponential
import os

from .arxiv_client import Paper
from datetime import datetime

logger = logging.getLogger(__name__)


class SemanticScholarClient:
    """Client for Semantic Scholar API."""

    BASE_URL = "https://api.semanticscholar.org/graph/v1"

    def __init__(self, api_key: Optional[str] = None):
        """Initialize Semantic Scholar client.

        Args:
            api_key: Optional API key for higher rate limits
        """
        self.api_key = api_key or os.getenv("SEMANTIC_SCHOLAR_API_KEY")
        self.session = requests.Session()

        if self.api_key:
            self.session.headers.update({"x-api-key": self.api_key})

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def search(
        self,
        query: str,
        limit: int = 100,
        fields: Optional[List[str]] = None,
        year: Optional[str] = None,
        min_citation_count: Optional[int] = None,
    ) -> List[Paper]:
        """Search for papers on Semantic Scholar.

        Args:
            query: Search query
            limit: Maximum number of results
            fields: Fields to include in response
            year: Year filter (e.g., "2020-2024")
            min_citation_count: Minimum citation count filter

        Returns:
            List of Paper objects
        """
        logger.info(f"Searching Semantic Scholar for: {query}")

        if fields is None:
            fields = [
                "paperId",
                "title",
                "abstract",
                "year",
                "authors",
                "citationCount",
                "referenceCount",
                "influentialCitationCount",
                "publicationDate",
                "venue",
                "externalIds",
                "url",
                "openAccessPdf",
            ]

        params = {
            "query": query,
            "limit": min(limit, 100),  # API max is 100
            "fields": ",".join(fields),
        }

        if year:
            params["year"] = year
        if min_citation_count:
            params["minCitationCount"] = min_citation_count

        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/search",
                params=params,
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            papers = []
            for item in data.get("data", []):
                paper = self._convert_result(item)
                if paper:
                    papers.append(paper)

            logger.info(f"Found {len(papers)} papers on Semantic Scholar")
            return papers

        except requests.exceptions.RequestException as e:
            logger.error(f"Error searching Semantic Scholar: {e}")
            raise

    def _convert_result(self, result: Dict[str, Any]) -> Optional[Paper]:
        """Convert Semantic Scholar result to Paper object."""
        try:
            # Extract PDF URL if available
            pdf_url = None
            if result.get("openAccessPdf"):
                pdf_url = result["openAccessPdf"].get("url")

            # Get arXiv ID if available
            external_ids = result.get("externalIds", {})
            arxiv_id = external_ids.get("ArXiv")
            paper_id = arxiv_id if arxiv_id else result.get("paperId")

            # Parse publication date
            pub_date = result.get("publicationDate")
            if pub_date:
                try:
                    published = datetime.fromisoformat(pub_date)
                except:
                    published = datetime.now()
            else:
                year = result.get("year")
                published = datetime(year, 1, 1) if year else datetime.now()

            return Paper(
                id=paper_id,
                title=result.get("title", ""),
                authors=[
                    author.get("name", "")
                    for author in result.get("authors", [])
                ],
                abstract=result.get("abstract") or "",
                published=published,
                updated=published,
                pdf_url=pdf_url or "",
                categories=[result.get("venue", "")],
                primary_category=result.get("venue", ""),
                citation_count=result.get("citationCount", 0),
                doi=external_ids.get("DOI"),
                source="semantic_scholar",
            )
        except Exception as e:
            logger.warning(f"Error converting Semantic Scholar result: {e}")
            return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_paper_by_id(
        self,
        paper_id: str,
        fields: Optional[List[str]] = None,
    ) -> Optional[Paper]:
        """Get paper details by ID.

        Args:
            paper_id: Semantic Scholar paper ID or arXiv ID
            fields: Fields to include

        Returns:
            Paper object or None
        """
        if fields is None:
            fields = [
                "paperId",
                "title",
                "abstract",
                "year",
                "authors",
                "citationCount",
                "externalIds",
                "openAccessPdf",
            ]

        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/{paper_id}",
                params={"fields": ",".join(fields)},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return self._convert_result(data)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching paper {paper_id}: {e}")
            return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_citations(
        self,
        paper_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get papers citing this paper.

        Args:
            paper_id: Paper ID
            limit: Maximum number of citations

        Returns:
            List of citing papers
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/{paper_id}/citations",
                params={"limit": limit, "fields": "title,year,citationCount"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching citations for {paper_id}: {e}")
            return []

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
    )
    def get_references(
        self,
        paper_id: str,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Get papers referenced by this paper.

        Args:
            paper_id: Paper ID
            limit: Maximum number of references

        Returns:
            List of referenced papers
        """
        try:
            response = self.session.get(
                f"{self.BASE_URL}/paper/{paper_id}/references",
                params={"limit": limit, "fields": "title,year,citationCount"},
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            return data.get("data", [])

        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching references for {paper_id}: {e}")
            return []
