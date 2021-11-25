## Generate telegram translations as the string-name
This script will generate translation files with all the translations set as its corresponding string-name. https://translations.telegram.org/stringnames has been created if you need to use it.

### If you want to generate the string-name along with the tokens present in the translation, use the [addTokens](https://github.com/rondevous/stringnames/tree/addTokens) branch

*Requires: Python 3*
Export the translation files for each of the telegram apps and place them in a folder

**To generate from within a folder**
```
python stringNames.py --folder langfiles
```
If `langfiles` is the folder where you saved all the exported language files.

**To generate one file only**
```
python stringNames.py --file ios_en_v567890.strings
```
