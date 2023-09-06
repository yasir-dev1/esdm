from setuptools import setup,find_packages

setup(
    name="esdm",
    version="1.0",
    packages=['esdm'],
    entry_points={
        'console_scripts': [
            'esdm=esdm.__main__:run'
        ],
    },
)
