import inspect

import markdown
from inline_snapshot import snapshot

from markdown_include_variants import IncludeVariantsExtension


def test_all_variants_plain():
    input_md = inspect.cleandoc(
        """
        {* docs_src/only_py_no_an/tutorial001_py310.py *}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.10+
            <code>python
            {!docs_src/only_py_no_an/tutorial001_py310.py!}</code></p>
            <p>////</p>
            <p>///// details | 🤓 Other versions and variants</p>
            <p>//// tab | Python 3.9+</p>
            <p><code>python
            {!docs_src/only_py_no_an/tutorial001_py39.py!}</code>
            ////
            //// tab | Python 3.8+</p>
            <p><code>python
            {!docs_src/only_py_no_an/tutorial001.py!}</code>
            ////</p>
            <p>/////</p>
            """
        )
    )
