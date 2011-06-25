from enigma import eTuxtxtApp, eTimer
from Screens.Screen import Screen
from Plugins.Plugin import PluginDescriptor
from Components.Renderer.Picon import reloadPicons
from os import symlink, mkdir, remove, rmdir, path

class ShellStarter(Screen):
	skin = """
		<screen position="1,1" size="1,1" title="TuxTXT" >
                </screen>"""

	def __init__(self, session, args = None):
		self.skin = ShellStarter.skin
		Screen.__init__(self, session)
		self.timer = eTimer()
		self.timer.callback.append(self.pollUIRunning)
		eTuxtxtApp.getInstance().startUi()
		self.timer.start(1000)

	def pollUIRunning(self):
		if eTuxtxtApp.getInstance().getTuxtxtUIRunning()[0] == 1:
			self.timer.start(1000)
		else:
			self.timer.stop()
			reloadPicons()
			self.close()

def main(session, **kwargs):
	session.open(ShellStarter)

def Plugins(**kwargs):
	return PluginDescriptor(name="TuxTXT", description="Videotext", where = PluginDescriptor.WHERE_TELETEXT, fnc=main)

