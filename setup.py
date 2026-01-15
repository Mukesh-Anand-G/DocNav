"""
Setup script for DocNav package
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "DocNav: AI-powered document querying with citations"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="docnav",
    version="1.0.1",
    author="Mukesh Anand G",
    author_email="mukesh@ailaysa.com",
    description="AI-powered document querying with citations",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ailaysa/docnav",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "full": [
            "sentence-transformers>=2.0.0",
            "python-docx>=0.8.11",
            "PyPDF2>=3.0.0",
            "pandas>=1.3.0",
            "python-pptx>=0.6.21",
            "openai>=1.0.0",
            "google-generativeai>=0.3.0",
            "anthropic>=0.8.0",
        ],
        "ocr": [
            "pdf2image>=1.16.0",
            "pytesseract>=0.3.10",
        ],
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.991",
        ]
    },
    entry_points={
        "console_scripts": [
            "docnav=docnav.cli:cli",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "document processing",
        "ai",
        "llm",
        "search",
        "query",
        "rag",
        "retrieval augmented generation",
        "document management",
        "text analysis",
        "citations",
        "openai",
        "gemini",
        "claude"
    ],
    project_urls={
        "Bug Reports": "https://github.com/ailaysa/docnav/issues",
        "Source": "https://github.com/ailaysa/docnav",
        "Documentation": "https://github.com/ailaysa/docnav/blob/main/README.md",
    },
)
