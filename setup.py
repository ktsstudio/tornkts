from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

setup(
    name='tornkts',
    version='0.2.8',
    description='Tuned Tornado classes for more simple creating powerful API',
    long_description='Tuned Tornado classes for more simple creating powerful API',

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

    install_requires=['tornado', 'torndsession', 'passlib', 'ujson']

)
