import sys
from setuptools import setup, find_packages

setup(
    name='pyfile',
    version='0.1.0',
    packages=['pyfile'],
    url='https://github.com/neriberto/pyfile',
    license='BSD 3-Clause License',
    author='Neriberto C.Prado',
    author_email='neriberto@gmail.com',
    description='A file inspector writed in Python',
    entry_points={
        "console_scripts": [
            "pyfile=pyfile:main",
            "pyfile%s=pyfile:main" % sys.version[:1],
            "pyfile%s=pyfile:main" % sys.version[:3],
        ],
    }
)
