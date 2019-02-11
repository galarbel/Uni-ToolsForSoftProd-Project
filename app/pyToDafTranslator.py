def readLineFromInput(f):
	line = f.readline().replace("# @", "@@").replace("#", "//")
	#print(line)
	if ("//" in line and not line.strip().startswith("//")):
		line = line.replace("//", ";//")
	return line

def readLineIgnoreNewLine(f):
	line = readLineFromInput(f)
	while("\n" == line):
			line = readLineFromInput(f)
	return line
	
def handleDecleration(f , line, decleration):
		flag = 0
		decleration = decleration.replace("def", "method").replace(":","")
		line = readLineIgnoreNewLine(f)
		lastLine = line
		
		if "@@" not in line:
			decleration += "{\n"
		
		while "@@" in line:
			
			#deal with types
			if "@types" in line:
				varLine = line
				varLine = varLine.replace("@@types:", "")
				varLine = varLine.strip()
					
				varTypeArr = varLine.split(":")
				varName = varTypeArr[0].strip()
				varType = varTypeArr[1].strip()
					
				#print("Test: varType is : " + varType)
				decleration = decleration.replace(varName, varName + ": " + varType)
				#print("Test: decliration is : " + decleration)
			if "@returns" in line:
				decleration = decleration.replace("\n","") + " returns (" + line.replace("@@returns:", "").strip() + ")\n{\n"
				
			if "@requires" in line or "@ensures" in line or "@modifies" in line:
				decleration = decleration.replace("{\n", '\t') + line.replace('@@', '').replace('::', '##').replace(':', '').replace('##', '::').strip() + "\n{\n"
					
			line = readLineIgnoreNewLine(f)
			lastLine = line

		#print("Test: Decliration is : " + decleration)
		return f,lastLine, decleration

def handleAssignment(line):
	assignmentLine = line
	tabsCount = len(assignmentLine) - len(assignmentLine.lstrip())
	assignmentLine = '\t' * tabsCount + assignmentLine.replace("=",":=").replace("\n","").strip() + ";\n"
	if( "len(" in assignmentLine):
		assignmentLine = assignmentLine.replace("len(","").replace(")",".Length")
	
	return assignmentLine
	

def handleIf(f, line, body):
	ifbody = line
	lastLine = ""
	tabsCount = len(ifbody) - len(ifbody.lstrip())
	ifbody = ifbody.replace("(","").replace(")","").replace(":","").replace("elif","else if")
	body += ifbody
	body += '\t' * tabsCount + "{\n"
			
	line = readLineIgnoreNewLine(f)
	while len(line) - len(line.lstrip()) == tabsCount + 1:
		#body += line.rstrip()  + ";\n"
		if("=" in line and ("if" not in line) and ("for" not in line)and ("while" not in line)
			and ("while" not in line) and ("@" not in line) and ("==" not in line)):
			body += handleAssignment(line)
		else:
			body += line.replace("\n","") + ";" + "\n"
		line = readLineIgnoreNewLine(f)
		
		lastLine = line
		
	body += '\t' * tabsCount + "}\n"
			
	if("else" in line):
		elsebody = line
		tabsCount = len(elsebody) - len(elsebody.lstrip())
		elsebody = elsebody.replace(":","")
		body += elsebody
		body += '\t' * tabsCount + "{\n"

		line = readLineIgnoreNewLine(f)
		
		while len(line) - len(line.lstrip()) == tabsCount + 1:
			body += line.rstrip()  + ";\n"
			line = readLineIgnoreNewLine(f)
			
			lastLine = line
			
			if("append" in line or "remove" in line):
				tabsCount = len(line) - len(line.lstrip())
				callfunc = line.split(".")
				arrName = callfunc[0].strip()
				funcName = callfunc[1].split("(")[0].strip()
				indexName = callfunc[1].split("(")[1].replace(")","").strip()
			
				body += '\t' * tabsCount + arrName + " := " + funcName + "(" + arrName + "," + indexName + ");\n" 
			
		body += "\n" + '\t' * tabsCount + "}\n"
		
	return f,lastLine, body
	
	
def handleLoop(f,line,body):
	whilebody = line
	tabsCount = len(whilebody) - len(whilebody.lstrip())
	whilebody = whilebody.replace("("," ").replace(")"," ").replace(":","")
	body += whilebody
			
	line = readLineIgnoreNewLine(f)
	
			
	if("invariant" in line):
		while "invariant" in line:
			body += line.replace("@@invariant:","invariant")
			line = readLineIgnoreNewLine(f)
			
		body += '\t' * tabsCount + "{\n"
	else:
		body += '\t' * tabsCount + "{\n"
				
	while len(line) - len(line.lstrip()) == tabsCount + 1:
		if("=" in line and ("if" not in line) and ("for" not in line)and ("while" not in line)
				and ("while" not in line) and ("@" not in line) and ("==" not in line)):
			body += handleAssignment(line)
			
		if("if" in line):
			f,line, body = handleIf(f,line, body)
			continue
		
		if("assert" in line):
			body += line.replace("@@assert:","assert")
			
		if("append" in line or "remove" in line):
			tabsCount = len(line) - len(line.lstrip())
			callfunc = line.split(".")
			arrName = callfunc[0].strip()
			funcName = callfunc[1].split("(")[0].strip()
			indexName = callfunc[1].split("(")[1].replace(")","").strip()
			
			body += '\t' * tabsCount + arrName + " := " + funcName + "(" + arrName + "," + indexName + ");\n" 
		
		if("=" not in line and ("if" not in line) and ("for" not in line)and ("while" not in line)
			and ("while" not in line) and ("@" not in line) and ("==" not in line)):
			body += '\t' * (tabsCount+1) + line.strip() +";\n"
			
		line = readLineIgnoreNewLine(f)
		
			
	body += "\n" + '\t' * tabsCount + "}\n"
			
	return f,line,body

	
	
def handleFor(f,line,body):
	forbody = line
	tabsCount = len(forbody) - len(forbody.lstrip())
	forbody = forbody.replace("(","").replace(")","").replace(":","").replace("for","while").replace("in range","<")
	whilePart = forbody.split("<")[0]
	rangePart = range1 = range2 = ""
	
	if("," in line):
		# in case we have : for index in range (i,a.Length)
		rangePart = forbody.split("<")[1].strip().split(",")
		range1 = rangePart[0]
		range2 = rangePart[1]
	else:
		# in case we have : for index in range (a.Length)
		#print (line + "...\n")
		rangePart = line.split("(")[1].replace("):","")
		range1 = "0"
		range2 = rangePart

	loopIndex = whilePart.split(" ")[1]
	
	body += '\t'*tabsCount + loopIndex + ":= " + range1 + ";\n"
	body += whilePart + "< " + range2 + "\n"

	line = readLineIgnoreNewLine(f)
	
			
	if("invariant" in line):
		while "invariant" in line:
			body += line.replace("@@invariant:","invariant")
			line = readLineIgnoreNewLine(f)
			
		body += '\t' * tabsCount + "{\n"

	else:
		body += '\t' * tabsCount + "{\n"
		
	while len(line) - len(line.lstrip()) == tabsCount + 1:
		if("=" in line and ("if" not in line) and ("for" not in line)and ("while" not in line)
				and ("while" not in line) and ("@" not in line) and ("==" not in line)):
			body += handleAssignment(line)
			
		if("if" in line):
			f,line, body = handleIf(f,line, body)
			continue
		
		if("assert" in line):
			body += line.replace("@@assert:","assert")
			
		if("append" in line or "remove" in line):
			tabsCount = len(line) - len(line.lstrip())
			callfunc = line.split(".")
			arrName = callfunc[0].strip()
			funcName = callfunc[1].split("(")[0].strip()
			indexName = callfunc[1].split("(")[1].replace(")","").strip()
			
			body += '\t' * tabsCount + arrName + " := " + funcName + "(" + arrName + "," + indexName + ");\n" 
		
		line = readLineIgnoreNewLine(f)
		
	
	body += '\t'*(tabsCount) + loopIndex + " := " + loopIndex + " + 1;"
	body += "\n" + '\t' * tabsCount + "}\n"
	
	return f,line,body

def handleNewMethod(body,vars,func,decleration):
	if body != "":
		body += "}\n\n"
		if(len(vars) > 0):
			vars = "\tvar " + vars[:-1].strip() + ";\n"
		func = func + decleration + vars + body
		decleration = ""
		body = ""
		vars = ""
	return body,vars,func
	
def Translate():
	#open py file
	f = open("checkEnv\codeToCheck\input.py", "r")
	#f = open("input.py", "r")
	
	line = readLineIgnoreNewLine(f)
	
	decleration = ""
	body = ""
	vars = ""
	func = ""
	main = ""
	
	while (len(line) > 0):				
		if("def" in line):
		
			body,vars,func = handleNewMethod(body,vars,func,decleration)
			
			decleration = line
			f, line, decleration = handleDecleration(f , line, decleration)
			
		#deal with functions body
		if("=" in line and ("if" not in line) and ("for" not in line)and ("while" not in line)
				and ("while" not in line) and ("@" not in line) and ("==" not in line)):
			#check if this is the first time we call this var so add it to vars string
			
			varArr = line.split("=")
			varName = varArr[0].strip()
			
			if(varName not in vars and varName not in decleration):
				vars += varName + " ,"
				
			body += handleAssignment(line)
			
			line = readLineIgnoreNewLine(f)
			
			continue
			
		if("if" in line):
			f,line, body = handleIf(f,line, body)
			continue
		
		if("while" in line):
			f, line, body = handleLoop(f,line,body)
			continue
			
		if("for" in line):
			f, line, body = handleFor(f,line,body)
			continue
			
		if("append" in line or "remove" in line):
			tabsCount = len(line) - len(line.lstrip())
			callfunc = line.split(".")
			arrName = callfunc[0].strip()
			funcName = callfunc[1].split("(")[0].strip()
			indexName = callfunc[1].split("(")[1].replace(")","").strip()
			
			body += '\t' * tabsCount + arrName + " := " + funcName + "(" + arrName + "," + indexName + ");\n" 
			
		if("print" in line):
			tabsCount = len(line) - len(line.lstrip())
			line = '\t' * tabsCount +line.replace("(","").replace(")","").strip() + ";\n"				
			body += line
		
		if("=" not in line and ("if" not in line) and ("for" not in line)and ("while" not in line)
			and ("while" not in line) and ("@" not in line) and ("==" not in line) and ("print" not in line) ):
			
			#print(line.strip().startswith("//"))
			
			
			if (len(line.strip()) == 0):
				body += "\n"
			else:
				body += line.replace("\n","") + ";" + "\n"
			
		line = readLineIgnoreNewLine(f)
		

	body += "\n}\n\n"
	if(len(vars) > 0):
		vars = "\tvar " + vars[:-1].strip() + ";\n"
	func = func + decleration + vars + body
		
	#print("---------------")
	#print(func)
	return 	(func)
