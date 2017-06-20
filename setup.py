#!/usr/bin/env python

from setuptools import setup
import sys

setup(
    name='wifiPassword',
    version='1.0',
    description='A cross platform CLI tool to get connected wifi network\'s password.',
    long_description=open('README.rst').read(),
    author='Ankit Jain',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Natural Language :: English',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords="cli utility, cli-tool, cross-platform, wifiPassword, wifi, password, wifi password ubuntu, wifi password windows",
    author_email='ankitjain28may77@gmail.com',
    url='https://github.com/ankitjain28may/wifiPassword',
    packages=['wifiPassword'],
    install_requires=[
        'colorama>=0.3.7'
    ],
    entry_points={
        'console_scripts': [
            'wifiPassword = wifiPassword.wifiPassword:main'
        ],
    }
)
