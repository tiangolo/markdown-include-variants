import inspect

import markdown
from inline_snapshot import snapshot
from mdx_include.mdx_include import IncludeExtension
from pymdownx.highlight import HighlightExtension
from pymdownx.superfences import SuperFencesCodeExtension

from markdown_include_variants import IncludeVariantsExtension


def test_simple_ln_hl():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1:4] hl[1:3] *}
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
            ```python hl_lines="1-3"
            {!docs_src/simple/tutorial001.py[ln:1-4]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="1-3"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_middle_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2:5] hl[2:3] *}
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
            ```python hl_lines="3-4"</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:2-5]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="2-3"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_middle_block_end_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2:5, 8:10] hl[2:3,8:10] *}
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
            ```python hl_lines="3-4 10-12"</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:2-5]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:8-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="2-3 8-10"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_middle_block_middle_block_end_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2:3,5:6,8:10] hl[2:3,5:6,8:10] *}
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
            ```python hl_lines="3-4 8-9 13-15"</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:2-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:5-6]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:8-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="2-3 5-6 8-10"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_middle_middle_block_end():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2,5:6,10] hl[2,5:6,10] *}
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
            ```python hl_lines="3 7-8 12"</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:2-2]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:5-6]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:10-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="2 5-6 10"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_first_middle_end():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1,6:8,10] hl[1,6:8,10] *}
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
            ```python hl_lines="1 5-7 11"
            {!docs_src/simple/tutorial001.py[ln:1-1]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:6-8]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:10-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="1 6-8 10"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_middle_block_end_block_hl_middle_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2:3,8:10] hl[2] *}
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
            ```python hl_lines="3"</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:2-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:8-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="2"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_middle_block_end_block_hl_end_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2:3,7:10] hl[8:9] *}
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
            ```python hl_lines="9-10"</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:2-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:7-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python hl_lines="8-9"
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_hl_middle_block_end_block_hl_end_block_include():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2:3,7:10] hl[8:9] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[
            IncludeVariantsExtension(),
            IncludeExtension(),
            SuperFencesCodeExtension(),
            HighlightExtension(),
        ],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <div class="highlight"><pre><span></span><code><span class="c1"># Code above omitted 👆</span>

            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 2&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 3&quot;</span><span class="p">)</span>

            <span class="c1"># Code here omitted 👈</span>

            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 7&quot;</span><span class="p">)</span>
            <span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 8&quot;</span><span class="p">)</span>
            </span><span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 9&quot;</span><span class="p">)</span>
            </span><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 10&quot;</span><span class="p">)</span>
            </code></pre></div></p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 1&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 2&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 3&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 4&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 5&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 6&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 7&quot;</span><span class="p">)</span>
            <span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 8&quot;</span><span class="p">)</span>
            </span><span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 9&quot;</span><span class="p">)</span>
            </span><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 10&quot;</span><span class="p">)</span>
            </code></pre></div>
            <p>////</p>
            """
        )
    )
