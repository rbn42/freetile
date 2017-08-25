from setuptools import setup

setup(name='freetile',
      version='0.1.0',
      description='freely tiling script for X',
      url='http://github.com/rbn42/freetile',
      download_url='https://github.com/rbn42/freetile/archive/0.1.0.tar.gz',
      author='rbn42',
      author_email='bl100@students.waikato.ac.nz',
      license='MIT',
      packages=[
          'freetile', 'freetile.helper'
      ],
      package_dir={
          'freetile': 'freetile',
          'freetile.helper': 'freetile/helper'
      },
      install_requires=[
          'docopt', 'ewmh', 'xcffib', 'python-xlib'
      ],
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'Environment :: X11 Applications',
          'Intended Audience :: End Users/Desktop',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Topic :: Desktop Environment :: Window Managers',
      ],
      zip_safe=False)
