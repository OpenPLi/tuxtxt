from enigma import eTuxtxtApp, eTimer
from enigma import eConsoleAppContainer, iServiceInformation, fbClass, eRCInput, eDBoxLCD
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
		self.container=eConsoleAppContainer()
		self.container.appClosed.append(self.finished)
		self.timer = eTimer()
		self.timer.callback.append(self.pollUIRunning)
		self.runapp()

	def runapp(self):
		eTuxtxtApp.getInstance().startUi()
		print eTuxtxtApp.getInstance().getTuxtxtUIRunning()
		self.timer.start(1000)

	def pollUIRunning(self):
		a = eTuxtxtApp.getInstance().getTuxtxtUIRunning()
		print a
		if eTuxtxtApp.getInstance().getTuxtxtUIRunning()[0] == 1:
			self.timer.start(1000)
		else:
			self.timer.stop()
			reloadPicons()
			self.finished(-1)

	def finished(self,retval):
		self.close()

def main(session, **kwargs):
	session.open(ShellStarter)

def Plugins(**kwargs):
	return PluginDescriptor(name="TuxTXT", description="Videotext", where = PluginDescriptor.WHERE_TELETEXT, fnc=main)

