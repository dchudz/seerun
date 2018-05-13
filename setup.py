from setuptools import setup, find_packages
import sys

if sys.version_info < (3, 4):
    sys.exit('Sorry, Python < 3.4 is not supported')

setup(
    author="David Chudzicki",
    author_email='dchudz@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python :: 3.6',
    ],
    description="Rewrite Coverage finds sections of code that can be rewritten"
                " (deleted, replaced) with tests still passing (be careful!)",
    entry_points={
        'console_scripts': [
            'seerun=seerun.cli:main',
        ],
    },
    install_requires=['Click>=6.0', 'asttokens>=1.1', 'Pygments>=2.2'],
    include_package_data=True,
    name='seerun',
    packages=find_packages(include=['seerun']),
    version='0.1.0',
)
