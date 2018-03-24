import html
from ast import NodeVisitor
import ast
from collections import Counter

import asttokens

# need to not be relative for running "like_pytest.py"... hack?
# current problem:
# showvalues /Users/davidchudzicki/hypothesis-python/src/hypothesis/internal/conjecture/engine.py  hi.html && open hi.html
# NameError: name 'attr' is not defined
from showvalues.execute import get_values_from_execution


class RangeFinder(NodeVisitor):
    """Find and record (in self.ranges) token ranges for AST nodes.

    This is complicated mostly because we decided not to record a range for
    functions given by just a Name. (If the user highlights that, they should
    see the whole function call. Just highlighting the function name is
    boring.) If not for that, all we would need is:

    ranges = [tokens.get_text_range(node)
              for node in asttokens.util.walk(tokens.tree)]

    TODO: this could probably be replaced with a call to
    asttokens.util.visit_tree.
    """

    def __init__(self):
        self.ranges = []

    def visit_call(self, node):
        for field, value in ast.iter_fields(node):
            # import ipdb; ipdb.set_trace()
            if field == 'func' and isinstance(value, ast.Name):  # don't really need isinstance?
                pass  # too boring for a node to be just a function name
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)

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


def get_html_for_source(code, values=None):
    ranges = get_ranges(code)
    if values is None:
        values = get_values_from_execution(code)

    # needlessly quadratic
    ends_by_start = {r[0]: [r2[1] for r2 in ranges if r2[0] == r[0]]
                     for r in ranges}
    ends = Counter([r[1] for r in ranges])

    html_lines = []

    for i, s in enumerate(code):
        if i in ends_by_start:
            ends_for_this_start = sorted(ends_by_start[i], reverse=True)
            if i > 0:
                html_lines.append(
                    '</span>')  # end the text span from previous ending
            for end in ends_for_this_start:
                value = values.get(id_string_from_start_end(i, end))
                html_lines.append('<span class="node" id="%s">' % (
                    html.escape(value) if value else "dunno"))
            html_lines.append('<span title="hi" class="text">')
        if ends[i]:
            html_lines.append('</span>')  # end the text span
            html_lines.append('</span>' * ends[i])  # end the nodes
            html_lines.append('<span title="hi" class="text">')
        html_lines.append(html.escape(s))

    return '''
<html>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1
/jquery.min.js"></script>
<style>
* {
    box-sizing: border-box;
}

html, body {margin: 0; height: 100%%; overflow: hidden}

/* Create two equal columns that floats next to each other */
.column1 {
    float: left;
    width: 60%%;
    padding: 10px;
    height: 7000px;
    overflow: auto;
    display:block;

}

.column2 {
    float: left;
    width: 40%%;
    padding: 10px;
    height: 300px; /* Should be removed. Only for demonstration */
    overflow: scroll;
}
/* Clear floats after the columns */
.row:after {
    content: "";
    display: table;
    clear: both;
}
</style>
</head>
<body>

<div class="row">
  <div class="column1">
<pre>

%s



</pre>

  </div>
  <div class="column2" style="background-color:#bbb;">
    <h2>Column 2</h2>
    <p>Some text..</p>
  </div>
</div>

</body>
</html>


<script>
    $(document).ready(function() {
        $('.text').mouseover(function() {
          parent = $(this).parent();
          parent.css("background-color", "yellow");
          $(".column2").text(parent[0].id)
        });
        $('.text').mouseout(function() {
          $(this).parent().css("background-color", "");
          $(".column2").text("hello!")
        });
    });
</script>

</html>
            ''' % ''.join(html_lines)
