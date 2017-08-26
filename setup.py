from setuptools import setup

setup(
    name='freetile',
    version='0.1.1',
    description='freely tiling script for X',
    url='http://github.com/rbn42/freetile',
    download_url='https://github.com/rbn42/freetile/archive/0.1.1.tar.gz',
    author='rbn42',
    author_email='bl100@students.waikato.ac.nz',
    license='MIT',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: X11 Applications',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Desktop Environment :: Window Managers',
    ],
    keywords=['window', 'tiling', 'xorg'],
    packages=[
        'freetile', 'freetile.helper'
    ],
    package_dir={
        'freetile': 'freetile',
        'freetile.helper': 'freetile/helper'
    },
    install_requires=[
        'docopt',
        'ewmh',
        'xcffib',
        'python-xlib',
        'setproctitle',
    ],
    entry_points={
        'console_scripts': [
            'freetile=freetile.__main__:main',
        ]
    }
)
