from setuptools import setup
import glob

setup(
    name='freetile',
    version='v0.1.2',
    description='freely tiling script for X',
    url='http://github.com/rbn42/freetile',
    download_url='https://github.com/rbn42/freetile/archive/v0.1.2.tar.gz',
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
    packages=['freetile', 'freetile.helper'],
    install_requires=[
        'docopt',
        'ewmh',
        'xcffib',
        'python-xlib',
        'setproctitle',
    ],
    data_files=[
        ('share/doc/visualbar/config', glob.glob('doc/config/*')),
    ],
    entry_points={
        'console_scripts': [
            'freetile=freetile.__main__:main',
        ]
    }
)
