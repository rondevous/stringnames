# Basic Info
"""
This is a replacer for the language pack: t.me/setlanguage/stringnames
--> Supports Android and Android_X (.xml) translation files
--> Does not support .strings file
"""

# DO NOT CHANGE THE CODE BELOW (unless you know Python and RegEx)

# Imports
import xml.etree.ElementTree as ET
import re
import argparse

# Command-line info and argument parsing
arg_parser = argparse.ArgumentParser(
	description='Translate strings with their stringnames using an exported XML file from https://translations.telegram.org/en')
arg_parser.add_argument(
	'--file', metavar='Langfile.xml', type=str, required=True,
	help='The exported language file (.xml) from the translations platform')
arg_parser.add_argument(
	'-p', action="store_true",
	help='Show a preview of the replacements.')

args = arg_parser.parse_args()
lang_file = str(args.file)  # str('android_lang_v1234567.xml')
print("\n\nUsing File:\n\t"+lang_file)

# Variables
global tree, total, skipped #string_names
total = 0
skipped = list()
# string_names = dict() # use for .strings

#"
# Checks if lang_file is in XML format
# "
def isXML():
	# return (re.search(r'.*\.xml$', lang_file, re.UNICODE) is not None)
	try:
		global tree
		tree = ET.parse(lang_file)
	except:
		return False
	else:
		return True

def isStrings ():
	global dot_strings
	try:
		dot_strings = open(lang_file, 'r').read()
	except:
		print('File does not exist')
		return False
	return len(re.findall(r'".*"\s=\s".*";', dot_strings)) > 1


# Algo for XML replacer
if(isXML()):
	global tree
	# tree = ET.parse(lang_file)
	root = tree.getroot()	# <Element 'resources'>
	#
	if(args.p):
		print('\n\nThese strings have been edited:\n')
	#
	strCount = 1
	for string in root.findall('string'):
		string_name = string.get('name')
		if(string_name == 'language_code' or string_name == "LanguageCode"): # skip
			skipped.append(string_name)
			continue
		string.text = string_name
		if(args.p):
			print('\n'+str(strCount)+'. '+string_name+'')
		strCount += 1
	#end replacing strings
	newName = re.sub(r'(android_x|android)(.*)\.xml', r'\1_stringnames.xml', lang_file)
	tree.write(newName, xml_declaration=True, encoding='Unicode')
	#
	print('\nSkipped:')
	for i in range(0, len(skipped)):
		print('\t<'+skipped[i]+'>')
	#
	print('\nSummary:')
	print('\t'+str(strCount-1),'strings done')
	print('\t'+str(len(skipped)),'skipped')
	print("\nImport this:\n\t"+newName)
	# CLEANUP MEMORY
	re.purge()
	del string, root, tree, ET # xml memory
	#
elif(isStrings()): # if a .strings file
	global dot_strings # string_names
	# open file, copy all data, manipulate it and write out to a new file
	dot_strings = open(lang_file, 'r').read()
	#
	newName = re.sub(r'(tdesktop|macos|ios)(.*).strings', r'\1_stringnames.strings', lang_file)
	new_strings = open(newName, 'w', encoding='UTF-8')
	#
	if(args.p):
		print('\n\nThese strings have been edited:\n')
	#
	strCount = 0
	for match in re.finditer(r'(?<!.)"(.*)"\s=\s"(.*)";\n', dot_strings):
		strName = match.groups()[0]
		# strValue = match.groups()[1]
		if(strName.startswith('//')):
			continue
		new_strings.write("\""+strName+"\" = \""+strName+"\";\n")
		# string_names[strName] = strName
		if(args.p):
			print('\n'+str(strCount)+'. '+strName+'')
		strCount += 1
	new_strings.close()
	print('\nSummary:')
	print('\t'+str(strCount-1),'strings done')
	print('\t0 skipped')
	print("\nImport this:\n\t"+newName)
	# CLEANUP MEMORY
	re.purge()
	del dot_strings, strCount, newName, new_strings, isStrings
else: # if not an xml file
	print("\nERROR: '"+lang_file+"' is neither an XML, nor a .strings file.")
	print("\nPlease export an 'Android' or 'Android_X' translation file from https://translations.telegram.org/en")
	print('How to export --> https://t.me/TranslationsTalk/1759)') #FIXME
