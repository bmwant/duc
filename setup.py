from distutils.core import setup

with open('README.txt') as file:
    long_description = file.read()

setup(name='duc',
      version='1.0',
      py_modules=['duc'],
      author='Most Wanted',
      author_email='bmwant@gmail.com',
      url='http://bmwlog.pp.ua',
      description='Module for validating and transforming data',
      keywords=['dictionary', 'validation', 'json'],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Developers',
      ],
      long_description=long_description,
      install_requires=[
          'cerberus',
      ])