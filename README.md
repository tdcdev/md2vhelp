Markdown to Vim help
====================

Description
-----------

This tiny python script allows you to convert a `markdown` file into a
`Vim help` file.

This is very usefull if you devolop a Vim plugin and write a `README.md`
for a git hosting provider. Indeed, you just
have to maintain the `README.md` file, and use `md2vhelp` to
generate the corresponding `Vim help` file.

Usage
-----

Use it like below:

    python md2vhelp.py <markdown-file> <plugin-name> > <vim-help-file>

You can see examples of `md2vhelp` translation [here](examples).

License
-------

This software is licensed under the [zlib license](LICENSE.txt).
