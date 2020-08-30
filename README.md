# String Names
This is a custom replacer for the [stringnames](t.me/setlanguage/stringnames) langpack. All translation apps are supported.

### Setup:
1. Download and Install [Python 3](https://www.python.org/downloads)
2. Download [stringNames.py](https://github.com/rondevous/stringnames/raw/master/stringNames.py)
_(right click the link > Save link as)_

### Preparations:
1. Export the base language files from [translations.telegram.org/**en/appname**](https://translations.telegram.org/en)
2. Keep all files in the same folder:
```
stringNames.py
android_en.xml
ios_en.strings
tdesktop_en.strings
macos_en.strings
android_x_en.xml
```

## Run the replacer:
[Open command prompt/terminal](https://github.com/rondevous/stringnames#opening-command-prompt--terminal) and enter this command for each file (do not copy `$`)
```
$ python stringNames.py --file langfile.xml
```
Tip: Pressing 'Tab' in the terminal will auto-complete the file name.

**If you get stuck**
```
$ python stringNames.py --help
```

### Opening command prompt / Terminal
- In Windows: type `cmd.exe` in the folder's address bar. (or simply open the prompt and enter: `cd path\to\folder`)
- In Linux terminal: `cd path/to/folder`

## More tools and support
Join us in the [Translation Platform Tools](https://t.me/TranslationTools) group

