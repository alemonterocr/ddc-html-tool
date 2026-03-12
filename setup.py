"""Setup configuration for HTML Cleaning Toolkit"""

from setuptools import setup, find_packages

with open("docs/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ddc-html-tool",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Professional HTML cleaning utility with three specialized tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alemonterocr/ddc-html-tool",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
    python_requires=">=3.10",
    install_requires=[
        "rich>=14.3.0",
        "beautifulsoup4>=4.12.0",
    ],
    entry_points={
        "console_scripts": [
            "html-cleaner=main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["README.md", "QUICKSTART.md"],
    },
)
