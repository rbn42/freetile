from setuptools import setup

setup(name='freetile',
      version='0.0',
      description='freely tiling script for X',
      url='http://github.com/rbn42/freetile',
      author='rbn42',
      author_email='bl100@students.waikato.ac.nz',
      license='MIT',
      packages=['freetile', 'freetile.helper'],
      package_dir={
          'freetile': 'freetile',
          'freetile.helper': 'freetile/helper',
      },
      install_requires=[
          'docopt', 'ewmh', 'xcffib', 'python-xlib'
      ],
      zip_safe=False)
