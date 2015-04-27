#
# your copyright info here
#

import FreeCAD


#
# the macro should have a test method to check the sucess of the installation
#
def test():
	errorMsg="There are some errors: a, b, c"
	warnMsg="There are some warnings: d, e"
	infoMsg="There is a info: f"
	errors=3
	warns=2
	infos=1
	result=[errors,errorMsg,warns,warnMsg,infos,infoMsg]
	return result

#
# the macro should have a main method - the macro itself
#
def main():
	t=FreeCAD.ParamGet('User parameter:BaseApp/Preferences/Macro')
	mp=t.GetString("MacroPath")
	FreeCAD.Console.PrintMessage("\n"*4+"H E L L O   W O R L D,\n I'm myMacro.py located in "+ mp+ "/MyMacroDir" + "\n"*4)




