"""
Setup configuration for cdk-aws-s3-transfer package
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cdk-aws-s3-transfer",
    version="1.0.0",
    author="StackSmiths",
    description="AWS CDK example for accelerated S3 data transfer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stacksmiths/cdk-aws-s3-transfer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    keywords="aws cdk s3 transfer acceleration cloudformation",
    project_urls={
        "Bug Reports": "https://github.com/stacksmiths/cdk-aws-s3-transfer/issues",
        "Source": "https://github.com/stacksmiths/cdk-aws-s3-transfer",
    },
)
