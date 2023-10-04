from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="tangent-cli",
    version="0.1",
    packages=find_packages(),
    package_data={'tangent': ['functions/*']},
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'tangent=tangent.__main__:main',
        ],
    },
)
