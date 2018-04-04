
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
- make it not obscenely slow

Done:

- allow clicking
- save/show multiple values
- fix <>'s not showing up
- fix for Starred expressions


Currently broken:

```
viewrun trackmodule /Users/davidchudzicki/hypothesis-python/src/hypothesis/strategies.py ../hypothesis.html --runscript examples/run_hypothesis.py && open ../hypothesis.html
```