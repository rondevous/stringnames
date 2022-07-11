# NOTE: USE THIS WEBSITE FROM NOW: https://rondevous.github.io/stringnames/
The python script will not be updated, unless necessary. The website processes all the stringnames in your browser itself, so its fast :thumbsup:

---

## Generate telegram language files with the keys/string-names as the translation

This script will generate translation files with all the translations set as its corresponding key-name. https://translations.telegram.org/stringnames has been created if you need to use this.

---

1. First, **export all the translation files** from https://translations.telegram.org/en

2. Generate the files using the
[stringNames.py](https://github.com/rondevous/stringnames/blob/master/stringNames.py) python3 script:

    a. To generate **all files** present in a folder
    ```powershell
    python stringNames.py --folder langfiles
    ```
    > where `langfiles` is the folder where you saved all the exported language files.
    
    b. To generate **only one** language file
    ```powershell
    python stringNames.py --file ios_en_v567890.strings
    ```

---

### **Note:** If you want to generate the string-names along with the tokens present in the translation, use the [addTokens](https://github.com/rondevous/stringnames/tree/addTokens) branch
---
> If you're a programmer: I have documented the [token-detection regex](https://github.com/rondevous/stringnames/blob/master/How-to-detect-tokens.md) which the translations website uses for highlighting the tokens. To include all stringnames, the script additionally rewrites strings that do not work without 'quotes' in translation, such as the one [here](https://translations.telegram.org/en/android/groups_and_channels/StartShortTodayAt), though they aren't covered by the token regex.