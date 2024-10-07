import inspect

import markdown
import pytest
from inline_snapshot import snapshot
from mdx_include.mdx_include import IncludeExtension

from markdown_include_variants import IncludeVariantsExtension


def test_simple():
    input_md = inspect.cleandoc(
        """
        {*docs_src/simple/tutorial001.py*}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_space():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py *}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_extra_space():
    input_md = inspect.cleandoc(
        """
        {*  docs_src/simple/tutorial001.py   *}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_include():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py *}
        """
    )

    result = markdown.markdown(
        input_md, extensions=[IncludeVariantsExtension(), IncludeExtension()]
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            print("simple line 1")
            print("simple line 2")
            print("simple line 3")
            print("simple line 4")
            print("simple line 5")
            print("simple line 6")
            print("simple line 7")
            print("simple line 8")
            print("simple line 9")
            print("simple line 10")</p>
            <p>```</p>
            <p>////</p>
            """
        )
    )


def test_simple_no_directive():
    input_md = inspect.cleandoc(
        """
        {! docs_src/simple/tutorial001.py !}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot("<p>{! docs_src/simple/tutorial001.py !}</p>")


def test_simple_no_variants():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial002.py *}
        """
    )
    with pytest.raises(FileNotFoundError):
        markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
