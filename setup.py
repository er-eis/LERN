from setuptools import setup, find_packages

setup(
    name="LERN",
    version="0.1.0",
    author="er-eis",
    author_email="eeisenberg0@gmail.com",
    description="A short description of your project",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/er-eis/LERN",
    license="LICENSE",
    packages=find_packages(exclude=("tests", "docs", "venv")),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "your_script=main",
        ],
    },
)
