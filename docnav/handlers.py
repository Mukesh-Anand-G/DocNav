"""
DocNav CLI Handlers

Handler functions for various CLI commands.
"""

import os
import sys
from pathlib import Path
from typing import Optional
import pickle
import numpy as np
from datetime import datetime

from .core import (
    Corpus, DocumentParser, SmartChunker, EmbeddingModel, LLMProvider,
    Colors, load_corpus
)


def handle_new(args):
    """Handle new corpus creation."""
    corpus = Corpus(name=args.corpus, base_path=args.base_path if hasattr(args, 'base_path') else None)
    print(Colors.success(f"✅ Corpus created successfully!"))
    print(f"   To add documents: {Colors.CYAN}docnav add {args.corpus} <files_or_folders>{Colors.END}")


def handle_add(args):
    """Handle adding documents to corpus."""
    corpus = load_corpus(args.corpus, args.base_path if hasattr(args, 'base_path') else None)
    
    added = corpus.add(
        args.paths,
        use_ocr=args.use_ocr,
        update_existing=args.update,
        chunk_size=args.chunk_size
    )
    
    if added > 0:
        print(Colors.success(f"✅ Added {added} chunks to corpus"))
    else:
        print(Colors.warning("⚠️ No new chunks added"))


def handle_query(args):
    """Handle querying corpus."""
    corpus = load_corpus(args.corpus, args.base_path if hasattr(args, 'base_path') else None)
    results = corpus.ask(
        args.question,
        llm_provider=args.provider,
        llm_model=args.model,
        api_key=args.api_key,
        top_k=args.top_k
    )
    
    if not results:
        print(Colors.warning("No relevant documents found."))
        return
    
    print(f"\n{Colors.BOLD}{Colors.BLUE}ANSWER:{Colors.END}")
    print(results.text)
    
    print(f"\n{Colors.BOLD}Details:{Colors.END}")
    print(f"  Confidence: {results.confidence:.1f}%")
    print(f"  Model: {results.model_used}")
    print(f"  Time: {results.processing_time:.2f}s")
    print(f"  Sources: {len(results.sources)}")
    
    if results.sources:
        print(f"\n{Colors.BOLD}Sources:{Colors.END}")
        for i, source in enumerate(results.sources, 1):
            print(f"  {i}. {Colors.CYAN}{source.metadata.get('file_name', 'Unknown')}{Colors.END} [{source.metadata.get('type', 'unknown').upper()}]")
            print(f"     {source.text[:200]}...")


def handle_list(args):
    """Handle listing documents in corpus."""
    corpus = load_corpus(args.corpus, args.base_path if hasattr(args, 'base_path') else None)
    documents = corpus.list()
    
    if not documents:
        print(Colors.warning("No documents in corpus"))
        return
    
    print(f"\n{Colors.info(f'Documents in corpus ({len(documents)}):')}")
    print("-" * 80)
    
    for i, doc in enumerate(documents, 1):
        print(f"{Colors.CYAN}{i:3}. {doc['file_name']}{Colors.END}")
        print(f"     Type: {doc.get('type', 'unknown')}")
        print(f"     Chunks: {doc['chunks']}")
        print(f"     Size: {doc.get('size', 0) / 1024:.1f} KB")
        print(f"     Path: {doc.get('file_path', 'N/A')[:60]}...")
        
        if args.details:
            print(f"     Processed: {doc.get('processed_at', 'N/A')[:19]}")
        
        print()


def handle_stats(args):
    """Handle showing corpus statistics."""
    corpus = load_corpus(args.corpus, args.base_path if hasattr(args, 'base_path') else None)
    stats = corpus.stats()
    
    print(f"\n{Colors.info('Corpus Statistics:')}")
    print("-" * 40)
    print(f"Name                : {stats['name']}")
    print(f"Total Chunks        : {stats['total_chunks']}")
    print(f"Total Documents     : {stats['total_documents']}")
    print(f"Total Size          : {stats['total_size_mb']:.2f} MB")
    print(f"Embedding Model     : {stats['embedding_model']}")
    print(f"Chunk Size          : {stats['chunk_size']}")
    print(f"Corpus Path         : {stats['corpus_path']}")


def handle_remove(args):
    """Handle removing document from corpus."""
    corpus = load_corpus(args.corpus, args.base_path if hasattr(args, 'base_path') else None)
    corpus.remove(args.file)


def handle_clear(args):
    """Handle clearing entire corpus."""
    corpus = load_corpus(args.corpus, args.base_path if hasattr(args, 'base_path') else None)
    corpus.clear(force=args.force)


def handle_quick(args):
    """Handle quick document query."""
    if not os.path.exists(args.file):
        print(Colors.error(f"File not found: {args.file}"))
        return
    
    print(f"{Colors.info('Processing document...')}")
    
    # Parse document
    parser = DocumentParser()
    chunks = parser.parse_file(args.file, use_ocr=args.use_ocr)
    
    if not chunks:
        print(Colors.error("Failed to parse document"))
        return
    
    # Chunk if needed
    chunker = SmartChunker()
    all_chunks = []
    for chunk in chunks:
        sub_chunks = chunker.chunk_text(chunk.text, chunk.metadata)
        all_chunks.extend(sub_chunks)
    
    # Create temporary corpus
    temp_corpus = Corpus("__temp__")
    temp_corpus.chunks = all_chunks
    
    # Query
    results = temp_corpus.query(
        args.question,
        provider=args.provider,
        model=args.model,
        api_key=args.api_key
    )
    
    if results:
        print(f"\n{Colors.BOLD}{Colors.BLUE}ANSWER:{Colors.END}")
        print(results['answer'])
    else:
        print(Colors.warning("No relevant information found."))


def handle_corpora(args):
    """Handle listing all corpora."""
    base_path = Path.home() / ".docnav" / "corpora"
    
    if not base_path.exists():
        print(Colors.info("No corpora found. Create one with 'docnav new <name>'"))
        return
    
    corpora = [d.name for d in base_path.iterdir() if d.is_dir()]
    
    if not corpora:
        print(Colors.info("No corpora found. Create one with 'docnav new <name>'"))
        return
    
    print(f"\n{Colors.info(f'Available Corpora ({len(corpora)}):')}")
    print("-" * 40)
    
    for corpus_name in sorted(corpora):
        corpus_path = base_path / corpus_name
        index_file = corpus_path / "corpus_index.pkl"
        
        if index_file.exists():
            try:
                with open(index_file, 'rb') as f:
                    chunks = pickle.load(f)
                docs = len(set(chunk.metadata.get('file_path') for chunk in chunks))
                print(f"  {Colors.CYAN}{corpus_name}{Colors.END} - {docs} documents, {len(chunks)} chunks")
            except:
                print(f"  {Colors.CYAN}{corpus_name}{Colors.END} - (corrupted)")
        else:
            print(f"  {Colors.CYAN}{corpus_name}{Colors.END} - (empty)")


def handle_info(args):
    """Handle showing system information."""
    print(f"\n{Colors.info('DocNav System Information:')}")
    print("-" * 40)
    print(f"Version             : 1.0.0")
    print(f"Python Version      : {sys.version.split()[0]}")
    print(f"Platform           : {sys.platform}")
    
    # Check optional dependencies
    deps = {
        'sentence-transformers': False,
        'python-docx': False,
        'PyPDF2': False,
        'pandas': False,
        'python-pptx': False,
        'openai': False,
        'google-generativeai': False,
        'anthropic': False
    }
    
    for dep in deps:
        try:
            __import__(dep.replace('-', '_'))
            deps[dep] = True
        except ImportError:
            pass
    
    print(f"\n{Colors.info('Optional Dependencies:')}")
    for dep, installed in deps.items():
        status = "✅" if installed else "❌"
        print(f"  {status} {dep}")
    
    print(f"\n{Colors.info('Storage:')}")
    docnav_path = Path.home() / ".docnav"
    print(f"  Base Path: {docnav_path}")
    print(f"  Exists: {'Yes' if docnav_path.exists() else 'No'}")
    
    if docnav_path.exists():
        corpora_path = docnav_path / "corpora"
        if corpora_path.exists():
            corpora_count = len([d for d in corpora_path.iterdir() if d.is_dir()])
            print(f"  Corpora: {corpora_count}")
        else:
            print(f"  Corpora: 0")
