import inspect

import markdown
from inline_snapshot import snapshot

from markdown_include_variants import IncludeVariantsExtension


def test_all_variants_plain():
    input_md = inspect.cleandoc(
        """
        {* docs_src/no_py39/tutorial001.py *}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.10+
            <code>python
            {!docs_src/no_py39/tutorial001_an_py310.py!}</code></p>
            <p>////</p>
            <p>///// details | 🤓 Other versions and variants</p>
            <p>//// tab | Python 3.8+</p>
            <p><code>python
            {!docs_src/no_py39/tutorial001_an.py!}</code>
            ////
            //// tab | Python 3.10+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/no_py39/tutorial001_py310.py!}</code>
            ////
            //// tab | Python 3.8+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/no_py39/tutorial001.py!}</code>
            ////</p>
            <p>/////</p>
            """
        )
    )
