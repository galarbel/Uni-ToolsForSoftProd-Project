from subprocess import Popen, PIPE, call
from subprocess import call


def isCodeSafe(code):
	'''here we check a little bit of the code to try and prevent 'easy' injections and hacks'''
	return not ("__" in code or "eval" in code or "exec" in code or "import" in code or "this" in code)
	
def writeCodeToFile(code):
	f = open('checkEnv\codeToCheck\input.py','w')
	f.write(code.replace(" " * 4, "\t").replace("\r", ""))

def runCodeAsPython(code):
	process=Popen('checkenv\Scripts\python checkEnv\codeToCheck\input.py', stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	return stdout, stderr
	
def cleanSTDvars(txt):
	res = str(txt).replace('\\n','<br/>').replace('\\r','').replace("b'",'').replace('File "checkEnv\\\\codeToCheck\\\\input.py", ',"").strip()
	return res[:-1]
	
def writeDafCodeToFile(code):
	f = open('checkEnv\codeToCheck\input.dfy','w')
	
	dafUtils = open('app/dafnyUtils.dfy', 'r')
	
	code += "\n\n" + dafUtils.read()
	
	f.write(code)
	
def runDafnyCheck():
	process=Popen('dafny/dafny.exe checkEnv\codeToCheck\input.dfy', stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	
	stdout = cleanDafnyResponse(stdout)
	
	if ("0 error" in str(stdout)):
		return (stdout, stderr)
	else:
		return ("", stdout)
		
def cleanDafnyResponse(txt):
	txt = str(txt)
	txt = txt.replace("Dafny program verifier version 1.9.8.30829, Copyright (c) 2003-2016, Microsoft.\\r\\n", "").replace("checkEnv\\\\codeToCheck\\\\input.dfy", "")
	txt = txt.replace("\\r\\nDafny program verifier","Dafny program verifier").replace("\\r\\nCompiled assembly into input.dll","")
	if ("Compiled assembly into input.exe" in txt):
		process=Popen('checkEnv\codeToCheck\input.exe', stdout=PIPE, stderr=PIPE)
		stdout, stderr = process.communicate()
		txt = txt.replace("Compiled assembly into input.exe", "\\nDafny:\\n" + str(stdout).replace("b'",''))
	return txt
	