from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='fichub-cli',
    author='arzkar',
    author_email="roguedevone@gmail.com",
    description="A CLI tool for the fichub.net API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version='0.1',
    license='MIT',
    url="https://github.com/FicHub/fichub_cli",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_package_data=True,
    install_requires=[
        'Click',
        'requests'
    ],
    entry_points='''
        [console_scripts]
        fichub_cli=fichub_cli:cli
    ''',
    classifiers=[
        'Development Status :: 5 - Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: CLI Tool',
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
