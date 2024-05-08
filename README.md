# schubertpy

## Overview

`schubertpy` is a powerful Python package designed for performing advanced mathematical operations on the Grassmannian, a key concept in algebraic geometry and representation theory. This module facilitates operations such as quantum Pieri rules, quantum Giambelli formulae, and the manipulation of Schubert classes. It is a Python implementation based on the comprehensive maple library available at [https://sites.math.rutgers.edu/~asbuch/qcalc/](https://sites.math.rutgers.edu/~asbuch/qcalc/).

References:

- [https://ar5iv.labs.arxiv.org/html/0809.4966](https://ar5iv.labs.arxiv.org/html/0809.4966)
- [https://sites.math.rutgers.edu/~asbuch/notes/grass.pdf](https://sites.math.rutgers.edu/~asbuch/notes/grass.pdf)
- [https://sites.math.rutgers.edu/~asbuch/notes/schurfcns.pdf](https://sites.math.rutgers.edu/~asbuch/notes/schurfcns.pdf)
- [https://sites.math.rutgers.edu/~asbuch/papers/qschub.pdf](https://sites.math.rutgers.edu/~asbuch/papers/qschub.pdf)
- [https://sites.math.rutgers.edu/~asbuch/papers/isogiam.pdf](https://sites.math.rutgers.edu/~asbuch/papers/isogiam.pdf)
- [https://sites.math.rutgers.edu/~asbuch/papers/qgig.pdf](https://sites.math.rutgers.edu/~asbuch/papers/qgig.pdf)
- [https://sites.math.rutgers.edu/~asbuch/papers/oggiam.pdf](https://sites.math.rutgers.edu/~asbuch/papers/oggiam.pdf)
- [https://sites.math.rutgers.edu/~asbuch/talks/cirm2020.pdf](https://sites.math.rutgers.edu/~asbuch/talks/cirm2020.pdf)
- [https://sites.math.rutgers.edu/~asbuch/papers/](https://sites.math.rutgers.edu/~asbuch/papers/)

## Features

- **Quantum Pieri Rule Calculations**: Efficient computation of quantum Pieri rules applied to Schubert classes.
- **Quantum Giambelli Formulae**: Expression of products of Schubert classes in alternative forms using quantum Giambelli formulae.
- **Schubert Class Operations**: Perform actions and multiplications on Schubert classes, in both classical and quantum contexts.
- **Dualization and Conversion**: Dualize Schubert classes and convert between different Schubert class representations.

## Installation

To install the `schubertpy` module, run the following command:

```bash
pip install schubertpy
```

If you wanna use with sagemath, run the following command:

```bash
sage -pip install schubertpy
```

## Usage

Example usage demonstrating the capabilities of `schubertpy`:

```python
from schubertpy import Grassmannian, OrthogonalGrassmannian, IsotropicGrassmannian

def main():
    # Initialize the Grassmannian object with dimensions
    gr = Grassmannian(2, 5)
    print(gr.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(gr.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(gr.qgiambelli('S[2,1]*S[2,1]'))
    print(gr.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(gr.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(gr.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(gr.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(gr.giambelli('S[2,1]*S[2,1]'))
    print(gr.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(gr.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(gr.dualize('S[1]+S[2]'))


    ig = Grassmannian(2, 6)
    print(ig.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(ig.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(ig.qgiambelli('S[2,1]*S[2,1]'))
    print(ig.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(ig.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(ig.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(ig.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(ig.giambelli('S[2,1]*S[2,1]'))
    print(ig.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(ig.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(ig.dualize('S[1]+S[2]'))

    og = Grassmannian(2, 6)
    print(og.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.qgiambelli('S[2,1]*S[2,1]'))
    print(og.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.giambelli('S[2,1]*S[2,1]'))
    print(og.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.dualize('S[1]+S[2]'))

    og = Grassmannian(2, 7)
    print(og.qpieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.qact('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.qgiambelli('S[2,1]*S[2,1]'))
    print(og.qmult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.qtoS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.pieri(1, 'S[2,1] - 7*S[3,2]'))
    print(og.act('S[1]+S[2]*S[3]', 'S[2,1]+S[3,2]'))
    print(og.giambelli('S[2,1]*S[2,1]'))
    print(og.mult('S[2,1]', 'S[2,1]+S[3,2]'))
    print(og.toS('S[2,1]*S[2,1]*S[2,1]'))
    print(og.dualize('S[1]+S[2]'))


if __name__ == "__main__":
    main()
```

You wanna use with sagemath? You can save above example to main.py and then run:

```bash
sage -python main.py
```


For detailed examples and more operations, refer to the test cases provided within the module's documentation.

## Running Tests

To verify the module's functionality, you can run the included tests with either of the following commands:

```bash
make test
```

Or directly with Python:

```bash
python3 -m unittest schubertpy/testcases/*.py
```

## Authors
- **Dang Tuan Hiep** 🇻🇳
  - <img width="100" alt="Screenshot 2024-05-08 at 15 58 33" src="https://github.com/tranduythanh/schubertpy/assets/6112723/3e2bc594-e192-4450-b624-c4b18ff2be84">
  - Email: hiepdt@dlu.edu.vn (Đặng Tuấn Hiệp)
  
- **Trần Duy Thanh** 🇻🇳
  - <img width="100" alt="Screenshot 2024-05-08 at 16 56 22" src="https://github.com/tranduythanh/schubertpy/assets/6112723/f3abca71-6bb5-44f6-b090-9ce206bdd5ad">
  - Email: coachtranduythanh@gmail.com
  - Email: 2015830@dlu.edu.vn

- **Hoàng Minh Đức** 🇻🇳
  - <img width="100" alt="Screenshot 2024-05-08 at 16 49 14" src="https://github.com/tranduythanh/schubertpy/assets/6112723/595e2bd1-33e0-42cd-8fc3-ee889c994664">  
  - Email: 2113423@dlu.edu.vn

- **Nguyễn Trương Thiên Ân** 🇻🇳
  - <img width="100" alt="Screenshot 2024-05-08 at 16 50 21" src="https://github.com/tranduythanh/schubertpy/assets/6112723/a8b695fa-48fd-42d5-831d-fc58bb26dd45">
  - Email: 2113421@dlu.edu.vn

## Contributing

We highly encourage contributions to `schubertpy`. Whether you are looking to expand functionality, enhance performance, or fix bugs, your input is valuable. To get started:

- **Report Issues**: If you encounter issues or have suggestions, please report them by creating an issue on our GitHub page.
- **Submit Pull Requests**: Feel free to fork the repository and submit pull requests. Whether it's adding new features, optimizing existing code, or correcting bugs, your contributions are welcome.

Please ensure your pull requests are well-documented and include any necessary tests. For more details on contributing, refer to our contribution guidelines on GitHub.

## License

`schubertpy` is open source software (under the GNU General Public License).
