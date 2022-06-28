[run]
branch = True
source =
    ./$src_dir/

omit =
    */tests/*

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if TYPE_CHECKING:

precision = 2
