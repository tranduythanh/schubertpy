# Repository Coverage

[Full report](https://htmlpreview.github.io/?https://github.com/tranduythanh/schubertpy/blob/python-coverage-comment-action-data/htmlcov/index.html)

| Name                                            |    Stmts |     Miss |   Cover |   Missing |
|------------------------------------------------ | -------: | -------: | ------: | --------: |
| schubertpy/\_\_init\_\_.py                      |        9 |        0 |    100% |           |
| schubertpy/abstract\_grassmannian.py            |      154 |       23 |     85% |22-26, 30, 34, 38, 42, 46, 51, 55, 60, 64, 68, 72, 95-99, 103, 108 |
| schubertpy/grassmannian.py                      |      127 |       42 |     67% |33, 35, 37, 47-52, 67, 78, 81, 89, 93, 96, 100, 104, 110, 122-124, 127, 154, 164, 173-223 |
| schubertpy/isotropic\_grassmannian.py           |       96 |       21 |     78% |31, 33, 37, 47-52, 69, 79, 82, 92, 102-105, 109-112, 117, 123, 135-137, 140 |
| schubertpy/lc.py                                |      217 |      105 |     52% |13-14, 32, 45, 52, 56, 62-66, 73, 77, 83-86, 91-99, 102-109, 118, 127, 159-185, 191-198, 207-232, 237, 247, 278, 283, 295, 328-365 |
| schubertpy/mult\_table.py                       |       39 |       18 |     54% |27-42, 46, 56-57, 61, 64, 67, 72, 75, 82, 85 |
| schubertpy/orthogonal\_grassmannian.py          |      216 |       39 |     82% |37, 56-67, 89, 110, 113, 126, 139-144, 148-153, 157, 168, 188-194, 197-205, 229-230, 316-317, 358, 362 |
| schubertpy/partition.py                         |      111 |       28 |     75% |19, 25, 27, 29, 31, 38, 42, 45, 48-53, 60, 66, 92, 94, 96, 124-127, 134, 145, 192, 194, 210-213 |
| schubertpy/qcalc.py                             |      499 |       93 |     81% |79, 81, 93-94, 101, 103, 106, 128, 579, 583, 592-598, 607-638, 647, 661-667, 671-677, 681-694, 698-711, 718-729, 733-736, 740-742, 746-747, 751-753, 757-758, 762-766, 771-775, 780-782, 787-788 |
| schubertpy/schur.py                             |      122 |       59 |     52% |31-33, 39, 47, 50-52, 58, 61-63, 68-74, 83, 87-88, 92, 96, 100-123, 127-148, 152-154, 190 |
| schubertpy/testcases/basic/test\_comps.py       |       49 |        1 |     98% |        69 |
| schubertpy/testcases/basic/test\_gr.py          |       76 |        1 |     99% |        97 |
| schubertpy/testcases/basic/test\_hash.py        |       31 |        1 |     97% |        38 |
| schubertpy/testcases/basic/test\_ig.py          |       80 |        1 |     99% |       101 |
| schubertpy/testcases/basic/test\_lc.py          |       85 |        1 |     99% |       113 |
| schubertpy/testcases/basic/test\_og\_b.py       |       79 |        1 |     99% |       102 |
| schubertpy/testcases/basic/test\_og\_d.py       |       88 |        1 |     99% |       110 |
| schubertpy/testcases/basic/test\_part.py        |      127 |        1 |     99% |       176 |
| schubertpy/testcases/basic/test\_part\_index.py |      260 |        1 |     99% |       323 |
| schubertpy/testcases/basic/test\_part\_pair.py  |       35 |        1 |     97% |        48 |
| schubertpy/testcases/basic/test\_piery.py       |       52 |        1 |     98% |        67 |
| schubertpy/testcases/basic/test\_rim\_hook.py   |       35 |        0 |    100% |           |
| schubertpy/testcases/basic/test\_schur.py       |       12 |        1 |     92% |        15 |
| schubertpy/testcases/basic/test\_type.py        |       62 |        1 |     98% |        75 |
| schubertpy/testcases/basic/test\_util.py        |       19 |        1 |     95% |        28 |
| schubertpy/utils/const.py                       |        6 |        2 |     67% |      5, 8 |
| schubertpy/utils/hash.py                        |       26 |        1 |     96% |        34 |
| schubertpy/utils/kstrict.py                     |       33 |        1 |     97% |        35 |
| schubertpy/utils/mix.py                         |       90 |       27 |     70% |11-13, 19-20, 23-31, 34-40, 45, 63-64, 71, 73, 99, 113 |
|                                       **TOTAL** | **2835** |  **473** | **83%** |           |


## Setup coverage badge

Below are examples of the badges you can use in your main branch `README` file.

### Direct image

[![Coverage badge](https://raw.githubusercontent.com/tranduythanh/schubertpy/python-coverage-comment-action-data/badge.svg)](https://htmlpreview.github.io/?https://github.com/tranduythanh/schubertpy/blob/python-coverage-comment-action-data/htmlcov/index.html)

This is the one to use if your repository is private or if you don't want to customize anything.

### [Shields.io](https://shields.io) Json Endpoint

[![Coverage badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/tranduythanh/schubertpy/python-coverage-comment-action-data/endpoint.json)](https://htmlpreview.github.io/?https://github.com/tranduythanh/schubertpy/blob/python-coverage-comment-action-data/htmlcov/index.html)

Using this one will allow you to [customize](https://shields.io/endpoint) the look of your badge.
It won't work with private repositories. It won't be refreshed more than once per five minutes.

### [Shields.io](https://shields.io) Dynamic Badge

[![Coverage badge](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=coverage&query=%24.message&url=https%3A%2F%2Fraw.githubusercontent.com%2Ftranduythanh%2Fschubertpy%2Fpython-coverage-comment-action-data%2Fendpoint.json)](https://htmlpreview.github.io/?https://github.com/tranduythanh/schubertpy/blob/python-coverage-comment-action-data/htmlcov/index.html)

This one will always be the same color. It won't work for private repos. I'm not even sure why we included it.

## What is that?

This branch is part of the
[python-coverage-comment-action](https://github.com/marketplace/actions/python-coverage-comment)
GitHub Action. All the files in this branch are automatically generated and may be
overwritten at any moment.