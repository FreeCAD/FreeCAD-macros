#
# your copyright info here
#

# meta data for  macro	management

__Comment__ = 'My macro is a super macro and can be used whenever other macros fail '
__Web__ = "http://forum.freecadweb.org/viewtopic.php?f=8&t=11302"
__Wiki__ = "http://www.freecadweb.org/wiki/index.php?title=Macro_FreeCAD_to_Kerkythea"
__Icon__  = "Part_Common.svg"
__Help__ = "This is the help text of this macro"
__Author__ = "Freek Ad"
__Version__ = 0.1
__Status__ = 'alpha'
__Requires__ = ''



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




