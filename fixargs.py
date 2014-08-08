#!/usr/bin/python

import sys
import re
import shutil
import os

class BColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class ParamsExists(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)


def get_tokens(php):
	tokens_re = r'([$A-Za-z0-9_]+|[\[\]"\'()=+-\.,])'
	return re.findall(tokens_re, php)

def getBraketsIndex(name,string):
	index = string.find(name)+len(name)
	indexBegin = string.find('(', index)
	count = 0
	for index, t in enumerate(string[indexBegin:], start=indexBegin):
		if t == '(':
			count += 1
		if t == ')':
			count -= 1
			if count == 0:
				indexEnd = index
	return (indexBegin,indexEnd)

def getFuncArgs(name,string):
	b,e = getBraketsIndex(name,string)
	return string[b:e+1]

def fixHtmlspecialchars(string,params="ENT_COMPAT | ENT_HTML401,'cp1251'"):
	name = 'htmlspecialchars'
	old_string = getFuncArgs(name,string)
	if params not in old_string:
		tokens = get_tokens(old_string)
		tokens[-1:-1] = [', '+params]
		new_string = string.replace(old_string, ''.join(tokens))
		return new_string
	else:
		raise ParamsExists(params)

def askYesNo():
	while True:
		answer = raw_input('Y/N (N) > ')
		answer = answer.lower()
		if answer == 'y':
			return True
		if answer == 'n' or answer == '':
			return False

def highlightLine(string, begin, end, color=BColors.WARNING):
	offset = len(color)
	string = string[:begin] + color + string[begin:]
	string = string[:end+offset+1] + BColors.ENDC + string[end+offset+1:]
	return string

def highlightFuncArgs(name,string, color=BColors.WARNING):
	b,e = getBraketsIndex(name,string)
	return highlightLine(string, b, e, color)

def editLine(line):
	res = fixHtmlspecialchars(line)
	print(highlightFuncArgs('htmlspecialchars', line.strip()))
	print(highlightFuncArgs('htmlspecialchars', res.strip(), BColors.OKGREEN))
	if askYesNo() :
		return res
	else:
		return line 

def fixLines(func, lines, params='' ):
	acc = []
	for line in lines:
		if func in line:
			acc.append(editLine(line))
		else:
			acc.append(line)
	return acc


# if len(sys.argv) != 2:
# 	print("Error: set file")
# 	sys.exit(1)

# FileName = sys.argv[1]

# shutil.copyfile(FileName , FileName+'_back')
# print("Edit file: " + FileName)
# with open(FileName, 'r') as inputFile:
#     data = inputFile.readlines()
#     output = fixLines('htmlspecialchars',data);

#     with open(FileName+'_tmp', 'w') as outputFile:
#     	outputFile.write('\n'.join(output))

# os.remove(FileName)
# shutil.move(FileName+'_tmp', FileName)
# print('Ok')