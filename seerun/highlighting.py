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
        self.start_insertions = defaultdict(str)
        self.end_insertions = defaultdict(str)

        self.current_position = 0

    def handle_starttag(self, tag, attrs):
        if tag=='div' or not attrs:  # kinda hacky to avoid extra stuff, results in hanging extra </span> that doesn't seem to cause problems
            return
        attr_strings = [f'{class_name}="{value}" ' for class_name, value in attrs]
        self.start_insertions[self.current_position] += f'<{tag} {"".join(attr_strings)}>'

    def handle_endtag(self, tag):
        if tag=='div':
            return
        self.end_insertions[self.current_position] += f'</{tag}>'

    def handle_data(self, data):
        self.current_position += len(data)


def get_insertions(code):
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

    return parser.start_insertions, parser.end_insertions


def get_style_defs():
    return HtmlFormatter().get_style_defs()
