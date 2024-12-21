import inspect

import markdown
from inline_snapshot import snapshot

from markdown_include_variants import IncludeVariantsExtension


def test_only_preview():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[0] *}
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
            <p>///// details | 👀 Full file preview</p>
            <p>//// tab | Python 3.8+</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            <p>/////</p>
            """
        )
    )
