from setuptools import setup
import pathlib

curdir = pathlib.Path(__file__).parent

README = (curdir / "README.md").read_text()

print(README)

setup(
    name="tidyfasta",
    version='1.0.2',
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
