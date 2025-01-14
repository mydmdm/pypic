# pypic
Package `pypic` is a `Python` package that provides a simple way to create text-based diagram that can be further rendered into an image. This backend of this project is [Pikchr](https://pikchr.org/home/doc/trunk/homepage.md) which is a PIC-like markup language for diagrams.

## Scope and Purpose
`Pikchr`, in praise of the historical `PIC` language, is a simple and powerful tool for creating diagrams. It's much simpler than `DOT` and `Graphviz` because of its innovative relative layout and natural language-like syntax.

However, due to its simplicity, it lacks the ability of a high-level programming language. Its native support to hierarchical structures and code reuse is limited. Besides, its relative layout highly depends on the order of the elements in the code, which makes it hard to maintain and modify.


## Design Principles
- For every object, `str()` is used in rendering to `pikchr` code, and `format()` is used in expression evaluation.
