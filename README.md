
# String Names \w Tokens Generator
### Generate telegram language files with the keys and tokens as the translation

**This script will generate files for the Telegram [tokenstringnames](translations.telegram.org/tokenstringnames) language**

### Requirements:
1. [Python-3](https://www.python.org/downloads), linux users can install it from their pkg repo (please don't use python-2)

### Preparations:
1. Download [stringNames.py](https://github.com/rondevous/stringnames/raw/master/stringNames.py)
_(right click > Save link as)_
2. Export the language files of each app from https://translations.telegram.org/en
3. Place all the languages files into a new folder (langfiles). And keep this folder beside stringNames.py

## Run the script
In the command prompt/ terminal, go to the folder where the script is:
```bash
cd path/to/stringNames/script
```
> Hint: Press Tab to auto-complete the folder name

**And generate them all at once!**
```
python stringNames.py --folder langfiles
```
> `langfiles` is the folder where you saved all your exported files.

**Or do it one at a time** ¯\\\_(ツ)\_/¯
```bash
python stringNames.py --file ios_en_v567890.strings
```

**Some info**
```bash
python stringNames.py -h
```
---
### **Note:** If you want to generate the string-names without the tokens, use the [master](https://github.com/rondevous/stringnames/tree/master) branch
---
> If you're a programmer: I have documented the [token-detection regex](https://github.com/rondevous/stringnames/blob/addTokens/How-to-detect-tokens.md) which the translations website uses for highlighting the tokens. To include all stringnames, the script additionally rewrites strings that do not work without 'quotes' in translation, such as the one [here](https://translations.telegram.org/en/android/groups_and_channels/StartShortTodayAt), though they aren't covered by the token regex.