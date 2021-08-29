# encoding: utf-8
# THIS FILE IS AUTOGENERATED!
from __future__ import unicode_literals
from setuptools import setup
setup(
    author='Various',
    author_email='kyle@lahnakoski.com',
    classifiers=["Development Status :: 4 - Beta","License :: OSI Approved :: MIT License","Programming Language :: Python :: 3.7","Topic :: Software Development :: Libraries","Topic :: Software Development :: Libraries :: Python Modules"],
    description='Another PEG Parsing Tool',
    install_requires=["mo-dots==5.22.21182","mo-future==5.17.21182"],
    license='MIT',
    long_description='# More Parsing!\n\nA fork of [pyparsing](https://github.com/pyparsing/pyparsing) for faster parsing\n\n\n|Branch      |Status   |\n|------------|---------|\n|master      | [![Build Status](https://travis-ci.org/klahnakoski/mo-parsing.svg?branch=master)](https://travis-ci.org/klahnakoski/mo-parsing) |\n|dev         | [![Build Status](https://travis-ci.org/klahnakoski/mo-parsing.svg?branch=dev)](https://travis-ci.org/klahnakoski/mo-parsing)    |\n\n\n## Differences from PyParsing\n\nThis fork was originally created to support faster parsing for [mo-sql-parsing](https://github.com/klahnakoski/moz-sql-parser).  Since then it has deviated sufficiently to be it\'s own collection of parser specification functions.  Here are the differences:\n\n* Added `Whitespace`, which controls parsing context and whitespace.  It replaces the whitespace modifying methods of pyparsing\n* the wildcard ("`*`") could be used to indicate multi-values are expected; this is not allowed: all values are multi-values\n* all actions are in `f(token, index, string)` form, which is opposite of pyparsing\'s `f(string, index token)` form\n* ParserElements are static: For example, `expr.addParseAction(action)` creates a new ParserElement, so must be assigned to variable or it is lost. **This is the biggest source of bugs when converting from pyparsing**\n* removed all backward-compatibility settings\n* no support for binary serialization (no pickle)\n\nFaster Parsing\n\n* faster infix operator parsing (main reason for this fork)\n* ParseResults point to ParserElement for reduced size\n* regex used to reduce the number of failed parse attempts  \n* packrat parser is not need\n* less stack used \n\n\n## Details\n\n### The `Whitespace` Skipper\n\nThe `mo_parsing.whitespaces.CURRENT` is used during parser creation: It is effectively defines "whitespace" for skipping, with additional features to simplify the language definition.  You declare "standard" `Whitespace` like so:\n\n    with Whitespace() as whitespace:\n        # PUT YOUR LANGUAGE DEFINITION HERE (space, tab and CR are "whitespace")\n\nIf you are declaring a large language, and you want to minimize indentation, and you are careful, you may also use this pattern:\n\n    whitespace = Whitespace().use()\n    # PUT YOUR LANGUAGE DEFINITION HERE\n    whitespace.release()\n\nThe whitespace can be used to set global parsing parameters, like\n\n* `set_whitespace()` - set the ignored characters (default: `"\\t\\n "`)\n* `add_ignore()` - include whole patterns that are ignored (like comments)\n* `set_literal()` - Set the definition for what `Literal()` means\n* `set_keyword_chars()` - For default `Keyword()` (important for defining word boundary)\n\n### Navigating ParseResults\n\nThe results off parsing are in `ParseResults` and are in the form of an n-ary tree; with the children found in `ParseResults.tokens`.  Each `ParseResult.type` points to the `ParserElement` that made it.  In general, if you want to get fancy with post processing (or in a `parseAction`), you will be required to navigate the raw `tokens` to generate a final result\n\nThere are some convenience methods;  \n* `__iter__()` - allows you to iterate through parse results in **depth first search**. Empty results are skipped, and `Group`ed results are treated as atoms (which can be further iterated if required) \n* `name` is a convenient property for `ParseResults.type.token_name`\n* `__getitem__()` - allows you to jump into the parse tree to the given `name`. This is blocked by any names found inside `Group`ed results (because groups are considered atoms).      \n\n### addParseAction\n\nParse actions are methods that are run after a ParserElement found a match. \n\n* Parameters must be accepted in `(tokens, index, string)` order (the opposite of pyparsing)\n* Parse actions are wrapped to ensure the output is a legitimate ParseResult\n  * If your parse action returns `None` then the result is the original `tokens`\n  * If your parse action returns an object, or list, or tuple, then it will be packaged in a `ParseResult` with same type as `tokens`.\n  * If your parse action returns a `ParseResult` then it is accepted ***even if is belongs to some other pattern***\n  \n### Debugging\n\nThe PEG-style of mo-parsing (from pyparsing) makes a very expressible and readable specification, but debugging a parser is still hard.  To look deeper into what the parser is doing use the `Debugger`:\n\n```\nwith Debugger():\n    expr.parseString("my new language")\n```\n\nThe debugger will print out details of what\'s happening\n\n* Each attempt, and if it matched or failed\n* A small number of bytes to show you the current position\n* location, line and character for more info about the current position\n* whitespace indicating stack depth\n* print out of the ParserElement performing the attempt\n\nThis should help to to isolate the exact position your grammar is failing. \n\n## Contributing\n\nIf you plan to extend or enhance this code, please [see the README in the tests directory](https://github.com/klahnakoski/mo-parsing/blob/dev/tests/README.md)',
    long_description_content_type='text/markdown',
    name='mo-parsing',
    packages=["mo_parsing"],
    url='https://github.com/klahnakoski/mo-parsing',
    version='5.40.21239'
)