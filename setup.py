#!/usr/bin/env python3
"""
Setup script for crunpyroll package.
Provides fallback configuration for environments where pyproject.toml is not fully supported.
"""

import sys
from setuptools import setup, find_packages

# Ensure we have a compatible setuptools version
try:
    from setuptools import __version__ as setuptools_version
    major, minor = map(int, setuptools_version.split('.')[:2])
    if major < 61:
        print("Warning: setuptools >= 61.0 is recommended for best compatibility")
except (ImportError, ValueError, AttributeError):
    pass

# Read README for long description
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except (FileNotFoundError, UnicodeDecodeError):
    long_description = "Async API wrapper for Crunchyroll"

# Fallback setup configuration
setup(
    name="crunpyroll",
    version="2.4.8.3",
    author="stefanodvx",
    author_email="pp.stefanodvx@gmail.com",
    description="Async API wrapper for Crunchyroll",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pixel-LH/crunpyroll",
    project_urls={
        "Homepage": "https://github.com/Pixel-LH/crunpyroll",
        "Repository": "https://github.com/Pixel-LH/crunpyroll.git",
        "Documentation": "https://crunpyroll.readthedocs.io/",
        "Bug Tracker": "https://github.com/Pixel-LH/crunpyroll/issues",
    },
    packages=find_packages(include=["crunpyroll", "crunpyroll.*"]),
    package_data={
        "crunpyroll": ["py.typed"],
    },
    include_package_data=True,
    install_requires=[
        "httpx",
        "xmltodict",
    ],
    extras_require={
        "docs": [
            "sphinx",
            "furo",
            "pygments",
            "sphinx_copybutton",
            "sphinx-autobuild",
        ],
        "dev": [
            "pytest",
            "pytest-asyncio",
            "black",
            "isort",
            "flake8",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Multimedia :: Video",
        "Framework :: AsyncIO",
    ],
    keywords="crunchyroll api async wrapper anime streaming",
    license="MIT",
    zip_safe=False,
)
