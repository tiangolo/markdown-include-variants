# markdown-include-variants

<a href="https://github.com/tiangolo/markdown-include-variants/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/markdown-include-variants/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://coverage-badge.samuelcolvin.workers.dev/redirect/tiangolo/markdown-include-variants" target="_blank">
    <img src="https://coverage-badge.samuelcolvin.workers.dev/tiangolo/markdown-include-variants.svg" alt="Coverage">
<a href="https://pypi.org/project/markdown-include-variants" target="_blank">
    <img src="https://img.shields.io/pypi/v/markdown-include-variants?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

---

## 🚨 Warning: Internal Project

This is an internal project, it is mainly useful for the docs in [@tiangolo](https://github.com/tiangolo)'s projects (e.g. all the [FastAPI](https://github.com/fastapi) projects).

It is probably **not useful** to you. You should probably not use it. 😅

There are no guarantees about behavior, it is made to suit the needs of these projects, to simplify writing documentation.

## How to Use

If you're still here it's probably because you are getting involved in one of the projects that use it. 🤓

Here's how it works. 🚀

### Configure Plugin in MkDocs Material

Make sure `mkdocs.yml` has a section with at least these configs:

```yaml
markdown_extensions:
  # Python Markdown Extensions
  pymdownx.highlight:
  pymdownx.superfences:

  # pymdownx blocks
  pymdownx.blocks.admonition:
    types:
    - tip
  pymdownx.blocks.details:
  pymdownx.blocks.tab:
    alternate_style: True

  # Other extensions
  mdx_include:
  markdown_include_variants:
```

The last config is the one specific to this extension, `markdown-include-variants`.

The other configs are for the extensions that actually render the output, this extension (`markdown-include-variants`) just generates the content to be rendered by those other extensions.

### Workflow

* You add a Python source example to the `docs_src` directory, with the minimum Python version supported by the project, and using `Annotated` where applicable, named something like `tutorial001.py`.
* If a non-Annotated alternative is useful, copy the file and name it with the suffix `_non_an`, like: `tutorial001_non_an.py`.
* If an example needs alternatives for different Python versions, give every variant an explicit Python version suffix, like `tutorial001_py311.py`, `tutorial001_py312.py`, and `tutorial001_non_an_py312.py`.
* In the Markdown file, include the preferred version of the file, using this syntax:

```markdown
{* ./docs_src/first_steps/tutorial001.py *}
```

That will be automatically expanded with [mdx-include](https://github.com/neurobin/mdx_include) to include the other variants below in a collapsed `details` box.

### Variant Names

| Filename | Display |
| --- | --- |
| `tutorial001.py` | Code block |
| `tutorial001_non_an.py` | non-Annotated |
| `tutorial001_py312.py` | Python 3.12+ |
| `tutorial001_non_an_py312.py` | Python 3.12+ - non-Annotated |

Examples without a version suffix target the project's supported Python versions. An explicit version suffix keeps its label even for a single file. Every variant of the same example must either have a Python version suffix or be unversioned.

### Directory Variants

For examples spanning multiple files, use the same suffixes on directories, such as `app` and `app_non_an`:

```markdown
{* ./docs_src/bigger_applications/app/routers/items.py title["app/routers/items.py"] *}
```

The extension finds the same relative file in each directory variant, including nested files. Use `title` to display a filename above the code block.

### Include Lines

To include specific line ranges, use the config `ln`:

```markdown
{* ./docs_src/first_steps/tutorial001.py ln[3:6,8,10:11] *}
```

That will include only:

* lines 3 to 6
* line 8
* lines 10 to 11

It will add blocks with comments in the middle like:

```python
# Code here omitted 👈️
```

If you include specific lines, it will also add another collapsed `details` box with the "Full file preview".

### Highlight Lines

You can highlight specific lines using the config `hl`:

```markdown
{* ./docs_src/first_steps/tutorial001.py hl[3,5:7,10] *}
```

That will highlight:

* line 3
* lines 5 to 7
* line 10

Have in mind that the main file shown will be the one named in the include, and the highlights will apply to that file.

So, when deciding which lines to highlight, do that based on the file you include.

### Include Lines and Highlight

You can combine both `ln` and `hl`:

```markdown
{* ./docs_src/first_steps/tutorial001.py ln[3:6,8,10:11] hl[3,5:6,10] *}
```

The highlighted lines refer to the source file (for the included version), not the final rendered code block.

This makes it easier to decide which lines to highlight just by opening the source file, without having to calculate the actual lines in the rendered block after included, the extra lines for comments when omitting lines, etc.

### Include Lines and Highlight - Example

For example, you could have a source file with:

```python
print("line 1")
print("line 2")
print("line 3")
print("line 4")
print("line 5")
print("line 6")  # highlight this
print("line 7")
```

Using a declaration like this:

```markdown
{* ./docs_src/first_steps/tutorial001.py ln[5:7] hl[6] *}
```

Could render something like:

```python
# Code above omitted 👈️

print("line 5")
print("line 6")  # highlight this
print("line 7")
```

Notice that the comment above adds 2 extra lines, and only the desired lines are included, the result is that the actual highlighted line is the rendered line 4, but the source line 6, it's all calculated automatically. 🤓

### Include Only File Preview

If you only want to generate the "File Preview" collapsed details section, without actually including a tab of source files, you can use `ln[0]`:

```markdown
{* ./docs_src/first_steps/tutorial001.py ln[0] *}
```

This is useful for example at the beginning of a new page, in a recap of the last used file in the previous page.

### Migrating Existing Examples

Legacy `_an` names still work: `tutorial001_an.py` is recommended and its bare counterpart, `tutorial001.py`, is non-Annotated. This also applies to directory variants and pairs with matching Python versions.

Rename both sides of a pair together:

| Existing filename | New filename |
| --- | --- |
| `tutorial001_py310.py` | `tutorial001_non_an.py` |
| `tutorial001_an_py310.py` | `tutorial001.py` |

Keep explicit versions where alternatives still need them. Use `_py38` for files previously relying on the implicit Python 3.8 version.

Update includes, test imports, configuration, and scripts to match. Each example family must use either the legacy `_an` convention or the new `_non_an` convention.

## License

This project is licensed under the terms of the [MIT license](https://github.com/tiangolo/markdown-include-variants/blob/main/LICENSE).
