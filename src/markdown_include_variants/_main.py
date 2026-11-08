import re
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor

re_variant_suffix = re.compile(r"(_non_an|_an)?(?:_py([1-9])(0|[1-9][0-9]*))?$")


@dataclass(frozen=True)
class Variant:
    path: Path
    # None is the default format, True is the legacy _an marker, and False
    # identifies a non-Annotated variant.
    is_annotated: bool | None
    version: tuple[int, int] | None

    @property
    def title(self) -> str:
        parts = []
        if self.version is not None:
            major, minor = self.version
            parts.append(f"Python {major}.{minor}+")
        if self.is_annotated is False:
            parts.append("non-Annotated")
        return " - ".join(parts)


def parse_variant_name(
    name: str,
) -> tuple[str, bool | None, tuple[int, int] | None]:
    match = re_variant_suffix.search(name)
    assert match is not None
    version = None
    if match[2] is not None:
        version = (int(match[2]), int(match[3]))
    is_annotated = None
    if match[1] is not None:
        is_annotated = match[1] == "_an"
    return name[: match.start()], is_annotated, version


def calculate_variants(base_path: Path) -> list[Variant]:
    if not base_path.is_file():
        raise FileNotFoundError(f"Included file does not exist: {base_path}")

    # Look for filename variants first, then variants of the nearest containing
    # directory. Keep the relative path inside directory variants, including
    # nested files such as app_non_an/routers/items.py.
    for variant_path in (base_path, *base_path.parents):
        if not variant_path.name:
            break
        is_file = variant_path == base_path
        name = variant_path.stem if is_file else variant_path.name
        base_name, is_annotated, version = parse_variant_name(name)
        variants = []
        for sibling in variant_path.parent.iterdir():
            if is_file:
                if sibling.suffix != base_path.suffix:
                    continue
                sibling_name = sibling.stem
                source_path = sibling
            else:
                sibling_name = sibling.name
                source_path = sibling / base_path.relative_to(variant_path)
            sibling_base, sibling_annotated, sibling_version = parse_variant_name(
                sibling_name
            )
            if sibling_base == base_name and source_path.is_file():
                variants.append(
                    Variant(
                        path=source_path,
                        is_annotated=sibling_annotated,
                        version=sibling_version,
                    )
                )
        if len(variants) > 1 or is_annotated is not None or version is not None:
            annotations = {variant.is_annotated for variant in variants}
            if True in annotations and False in annotations:
                raise ValueError(
                    f"Cannot mix legacy _an and _non_an variants for {base_path}. "
                    "Migrate the whole example family to _non_an together."
                )
            versions = {variant.version for variant in variants}
            if None in versions and len(versions) > 1:
                raise ValueError(
                    f"Cannot mix versioned and unversioned variants for {base_path}. "
                    "Add a Python version suffix to every variant, or remove all "
                    "Python version suffixes."
                )
            # In the legacy convention, the bare counterpart of an _an file
            # is non-Annotated. Keep that interpretation for each Python version.
            legacy_versions = {
                variant.version for variant in variants if variant.is_annotated is True
            }
            variants = [
                replace(variant, is_annotated=False)
                if variant.is_annotated is None and variant.version in legacy_versions
                else variant
                for variant in variants
            ]
            return sorted(
                variants,
                key=lambda variant: (
                    variant.is_annotated is not False,
                    variant.version or (0, 0),
                ),
                reverse=True,
            )
    return [Variant(path=base_path, is_annotated=None, version=None)]


def wrap_tab(lines: list[str], title: str) -> list[str]:
    if title:
        return [f"//// tab | {title}", *lines, "", "////", ""]
    return [*lines, ""]


def parse_lines_index(include_lines_config: str) -> list[tuple[int, int]]:
    lines = []
    for line in include_lines_config.strip().split(","):
        clean_line = line.strip()
        if ":" in clean_line:
            start, end = clean_line.split(":")
            lines.append((int(start), int(end)))
        else:
            lines.append((int(line), int(line)))
    lines.sort()
    return lines


@dataclass
class IncludeInfo:
    start: int
    end: int
    offset: int
    hl_lines: list[tuple[int, int]]

    def computed_hl_lines(self) -> list[tuple[int, int]]:
        return [
            (
                hl_line[0] - self.start + self.offset + 1,
                hl_line[1] - self.start + self.offset + 1,
            )
            for hl_line in self.hl_lines
        ]


def calculate_includes(
    lines_to_include: list[tuple[int, int]], hl_lines: list[tuple[int, int]]
) -> dict[tuple[int, int], IncludeInfo]:
    lines_groups: dict[tuple[int, int], IncludeInfo] = {}
    offset = 0
    for i, line_group in enumerate(lines_to_include):
        if line_group[0] > 1:
            if i == 0:
                offset = 2
            else:
                offset += 3
        info = IncludeInfo(
            start=line_group[0],
            end=line_group[1],
            offset=offset,
            hl_lines=[],
        )
        offset += line_group[1] - line_group[0] + 1
        for hl_line in hl_lines:
            if hl_line[0] >= line_group[0] and hl_line[1] <= line_group[1]:
                info.hl_lines.append(hl_line)
        lines_groups[line_group] = info
    return lines_groups


def generate_hl_string(hl_lines: list[tuple[int, int]]) -> str:
    hl_lines_strs: list[str] = []
    for hl_line in hl_lines:
        if hl_line[0] == hl_line[1]:
            hl_lines_strs.append(str(hl_line[0]))
        else:
            hl_lines_strs.append(f"{hl_line[0]}-{hl_line[1]}")
    return " ".join(hl_lines_strs)


re_line = r"^\{\*\s*(\S+)\s*(.*)\*\}$"
re_config = r"(\w+)\[([^\]]+)\]"


class IncludeVariantsPreprocessor(Preprocessor):
    def run(self, lines: list[str]) -> list[str]:
        new_lines = []
        for line in lines:
            line_match = re.match(re_line, line)
            if not line_match:
                new_lines.append(line)
                continue
            block_lines = []
            src_file_str = line_match.group(1)
            base_path = Path(src_file_str)

            configs_str = line_match.group(2).strip()
            include_lines: list[tuple[int, int]] = []
            highlight_lines: list[tuple[int, int]] = []
            title: str | None = None
            for config_match in re.finditer(re_config, configs_str):
                if config_match:
                    name = config_match.group(1)
                    value_str = config_match.group(2)
                    if name == "ln":
                        include_lines.extend(parse_lines_index(value_str))
                    elif name == "hl":
                        highlight_lines.extend(parse_lines_index(value_str))
                    elif name == "title":
                        assert value_str.startswith('"') and value_str.endswith('"')
                        title = value_str[1:-1]
            use_hl_lines: list[tuple[int, int]] = []
            if highlight_lines:
                if include_lines:
                    include_infos = calculate_includes(include_lines, highlight_lines)
                    for info in include_infos.values():
                        use_hl_lines.extend(info.computed_hl_lines())
                else:
                    use_hl_lines = highlight_lines
            use_hl_lines_str = generate_hl_string(use_hl_lines)

            variants = calculate_variants(base_path)
            preferred_variant = next(v for v in variants if v.path == base_path)
            sorted_variants = [v for v in variants if v.path != base_path]
            preferred_title = preferred_variant.title
            content_lines = preferred_variant.path.read_text().splitlines()

            internal_block_lines: list[str] = []
            if not include_lines:
                internal_block_lines.append(
                    f"{{!{preferred_variant.path}!}}",
                )
            if include_lines != [(0, 0)]:
                for i, line_group in enumerate(include_lines):
                    if i == 0 and line_group[0] > 1:
                        internal_block_lines.extend(
                            [
                                "# Code above omitted 👆",
                                "",
                            ]
                        )
                    if i >= 1:
                        internal_block_lines.extend(
                            [
                                "",
                                "# Code here omitted 👈",
                                "",
                            ]
                        )
                    internal_block_lines.append(
                        f"{{!{preferred_variant.path}[ln:{line_group[0]}-{line_group[1]}]!}}"
                    )
                    if i == len(include_lines) - 1 and line_group[1] < len(
                        content_lines
                    ):
                        internal_block_lines.extend(
                            [
                                "",
                                "# Code below omitted 👇",
                            ]
                        )
                first_line = "```python"
                if use_hl_lines:
                    first_line += f' hl_lines="{use_hl_lines_str}"'
                if title:
                    first_line += f' title="{title}"'

                block_lines.extend(
                    wrap_tab(
                        [first_line, *internal_block_lines, "```"],
                        preferred_title,
                    )
                )
            if include_lines:
                first_line_full = "```python"
                if highlight_lines:
                    hl_lines_full_str = generate_hl_string(highlight_lines)
                    first_line_full += f' hl_lines="{hl_lines_full_str}"'
                if title:
                    first_line_full += f' title="{title}"'
                block_lines.extend(
                    [
                        "///// details | 👀 Full file preview",
                        "",
                        *wrap_tab(
                            [
                                first_line_full,
                                f"{{!{preferred_variant.path}!}}",
                                "```",
                            ],
                            preferred_title,
                        ),
                        "/////",
                        "",
                    ]
                )
            if len(sorted_variants):
                first_line_variant = "```python"
                if title:
                    first_line_variant += f' title="{title}"'
                block_lines.extend(
                    [
                        "///// details | 🤓 Other versions and variants",
                        "",
                    ]
                )

                for variant in sorted_variants:
                    if variant.title:
                        block_lines.extend([f"//// tab | {variant.title}", ""])
                    if variant.is_annotated is False:
                        block_lines.extend(
                            [
                                "/// tip",
                                "",
                                "Prefer to use the `Annotated` version if possible.",
                                "",
                                "///",
                                "",
                            ]
                        )

                    block_lines.extend(
                        [
                            first_line_variant,
                            f"{{!{variant.path}!}}",
                            "```",
                        ]
                    )
                    if variant.title:
                        block_lines.append("////")

                block_lines.extend(
                    [
                        "",
                        "/////",
                        "",
                    ]
                )
            new_lines.extend(block_lines)
        return new_lines


class IncludeVariantsExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.preprocessors.register(
            IncludeVariantsPreprocessor(md), "include_variants", 110
        )


def makeExtension(
    *args: Any, **kwargs: Any
) -> IncludeVariantsExtension:  # pragma: no cover
    return IncludeVariantsExtension(*args, **kwargs)
