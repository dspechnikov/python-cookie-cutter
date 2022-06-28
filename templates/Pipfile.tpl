[[source]]
name = "pypi"
url = "https://pypi.org/simple"
verify_ssl = true

[requires]
python_version = "$python_version"

[packages]

[dev-packages]
# testing
pytest = "*"
pytest-env = "*"
pytest-mock = "*"
pytest-cov = "*"

# code quality
flake8 = "*"
black = "22.6.0"
isort = "*"
pre-commit = "*"
