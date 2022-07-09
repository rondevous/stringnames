/* eslint-disable prefer-regex-literals, semi, prefer-const */

// RegExps
const requireQuotes = new RegExp(/\\'.*\\'.*HH:mm/, 'g')

const TOKENS = new RegExp('%(\\d+\\$)?\\.?\\d*[%@sdf]|\\{[A-Za-z0-9_]+\\}|\\bun\\d\\b', 'g');

const TOKENSpair = new RegExp('<!\\[CDATA\\[<a href=\\\\".*?\\\\">|<\\/a>\\]\\]>|\\[a href=\\\\".*?\\\\"\\]|\\[\\/?[A-Za-z]\\]', 'g');
// Markup tokens, needing to enclose one or more text entities
// let href='' hold the same old value
// results in an even number of matches (pairs)
// use \\\\" (four backslashes before double quote) for properly matching \" in innerHTML.

function getOptions () {
  const preservetokens = document.querySelector('#preservetokens').checked
  const radios = document.getElementsByName('stringvalue')
  let value = false
  for (let radio of radios) {
    if (radio.checked) {
      switch (radio.value) {
        case 'default':
          value = false
          break;
        case 'randomvalue':
          value = true
          break;
        case 'onevalueradio':
          value = document.querySelector('#onevalue').value
          break;
      } break // from loop
    }
  }
  return [preservetokens, value]
}

function processXML (file, filename) {
  let reader = new FileReader()
  reader.readAsText(file)
  reader.onloadend = function () {
    // XML processing code
    text = reader.result
    parser = new DOMParser();
    xmlDoc = parser.parseFromString(text, "text/xml");
    var strings = xmlDoc.getElementsByTagName('string')
    options = getOptions() // get choosen options
    console.log(options[0], options[1])
    for (string of strings) {
      // if (string.getAttribute('name')==="AskAQuestionInfo" ) { /*debugging*/ }
      // when cycling strings
      if (options[0] === true) {
        // preserve tokens
        if (typeof options[1] === 'string') {
          var value = options[1]
        } else if (options[1] === true) {
          var value = Math.random()
        } else if (options[1] === false) {
          var value = string.getAttribute('name')
        }
        let temp = String(string.innerHTML) // do not use string.textContent as it swallows the <![[CDATA from the string
        pairmatches = temp.match(TOKENSpair)
        var textstring = ''
        if (pairmatches !== null) {
          for (let i = 0; i <= pairmatches.length / 2; i++) {
            let first = pairmatches.pop()
            let second = pairmatches.pop()
            textstring = second + value + first + ' ' + textstring
          }
          if (temp.match(TOKENS) !== null) {
            for (tok of temp.match(TOKENS)) {
              textstring += ' ' + tok
            }
          }
          string.innerHTML = textstring
        } else if (temp.match(TOKENS) !== null) {
          for (let tok of temp.match(TOKENS)) {
            textstring += ' ' + tok
          }
          string.innerHTML = value + textstring
        } else if (String(string.innerHTML).match(requireQuotes) !== null) {
          string.innerHTML = "\\'" + value + "\\' HH:mm"
        } else {
          string.innerHTML = value
        }
      } else {
        // without tokens
        if (typeof(options[1]) === 'string') {
          string.innerHTML = options[1]
        } else if (options[1]) {
          string.innerHTML = Math.random()
        } else {
          string.innerHTML = string.getAttribute('name')
        }
      }
    }
    var xmlString = new XMLSerializer()
    xmlString = xmlString.serializeToString(xmlDoc); // XML to String
    if (options[0]) {
      filename = filename.replace(/(android_x|android)(?:.*).xml/, '$1_StringnamesTokens.xml')
    } else {
      filename = filename.replace(/(android_x|android)(?:.*).xml/, '$1_Stringnames.xml')
    }
    let saveFiles = document.querySelector("#saveFiles")
    // Save to file, thanks: https://stackoverflow.com/a/24191504
    var bb = new Blob([xmlString], { type: 'text/xml' });
    saveFiles.setAttribute('href', window.URL.createObjectURL(bb));
    saveFiles.setAttribute('download', filename);
    saveFiles.dataset.downloadurl = ['text/xml', saveFiles.download, saveFiles.href].join(':');
    saveFiles.click()
  }
}

function processStrings (file, filename) {
  let reader = new FileReader()
  reader.readAsText(file)
  reader.onloadend = function () {
    // processing code
    text = reader.result
    options = getOptions() // get chosen options
    console.log(options[0], options[1])
    for (let matches of text.matchAll(/(?<!.)"(.*?)"[ ]*=[ ]*"([^;]*?)";\n/g)) { 
      // use [^] instead of . to match line terminators because of MacOS strings like 'EmptyChat.Stickers.Desc'
      line = matches[0]
      stringName = matches[1]
      stringText = matches[2]
      if(options[0]) {
        //preserve tokens
        if (typeof options[1] === 'string') {
          var value = options[1]
        } else if (options[1] === true) {
          var value = Math.random()
        } else if (options[1] === false) {
          var value = stringName
        }
        pairmatches = stringText.match(TOKENSpair)
        var textstring = ''
        if (pairmatches !== null) {
          for (let i = 0; i <= pairmatches.length / 2; i++) {
            let first = pairmatches.pop()
            let second = pairmatches.pop()
            textstring = second + value + first + ' ' + textstring
          }
          if (stringText.match(TOKENS) !== null) {
            for (tok of stringText.match(TOKENS)) {
              textstring += ' ' + tok
            }
          }
          text = text.replace(line, '"'+stringName+'" = "'+ textstring +'";\n')
        } else if (stringText.match(TOKENS) !== null) {
          for (let tok of stringText.match(TOKENS)) {
            textstring += ' ' + tok
          }
          text = text.replace(line, '"'+stringName+'" = "'+ value + textstring +'";\n')
        } else if (stringText.match(requireQuotes) !== null) {
          textstring = "\\'" + value + "\\' HH:mm"
          text = text.replace(line, '"'+stringName+'" = "'+ textstring +'";\n')
        } else {
          text = text.replace(line, '"'+stringName+'" = "'+ value + '";\n')
        }
      } else {
        // don't preserve tokens
        if (typeof options[1] === 'string') {
          text = text.replace(line, '"'+stringName+'" = "'+ options[1] +'";\n')
        } else if (options[1] === true) {
          text = text.replace(line, '"'+stringName+'" = "'+ Math.random() +'";\n')
        } else if (options[1] === false) {
          text = text.replace(line, '"'+stringName+'" = "'+stringName+'";\n')
        }
      }
    }
    if (options[0]) {
      filename = filename.replace(/(macos|ios|tdesktop)(?:.*).strings/, '$1_StringnamesTokens.strings')
    } else {
      filename = filename.replace(/(macos|ios|tdesktop)(?:.*).strings/, '$1_Stringnames.strings')
    }
    let saveFiles = document.querySelector("#saveFiles")
    // Save to file, thanks: https://stackoverflow.com/a/24191504
    var bb = new Blob([text], { type: 'text/strings' });
    saveFiles.setAttribute('href', window.URL.createObjectURL(bb));
    saveFiles.setAttribute('download', filename);
    saveFiles.dataset.downloadurl = ['text/strings', saveFiles.download, saveFiles.href].join(':');
    saveFiles.click()
  }
}

function myFunction () {
  let x = document.getElementById("myFile");
  let txt = "";
  if ('files' in x) {
    if (x.files.length === 0) {
      txt = "Select one or more files.";
    } else {
      for (let i = 0; i < x.files.length; i++) {
        let file = x.files[i];
        if ('name' in file) {
          txt += "<br><strong>" + file.name + "</strong><br>";
        }
        if ('size' in file) {
          txt += "size: " + Math.round(file.size / 1024) + " KiB<br>";
        }
        if ('type' in file) {
          txt += " type: " + file.type;
        }

        if (file.type === 'text/xml') {
          // Process .xml
          processXML(file, file.name)
        } else if (file.name.match(/\.strings$/) !== null) {
          // Process .strings
          processStrings(file, file.name)
        }
      }
    }
  } else {
    if (x.value === '') {
      txt += 'Select one or more files.'
    } else {
      txt += 'The files property is not supported by your browser!'
      txt += '<br>The path of the selected file: ' + x.value // If the browser does not support the files property, it will return the path of the selected file instead.
    }
  }
  document.getElementById('demo').innerHTML = txt
}

document.onreadystatechange = function () {
  if (document.readyState === 'complete') {
    // reset the input to clear previous value
    document.getElementById('myFile').value = null
  }
}
