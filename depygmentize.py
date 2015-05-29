import re
import argparse

import pygments
from pygments import lexers, formatters

#options
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", dest="in_file", required=True)
parser.add_argument("-o", "--output", dest="out_file", required=True)
parser.add_argument("-l", "--language", dest="lang_lexer", required=True)
parser.add_argument("-m", "--macroname", dest="lang_macro")
parser.add_argument("-p", "--prelude-filename", dest="prelude_filename", default="pygments_prelude.tex")

args = parser.parse_args()

in_file = args.in_file
out_file = args.out_file
lang_lexer = args.lang_lexer
if args.lang_macro:
	lang_macro = args.lang_macro
else:
	lang_macro = lang_lexer
prelude_filename = args.prelude_filename

file = open(in_file).read()

blockname = lang_macro + "code"
coqcode = r"(\\begin{%s}\n(.*?)\\end{%s})" % (blockname, blockname)

minted="""\\usepackage{minted}
\\newminted{%s}{fontsize=\\footnotesize,mathescape}
""" % lang_lexer

res = re.findall(coqcode, file, re.DOTALL) # : str * str

lexer = lexers.get_lexer_by_name(lang_lexer)
formatter = formatters.get_formatter_for_filename("toto.tex", verboptions="fontsize=\\small", mathescape=True)

# Create prelude file
prelude = open(prelude_filename, "w")
prelude.write(r"""\usepackage{fancyvrb}
\usepackage{color}""")
prelude.write(formatter.get_style_defs())

def highlight(code):
	r = pygments.highlight(code, lexer, formatter, None)
	return r[0:-1]

for (with_begin, coq) in res:
	file = file.replace(with_begin, highlight(coq))
out = open(out_file, "w")
out.write(file.replace(minted, "\\include{%s}" % prelude_filename[:-4]))
