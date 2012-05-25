from setuptools import setup, find_packages
import sys, os

version = '0.2'

setup(name='BenderBot',
      version=version,
      description="A configurable bare bone IRC bot written in Python",
      long_description="",
      classifiers=[],
      keywords='',
      author='Jeffrey Ness',
      author_email='jeffrey.ness@rackspace.com',
      url='',
      license='GPLv3',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[],
      test_suite='nose.collector',
      entry_points= {'console_scripts': ['Bender = BenderBot.Bender:main']},
      )
