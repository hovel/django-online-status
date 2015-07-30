import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), 'README')) as readme:
    README = readme.read()

with open(os.path.join(os.path.dirname(__file__), 'UNLICENSE')) as license:
    LICENSE = license.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-online-status',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license=LICENSE,
    description=README,
    author='Jakub Zalewski',
    author_email='zalew7@gmail.com',
    url='https://github.com/hovel/django-online-status',
    classifiers=[
        'Development Status :: Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
