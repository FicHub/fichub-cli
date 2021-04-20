from setuptools import setup, find_packages

setup(
    name='fichub-cli',
    author='arzkar',
    author_email="roguedevone@gmail.com",
    description="A CLI for the fichub.net API",
    version='0.1',
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
)
