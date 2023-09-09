from setuptools import setup,find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


setup(
    name="esdm",
    version="1.8",
    packages=['esdm'],
    description='A easy SSH device manger',
    long_description=long_description,
    long_description_content_type="text/markdown",
    entry_points={
        'console_scripts': [
            'esdm=esdm.__main__:run'
        ],
    },
)
