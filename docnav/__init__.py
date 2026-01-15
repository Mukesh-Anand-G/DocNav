"""
DocNav: AI-powered document querying with citations

A professional document management and querying system that supports multiple file formats,
intelligent chunking, and LLM-powered question answering with source citations.
"""

__version__ = "1.0.1"
__author__ = "Mukesh Anand G"
__email__ = "mukesh@ailaysa.com"
__description__ = "AI-powered document querying with citations"

from .core import Corpus, DocumentChunk, DocumentParser, SmartChunker, EmbeddingModel, LLMProvider
from .cli import cli

__all__ = [
    'Corpus',
    'DocumentChunk', 
    'DocumentParser',
    'SmartChunker',
    'EmbeddingModel',
    'LLMProvider',
    'cli',
    '__version__'
]
