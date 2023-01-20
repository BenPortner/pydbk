from distutils.core import setup

setup(
    name="pydbk",
    version="0.1.1",
    description="A Python tool to extract .dbk archives.",
    long_description=open('README.md', encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Benjamin W. Portner",
    author_email="benwportner@gmail.com",
    url="https://github.com/BenPortner/pydbk",
    packages=["pydbk"],
    install_requires=[],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers"
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
    ],
    license="License :: OSI Approved :: GNU Affero General Public License v3",
)
