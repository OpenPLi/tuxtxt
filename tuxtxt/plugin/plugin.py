from enigma import eTuxtxtApp, getDesktop
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Screens.InfoBar import InfoBar

class ShellStarter(Screen):
	skin = """
		<screen position="1,1" size="1,1" title="TuxTXT" >
		</screen>"""

	def __init__(self, session, args = None):
		self.skin = ShellStarter.skin
		Screen.__init__(self, session)
		self.subtitle = InfoBar.instance.selected_subtitle
		if self.subtitle:
			InfoBar.instance.enableSubtitle(None)
		eTuxtxtApp.getInstance().appClosed.get().append(self.appClosed)
		eTuxtxtApp.getInstance().startUi()

	def appClosed(self):
		eTuxtxtApp.getInstance().appClosed.get().remove(self.appClosed)
		#force redraw
		dsk = getDesktop(0)
		dsk.resize(dsk.size())
		if self.subtitle:
			InfoBar.instance.enableSubtitle(self.subtitle)
		self.close()

def main(session, **kwargs):
	session.open(ShellStarter)

def Plugins(**kwargs):
	return PluginDescriptor(name="TuxTXT", description="Videotext", where = PluginDescriptor.WHERE_TELETEXT, fnc=main)

