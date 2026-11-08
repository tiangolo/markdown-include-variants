from pathlib import Path
from xml.etree import ElementTree

import markdown
import pytest

from markdown_include_variants import IncludeVariantsExtension


@pytest.fixture(params=["file", "folder", "nested_folder"])
def examples(request, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)

    def create(*names):
        paths = {}
        for name in names:
            if request.param == "file":
                path = Path(f"{name}.py")
            elif request.param == "folder":
                path = Path(name) / "main.py"
            else:
                path = Path(name) / "routers" / "items.py"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "".join(f'print("{name}: {line}")\n' for line in range(1, 7))
            )
            paths[name] = path
        return paths

    return create


def render(path, config=""):
    html = markdown.markdown(
        f"{{* {path} {config} *}}",
        extensions=[
            IncludeVariantsExtension(),
            "mdx_include",
            "pymdownx.superfences",
            "pymdownx.highlight",
            "pymdownx.blocks.tab",
            "pymdownx.blocks.details",
            "pymdownx.blocks.admonition",
        ],
        extension_configs={"pymdownx.blocks.tab": {"alternate_style": True}},
    )
    assert "////" not in html
    return ElementTree.fromstring(f"<root>{html}</root>")


def labels(root):
    return ["".join(label.itertext()) for label in root.iter("label")]


def code_blocks(root):
    return ["".join(code.itertext()) for code in root.findall(".//pre/code")]


@pytest.mark.parametrize("name", ["example", "example_an"])
def test_single_unversioned_example(examples, name):
    paths = examples(name)
    root = render(paths[name])

    assert labels(root) == []
    assert root.findall(".//details") == []
    assert code_blocks(root) == [paths[name].read_text()]


@pytest.mark.parametrize("preferred", ["example", "example_an"])
def test_legacy_unversioned_annotated_pair(examples, preferred):
    paths = examples("example", "example_an")
    root = render(paths[preferred])

    assert labels(root) == ["non-Annotated"]
    assert code_blocks(root)[0] == paths[preferred].read_text()
    details = root.findall(".//details")
    assert len(details) == 1
    assert details[0].findtext("summary") == "🤓 Other versions and variants"
    assert "Python" not in "".join(root.itertext())
    if preferred == "example_an":
        assert root[0].get("class") == "highlight"
        assert "Prefer to use the Annotated version" in "".join(details[0].itertext())
    else:
        assert labels(details[0]) == []
        assert code_blocks(details[0]) == [paths["example_an"].read_text()]


@pytest.mark.parametrize("preferred", ["example", "example_non_an"])
def test_unversioned_non_annotated_pair(examples, preferred):
    paths = examples("example", "example_non_an")
    root = render(paths[preferred])

    assert labels(root) == ["non-Annotated"]
    assert code_blocks(root)[0] == paths[preferred].read_text()
    details = root.findall(".//details")
    assert len(details) == 1
    assert details[0].findtext("summary") == "🤓 Other versions and variants"
    assert "Python" not in "".join(root.itertext())
    if preferred == "example":
        assert root[0].get("class") == "highlight"
        assert "Prefer to use the Annotated version" in "".join(details[0].itertext())
    else:
        assert labels(details[0]) == []
        assert code_blocks(details[0]) == [paths["example"].read_text()]


def test_single_non_annotated_example_keeps_label(examples):
    paths = examples("example_non_an")
    root = render(paths["example_non_an"])

    assert labels(root) == ["non-Annotated"]
    assert root.findall(".//details") == []
    assert code_blocks(root) == [paths["example_non_an"].read_text()]


@pytest.mark.parametrize(
    "name, title",
    [
        ("example_py312", "Python 3.12+"),
        ("example_an_py312", "Python 3.12+"),
        ("example_non_an_py312", "Python 3.12+ - non-Annotated"),
    ],
)
def test_single_explicit_version_keeps_label(examples, name, title):
    paths = examples(name)
    root = render(paths[name], "ln[2:4] hl[3]")

    assert labels(root) == [title, title]
    assert code_blocks(root)[1] == paths[name].read_text()


def test_version_order_and_preferred_file(examples):
    paths = examples("example_py39", "example_py314", "example_py310", "example_py312")
    root = render(paths["example_py310"])

    assert labels(root) == [
        "Python 3.10+",
        "Python 3.14+",
        "Python 3.12+",
        "Python 3.9+",
    ]
    assert code_blocks(root) == [
        paths[name].read_text()
        for name in ["example_py310", "example_py314", "example_py312", "example_py39"]
    ]


def test_legacy_incomplete_annotated_version_pairs(examples):
    paths = examples("example_an_py312", "example_py311", "example_an_py311")
    root = render(paths["example_an_py312"])

    assert labels(root) == [
        "Python 3.12+",
        "Python 3.11+",
        "Python 3.11+ - non-Annotated",
    ]
    assert (
        "".join(root.itertext()).count(
            "Prefer to use the Annotated version if possible."
        )
        == 1
    )


def test_legacy_bare_version_without_annotated_counterpart(examples):
    paths = examples("example_an_py312", "example_py311")
    root = render(paths["example_an_py312"])

    assert labels(root) == ["Python 3.12+", "Python 3.11+"]
    assert "non-Annotated" not in "".join(root.itertext())
    assert "Prefer to use" not in "".join(root.itertext())


def test_non_annotated_versions_follow_recommended_versions(examples):
    paths = examples(
        "example_non_an_py311",
        "example_non_an_py312",
        "example_py311",
        "example_py312",
    )
    root = render(paths["example_non_an_py311"])

    assert labels(root) == [
        "Python 3.11+ - non-Annotated",
        "Python 3.12+",
        "Python 3.11+",
        "Python 3.12+ - non-Annotated",
    ]
    assert code_blocks(root) == [
        paths[name].read_text()
        for name in [
            "example_non_an_py311",
            "example_py312",
            "example_py311",
            "example_non_an_py312",
        ]
    ]


def test_incomplete_non_annotated_version_pairs(examples):
    paths = examples("example_py312", "example_non_an_py311")
    root = render(paths["example_py312"])

    assert labels(root) == ["Python 3.12+", "Python 3.11+ - non-Annotated"]
    assert "Prefer to use the Annotated version" in "".join(root.itertext())


@pytest.mark.parametrize("preferred", ["example", "example_an", "example_non_an"])
def test_mixed_annotation_conventions_are_rejected(examples, preferred):
    paths = examples("example", "example_an", "example_non_an")

    with pytest.raises(ValueError, match="Cannot mix legacy _an and _non_an") as exc:
        render(paths[preferred])
    assert str(paths[preferred]) in str(exc.value)
    assert "Migrate the whole example family" in str(exc.value)


def test_mixed_annotation_conventions_across_versions_are_rejected(examples):
    paths = examples("example_an_py311", "example_non_an_py312")

    with pytest.raises(ValueError, match="Cannot mix legacy _an and _non_an"):
        render(paths["example_an_py311"])


@pytest.mark.parametrize("preferred", ["example", "example_an_py312"])
def test_mixed_version_markers_are_rejected(examples, preferred):
    paths = examples("example", "example_an_py312")

    with pytest.raises(ValueError, match="Cannot mix versioned and unversioned") as exc:
        render(paths[preferred])
    assert str(paths[preferred]) in str(exc.value)
    assert "Add a Python version suffix to every variant" in str(exc.value)


def test_mixed_version_markers_with_non_annotated_are_rejected(examples):
    paths = examples("example", "example_non_an_py312")

    with pytest.raises(ValueError, match="Cannot mix versioned and unversioned"):
        render(paths["example"])


def test_missing_preferred_file_does_not_select_an_alternative(examples):
    paths = examples("example_an_py312")
    missing = Path(str(paths["example_an_py312"]).replace("_an_py312", "_py312"))

    with pytest.raises(FileNotFoundError, match="Included file does not exist") as exc:
        render(missing)
    assert str(missing) in str(exc.value)


@pytest.mark.parametrize("name", ["example", "example_an"])
def test_unversioned_preview_highlights_and_filename_title(examples, name):
    paths = examples(name)
    root = render(paths[name], 'ln[2:4] hl[3] title["app/main.py"]')

    assert labels(root) == []
    assert len(root.findall(".//details")) == 1
    assert code_blocks(root) == [
        "# Code above omitted 👆\n\n"
        + "".join(f'print("{name}: {line}")\n' for line in range(2, 5))
        + "\n# Code below omitted 👇\n",
        paths[name].read_text(),
    ]
    highlights = root.findall(".//*[@class='hll']")
    assert ["".join(span.itertext()) for span in highlights] == [
        f'print("{name}: 3")\n',
        f'print("{name}: 3")\n',
    ]
    titles = root.findall(".//*[@class='filename']")
    assert [title.text for title in titles] == ["app/main.py", "app/main.py"]


def test_unversioned_preview_only(examples):
    paths = examples("example_an")
    root = render(paths["example_an"], 'ln[0] title["main.py"]')

    assert labels(root) == []
    assert len(root) == 1
    assert root[0].tag == "details"
    assert root[0].findtext("summary") == "👀 Full file preview"
    assert code_blocks(root) == [paths["example_an"].read_text()]


def test_recommended_preview_with_non_annotated_alternative(examples):
    paths = examples("example", "example_non_an")
    root = render(paths["example"], 'ln[2:4] hl[3] title["main.py"]')

    assert labels(root) == ["non-Annotated"]
    assert root[0].get("class") == "highlight"
    preview, alternatives = root.findall(".//details")
    assert labels(preview) == []
    assert code_blocks(preview) == [paths["example"].read_text()]
    assert code_blocks(alternatives) == [paths["example_non_an"].read_text()]
    highlights = root.findall(".//*[@class='hll']")
    assert ["".join(span.itertext()) for span in highlights] == [
        'print("example: 3")\n',
        'print("example: 3")\n',
    ]
    assert [title.text for title in root.findall(".//*[@class='filename']")] == [
        "main.py",
        "main.py",
        "main.py",
    ]


def test_unrelated_example_can_use_legacy_annotation_convention(examples):
    paths = examples("example", "example_non_an", "other", "other_an")

    for name in ["example", "other_an"]:
        root = render(paths[name])
        assert labels(root) == ["non-Annotated"]
        assert code_blocks(root)[0] == paths[name].read_text()
        assert len(code_blocks(root)) == 2


def test_unrelated_files_and_directories_are_not_variants(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("example.py").write_text("pass\n")
    Path("example_extra.py").write_text("raise RuntimeError\n")
    Path("example_py312.txt").write_text("not Python\n")
    Path("example_py313.py").mkdir()

    root = render("example.py")

    assert labels(root) == []
    assert code_blocks(root) == ["pass\n"]


@pytest.mark.parametrize(
    "directories", [("app_py312", "app_non_an_py312"), ("app_an_py312", "app_py312")]
)
def test_nested_directory_variants_with_absolute_path(tmp_path, directories):
    paths = []
    for directory in directories:
        path = tmp_path / directory / "routers" / "items.py"
        path.parent.mkdir(parents=True)
        path.write_text(f'print("{directory}")\n')
        paths.append(path)
    # A sibling package without the requested relative file is not an alternative.
    other = tmp_path / "app_py311" / "routers" / "other.py"
    other.parent.mkdir(parents=True)
    other.write_text("pass\n")

    root = render(paths[0])

    assert labels(root) == [
        "Python 3.12+",
        "Python 3.12+ - non-Annotated",
    ]
    assert code_blocks(root) == [path.read_text() for path in paths]
