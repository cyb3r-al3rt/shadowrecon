#!/usr/bin/env python3
"""
Setup script for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios
"""

from setuptools import setup, find_packages
import os

# Read the README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    requirements = []
    try:
        with open("requirements.txt", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "extra ==" not in line:
                    requirements.append(line.split(";")[0].strip())
    except FileNotFoundError:
        pass
    return requirements

setup(
    name="shadowrecon",
    version="1.0.0",
    author="kernelpanic | A product of infosbios",
    author_email="contact@infosbios.com",
    description="Ultimate Web Attack Surface Discovery Framework",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/infosbios/shadowrecon",
    project_urls={
        "Bug Reports": "https://github.com/infosbios/shadowrecon/issues",
        "Source": "https://github.com/infosbios/shadowrecon",
        "Documentation": "https://github.com/infosbios/shadowrecon/wiki",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: System :: Networking :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9", 
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "full": [
            "pyOpenSSL>=22.0.0",
            "dns-lexicon>=3.8.0",
        ],
        "screenshots": [
            "selenium>=4.0.0",
            "webdriver-manager>=3.8.0",
        ],
        "database": [
            "sqlalchemy>=1.4.0",
        ],
        "dev": [
            "pytest>=6.2.0",
            "pytest-asyncio>=0.18.0",
            "pytest-cov>=2.12.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "bandit>=1.7.0",
            "safety>=2.0.0",
            "pre-commit>=2.15.0",
        ],
        "docs": [
            "sphinx>=4.5.0",
            "sphinx-rtd-theme>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "shadowrecon=shadowrecon:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords="security, penetration-testing, reconnaissance, bug-bounty, vulnerability-scanner, ctf, web-security",
    license="MIT",
)
