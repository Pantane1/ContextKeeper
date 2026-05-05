from setuptools import setup, find_packages

setup(
    name="ContextKeeper",
    version="1.0.0",
    author="Pantane1",
    author_email="your.email@example.com",
    description="Smart clipboard manager that automatically groups copied items into contextual sessions",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Pantane1/ContextKeeper",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pyperclip",
    ],
    entry_points={
        "console_scripts": [
            "contextkeeper=main:main",
        ],
    },
)