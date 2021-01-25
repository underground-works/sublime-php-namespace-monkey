## PHP Namespace Monkey for Sublime Text

#### Never write a PHP namespace declaration again.

The namespace monkey pre-fills all created PHP files in a Composer-enabled project with a namespace declaration and optionally an empty class definition so you don't have to.

*You can save literally seconds every day thanks to this package.*

![sublime-php-namespace-monkey](https://user-images.githubusercontent.com/821582/56864048-37a87380-69be-11e9-9c94-4e54334ed39f.gif)

Available settings:

```python
{
    // Namespace style
    // - same-line - Same line as PHP tag
    // - next-line - Next line after PHP tag
    // - psr-2 - One blank line after PHP tag (PSR-2)
    "namespace_style": "psr-2",

    // Include class definition
    "include_class_definition": true,

    // Include strict types declaration
    "declare_strict_types": false
}
```

### Licence

Copyright (c) 2019 Miroslav Rigler

MIT License

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
"Software"), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
