import inspect

import markdown
from inline_snapshot import snapshot

from markdown_include_variants import IncludeVariantsExtension


def test_all_variants_plain():
    input_md = inspect.cleandoc(
        """
        {* docs_src/only_py310_no_an_folder/app_py310/tutorial001.py *}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.10+
            <code>python
            {!docs_src/only_py310_no_an_folder/app_py310/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )
