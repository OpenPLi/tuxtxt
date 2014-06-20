from enigma import eTuxtxtApp, getDesktop
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.ActionMap import NumberActionMap
from Screens.PictureInPicture import PipPigMode

class RcCode:
	RC_0 = 0x00
	RC_1 = 0x01
	RC_2 = 0x02
	RC_3 = 0x03
	RC_4 = 0x04
	RC_5 = 0x05
	RC_6 = 0x06
	RC_7 = 0x07
	RC_8 = 0x08
	RC_9 = 0x09
	RC_RIGHT = 0x0A
	RC_LEFT = 0x0B
	RC_UP = 0x0C
	RC_DOWN = 0x0D
	RC_OK = 0x0E
	RC_MUTE = 0x0F
	RC_STANDBY = 0x10
	RC_GREEN = 0x11
	RC_YELLOW = 0x12
	RC_RED = 0x13
	RC_BLUE = 0x14
	RC_PLUS = 0x15
	RC_MINUS = 0x16
	RC_HELP = 0x17
	RC_MENU = 0x18
	RC_HOME = 0x1F

class ShellStarter(Screen):
	skin = """
		<screen position="1,1" size="1,1" title="TuxTXT" >
		</screen>"""

	def __init__(self, session, args = None):
		self.skin = ShellStarter.skin
		Screen.__init__(self, session)
		self.session = session
		eTuxtxtApp.getInstance().appClosed.get().append(self.appClosed)
		eTuxtxtApp.getInstance().startUi()
		self["actions"] = NumberActionMap(["TeletextActions","NumberActions"],
		{
			"0": self.handleNumberKey,
			"1": self.handleNumberKey,
			"2": self.handleNumberKey,
			"3": self.handleNumberKey,
			"4": self.handleNumberKey,
			"5": self.handleNumberKey,
			"6": self.handleNumberKey,
			"7": self.handleNumberKey,
			"8": self.handleNumberKey,
			"9": self.handleNumberKey,
			"nextSubPage": self.handleNextSubPage,
			"prevSubPage": self.handlePrevSubPage,
			"nextPage": self.handleNextPage,
			"prevPage": self.handlePrevPage,
			"ok": self.handleKeyOk,
			"transparent": self.handleTransparent,
			"green": self.handleKeyGreen,
			"yellow": self.handleKeyYellow,
			"red": self.handleKeyRed,
			"blue": self.handleKeyBlue,
			"zoomMode": self.handleZoom,
			"screenMode": self.handleScreenMode,
			"hint": self.handleHint,
			"menu": self.handleKeyMenu,
			"exit": self.handleKeyExit,
		})
		PipPigMode(True)

	def appClosed(self):
		eTuxtxtApp.getInstance().appClosed.get().remove(self.appClosed)
		#force redraw
		dsk = getDesktop(0)
		dsk.resize(dsk.size())
		PipPigMode(False)
		if hasattr(self.session, "pip"):
			self.session.pip.relocate()
		self.close()

	def handleNumberKey(self, key):
		eTuxtxtApp.getInstance().handleKey(key)

	def handleNextSubPage(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_RIGHT)

	def handlePrevSubPage(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_LEFT)

	def handleNextPage(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_UP)

	def handlePrevPage(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_DOWN)

	def handleKeyOk(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_OK)

	def handleTransparent(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_MUTE)

	def handleKeyGreen(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_GREEN)

	def handleKeyYellow(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_YELLOW)

	def handleKeyRed(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_RED)

	def handleKeyBlue(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_BLUE)

	def handleZoom(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_PLUS)

	def handleScreenMode(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_MINUS)

	def handleHint(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_HELP)

	def handleKeyMenu(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_MENU)

	def handleKeyExit(self):
		eTuxtxtApp.getInstance().handleKey(RcCode.RC_HOME)

def main(session, **kwargs):
	session.open(ShellStarter)

def Plugins(**kwargs):
	return PluginDescriptor(name="TuxTXT", description="Videotext", where = PluginDescriptor.WHERE_TELETEXT, fnc=main)

