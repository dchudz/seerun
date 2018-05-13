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


def get_html_for_source(code, values):
    highlighting_start_insertions, highlighting_end_insertions = highlighting.get_insertions(code)

    ranges = get_ranges(code)

    # needlessly quadratic
    ends_by_start = {r[0]: [r2[1] for r2 in ranges if r2[0] == r[0]]
                     for r in ranges}
    ends = Counter([r[1] for r in ranges])

    html_lines = []

    for i, char in enumerate(code):
        if i in ends_by_start:
            ends_for_this_start = sorted(ends_by_start[i], reverse=True)
            if i > 0:
                html_lines.append(
                    '</span>')  # end the text span from previous ending
                # ohhh
            for end in ends_for_this_start:
                values_for_loc = values.get(id_string_from_start_end(i, end))
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
            html_lines.append('<span title="hi" class="text">')
        if ends[i]:
            html_lines.append('</span>')  # end the text span
            html_lines.append('</span>' * ends[i])  # end the nodes
            html_lines.append('<span title="hi" class="text">')

        html_lines.append(highlighting_start_insertions[i])
        html_lines.append(html.escape(char))
        html_lines.append(highlighting_end_insertions[i+1])
        # todonext:
        # fix extra space getting highlighted on next line after range(5):
        # 1st "silly_list" doesn't get highlighted
        # highlighting 1st "=" highlights entire code
        # nothing gets values
        # clicking totally broken

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
