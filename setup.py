from setuptools import setup, find_packages

setup(
    name="physics-utils",
    version="0.0.1",
    description="Helpers for physics data handling and plotting",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Jahan Rashidi",
    url="https://github.com/ImNotJahan/PhysicsTools",
    license="GPL-3.0-only",
    packages=find_packages(exclude=("tests", "docs", "labs", "examples")),
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.23",
        "matplotlib>=3.7",
        "pandas>=2.0",
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3.0 License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Source": "https://github.com/ImNotJahan/PhysicsTools",
        "Issues": "https://github.com/ImNotJahan/PhysicsTools/issues",
    },
)