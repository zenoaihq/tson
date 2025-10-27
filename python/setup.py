"""
Setup script for TSON package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tson",
    version="1.0.0",
    author="Zeno AI",
    author_email="shubham@zenoai.tech",
    description="Token-efficient Structured Object Notation for LLMs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zenoaihq/tson",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.7",
    install_requires=[
        # No required dependencies for core functionality
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
        ],
    },
    keywords="serialization, json, llm, tokens, efficiency, data-format, tson",
    project_urls={
        "Bug Reports": "https://github.com/zenoaihq/tson/issues",
        "Source": "https://github.com/zenoaihq/tson",
        "Documentation": "https://github.com/zenoaihq/tson/blob/main/SPEC.md",
    },
)
