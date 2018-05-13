import html
from ast import NodeVisitor
import ast
from collections import Counter

import asttokens

from seerun import highlighting


class RangeFinder(NodeVisitor):
    """Find and record (in self.ranges) token ranges for AST nodes.

    This is complicated mostly because we decided not to record a range for
    functions given by just a Name. (If the user highlights that, they should
    see the whole function call. Just highlighting the function name is
    boring.) If not for that, all we would need is:

    ranges = [tokens.get_text_range(node)
              for node in asttokens.util.walk(tokens.tree)]
    """

    def __init__(self):
        self.ranges = []

    def visit_call(self, node):
        for field, value in ast.iter_fields(node):
            if field == 'func' and isinstance(value, ast.Name):  # don't really need isinstance?
                pass  # too boring for a node to be just a function name
            elif isinstance(value, list):  # pragma: no cover
                for item in value:
                    if isinstance(item, ast.AST):  # pragma: no cover
                        self.visit(item)
            elif isinstance(value, ast.AST):  # pragma: no cover
                self.visit(value)  # pragma: no cover

    def visit(self, node):
        if hasattr(node, 'first_token'):  # Some don't have token ranges.
            start_end = (node.first_token.startpos, node.last_token.endpos)
            self.ranges.append(
                start_end
            )
        if isinstance(node, ast.Call):
            return self.visit_call(node)
        else:
            return self.generic_visit(node)


def write_html(*, script_path, html_path, values=None):
    with open(script_path) as source_file:
        source_code = source_file.read()
    html = get_html_for_source(source_code, values=values)
    with open(html_path, 'w') as html_file:
        html_file.write(html)


def id_string_from_start_end(start, end):
    return str(start) + 'to' + str(end)


def get_ranges(code):
    tokens = asttokens.ASTTokens(code, parse=True)
    visitor = RangeFinder()
    visitor.visit(tokens.tree)
    return visitor.ranges


def get_text_class_start_html(pygments_class, has_value):
    assert pygments_class
    return '<span class="text {} {}">'.format(
        pygments_class, "will_show_values" if has_value else '')


def get_html_for_source(code, values):
    """Get the html to display code with values.

    Args:
        code: the code
        values: maps nodes (identified as strings "{start_pos}to{end_pos}" to values

    Returns: a string of HTML

    The structure of our HTML and how we put it together is a bit complicated, so here's an
    explanation:

    There are two important classes of <span> tags, "node" and "text".

    The innermost tags are "text" tags, and every bit of code is directly surrounded by exactly one
    of these. When we ask the JavaScript what element is mouseovered or clicked, this is what we
    get.

    Besides having the "text" class, text tags also have classes that come from the Pygments library
    for syntax highlighting. We're making a bunch of assumptions about how the HTML from Pygments
    works: we expect that every bit of code is within exactly one <span> tag, and that getting the
    class on our span tags right is all we need in order to have correct highlighting.

    We also have one "node" tag for each node in the AST. These begin and end at the locations
    corresponding to the beginning and end of the code for that node.

    In order to get correct highlighting, there are some rules about when we must end the current
    text span:

    - whenever the Pygments class changes
    - whenever we're about to end a node span
    - whenever we're about to start a node span

    Whenever we end the current text span, we start a new one -- after whatever has to happen with
    the node spans is done.
    """
    pygments_start_classes = highlighting.get_classes_by_start(code)
    ranges = get_ranges(code)

    # needlessly quadratic
    ends_by_start = {r[0]: [r2[1] for r2 in ranges if r2[0] == r[0]]
                     for r in ranges}
    ends = Counter([r[1] for r in ranges])

    html_lines = []

    # when we encounter a node, we both True/False onto this stack depending on whether it has a
    # recorded value. (the top item on the stack corresponds to whether we have a value for the
    # immediate parent of the current text, and is used for determining whether to make the text
    # bold)
    has_values_stack = []

    pygments_class = None
    for i, char in enumerate(code):
        print(char)
        if i in pygments_start_classes:
            pygments_class = pygments_start_classes[i]
        # need to start a new text span if either: the highlighting class changed OR we need to start a new node
        if i in ends_by_start or i in pygments_start_classes:
            ends_for_this_start = sorted(ends_by_start[i], reverse=True) if i in ends_by_start else []
            if i > 0:
                html_lines.append(
                    '</span>')  # end the text span from previous ending
                # ohhh
            for end in ends_for_this_start:
                values_for_loc = values.get(id_string_from_start_end(i, end))
                has_values_stack.append(bool(values_for_loc))
                # silly double escaping because somewhere our stuff gets unescaped
                # in the javascript `$(".column2").html(parent[0].id)`
                #
                # Without this, `examples/no_repr` doesn't show its
                # repr (<class '__main__.MyClass'>) at all.
                values_str = '<hr>'.join('<pre>' + html.escape(html.escape(v)) + '</pre>'
                                         for v in values_for_loc) \
                    if values_for_loc else '¯\_(ツ)_/¯'
                # value_str = html.escape(repr(value)) if value else 'dunno'
                html_lines.append('<span class="node" id="%s">' % values_str)
            html_lines.append(get_text_class_start_html(pygments_class, has_values_stack[-1]))
        if ends[i]:
            html_lines.append('</span>')  # end the text span
            html_lines.append('</span>' * ends[i])  # end the nodes
            for _ in range(ends[i]):
                print(has_values_stack)
                has_values_stack.pop()
            # has_values_stack can be empty at the very end
            # (and also at the end we start a text span w/o ending it... silly)
            html_lines.append(get_text_class_start_html(pygments_class, has_values_stack and has_values_stack[-1]))

        html_lines.append(html.escape(char))

    return '''
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1
/jquery.min.js"></script>
<style>''' + highlighting.get_style_defs() + '''
* {
    box-sizing: border-box;
}

#content,
html,
body {
  height: 98%;
}

#left {
  float: left;
  width: 50%;
  height: 100%;
  overflow: scroll;
}

#right {
  float: left;
  width: 50%;
  height: 100%;
  overflow: scroll;
}

.highlight-mouseover {
  background: cyan;
}
.highlight-click {
  background: yellow;
}

.will_show_values {
    font-weight: 900;
}


</style>
</head>
<body>

<div class="row">
  <div id="left">
<pre>''' + ''.join(html_lines) + '''

</pre>

  </div>
  <div id="right" style="background-color:#bbb;">
    <h2>Values go here</h2>
    <p>Put your mouse over an expression. If we've saved any values for it, they'll go here.</p>
  </div>
</div>

</body>
</html>


<script>
    $(document).ready(function() {
        $('.text').click(function() {

          var parent = $(this).parent();
          $('.highlight-click').not(parent).removeClass("highlight-click")
          parent.toggleClass( "highlight-click" );
          $("#right").html(parent[0].id)
        });
        
        $('.text').mouseover(function() {
          var parent = $(this).parent();
          parent.addClass("highlight-mouseover");
          if ($('.highlight-click').length === 0) {
            // if there's a clicked expression, that takes precedence - don't do anything
            $("#right").html(parent[0].id)
          }
        });
        $('.text').mouseout(function() {
          $(this).parent().removeClass("highlight-mouseover")
        });
    });
    $(document).on("click", function(e) {
      if ($(e.target).is(".text") === false) {
        $('.highlight-click').removeClass("highlight-click")
      }
  });
</script>

</html>
'''
