# Basic Info
"""
This script is a generator for the language pack: t.me/setlanguage/stringnames
It supports Telegram translation files of type .xml and .strings
>--		Head over to t.me/TranslationTools for more tools 		--<
"""

import argparse
import os
import re
import time
import xml.etree.ElementTree as ET

# Variables
global tree, total, skipped
total = 0
skipped = list()

# RegExps
req_quotes = re.compile(r"\\'.*\\'.*HH:mm")  # \'Sample Text\' HH:mm


def isXML(file):
	"""Checks if a file is in .XML format
	"""
	try:
		global tree
		tree = ET.parse(file)
	except:
		return False
	else:
		print("----\nProcessing: ", file)
		return True


def isStrings(file):
	"""Checks if a file is in .strings format
	"""
	global dot_strings
	try:
		dot_strings = open(file, 'r').read()
	except:
		return False
	if len(re.findall(r'".*"\s=\s".*";', dot_strings)) > 0:
		return True


# Print summary
def printSummary():
	global strCount, outFile
	print('  '+str(strCount-1), 'strings changed')
	if len(skipped) > 0:
		print('  '+str(len(skipped)), 'skipped')
	print("  Saved to: ", outFile)


def XMLreplace(file=str, folder=None):
	""" Algo for XML replacer
	"""
	global tree, strCount, outFile
	""" tree = ET.parse(file)"""
	root = tree.getroot()  # <Element 'resources'>
	if(args.p):
		print('\n\nThese strings have been edited with their names:\n')
	strCount = 1
	for string in root.findall('string'):
		string_name = string.get('name')
		if(string_name == 'language_code' or string_name == "LanguageCode"):
			string_name = 'en'
			"""
			strCount += 1
			skipped.append(string_name)
			continue
		string.text = "dummyText"
		"""
		if(req_quotes.match(string.text) != None):  # strings that require "quotes"
			string.text = req_quotes.sub(
				("\\'{}\\'").format(string_name), string.text)
		else:
			string.text = string_name
		if(args.p):
			print('\n'+str(strCount)+'. '+string_name+'')
		strCount += 1
	outFile = str(re.sub(r'(android_x|android)(.*)\.xml',
						 r'\1_stringnames.xml', os.path.basename(file)))
	outFolder = 'stringnames (IMPORT)'
	if folder is None:
		try:
			os.mkdir(outFolder)
			print("created folder:", outFolder)
		except:
			pass
		outFile = os.path.join(outFolder, outFile)
	else:
		outFolder = os.path.join(folder, outFolder)
		try:
			os.mkdir(outFolder)
			print("created folder:", outFolder)
		except:
			pass
		outFile = os.path.join(outFolder, outFile)
	tree.write(outFile, xml_declaration=True, encoding='Unicode')
	if args.p:
		print('\nSkipped:')
		for i in range(0, len(skipped)):
			print('\t<'+skipped[i]+'>')
	printSummary()
	""" MEMORY CLEANUP  """
	re.purge()
	del string, root, tree  # xml memory


def STRINGSreplace(file=str, folder=None):
	""" Algo for .strings replacer:
	>>> # open file, copy all data, iterate and write out to a new file
	"""
	global dot_strings, strCount, outFile
	path = os.path.join(folder, file)
	print("----\nProcessing: ", path)
	dot_strings = open(path, 'r').read()
	outFile = re.sub(r'(tdesktop|macos|ios)(.*).strings',
					 r'\1_stringnames.strings', os.path.basename(file))
	outFolder = 'stringnames (IMPORT)'
	if folder is None:
		try:
			os.mkdir(outFolder)
			print("created folder:", outFolder)
		except:
			pass
		outFile = os.path.join(outFolder, outFile)
	else:
		outFolder = os.path.join(folder, outFolder)
		try:
			os.mkdir(outFolder)
			print("created folder:", outFolder)
		except:
			pass
		outFile = os.path.join(outFolder, outFile)

	new_strings = open(outFile, 'w', encoding='UTF-8')
	new_strings.write(
		'/*\nThis file was generated for importing into the t.me/setlanguage/stringnames language.\n*/\n')
	if args.p:
		print('\nThese strings have been edited with their names:\n')
	strCount = 0
	for match in re.finditer(r'(?<!.)"(.*)"\s=\s"(.*)";\n', dot_strings):
		strName = match.groups()[0]
		new_strings.write("\""+strName+"\" = \""+strName+"\";\n")
		if(args.p):
			print('\n'+str(strCount)+'. '+strName+'')
		strCount += 1
	new_strings.close()
	printSummary()
	""" MEMORY CLEANUP  """
	re.purge()
	del dot_strings, strCount, outFile, new_strings


def stringnames(file=str, folder=None):
	global total, skipped
	total = 0
	skipped = list()
	temp = os.path.join(folder, file)
	if(isXML(temp)):
		XMLreplace(file, folder)
	elif(isStrings(temp)):
		STRINGSreplace(file, folder)
	else:  # invalid translation file
		print("\n\t[ ERROR ]: '" + file +
			  "\n This is not a valid translations file. Looking for .XML or .strings")
		print("\nPlease export a translation file from one of the apps at https://translations.telegram.org/en")
		print('How to export --> https://t.me/TranslationsTalk/1759)')  # FIXME


# Command-line info and argument parsing
arg_parser = argparse.ArgumentParser(
	description='Overwrites translations with their string-names using exported files from https://translations.telegram.org/en')
arg_parser.add_argument(
	'-f', '--file', metavar='language[ .xml | .strings]', type=str, required=False,
	help='The exported language file (.xml or .strings) from the translations platform')
arg_parser.add_argument(
	'-d', '--folder', metavar='folder', type=str, required=False,
	help='The folder in which the exported language files are placed in.')
arg_parser.add_argument(
	'-p', action="store_true",
	help='Show the replaced string names.')

args = arg_parser.parse_args()

if args.folder is None:
	if args.file is None:
		import sys
		sys.exit("You must specify a valid file or folder!\
			\nExample:\
			\n\tpython stringNames --file android.xml\
			\n\t\t\tOR\
			\n\tpython stringNames --folder langfiles")
	else:
		stringnames(str(args.file))  # str('android_lang_v1234567.xml')
else:
	folder = str(args.folder)
	if os.path.isdir(folder):
		print('Looking into folder:', folder)
		files = os.listdir(folder)
		for file in files:
			path = os.path.join(folder, file)
			if os.path.isfile(path):
				stringnames(file, folder)
				time.sleep(1)
			else:
				continue
	else:
		print('Not a folder ')

# begin
# stringnames()
