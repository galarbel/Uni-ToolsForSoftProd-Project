from flask import render_template,request,jsonify
import traceback

from app import app
from app.utils import *
from app.pyToDafTranslator import Translate



@app.route('/index',  methods=['GET', 'POST'])
def index():
	return render_template('index.html')
	
@app.route('/run',  methods=['GET', 'POST'])
def checkCode():
	#print (request.form["code"])
	code = request.form["code"]
	responseDict = {}
	
	if (not isCodeSafe(code)):
		responseDict["response"] = "Code was found unsafe to run."
		return jsonify(responseDict)
	
	#--------Write Code to input file----------#
	try:
		writeCodeToFile(code)
	except IOError as e:
		responseDict["response"] = "failed to write code to file on server. I/O error({0}): {1}".format(e.errno, e.strerror)
		return jsonify(responseDict)
	except:
		responseDict["response"] = "unknown error occured when writing to server. :("
		return jsonify(responseDict)
		
	#--------Check Python Code ----------#
	try:
		pyAnswer, pyError = runCodeAsPython(code)
		responseDict["pyAnswer"] = cleanSTDvars(pyAnswer)
		responseDict["pyError"] = cleanSTDvars(pyError)
	except IOError as e:
		responseDict["response"] = "failed to check code from file on server. I/O error({0}): {1}".format(e.errno, e.strerror)
		return jsonify(responseDict)
	except:
		responseDict["response"] = "unknown error occured when checking py code. :("
		return jsonify(responseDict)
	if (len(responseDict["pyError"]) > 0):
		responseDict["response"] = "Python Code Error"
		return jsonify(responseDict)
	
	if (code.startswith("# @noDafny")):
		responseDict["response"] = "Code working but not verified! (@noDafny)"
		return jsonify(responseDict)
	
	
	#--------Translate To Dafny ----------#	
	try:
		dafCode = Translate()
		responseDict["dafCode"] = dafCode.replace("<", "&lt;").replace("\n", "<br>").replace("\t", "&nbsp;" * 4)
	except IOError as e:
		responseDict["response"] = "failed to translate code from file on server. I/O error({0}): {1}".format(e.errno, e.strerror)
		return jsonify(responseDict)
	except:
		traceback.print_exc()		
		responseDict["response"] = "unknown error occured when translating code. :("
		return jsonify(responseDict)
		
		
	#-------Write Dafny Code to File ----------#
	try:
		writeDafCodeToFile(dafCode)
	except IOError as e:
		responseDict["response"] = "failed to write daf code to file on server. I/O error({0}): {1}".format(e.errno, e.strerror)
		return jsonify(responseDict)
	except:
		responseDict["response"] = "unknown error occured when writing daf code to server. :("
		return jsonify(responseDict)
		
	#-------Run Dafny ----------#	
	try:
		dafAnswer, dafError = runDafnyCheck()
		responseDict["dafAnswer"] = cleanSTDvars(dafAnswer)
		responseDict["dafError"] = cleanSTDvars(dafError)
	except:
		responseDict["response"] = "unknown error occured when running dafny code on server. :("
		return jsonify(responseDict)
		
	if (len(responseDict["dafError"]) > 0):
		responseDict["response"] = "Dafny Code/Verify Error"
		return jsonify(responseDict)
	
	responseDict["response"] = "Code working and verified!"
	return jsonify(responseDict)
	
	
