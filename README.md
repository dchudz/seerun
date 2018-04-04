




```
viewrun trackmodule /Users/davidchudzicki/showvalues/showvalues/just_for_a_test.py hi.html --runscript tests/b.py && open hi.html
```

Run in hypothesis source directory:

```
viewrun trackmodule /Users/davidchudzicki/hypothesis-python/src/hypothesis/internal/conjecture/engine.py /Users/davidchudzicki/hypothesis-python/hi.html --runmodule pytest tests/cover/test_one_of.py
```




Todo before release:

- show more stuff
 - A and B
 -
- try it!
- README sections
 - intro / summary
 - usage examples
  - script
  - module:
- new name, seerun
- cli docs
- hypothesis shrinkage example?

Issues for later:

- specify module as "some.module.submodule" instead of the path
- docstrings everywhere
- group stuff with the same stacktrace
- combine with coverage so we know where to even look for anything
- can we distinguish "we don't track this *kind* of thing" from "we didn't track this particular one"


Done:

- allow clicking
- save/show multiple values



viewrun trackmodule /Users/davidchudzicki/hypothesis-python/src/hypothesis/internal/conjecture/engine.py ../hypothesis.html --runscript examples/hypothesis.py && open ../hypothesis.html


## Maybe address:

- missing from % operator





```
def redraw_last(data, n):
            u = target_data[0].blocks[-1][0]
            if data.index + n <= u:
                return target_data[0].buffer[data.index:data.index + n]
            else:
                return uniform(self.random, n)
```

why is `target_data` an empty list and `target_data[0]` completely blank?