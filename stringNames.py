# Basic Info
"""
This is a replacer for the language pack: t.me/setlanguage/stringnames
--> Supports '.xml' and '.strings' translation files
--> Head over to t.me/TranslationTools to find more tools
"""

# DO NOT EDIT THE CODE BELOW (unless you know Python and RegEx)

# Imports
import xml.etree.ElementTree as ET
import re
import argparse

# Command-line info and argument parsing
arg_parser = argparse.ArgumentParser(
	description='Translate strings with their stringnames using an exported file from https://translations.telegram.org/en')
arg_parser.add_argument(
	'--file', metavar='Langfile[.xml|.strings]', type=str, required=True,
	help='The exported language file (.xml or .strings) from the translations platform')
arg_parser.add_argument(
	'-p', action="store_true",
	help='Show the replaced string names.')

args = arg_parser.parse_args()
lang_file = str(args.file)  # str('android_lang_v1234567.xml')

# Variables
global tree, total, skipped
total = 0
skipped = list()

# Checks if lang_file is in XML format
def isXML():
	try:
		global tree
		tree = ET.parse(lang_file)
	except:
		return False
	else:
		return True

# Checks if lang_file is in .strings format
def isStrings ():
	global dot_strings
	try:
		dot_strings = open(lang_file, 'r').read()
	except:
		print('File does not exist')
		return False
	return len(re.findall(r'".*"\s=\s".*";', dot_strings)) > 0

# Print summary
def printSummary():
	print("\nFile Used:\n\t"+lang_file)
	print('Summary:')
	print('\t'+str(strCount-1),'strings done')
	print('\t'+str(len(skipped)),'skipped')
	print("Import this:")
	print('\t'+newName+'\n')

# Algo for XML replacer
if(isXML()):
	global tree
	# tree = ET.parse(lang_file)
	root = tree.getroot()	# <Element 'resources'>
	#
	if(args.p):
		print('\n\nThese strings have been edited with their names:\n')
	#
	strCount = 1
	for string in root.findall('string'):
		string_name = string.get('name')
		if(string_name == 'language_code' or string_name == "LanguageCode"): # skip
			strCount += 1
			skipped.append(string_name)
			continue
		string.text = string_name
		if(args.p):
			print('\n'+str(strCount)+'. '+string_name+'')
		strCount += 1
	#end replacing strings
	newName = str(re.sub(r'(android_x|android)(.*)\.xml', r'\1_stringnames.xml', lang_file))
	tree.write(newName, xml_declaration=True, encoding='Unicode')
	#
	print('\nSkipped:')
	for i in range(0, len(skipped)):
		print('\t<'+skipped[i]+'>')
	#
	printSummary()
	# CLEANUP MEMORY
	re.purge()
	del string, root, tree, ET # xml memory
	#
# Algo for .strings replacer
elif(isStrings()):
	global dot_strings
	# open file, copy all data, iterate and write out to a new file
	dot_strings = open(lang_file, 'r').read()
	newName = re.sub(r'(tdesktop|macos|ios)(.*).strings', r'\1_stringnames.strings', lang_file)
	new_strings = open(newName, 'w', encoding='UTF-8')
	#
	if(args.p):
		print('\n\nThese strings have been edited with their names:\n')
	#
	strCount = 0
	for match in re.finditer(r'(?<!.)"(.*)"\s=\s"(.*)";\n', dot_strings):
		strName = match.groups()[0]
		# strValue = match.groups()[1]
		new_strings.write("\""+strName+"\" = \""+strName+"\";\n")
		if(args.p):
			print('\n'+str(strCount)+'. '+strName+'')
		strCount += 1
	new_strings.close()
	#
	printSummary()
	# CLEANUP MEMORY
	re.purge()
	del dot_strings, strCount, newName, new_strings, isStrings
else: # if not an xml file
	print("\n\t[ ERROR ]: '"+lang_file+"' is neither an XML, nor a .strings file.")
	print("\nPlease export a translation file from one of the apps at https://translations.telegram.org/en")
	print('How to export --> https://t.me/TranslationsTalk/1759)') #FIXME
