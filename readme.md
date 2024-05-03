# tree-down

Turn contents of a directory into a tree of markdown with file content

## Basic Usage

Given the following directory structure:

```
.
├── index.html
├── stylesheets
│   ├── index.css
│   └── reset.css
└── script.js
├── favicon.ico
└── images
│   ├── index.css
│   └── reset.css
└── notes
    ├── note1.txt
    └── reset.txt
```

the following command:

```bash
$ tree-down <directory>
```

creates the following markdown:

(note: unless the flag `--binary` is passed, the content of binary files is omitted. See Below)

````markdown
- [index.html](file:///./index.html)

```html
<!-- content of index.html -->
```
````

- stylesheets/index.css

```css
/* content of stylesheets/index.css */
```

- stylesheets/reset.css

```css
/* content of stylesheets/reset.css */
```

- script.js

```javascript
// content of script.js
```

- notes/note1.txt

```text
content of ./notes/note1.txt
```

- notes/note2.txt

```text
content of ./notes/note2.txt
```

````

## Flag: --output (-o)

Output is written to stdout by default. To write to a file, use the `--output` flag:

```bash
$ tree-down <directory> --output=<output-file>
````

## Flag: --ignore (-i)

Files can be ignored by passing globs to one or more `--ignore` flags.

Ignore files `notes/note1.txt` and `notes/note2.txt` with any of the following:

```bash
$ tree-down --ignore=notes/note1.txt --ignore=notes/note2.txt
```

OR

```bash
$ tree-down -i=notes/note1.txt,notes/note2.txt <directory>
```

OR

```bash
$ tree-down -i=notes/*.txt <directory>
```

## Flag: --ignore-file (-I)

Pass a list of globs via the --ignore-file flag.

Ignore all globs in a file named `.gitignore` with the following:

```bash
$ tree-down --ignore-file=../.gitignore <directory>
```

OR

```bash
$ tree-down --I=../.gitignore <directory>
```

## Flag: --binary (-b)

By default, the content of binary files is omitted.

To include the content of binary files represented in base64, set the `--binary` flag to `base64`:

```bash
$ tree-down --binary=base64 <directory>
```

Produces the following markdown:

````markdown
...

- favicon.ico

```base64
<Base64 data>
```
````

````

To include the content of binary files represented as a placeholder, set the `--binary` flag to `placeholder`:

```bash
$ tree-down -b=placeholder <directory>
````

````markdown
...

- favicon.ico

```base64
...
```
````

```

```
