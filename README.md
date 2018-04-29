
Todo before release:

- new name, seerun
- try it!
- README sections
 - intro / summary
 - usage examples
  - script
  - module:
- cli docs

Issues for later:

- specify module as "some.module.submodule" instead of the path
- docstrings everywhere
- group stuff with the same stacktrace
- combine with coverage so we know where to even look for anything
- can we distinguish "we don't track this *kind* of thing" from "we didn't track this particular one"
- make it not obscenely slow


## Development

Test coverage is 100%, except a bunch of `pragma: no cover`s. The
philosophy is that everything should either be covered or explicitly
say it's not coveraged. (The uncovered stuff is either plausibly not
worth the trouble, or much more embarrassingly, because I copied code
I don't understand.)
