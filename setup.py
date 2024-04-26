from setuptools import setup, find_packages

# Function to read the contents of the requirements.txt file
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip()]
    

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='schubertpy',
    version='0.3.13',
    packages=find_packages(),
    description='This Python module facilitates operations such as quantum Pieri rules, quantum Giambelli formulae, action and multiplication of Schubert classes, and conversion between different representations of Schubert classes',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    author='Trần Duy Thanh',
    author_email='fbtranduythanh@gmail.com',
    url='https://github.com/tranduythanh/schubertpy',
    install_requires=read_requirements(),
)
