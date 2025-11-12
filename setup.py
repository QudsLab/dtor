from setuptools import setup, find_packages

setup(
    name="dtor",
    version="0.1.0",
    description="A Tor process management library",
    author="Ahmad Yousuf",
    author_email="0xAhmadYousuf@protonmail.com",
    packages=find_packages(),
    install_requires=[
        "psutil",
    ],
    python_requires=">=3.6",
    url="https://github.com/0xAhmadYousuf/dtor",  # optional
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)