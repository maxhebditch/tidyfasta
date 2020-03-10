from setuptools import setup
import pathlib

curdir = pathlib.Path(__file__).parent

README = (curdir / "README.md").read_text()

print(README)

setup(
    name='tidyfasta',
    version='1.0.1',
    packages=['tidyfasta', 'tidyfasta.common'],
    url='https://github.com/maxhebditch/tidyfasta',
    license='MIT',
    author='Max Hebditch',
    author_email='max@maxhebditch.co.uk',
    description='Sanitise protein FASTA files / data',
    long_description=README,
    long_description_content_type="text/markdown",
)
