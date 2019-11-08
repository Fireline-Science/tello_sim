import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tello_sim',
    version='0.0.1',
    description='A simulator for dry-running DJI Tello commands in Python 3 based on the instruction set provided by https://github.com/Virodroid/easyTello',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/FIreline-Science/tello_sim',
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'matplotlib'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
