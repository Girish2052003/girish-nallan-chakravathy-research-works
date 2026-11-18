"""Rebuild the PDF from the four Markdown sources using Pandoc 3 and XeLaTeX."""

from pathlib import Path
import posixpath
import re
import shutil
import subprocess
import tempfile


HERE = Path(__file__).resolve().parent
REPO = 'https://github.com/Girish2052003/girish-nallan-chakravathy-research-works/blob/main/'
APPENDICES = [('OBSTRUCTION.md', 'obstruction'), ('TWO_VIEW_BOUND.md', 'two-views'),
              ('RELATED_WORK.md', 'related-work')]
ANCHORS = {'README.md': 'main-note', **dict(APPENDICES)}

HEADER = r'''
\usepackage{titlesec,fancyhdr,needspace}
\definecolor{ink}{HTML}{142B37}
\definecolor{accent}{HTML}{21666D}
\definecolor{secondary}{HTML}{49616C}
\titleformat{\section}{\large\sffamily\bfseries\color{ink}}{}{0pt}{}
\titleformat{\subsection}{\normalsize\sffamily\bfseries\color{ink}}{}{0pt}{}
\titlespacing*{\section}{0pt}{2.3ex plus .5ex minus .3ex}{.8ex}
\titlespacing*{\subsection}{0pt}{1.8ex plus .4ex minus .2ex}{.5ex}
\setlength{\parskip}{4pt plus .8pt minus .8pt}
\setlength{\parindent}{0pt}
\setlength{\headheight}{15pt}
\setlength{\LTpre}{4pt}\setlength{\LTpost}{5pt}
\setlength{\emergencystretch}{1.5em}
\renewcommand{\arraystretch}{1.12}
\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\footnotesize\sffamily\color{secondary}SG-DIFRA research note}
\fancyhead[R]{\footnotesize\sffamily\color{secondary}Local differential collisions}
\fancyfoot[R]{\footnotesize\sffamily\thepage}
\renewcommand{\headrulewidth}{0pt}
\widowpenalty=7000 \clubpenalty=7000 \raggedbottom
\AtBeginDocument{\hypersetup{pdftitle={Local strategies for ternary differential collisions},
 pdfsubject={SG-DIFRA mathematical research note},colorlinks=true,
 linkcolor=accent,urlcolor=accent}}
'''


def links(text):
    """Use PDF destinations for included notes and public URLs for other files."""
    def resolve(match):
        target = match[1]
        if target in ANCHORS:
            return '](#' + ANCHORS[target] + ')'
        if target.startswith(('https:', 'http:', '#', 'mailto:')):
            return match[0]
        return '](' + REPO + posixpath.normpath('research-2028/round10/' + target) + ')'
    return re.sub(r'\]\(([^()\s]+)\)', resolve, text)


def markdown():
    title, body = (HERE / 'README.md').read_text().split('\n', 1)
    # The dated source label is typeset once in the masthead.
    body = re.sub(r'^\*\*SG-DIFRA mathematical research note, [^\n]+\*\*\n', '', body, flags=re.M)
    # This quantified definition is one display in the source. Break its
    # three existing lines at the same mathematical boundaries for typesetting.
    def break_definition(match):
        lines = match[1].strip().splitlines()
        return '$$\n\\begin{gathered}\n' + r'\\'.join(lines) + '\n\\end{gathered}\n$$'
    body = re.sub(r'\$\$\n(\\exists f:.*?\n)\$\$', break_definition, body, count=1, flags=re.S)
    body = re.sub(r'^## ', '# ', body, flags=re.M)
    body = re.sub(r'(?m)^(\*\*(?:Theorem 1|Proposition 2))', lambda m: r'\Needspace{6\baselineskip}' + '\n\n' + m[1], body)
    body = body.replace('| Input and observation restriction | Complexity |\n| --- | --- |',
                        '| Input and observation restriction | Complexity |\n| ' + '-' * 56 + ' | ' + '-' * 20 + ' |')
    title = title.removeprefix('# ')
    masthead = '\n'.join([
        '```{=latex}', r'\thispagestyle{empty}', r'\phantomsection\label{main-note}',
        r'\pdfbookmark[1]{' + title + r'}{note-title}',
        r'{\small\sffamily\bfseries\color{accent}SG-DIFRA RESEARCH NOTE}\par',
        r'\vspace{3pt}{\raggedright\fontsize{23}{26}\selectfont\sffamily\bfseries\color{ink}'
        + title.replace('differential collisions', r'\mbox{differential collisions}') + r'\par}',
        r'{\small\sffamily\color{secondary}18 November 2026}\par\vspace{4pt}',
        '```', '', '',
    ])
    parts = [masthead + body]
    for letter, (filename, anchor) in zip('ABC', APPENDICES):
        title, body = (HERE / filename).read_text().split('\n', 1)
        parts.extend([r'\clearpage', f'# Appendix {letter}. {title[2:]} {{#{anchor}}}', body])
    return links('\n\n'.join(parts))


def build():
    with tempfile.TemporaryDirectory(prefix='sg-difra-paper-') as tmp:
        work = Path(tmp)
        (work / 'note.md').write_text(markdown())
        (work / 'style.tex').write_text(HEADER)
        options = ['--variable', 'papersize=a4', '--variable', 'fontsize=11pt',
                   '--variable', 'geometry=top=22mm,bottom=23mm,left=26mm,right=26mm',
                   '--variable', 'mainfont=Latin Modern Roman', '--variable', 'sansfont=Latin Modern Sans',
                   '--variable', 'monofont=Latin Modern Mono', '--variable', 'mathfont=Latin Modern Math']
        subprocess.run(['pandoc', 'note.md', '--from=markdown+tex_math_single_backslash',
                        '--standalone', '-t', 'latex', '-o', 'note.tex', '--include-in-header=style.tex',
                        *options], cwd=work, check=True)
        for _ in range(2):
            run = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'note.tex'],
                                 cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            if run.returncode:
                raise RuntimeError('\n'.join(run.stdout.splitlines()[-35:]))
        warnings = [line for line in (work / 'note.log').read_text().splitlines()
                    if 'Overfull' in line or 'Missing character:' in line]
        if warnings:
            raise RuntimeError('Check typesetting:\n' + '\n'.join(warnings))
        shutil.copyfile(work / 'note.pdf', HERE / 'local_differential_collisions.pdf')


if __name__ == '__main__':
    build()
