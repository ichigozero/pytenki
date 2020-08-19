from setuptools import find_packages
from setuptools import setup

setup(
    name='pytenki',
    version='1.0.0',
    description='Raspberry Pi Weather Station',
    license='MIT',
    author='Gary Sentosa',
    author_email='gary.sentosa@gmail.com',
    url='https://github.com/ichigozero/pytenki',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    zip_safe=False,
    install_requires=[
        'gpiozero>=1.5.1',
    ],
)
