import inspect

import markdown
from inline_snapshot import snapshot
from mdx_include.mdx_include import IncludeExtension
from pymdownx.superfences import SuperFencesCodeExtension

from markdown_include_variants import IncludeVariantsExtension


def test_simple_ln():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1:3] *}
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
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-3]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_include():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1:3] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[
            IncludeVariantsExtension(),
            IncludeExtension(),
            SuperFencesCodeExtension(),
        ],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            <div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 1&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 2&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 3&quot;</span><span class="p">)</span>

            <span class="c1"># Code below omitted 👇</span>
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
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 8&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 9&quot;</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">&quot;simple line 10&quot;</span><span class="p">)</span>
            </code></pre></div>
            <p>////</p>
            """
        )
    )


def test_simple_ln_one():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-1]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_one_include():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension(), IncludeExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            print("simple line 1")</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p>```python
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


def test_simple_ln_one_below():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[3] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:3-3]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_one_last():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[10] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:10-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_block_below():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[2:4] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:2-4]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_block_last():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[8:10] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:8-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_first_middle():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1, 3] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-1]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:3-3]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_first_middle_last():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1, 3,10 ] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-1]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:3-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:10-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_middle_middle():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[3,8 ] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:3-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:8-8]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_first_block_middle_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1:3, 5:7] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:5-7]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_first_block_middle_block_last_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1:3, 5:7,9:10] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:5-7]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:9-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_first_block_middle_last_block():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1:3, 5,9:10] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-3]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:5-5]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:9-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )


def test_simple_ln_first_middle_block_last():
    input_md = inspect.cleandoc(
        """
        {* docs_src/simple/tutorial001.py ln[1, 5:7,10] *}
        """
    )

    result = markdown.markdown(
        input_md,
        extensions=[IncludeVariantsExtension()],
    )
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.8+
            ```python
            {!docs_src/simple/tutorial001.py[ln:1-1]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:5-7]!}</p>
            <h1>Code here omitted 👈</h1>
            <p>{!docs_src/simple/tutorial001.py[ln:10-10]!}
            ```</p>
            <p>////</p>
            <p>//// details | 👀 Full file preview</p>
            <p><code>python
            {!docs_src/simple/tutorial001.py!}</code></p>
            <p>////</p>
            """
        )
    )
