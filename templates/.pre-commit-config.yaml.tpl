default_language_version:
  python: python$python_version

repos:
  - repo: https://github.com/pycqa/isort
    rev: 5.9.3
    hooks:
      - id: isort

  - repo: https://github.com/psf/black
    rev: 22.6.0
    hooks:
      - id: black

  - repo: https://github.com/pycqa/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
