from setuptools import setup, find_packages

setup(
    name="mkdocs-fp-book",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["mkdocs"],
    entry_points={
        "mkdocs.plugins": [
            "fp_book = mkdocs_fp_book.plugin:FPBookPlugin"
        ]
    },
)