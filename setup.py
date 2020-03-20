from setuptools import setup, find_packages

setup(
    name='pytenki',
    description='Raspberry Pi Weather Station',
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
)
