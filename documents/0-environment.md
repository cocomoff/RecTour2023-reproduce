# 0. Environment

Standard python environment is required. At least the following libraries should be installed.

- Language
  - Python 3.9
- Libraries
  - dill 0.3.7
  - matplotlib 3.7.2
  - numpy 1.25.2
  - pandas 2.1.0
  - pulp 2.7.0
  - scipy 1.11.2
  - scikit-learn 1.3.0
  - tqdm 4.66.1
- Some python standard libraries: argparse, json, gzip, os, glob, datetime, etc.


## Using venv

Here, we generate our virtual environment of name `rectour2023` and activate the environment as follows.

```python
> python -V # Python 3.9.18
> python -m venv rectour2023
> source rectour2023/bin/activate
> pip install argparse dill matplotlib numpy pandas pulp tqdm
```

Our freezed pip environment is stored in `environment-rectour2023.yaml`.