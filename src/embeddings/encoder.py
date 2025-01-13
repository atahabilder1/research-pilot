"""GPU-accelerated embedding generation."""

import logging
from typing import List, Union, Optional
import torch
from sentence_transformers import SentenceTransformer
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)


class EmbeddingEncoder:
    """Generate embeddings with GPU acceleration."""

    def __init__(
        self,
        model_name: str = "sentence-transformers/all-mpnet-base-v2",
        device: Optional[str] = None,
        batch_size: int = 128,
        use_fp16: bool = True,
    ):
        """Initialize embedding encoder.

        Args:
            model_name: Sentence transformer model name
            device: Device to use (cuda/cpu). Auto-detect if None
            batch_size: Batch size for encoding
            use_fp16: Use FP16 precision for faster encoding on GPU
        """
        self.model_name = model_name
        self.batch_size = batch_size
        self.use_fp16 = use_fp16

        # Auto-detect device
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = device

        logger.info(f"Loading model {model_name} on {device}")
        self.model = SentenceTransformer(model_name, device=device)

        # Enable FP16 on GPU for 2x speedup
        if self.device == "cuda" and use_fp16:
            self.model.half()
            logger.info("Enabled FP16 precision")

        # Enable TF32 for A6000 tensor cores
        if self.device == "cuda":
            torch.backends.cuda.matmul.allow_tf32 = True
            torch.backends.cudnn.allow_tf32 = True

        logger.info(f"Model loaded. Embedding dimension: {self.get_embedding_dim()}")

    def encode(
        self,
        texts: Union[str, List[str]],
        batch_size: Optional[int] = None,
        show_progress: bool = True,
        normalize: bool = True,
    ) -> np.ndarray:
        """Encode texts to embeddings.

        Args:
            texts: Single text or list of texts
            batch_size: Override default batch size
            show_progress: Show progress bar
            normalize: Normalize embeddings to unit length

        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]

        batch_size = batch_size or self.batch_size

        logger.info(f"Encoding {len(texts)} texts with batch size {batch_size}")

        try:
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress,
                convert_to_numpy=True,
                normalize_embeddings=normalize,
            )

            logger.info(f"Generated embeddings with shape {embeddings.shape}")
            return embeddings

        except Exception as e:
            logger.error(f"Error encoding texts: {e}")
            raise

    def encode_chunks(
        self,
        chunks: List[dict],
        text_key: str = "text",
        batch_size: Optional[int] = None,
    ) -> List[dict]:
        """Encode chunks and add embeddings to them.

        Args:
            chunks: List of chunk dictionaries
            text_key: Key containing text in chunk dict
            batch_size: Override default batch size

        Returns:
            Chunks with added 'embedding' field
        """
        texts = [chunk[text_key] for chunk in chunks]
        embeddings = self.encode(texts, batch_size=batch_size)

        for chunk, embedding in zip(chunks, embeddings):
            chunk["embedding"] = embedding.tolist()

        return chunks

    def get_embedding_dim(self) -> int:
        """Get embedding dimension.

        Returns:
            Embedding dimension
        """
        return self.model.get_sentence_embedding_dimension()

    def clear_cache(self):
        """Clear GPU memory cache."""
        if self.device == "cuda":
            torch.cuda.empty_cache()
            logger.info("Cleared GPU cache")

    def get_memory_usage(self) -> dict:
        """Get GPU memory usage stats.

        Returns:
            Dictionary with memory stats
        """
        if self.device != "cuda":
            return {}

        return {
            "allocated_gb": torch.cuda.memory_allocated() / 1e9,
            "reserved_gb": torch.cuda.memory_reserved() / 1e9,
            "max_allocated_gb": torch.cuda.max_memory_allocated() / 1e9,
        }
