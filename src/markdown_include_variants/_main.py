import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal, Union

from markdown import Extension, Markdown
from markdown.preprocessors import Preprocessor


@dataclass(frozen=True)
class Variant:
    path: Path
    title: str
    is_annotated: Union[bool, None]
    version: Literal["py38", "py39", "py310"]


def calculate_variants(base_path: Path) -> dict[tuple[str, Union[bool, None]], Variant]:
    base_name = base_path.stem
    base_dir = base_path.parent
    variants: dict[tuple[str, Union[bool, None]], Variant] = {}
    an = "_an"
    py39 = "_py39"
    py310 = "_py310"
    an_p310_path = base_dir / f"{base_name}{an}{py310}.py"
    an_p39_path = base_dir / f"{base_name}{an}{py39}.py"
    an_path = base_dir / f"{base_name}{an}.py"
    p310_path = base_dir / f"{base_name}{py310}.py"
    p39_path = base_dir / f"{base_name}{py39}.py"
    if an_p310_path.exists():
        v = Variant(
            path=an_p310_path, title="Python 3.10+", is_annotated=True, version="py310"
        )
        variants[(v.version, v.is_annotated)] = v
        if p310_path.exists():
            v = Variant(
                path=p310_path,
                title="Python 3.10+ - non-Annotated",
                is_annotated=False,
                version="py310",
            )
            variants[(v.version, v.is_annotated)] = v
    elif p310_path.exists():
        v = Variant(
            path=p310_path, title="Python 3.10+", is_annotated=None, version="py310"
        )
        variants[(v.version, v.is_annotated)] = v
    if an_p39_path.exists():
        v = Variant(
            path=an_p39_path, title="Python 3.9+", is_annotated=True, version="py39"
        )
        variants[(v.version, v.is_annotated)] = v
        if p39_path.exists():
            v = Variant(
                path=p39_path,
                title="Python 3.9+ - non-Annotated",
                is_annotated=False,
                version="py39",
            )
            variants[(v.version, v.is_annotated)] = v
    elif p39_path.exists():
        v = Variant(
            path=p39_path, title="Python 3.9+", is_annotated=None, version="py39"
        )
        variants[(v.version, v.is_annotated)] = v
    if an_path.exists():
        v = Variant(
            path=an_path, title="Python 3.8+", is_annotated=True, version="py38"
        )
        variants[(v.version, v.is_annotated)] = v
        if base_path.exists():
            v = Variant(
                path=base_path,
                title="Python 3.8+ - non-Annotated",
                is_annotated=False,
                version="py38",
            )
            variants[(v.version, v.is_annotated)] = v
    elif base_path.exists():
        v = Variant(
            path=base_path, title="Python 3.8+", is_annotated=None, version="py38"
        )
        variants[(v.version, v.is_annotated)] = v
    return variants


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
            for config_match in re.finditer(re_config, configs_str):
                if config_match:
                    name = config_match.group(1)
                    ranges_str = config_match.group(2)
                    ranges = parse_lines_index(ranges_str)
                    if name == "ln":
                        include_lines.extend(ranges)
                    elif name == "hl":
                        highlight_lines.extend(ranges)
            use_hl_lines: list[tuple[int, int]] = []
            if highlight_lines:
                if include_lines:
                    include_infos = calculate_includes(include_lines, highlight_lines)
                    for info in include_infos.values():
                        use_hl_lines.extend(info.computed_hl_lines())
                else:
                    use_hl_lines = highlight_lines
            use_hl_lines_strs: list[str] = []
            for hl_line in use_hl_lines:
                if hl_line[0] == hl_line[1]:
                    use_hl_lines_strs.append(str(hl_line[0]))
                else:
                    use_hl_lines_strs.append(f"{hl_line[0]}-{hl_line[1]}")
            use_hl_lines_str = " ".join(use_hl_lines_strs)

            variants = calculate_variants(base_path)
            if len(variants) == 0:
                raise FileNotFoundError(f"Could not find any variants for {base_path}")
            sorted_variants: list[Variant] = []
            for an in [True, False, None]:
                for version in ["py310", "py39", "py38"]:
                    v = variants.get((version, an))
                    if v:
                        sorted_variants.append(v)
            assert sorted_variants
            preferred_variant = sorted_variants[0]
            content_lines = preferred_variant.path.read_text().splitlines()

            internal_block_lines: list[str] = []
            if not include_lines:
                internal_block_lines.append(
                    f"{{!{preferred_variant.path}!}}",
                )
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
                if i == len(include_lines) - 1 and line_group[1] < len(content_lines):
                    internal_block_lines.extend(
                        [
                            "",
                            "# Code below omitted 👇",
                        ]
                    )
            first_line = "```python"
            if use_hl_lines:
                first_line += f' hl_lines="{use_hl_lines_str}"'

            block_lines.extend(
                [
                    f"//// tab | {preferred_variant.title}" "",
                    first_line,
                    *internal_block_lines,
                    "```",
                    "",
                    "////",
                    "",
                ]
            )
            if include_lines:
                block_lines.extend(
                    [
                        "//// details | 👀 Full file preview",
                        "",
                        "```python",
                        f"{{!{preferred_variant.path}!}}",
                        "```",
                        "",
                        "////",
                        "",
                    ]
                )
            if len(sorted_variants) > 1:
                block_lines.extend(
                    [
                        "///// details | 🤓 Other versions and variants",
                        "",
                    ]
                )

                for variant in sorted_variants[1:]:
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
                            "```python",
                            f"{{!{variant.path}!}}",
                            "```",
                            "////",
                        ]
                    )

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
