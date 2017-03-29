'''Cloudify plugin package config'''

from setuptools import setup


setup(
    name='lab-wf-graphs-plugin',
    version='1.4',
    license='LICENSE',
    packages=[
        'plugin'
    ],
    description='A Cloudify plugin for training labs',
    install_requires=[
        'cloudify-plugins-common>=3.4'
    ]
)
