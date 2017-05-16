from setuptools import setup
import unittest

def test_suite():
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    return test_suite

setup(name='wdlabelbuilder',
      version='0.1.1',
      author='Migdalo',
      license='MIT',
      packages=['wdlabelbuilder'],
      test_suite='setup.test_suite',
      entry_points={
        'console_scripts': [
            'wdlabelbuilder = wdlabelbuilder.wdlabelbuilder:process_arguments'
        ]
      },
      zip_safe=True)

