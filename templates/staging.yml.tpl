on: push

name: Code QA & Staging

jobs:
  python-formatting:
    runs-on: ubuntu-latest
    container: python:$python_version-slim
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Check formatting
        run: |
          pip install -q black==21.8b0
          black --check src

  python-linting:
    runs-on: ubuntu-latest
    container: python:$python_version-slim
    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Run linter
        run: |
          pip install -q flake8
          flake8 src

  unit-tests:
    runs-on: ubuntu-latest
    container:
      image: python:$python_version-slim

    steps:
      - name: Checkout
        uses: actions/checkout@v2

      - name: Install required packages
        run: |
          pip install -q pipenv
          pipenv install -d --system --deploy

      - name: Run unit tests
        run: |
          pytest -c pytest.ini --cov --cov-report term-missing:skip-covered src/

  deploy-staging:
    if: github.event.ref == 'refs/heads/main'
    needs:
      - python-formatting
      - python-linting
      - unit-tests

    runs-on: ubuntu-latest
    container: python:$python_version-slim

    steps:
      - name: Checkout
        uses: actions/checkout@v2
