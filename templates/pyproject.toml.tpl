[tool.isort]
profile = "black"

[tool.pytest.ini_options]
addopts = "-ra -q --strict-markers"

[tool.coverage.run]
branch = true
source = [
    "./$src_dir/",
]
omit = [
    "*/tests/*",
]
