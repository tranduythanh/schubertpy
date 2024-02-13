from setuptools import setup, find_packages

# Function to read the contents of the requirements.txt file
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip()]
    
setup(
    name='schubertpy',
    version='0.3.5',
    packages=find_packages(),
    description='A brief description of your package',
    long_description=open('README.md').read(),
    python_requires='>=3.6',
    author='Trần Duy Thanh',
    author_email='fbtranduythanh@gmail.com',
    url='https://github.com/tranduythanh/schubertpy',
    install_requires=read_requirements(),
)
