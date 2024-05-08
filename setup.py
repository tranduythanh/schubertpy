from setuptools import setup, find_packages
from cff import Citation

# Function to read the contents of the requirements.txt file
def read_requirements():
    with open('requirements.txt') as f:
        return [line.strip() for line in f if line.strip()]

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

# Define package metadata
package_name = 'schubertpy'
package_version = '0.3.19'
package_author = 'Trần Duy Thanh'
package_author_email = 'fbtranduythanh@gmail.com'
package_url = 'https://github.com/tranduythanh/schubertpy'
package_description = 'This Python module facilitates operations such as quantum Pieri rules, quantum Giambelli formulae, action and multiplication of Schubert classes, and conversion between different representations of Schubert classes'
package_license = 'GNU General Public License'

# Generate CITATION.cff content
citation = Citation(
    title=package_name,
    authors=['Dang Tuan Hiep',package_author,'Hoàng Minh Đức','Nguyễn Trương Thiên Ân'],
    version=package_version,
    url=package_url,
    license=package_license,
)

# Write CITATION.cff content to file
with open('CITATION.cff', 'w') as f:
    f.write(citation.cff())

setup(
    name=package_name,
    version=package_version,
    packages=find_packages(),
    description=package_description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6',
    author=package_author,
    author_email=package_author_email,
    url=package_url,
    install_requires=read_requirements(),
)
