
# String Names Generator
**This script will generate files for the Telegram [stringnames](t.me/setlanguage/stringnames) language**

### Requirements:
1. Download and Install [Python-3](https://www.python.org/downloads), linux users can install it from their pkg repo (please don't use python-2)

### Preparations:
1. Download [stringNames.py](https://github.com/rondevous/stringnames/raw/master/stringNames.py)
_(right click > Save link as)_
2. Export the language files of each app from https://translations.telegram.org/en
3. Place them all into a new folder

## Run the script
[Open command prompt/terminal](https://github.com/rondevous/stringnames#opening-command-prompt--terminal)

Navigate the terminal to the folder where the script is placed

`Tip: Press Tab to auto-complete the folder name`
```
cd path/to/stringNames/script
```

**And generate them all at once!** \\(^-^)/
```
python stringNames.py --folder langfiles
```
If `langfiles` is the folder where you saved all your exported files.

**Or do it one at a time** ¯\\\_(ツ)\_/¯
```
$ python stringNames.py --file ios_en_v567890.strings
```

**Some info**
```
$ python stringNames.py -h
```

### How to open the Terminal/Command Prompt 
- In Windows: type `cmd.exe` in the folder's address bar. (or simply open the prompt and enter: `cd path\to\folder`)
- In Linux: right-click in the file manager or else: `cd path/to/folder`

## More tools and support for Telegram Translators
Join us in the group [Translation Platform Tools](https://t.me/translationtools/5), we have tools! 

