import inspect

import markdown
from inline_snapshot import snapshot
from mdx_include.mdx_include import IncludeExtension
from pymdownx.highlight import HighlightExtension
from pymdownx.superfences import SuperFencesCodeExtension

from markdown_include_variants import IncludeVariantsExtension


def test_all_variants_plain():
    input_md = inspect.cleandoc(
        """
        {* docs_src/all_variants_folder/app_an_py311/tutorial001.py *}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.11+
            <code>python
            {!docs_src/all_variants_folder/app_an_py311/tutorial001.py!}</code></p>
            <p>////</p>
            <p>///// details | 🤓 Other versions and variants</p>
            <p>//// tab | Python 3.10+</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_an_py310/tutorial001.py!}</code>
            ////
            //// tab | Python 3.9+</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_an_py39/tutorial001.py!}</code>
            ////
            //// tab | Python 3.8+</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_an/tutorial001.py!}</code>
            ////
            //// tab | Python 3.11+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_py311/tutorial001.py!}</code>
            ////
            //// tab | Python 3.10+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_py310/tutorial001.py!}</code>
            ////
            //// tab | Python 3.9+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_py39/tutorial001.py!}</code>
            ////
            //// tab | Python 3.8+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app/tutorial001.py!}</code>
            ////</p>
            <p>/////</p>
            """
        )
    )


def test_all_variants_ln_hl():
    input_md = inspect.cleandoc(
        """
        {* docs_src/all_variants_folder/app_an_py311/tutorial001.py ln[3:5] hl[4:5] *}
        """
    )

    result = markdown.markdown(input_md, extensions=[IncludeVariantsExtension()])
    assert result == snapshot(
        inspect.cleandoc(
            """
            <p>//// tab | Python 3.11+
            ```python hl_lines="4-5"</p>
            <h1>Code above omitted 👆</h1>
            <p>{!docs_src/all_variants_folder/app_an_py311/tutorial001.py[ln:3-5]!}</p>
            <h1>Code below omitted 👇</h1>
            <p>```</p>
            <p>////</p>
            <p>///// details | 👀 Full file preview</p>
            <p>//// tab | Python 3.11+</p>
            <p><code>python hl_lines="4-5"
            {!docs_src/all_variants_folder/app_an_py311/tutorial001.py!}</code></p>
            <p>////</p>
            <p>/////</p>
            <p>///// details | 🤓 Other versions and variants</p>
            <p>//// tab | Python 3.10+</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_an_py310/tutorial001.py!}</code>
            ////
            //// tab | Python 3.9+</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_an_py39/tutorial001.py!}</code>
            ////
            //// tab | Python 3.8+</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_an/tutorial001.py!}</code>
            ////
            //// tab | Python 3.11+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_py311/tutorial001.py!}</code>
            ////
            //// tab | Python 3.10+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_py310/tutorial001.py!}</code>
            ////
            //// tab | Python 3.9+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app_py39/tutorial001.py!}</code>
            ////
            //// tab | Python 3.8+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><code>python
            {!docs_src/all_variants_folder/app/tutorial001.py!}</code>
            ////</p>
            <p>/////</p>
            """
        )
    )


def test_all_variants_ln_hl_include():
    input_md = inspect.cleandoc(
        """
        {* docs_src/all_variants_folder/app_an_py311/tutorial001.py ln[3:5] hl[4:5] *}
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
            <p>//// tab | Python 3.11+
            <div class="highlight"><pre><span></span><code><span class="c1"># Code above omitted 👆</span>

            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 3"</span><span class="p">)</span>
            <span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 4"</span><span class="p">)</span>
            </span><span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 5"</span><span class="p">)</span>
            </span>
            <span class="c1"># Code below omitted 👇</span>
            </code></pre></div></p>
            <p>////</p>
            <p>///// details | 👀 Full file preview</p>
            <p>//// tab | Python 3.11+</p>
            <div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 3"</span><span class="p">)</span>
            <span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 4"</span><span class="p">)</span>
            </span><span class="hll"><span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 5"</span><span class="p">)</span>
            </span><span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py311 line 10"</span><span class="p">)</span>
            </code></pre></div>
            <p>////</p>
            <p>/////</p>
            <p>///// details | 🤓 Other versions and variants</p>
            <p>//// tab | Python 3.10+</p>
            <p><div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 3"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 4"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 5"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py310 line 10"</span><span class="p">)</span>
            </code></pre></div>
            ////
            //// tab | Python 3.9+</p>
            <p><div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 3"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 4"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 5"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an py39 line 10"</span><span class="p">)</span>
            </code></pre></div>
            ////
            //// tab | Python 3.8+</p>
            <p><div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"an line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 3"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 4"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 5"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"an line 10"</span><span class="p">)</span>
            </code></pre></div>
            ////
            //// tab | Python 3.11+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 3"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 4"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 5"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py311 line 10"</span><span class="p">)</span>
            </code></pre></div>
            ////
            //// tab | Python 3.10+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 3"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 4"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 5"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py310 line 10"</span><span class="p">)</span>
            </code></pre></div>
            ////
            //// tab | Python 3.9+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 3"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 4"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 5"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"py39 line 10"</span><span class="p">)</span>
            </code></pre></div>
            ////
            //// tab | Python 3.8+ - non-Annotated</p>
            <p>/// tip</p>
            <p>Prefer to use the <code>Annotated</code> version if possible.</p>
            <p>///</p>
            <p><div class="highlight"><pre><span></span><code><span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 1"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 2"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 3"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 4"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 5"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 6"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 7"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 8"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 9"</span><span class="p">)</span>
            <span class="nb">print</span><span class="p">(</span><span class="s2">"simple line 10"</span><span class="p">)</span>
            </code></pre></div>
            ////</p>
            <p>/////</p>
            """
        )
    )
