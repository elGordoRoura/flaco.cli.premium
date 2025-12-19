from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="flaco-ai-premium",
    version="1.0.0",
    author="Roura.io",
    description="Flaco Premium - Advanced Local AI Coding Assistant powered by Ollama",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/RouraIO/flaco.cli.premium",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "rich>=13.7.0",
        "prompt_toolkit>=3.0.43",
        "pygments>=2.17.0",
        "gitpython>=3.1.40",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0.1",
        "click>=8.1.7",
        "aiohttp>=3.9.1",
        "pillow>=10.1.0",
        "pydantic>=2.5.0",
        "watchdog>=3.0.0",
    ],
    entry_points={
        "console_scripts": [
            "flaco-premium=flaco.cli:main",
            "flacopro=flaco.cli:main",  # Short alias
        ],
    },
)
