# How to detect tokens in Telegram Translations
The following regular expression (regEx) was taken directly from https://translations.telegram.org (Look for 'TOKEN_REGEX' in __translations.js__ via the browser debugger). This regex will match the tokens present in translations of telegram apps.

- ### In **Javascript**, as it is now:
```javascript
var TOKEN_REGEX = new RegExp('%(\\d+\\$)?\\.?\\d*[%@sdf]|\\{[A-Za-z0-9_]+\\}|\\[\\/?[A-Za-z]\\]|\\bun\\d\\b|&lt;!\\[CDATA\\[&lt;a href=&quot;|&quot;&gt;|&lt;\\/a&gt;\\]\\]&gt;|\\[a href=&quot;|&quot;\\]', 'g');
```

- ### In **Python 3**, after replacing html-escapes and using the (?:non-grouping) version of (brackets)
```python
TOKEN_REGEX = re.compile("%(?:\\d+\\$)?\\.?\\d*[%@sdf]|\\{[A-Za-z0-9_]+\\}|\\[\\/?[A-Za-z]\\]|\\bun\\d\\b|<!\\[CDATA\\[<a href=\"|\">|<\\/a>\\]\\]>|\\[a href=\"|\"\\]")
```

### To feed curiosity, I have broken down the (raw, unescaped) regex stolen directly from the translations website to match tokens of only specific Telegram apps:


1. Matching tokens of **Telegram-Android**
```regex
\bun\d\b
%(\d+\$)?\d*[%@sdf]
<!\[CDATA\[<a href=\"|\">|<\/a>\]\]>
```

> Extra tokens not yet handled by translations website
```regex
<!\[CDATA\[(<a href=\")?|\]\]>
```

> Markup tokens:
```
<!\[CDATA\[(<a href=\")?|\">|(<\/a>)?\]\]>
```

2. Matching tokens of **Telegram-X**
```regex
%(\d+\$)?\d*[%@sdf]
```

3. Matching tokens of **iOS**
```regex
%(\d+\$)?\.?\d*[%@sdf]
\{[A-Za-z0-9_]+\}
```

4. Matching tokens of **MacOS**
```regex
%(\d+\$)?\d*[%@sdf]
```

5. Matching tokens of **TDesktop**
```regex
\{[A-Za-z0-9_]+\}
\[\/?[A-Za-z]\]
\[a href=\"|\"\]
```

> Token Pairs used above
```
\[CDATA\[<a href=\"|\">|<\/a>\]\]>
\[a href=\"|\"\]
```