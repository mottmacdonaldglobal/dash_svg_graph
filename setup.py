  
"""Setup for pyiges"""
from setuptools import setup
import os
from io import open as io_open

package_name = 'dash_svg_graph'

# Get version
__version__ = None
filepath = os.path.dirname(__file__)
version_file = os.path.join(filepath, package_name, '_version.py')
with io_open(version_file, mode='r') as fd:
    exec(fd.read())

readme_file = os.path.join(filepath, 'README.md')

setup(
    name=package_name,
    packages = [package_name],
    version=__version__,
    author='Jon',
    author_email='jonrobinson1980@gmail.com',
    long_description=io_open(readme_file, encoding="utf-8").read(),
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: MacOS',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description='Add svg files printed in Rhino to Dash Plotly graph',
    url='https://github.com/mottmacdonaldglobal/dash_svg_graph.git',
    install_requires=['dash',]
)