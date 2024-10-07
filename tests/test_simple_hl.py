import inspect

import markdown
from inline_snapshot import snapshot
from mdx_include.mdx_include import IncludeExtension

from markdown_include_variants import IncludeVariantsExtension


def test_simple_hl():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py hl[1:3] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[
            IncludeVariantsExtension(),
        ],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <code>python hl_lines="1-3"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_hl_include():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py hl[1:3] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[
            IncludeVariantsExtension(),
            IncludeExtension(),
        ],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python hl_lines="1-3"
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


def test_simple_hl_one():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py hl[2 ] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[
            IncludeVariantsExtension(),
        ],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <code>python hl_lines="2"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_hl_one_middle():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py hl[2,5] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[
            IncludeVariantsExtension(),
        ],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <code>python hl_lines="2 5"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_hl_one_block_middle_end():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py hl[2,5:8,10] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[
            IncludeVariantsExtension(),
        ],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <code>python hl_lines="2 5-8 10"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )
