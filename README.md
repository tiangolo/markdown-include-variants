# markdown-include-variants

<a href="https://github.com/tiangolo/markdown-include-variants/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/tiangolo/markdown-include-variants/workflows/Test/badge.svg" alt="Test">
</a>
<a href="https://github.com/tiangolo/markdown-include-variants/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/tiangolo/markdown-include-variants/workflows/Publish/badge.svg" alt="Publish">
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

* You add a Python source example to the `docs_src` directory, with the minimum Python version supported by the project, and using the old format without `Annotated`, if that applies, it would be named something like `tutorial001.py`.
* Copy the file and update it to use `Annotated` (if that applies), and name the file with a "tag" (a prefix) of `_an`, like: `tutorial001_an.py`.
* Run the internal script to generate the variants of the files for superior versions of Python, like `3.9`, `3.10`, etc. (this internal script is in the project itself). This would generate files like `tutorial001_py39.py`, `tutorial001_py310.py`, etc. and `tutorial001_an_py39.py`, `tutorial001_an_py310.py`, etc.
* In the Markdown file, include the preferred version of the file, using this syntax:

```markdown
{* ./docs_src/first_steps/tutorial001_an_py310.py *}
```

That will be automatically expanded with [mdx-include](https://github.com/neurobin/mdx_include) to include the other variants below in a collapsed `details` box.

### Include Lines

To include specific line ranges, use the config `ln`:

```markdown
{* ./docs_src/first_steps/tutorial001_an_py310.py ln[3:6,8,10:11] *}
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
{* ./docs_src/first_steps/tutorial001_an_py310.py hl[3,5:7,10] *}
```

That will highlight:

* line 3
* lines 5 to 7
* line 10

Have in mind that the file path points to the simplest version of the file, the one without the `_an` suffix. But the main file shown will be the highest (recommended) version, and the highlights will apply to that file.

So, when deciding which lines to highlight, do that based on the highest version of the file.

### Include Lines and Highlight

You can combine both `ln` and `hl`:

```markdown
{* ./docs_src/first_steps/tutorial001_an_py310.py ln[3:6,8,10:11] hl[3,5:6,10] *}
```

The highlighted lines refer to the source file (for the highest/recommended version), not the final rendered code block.

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
{* ./docs_src/first_steps/tutorial001_an_py310.py ln[5:7] hl[6] *}
```

Could render something like:

```python
# Code above omitted 👈️

print("line 5")
print("line 6")  # highlight this
print("line 7")
```

Notice that the comment above adds 2 extra lines, and only the desired lines are included, the result is that the actual highlighted line is the rendered line 4, but the source line 6, it's all calculated automatically. 🤓

## License

This project is licensed under the terms of the [MIT license](https://github.com/tiangolo/markdown-include-variants/blob/main/LICENSE).
