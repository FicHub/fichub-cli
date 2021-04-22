from setuptools import setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='fichub-cli',
    author='arzkar',
    author_email="roguedevone@gmail.com",
    description="A CLI tool for the fichub.net API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.3.2',
    license='MIT',
    url="https://github.com/FicHub/fichub-cli",
    packages=['fichub_cli'],
    include_package_data=True,
    install_requires=[
        'click',
        'requests',
        'loguru',
        'tqdm'
    ],
    entry_points='''
        [console_scripts]
        fichub_cli=fichub_cli.cli:run_cli
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
