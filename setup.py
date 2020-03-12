from setuptools import setup
import pathlib
import re

curdir = pathlib.Path(__file__).parent

README = (curdir / "README.md").read_text()
VERSION = (curdir / "tidyfasta" / "__init__.py").read_text()
version_number=re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", VERSION).group(1)

setup(
    name="tidyfasta",
    version=version_number,
    packages=['tidyfasta', 'tidyfasta.common'],
    url='https://github.com/maxhebditch/tidyfasta',
    license='MIT',
    author='Max Hebditch',
    author_email='max@maxhebditch.co.uk',
    description='Sanitise protein FASTA files / data',
    long_description=README,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "tidyfasta=tidyfasta.__main__:main",
        ]
    }
)
