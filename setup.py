from setuptools import setup, find_packages

from os import path

PROJECT_ROOT = path.abspath(path.dirname(__file__))

with open(path.join(PROJECT_ROOT, "README.md"), encoding="utf-8") as f:
    LONG_DESCRIPTION = f.read()

requires_extra = {}

requires_extra["all"] = [m for v in requires_extra.values() for m in v]

setup(
    name="rengu-utils-misc",
    version="6.0",
    description="Extra tools used with rengu",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://prajna.io",
    author="Thornton K. Prime",
    author_email="thornton.prime@gmail.com",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(),
    install_requires=[
        "rengu",
    ],
    extras_require=requires_extra,
    scripts=[
        "textflow",
        "list-source",
    ],
)
