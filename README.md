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

## Contributing

Contributions to `schubertpy` are highly encouraged, whether they involve extending functionality, enhancing performance, or fixing bugs. Please feel free to submit issues or pull requests on GitHub to suggest changes or improvements.

## License

`schubertpy` is made available under the MIT License. For more details, see the LICENSE file included with the source code.
