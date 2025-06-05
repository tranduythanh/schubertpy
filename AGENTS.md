# AGENTS Instructions for `schubertpy`

This repository implements **schubertpy**, a Python package for classical and quantum Schubert calculus.

## Repository structure
- `schubertpy/`: main package
- `schubertsage/`: conversion helpers for SageMath
- `docs/`: descriptions of algorithms
- `example/`: small example script
- `schubertpy/testcases/`: unit tests (`basic/` and optional `brute_force/`)

## Development guidelines
- **Testing**: After **each** code change, run the basic unit tests:
  ```bash
  python3 -m unittest schubertpy/testcases/basic/*.py
  ```
  Once all changes are complete, also run the slower `brute_force` tests:
  ```bash
  python3 -m unittest schubertpy/testcases/brute_force/*.py
  ```
- Install dependencies with `pip install -r requirements.txt` if tests fail due to missing packages.
- Follow standard PEP8 style when editing Python files.

## Notes for Codex agents
- Always ensure tests pass before committing changes.
- Look in `docs/` for algorithm explanations if you need implementation details.
