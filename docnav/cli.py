#!/usr/bin/env python3
"""
DocNav CLI Interface

Command-line interface for DocNav document management and querying system.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from .core import (
    Corpus, DocumentParser, SmartChunker, EmbeddingModel, LLMProvider,
    Colors, load_corpus
)
from .handlers import (
    handle_new, handle_add, handle_query, 
    handle_list, handle_stats, handle_remove, handle_clear, 
    handle_quick, handle_corpora, handle_info
)


def cli():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="DocNav: AI-powered document querying with citations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
{Colors.CYAN}Examples:{Colors.END}
  {Colors.CYAN}docnav new mydocs{Colors.END}
  {Colors.CYAN}docnav add mydocs documents/ --use-ocr{Colors.END}
  {Colors.CYAN}docnav query mydocs "What is refund policy?"{Colors.END}
  {Colors.CYAN}docnav query mydocs "Summarize this" --provider gemini --model gemini-2.5-pro{Colors.END}
  {Colors.CYAN}docnav list mydocs{Colors.END}
  {Colors.CYAN}docnav stats mydocs{Colors.END}
  {Colors.CYAN}docnav quick document.pdf "Summarize this"{Colors.END}
  {Colors.CYAN}docnav corpora{Colors.END}
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # New corpus command
    new_parser = subparsers.add_parser("new", help="Create a new corpus")
    new_parser.add_argument("corpus", help="Corpus name")
    new_parser.add_argument("--base-path", help="Base path for storage")
    
    # Add documents command
    add_parser = subparsers.add_parser("add", help="Add documents to corpus")
    add_parser.add_argument("corpus", help="Corpus name")
    add_parser.add_argument("paths", nargs="+", help="Files or directories to add")
    add_parser.add_argument("--use-ocr", action="store_true", help="Use OCR for scanned PDFs")
    add_parser.add_argument("--update", action="store_true", 
                          help="Update existing documents")
    add_parser.add_argument("--chunk-size", type=int, default=1000, 
                          help="Chunk size in tokens")
    add_parser.add_argument("--base-path", help="Base path for storage")
    
    # Query command
    query_parser = subparsers.add_parser("query", help="Query a corpus")
    query_parser.add_argument("corpus", help="Corpus name")
    query_parser.add_argument("question", help="Question to ask")
    query_parser.add_argument("--provider", default="openai", 
                           choices=["openai", "gemini", "claude"],
                           help="LLM provider")
    query_parser.add_argument("--model", help="Model name")
    query_parser.add_argument("--api-key", help="API key (overrides environment)")
    query_parser.add_argument("--top-k", type=int, default=5, 
                          help="Number of top results to consider")
    query_parser.add_argument("--base-path", help="Base path for storage")
    
    # List documents command
    list_parser = subparsers.add_parser("list", help="List documents in corpus")
    list_parser.add_argument("corpus", help="Corpus name")
    list_parser.add_argument("--details", action="store_true", 
                           help="Show detailed information")
    list_parser.add_argument("--base-path", help="Base path for storage")
    
    # Statistics command
    stats_parser = subparsers.add_parser("stats", help="Get corpus statistics")
    stats_parser.add_argument("corpus", help="Corpus name")
    stats_parser.add_argument("--base-path", help="Base path for storage")
    
    # Remove document command
    remove_parser = subparsers.add_parser("remove", help="Remove document from corpus")
    remove_parser.add_argument("corpus", help="Corpus name")
    remove_parser.add_argument("file", help="File to remove")
    remove_parser.add_argument("--base-path", help="Base path for storage")
    
    # Clear corpus command
    clear_parser = subparsers.add_parser("clear", help="Clear entire corpus")
    clear_parser.add_argument("corpus", help="Corpus name")
    clear_parser.add_argument("--force", action="store_true", 
                            help="Skip confirmation")
    clear_parser.add_argument("--base-path", help="Base path for storage")
    
    # Quick query command
    quick_parser = subparsers.add_parser("quick", help="Quickly ask a document")
    quick_parser.add_argument("file", help="Document file")
    quick_parser.add_argument("question", help="Question to ask")
    quick_parser.add_argument("--provider", default="openai", 
                           choices=["openai", "gemini", "claude"],
                           help="LLM provider")
    quick_parser.add_argument("--model", help="Model name")
    quick_parser.add_argument("--api-key", help="API key")
    quick_parser.add_argument("--use-ocr", action="store_true", 
                           help="Use OCR for scanned PDFs")
    
    # List corpora command
    corpora_parser = subparsers.add_parser("corpora", help="List all available corpora")
    
    # System info command
    info_parser = subparsers.add_parser("info", help="Show system information")
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Route to appropriate handler
    try:
        if args.command == "new":
            handle_new(args)
        elif args.command == "add":
            handle_add(args)
        elif args.command == "query":
            handle_query(args)
        elif args.command == "list":
            handle_list(args)
        elif args.command == "stats":
            handle_stats(args)
        elif args.command == "remove":
            handle_remove(args)
        elif args.command == "clear":
            handle_clear(args)
        elif args.command == "quick":
            handle_quick(args)
        elif args.command == "corpora":
            handle_corpora(args)
        elif args.command == "info":
            handle_info(args)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Operation cancelled by user{Colors.END}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.ERROR}Error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    cli()
