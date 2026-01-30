"""
Setup configuration for Codeflash
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="codeflash",
    version="0.1.0",
    author="Codeflash Team",
    author_email="alonewolfsupp@gmail.com",
    description="AI-Powered Python Performance Optimizer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Benhubbard9891/codeflash",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
    ],
    python_requires=">=3.8",
    install_requires=[
        "click>=8.0.0",
        "PyGithub>=1.55",
        "openai>=1.0.0",
        "ast-grep-py>=0.5.0",
        "gitpython>=3.1.0",
    ],
    entry_points={
        "console_scripts": [
            "codeflash=codeflash.cli:main",
        ],
    },
)
