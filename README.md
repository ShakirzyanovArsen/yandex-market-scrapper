## Requirements
1) [Pyenv](https://github.com/pyenv/pyenv) ([for Windows](https://github.com/pyenv-win/pyenv-win))
## Getting started
Install and use specific python version
```shell
pyenv install 3.11.1
pyenv local 3.11.1
```

Install poetry and virtualenv
```shell
pip install poetry virtualenv
```

Create venv and install dependencies
```shell
poetry install
poetry shell
```

Run tests
```shell
poetry run pytest
```
Run as module
```shell
python -m scrapper_lib <link>
```