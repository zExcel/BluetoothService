from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='BluetoothService',
    version='0.1.0',
    description='Project to host the code associated with my Orange Pi\'s bluetooth services ',
    long_description=readme,
    author='Justin Clark',
    author_email='clarkjustin246@gmail.com',
    url='https://github.com/zExcel/BluetoothService',
    packages=find_packages(exclude=('tests', 'docs'))
)