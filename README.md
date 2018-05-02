[![Build Status](https://travis-ci.org/dchudz/seerun.svg?branch=master)](https://travis-ci.org/dchudz/seerun)

I like reading code, but even very nice code can be hard to follow without seeing what it does.

You can always enter a debugger to look at values during an execution, but that's annoying.

This package records values during execution, and shows them to you in an HTML page afterward.

## Examples

### Script Example

This runs the script at `examples/loop.py` while tracking values of expressions in that script:

```
seerun trackscript docs/examples/loop.html examples/loop.py
```

The HTML is [here](https://dchudz.github.io/seerun/examples/loop.html).

## Module Example

This runs the script at `examples/run_hypothesis.py` while tracking expressions in a hypothesis-internal module I picked:

```
seerun trackmodule /Users/davidchudzicki/hypothesis-python/src/hypothesis/internal/conjecture/engine.py docs/examples/hypothesis.html --runscript examples/run_hypothesis.py
```

The HTML is [here](https://dchudz.github.io/seerun/examples/hypothesis.html).

Here's the console output:

```
Falsifying example: test_one_of_filtered(x=4.0)
ERROR:root:`got exception executing tranformed tree
Traceback (most recent call last):
  File "/Users/davidchudzicki/seerun/seerun/run.py", line 108, in run
    **environment
  File "<string>", line 10, in <module>
  File "<string>", line 5, in test_one_of_filtered
  File "/Users/davidchudzicki/hypothesis-python/src/hypothesis/core.py", line 1052, in wrapped_test
    state.run()
  File "/Users/davidchudzicki/hypothesis-python/src/hypothesis/core.py", line 820, in run
    falsifying_example.__expected_traceback,
  File "/Users/davidchudzicki/hypothesis-python/src/hypothesis/core.py", line 581, in execute
    result = self.test_runner(data, run)
  File "/Users/davidchudzicki/hypothesis-python/src/hypothesis/executors.py", line 58, in default_new_style_executor
    return function(data)
  File "/Users/davidchudzicki/hypothesis-python/src/hypothesis/core.py", line 573, in run
    return test(*args, **kwargs)
  File "<string>", line 5, in test_one_of_filtered
  File "/Users/davidchudzicki/hypothesis-python/src/hypothesis/core.py", line 520, in test
    result = self.test(*args, **kwargs)
  File "<string>", line 7, in test_one_of_filtered
AssertionError
```

In this case, the log is showing us the expected exception.  (Hypothesis raised `AssertionError` for the counterexample.)

The exception does not prevent the HTML output from being produced.


## Development

Test coverage is 100%, except a bunch of `pragma: no cover`s. The
philosophy is that everything should either be covered or explicitly
say it's not coveraged. (The uncovered stuff is either plausibly not
worth the trouble, or much more embarrassingly, because I copied code I
don't understand.)
