from enigma import eTuxtxtApp, getDesktop
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor

class ShellStarter(Screen):
	skin = """
		<screen position="1,1" size="1,1" title="TuxTXT" >
		</screen>"""

	def __init__(self, session, infobar):
		self.skin = ShellStarter.skin
		Screen.__init__(self, session)
		self.infobar = infobar
		self.subtitle = infobar and infobar.selected_subtitle
		if self.subtitle:
			infobar.enableSubtitle(None)
		eTuxtxtApp.getInstance().appClosed.get().append(self.appClosed)
		eTuxtxtApp.getInstance().startUi()

	def appClosed(self):
		eTuxtxtApp.getInstance().appClosed.get().remove(self.appClosed)
		#force redraw
		dsk = getDesktop(0)
		dsk.resize(dsk.size())
		if self.subtitle:
			self.infobar.enableSubtitle(self.subtitle)
		self.close()

def main(session, infobar=None, **kwargs):
	session.open(ShellStarter, infobar)

def Plugins(**kwargs):
	return PluginDescriptor(name="TuxTXT", description="Videotext", where = PluginDescriptor.WHERE_TELETEXT, fnc=main)

