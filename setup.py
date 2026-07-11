from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="panel-editor",
    version="0.1.0",
    author="Greg",
    description="A visual panel editor built with Textual",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/panel-editor",
    packages=find_packages(),
    install_requires=[
        "textual>=0.1.0",
        "textual-dev>=1.0.0",
        "textual-web>=0.1.0",
        "pyperclip>=1.8.0",
        "munch>=2.5.0",
        "json5>=0.9.0",
        "pyinstaller>=6.0.0",
        "tree-sitter-python>=0.20.0",
        "tree-sitter-ruby>=0.20.0",
        "glslib @ git+https://github.com/devcybiko/glslib.git",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13",
)
