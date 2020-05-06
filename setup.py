from setuptools import setup, find_packages


setup(
    name='ES21',
    version='0.1-beta',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[
        'flask',
        'tinydb',
        'tinydb-serialization',
        'Flask-WTF',
        'PyFladesk',
    ],
)
