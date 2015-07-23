from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='tornkts',
    version='0.1.2',

    description='Helper for tornado',
    long_description='Helper for tornado',

    author='KTS',
    author_email='team@ktsstudio.ru',

    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],

    keywords='tornkts setuptools development',

    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),

    install_requires=['tornado', 'torndsession', 'passlib']

)
