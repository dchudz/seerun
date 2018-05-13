import html
import io
from collections import defaultdict

from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import Python3Lexer

from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self, *args, start_position=0, **kwargs):
        super().__init__(*args, **kwargs)

        # positions (in original text) & what to insert before
        self.start_classes = {}
        self.current_position = start_position

    def handle_starttag(self, tag, attrs):
        if tag == 'div':
            assert attrs == [('class', 'highlight')]
            return
        if tag == 'pre':
            assert not attrs, "{} {}".format(tag, attrs)
            return
        assert tag == 'span', "{} {}".format(tag, attrs)
        if not attrs:
            return

        # we assume there's only one attr and it's a class -- revisit if that fails
        assert len(attrs) == 1
        attr_name, value = attrs[0]
        assert attr_name == 'class'

        # assume we only get one start tag at any given position
        assert self.current_position not in self.start_classes

        self.start_classes[self.current_position] = value

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        self.current_position += len(data)


def get_classes_by_start(code):
    """Returns a dictionary mapping positions in the code to html equivalent to what Pygments would
    insert prior to that position."""
    lexer = Python3Lexer()
    formatter = HtmlFormatter()

    # pygments seems to ignore initial newlines (etc.?), so to line up with all our other stuff,
    # we need to shift the starting position by that much
    start_position = len(code) - len(code.lstrip())
    parser = MyHTMLParser(start_position=start_position)

    tokens = lexer.get_tokens(code.lstrip())
    pygments_html = io.StringIO()
    formatter.format(tokens, pygments_html)
    pygments_html.seek(0)
    html = pygments_html.read()
    parser.feed(html)

    # not really sure why these are different by 1, but let's make sure we find out about it if
    # that changes
    assert parser.current_position== len(code) + 1, 'code is length {}, parser ended up at {}'.format(len(code), parser.current_position)
    return parser.start_classes


def get_style_defs():
    """Our own version of the pygments style defines, b/c we don't want anything bolded.

    (For us, bold means "has a value we recorded", so boldness in here would confuse things.)

    The originals can be obtained as: HtmlFormatter().get_style_defs()
    """
    return """
.hll { background-color: #ffffcc }
.c { color: #408080; font-style: italic } /* Comment */
.err { border: 1px solid #FF0000 } /* Error */
.k { color: #008000;} /* Keyword */
.o { color: #666666 } /* Operator */
.ch { color: #408080; font-style: italic } /* Comment.Hashbang */
.cm { color: #408080; font-style: italic } /* Comment.Multiline */
.cp { color: #BC7A00 } /* Comment.Preproc */
.cpf { color: #408080; font-style: italic } /* Comment.PreprocFile */
.c1 { color: #408080; font-style: italic } /* Comment.Single */
.cs { color: #408080; font-style: italic } /* Comment.Special */
.gd { color: #A00000 } /* Generic.Deleted */
.ge { font-style: italic } /* Generic.Emph */
.gr { color: #FF0000 } /* Generic.Error */
.gh { color: #000080;} /* Generic.Heading */
.gi { color: #00A000 } /* Generic.Inserted */
.go { color: #888888 } /* Generic.Output */
.gp { color: #000080;} /* Generic.Prompt */
.gs {} /* Generic.Strong */
.gu { color: #800080;} /* Generic.Subheading */
.gt { color: #0044DD } /* Generic.Traceback */
.kc { color: #008000;} /* Keyword.Constant */
.kd { color: #008000;} /* Keyword.Declaration */
.kn { color: #008000;} /* Keyword.Namespace */
.kp { color: #008000 } /* Keyword.Pseudo */
.kr { color: #008000;} /* Keyword.Reserved */
.kt { color: #B00040 } /* Keyword.Type */
.m { color: #666666 } /* Literal.Number */
.s { color: #BA2121 } /* Literal.String */
.na { color: #7D9029 } /* Name.Attribute */
.nb { color: #008000 } /* Name.Builtin */
.nc { color: #0000FF;} /* Name.Class */
.no { color: #880000 } /* Name.Constant */
.nd { color: #AA22FF } /* Name.Decorator */
.ni { color: #999999;} /* Name.Entity */
.ne { color: #D2413A;} /* Name.Exception */
.nf { color: #0000FF } /* Name.Function */
.nl { color: #A0A000 } /* Name.Label */
.nn { color: #0000FF;} /* Name.Namespace */
.nt { color: #008000;} /* Name.Tag */
.nv { color: #19177C } /* Name.Variable */
.ow { color: #AA22FF;} /* Operator.Word */
.w { color: #bbbbbb } /* Text.Whitespace */
.mb { color: #666666 } /* Literal.Number.Bin */
.mf { color: #666666 } /* Literal.Number.Float */
.mh { color: #666666 } /* Literal.Number.Hex */
.mi { color: #666666 } /* Literal.Number.Integer */
.mo { color: #666666 } /* Literal.Number.Oct */
.sa { color: #BA2121 } /* Literal.String.Affix */
.sb { color: #BA2121 } /* Literal.String.Backtick */
.sc { color: #BA2121 } /* Literal.String.Char */
.dl { color: #BA2121 } /* Literal.String.Delimiter */
.sd { color: #BA2121; font-style: italic } /* Literal.String.Doc */
.s2 { color: #BA2121 } /* Literal.String.Double */
.se { color: #BB6622;} /* Literal.String.Escape */
.sh { color: #BA2121 } /* Literal.String.Heredoc */
.si { color: #BB6688;} /* Literal.String.Interpol */
.sx { color: #008000 } /* Literal.String.Other */
.sr { color: #BB6688 } /* Literal.String.Regex */
.s1 { color: #BA2121 } /* Literal.String.Single */
.ss { color: #19177C } /* Literal.String.Symbol */
.bp { color: #008000 } /* Name.Builtin.Pseudo */
.fm { color: #0000FF } /* Name.Function.Magic */
.vc { color: #19177C } /* Name.Variable.Class */
.vg { color: #19177C } /* Name.Variable.Global */
.vi { color: #19177C } /* Name.Variable.Instance */
.vm { color: #19177C } /* Name.Variable.Magic */
.il { color: #666666 } /* Literal.Number.Integer.Long */
"""
