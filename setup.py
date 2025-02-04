from setuptools import setup, find_packages

setup(
    name="cryptobot",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "streamlit",
        "langchain",
        "openai",
        "chromadb",
        "python-dotenv",
        "pypdf",
        "requests",
        "beautifulsoup4"
    ]
) 