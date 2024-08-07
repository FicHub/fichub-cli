from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='fichub-cli',
    author='Arbaaz Laskar',
    author_email="arzkar.dev@gmail.com",
    description="A CLI for the fichub.net API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="0.10.3",
    license='Apache License',
    url="https://github.com/FicHub/fichub-cli",
    packages=find_packages(include=['fichub_cli', 'fichub_cli.*']),
    include_package_data=True,
    install_requires=[
        'typer>=0.4.0',
        'requests>=2.31.0',
        'loguru>=0.6.0',
        'tqdm>=4.60.0',
        'BeautifulSoup4>=4.9.3',
        'colorama>=0.4.4',
        'platformdirs>=2.5.1'
    ],
    entry_points= {
        'console_scripts': [
            'fichub_cli=fichub_cli.cli:app'
        ]
        },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
