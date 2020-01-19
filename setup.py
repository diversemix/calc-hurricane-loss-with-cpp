import sys
import codecs

from setuptools import setup, find_packages, Extension
from setuptools.command.test import test as TestCommand

import gethurricaneloss


# the c++ extension module
extension_mod = Extension("loss_framework", [
    "src/loss-framework.cpp",
    "src/calculate-loss.cpp",
])

class PyTest(TestCommand):
    # `$ python setup.py test' simply installs minimal requirements
    # and runs the tests with no fancy stuff like parallel execution.
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = [
            '--doctest-modules', '--verbose',
            './gethurricaneloss', './tests'
        ]
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


tests_require = [
    'pytest',
    'mock',
]


install_requires = [
    'wheel',
    'numpy',
    'click',
]


# Conditional dependencies:

# sdist
if 'bdist_wheel' not in sys.argv:
    try:
        import argparse
    except ImportError:
        install_requires.append('argparse>=1.2.1')



# bdist_wheel
extras_require = {
    # https://wheel.readthedocs.io/en/latest/#defining-conditional-dependencies
    'python_version == "3.0" or python_version == "3.1"': ['argparse>=1.2.1'],
}


def long_description():
    with codecs.open('README.md', encoding='utf8') as f:
        return f.read()


setup(
    name='gethurricaneloss',
    version=gethurricaneloss.__version__,
    description=gethurricaneloss.__doc__.strip(),
    long_description=long_description(),
    url='https://github.com/diversemix/gethurricaneloss',
    download_url='https://github.com/diversemix/gethurricaneloss',
    author=gethurricaneloss.__author__,
    author_email='diversemix@gmail.com',
    license=gethurricaneloss.__licence__,
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'gethurricaneloss = gethurricaneloss.__main__:main',
        ],
    },
    extras_require=extras_require,
    install_requires=install_requires,
    tests_require=tests_require,
    cmdclass={'test': PyTest},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
    ],
    ext_modules=[extension_mod],
)


