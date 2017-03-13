'''Cloudify plugin package config'''

from setuptools import setup


setup(
    name='cloudify-aws-api-gateway-plugin',
    version='1.4',
    license='LICENSE',
    packages=[
        'api_gateway',
        'api_gateway.resources'
    ],
    description='A Cloudify plugin for training labs',
    install_requires=[
        'cloudify-plugins-common>=3.4',
        'boto3==1.4.4'
    ]
)
