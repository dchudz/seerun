import html
import io
from collections import defaultdict

from pygments.formatters.html import HtmlFormatter
from pygments.lexers.python import Python3Lexer

from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # positions (in original text) & what to insert before
        self.start_classes = {}
        self.current_position = 0

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
    parser = MyHTMLParser()

    tokens = lexer.get_tokens(code)
    pygments_html = io.StringIO()
    formatter.format(tokens, pygments_html)
    pygments_html.seek(0)
    html = pygments_html.read()
    parser.feed(html)
    return parser.start_classes


def get_style_defs():
    return HtmlFormatter().get_style_defs()
