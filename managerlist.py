from colors import *
import string
import tasbot
from tasbot.Plugin import IPlugin
from tasbot.utilities import *
from tasbot.customlog import Log
class Main(IPlugin):
        def __init__(self,name,tasclient):
                IPlugin.__init__(self,name,tasclient)

	def oncommandfromserver(self,command,args,socket):
	  self.logger.Info( command + " ".join(args) )
	  if command == "SAIDPRIVATE" and len(args) >= 2:
	    if args[1].lower() == "!listmanagers":
	      socket.send("SAYPRIVATE %s managerlist %s\n" % ( args[0] , '\t'.join(tasbot.ParseConfig.parselist(self.app.config["managerlist"],','))))
	    if args[1].lower() == "!lm":
	      socket.send("SAYPRIVATE %s managerlist %s\n" % ( args[0] , '\t'.join(parselist(self.app.config["managerlist"],','))))
	    if args[1].lower() == "!addmanager" and args[0] in tasbot.ParseConfig.parselist(self.app.config["admins"],',') and len(args) >= 3:
	      cmns = tasbot.ParseConfig.parselist(self.app.config["managerlist"],',')
	      if args[2] in cmns:
		socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager already in the list"))
	      else:
		cmns.append(args[2])
		self.app.config["managerlist"] = ','.join(cmns)
		self.app.SaveConfig()
		socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager added"))
	    if args[1].lower() == "!removemanager" and args[0] in tasbot.ParseConfig.parselist(self.app.config["admins"],',') and len(args) >= 3:
	      cmns = tasbot.ParseConfig.parselist(self.app.config["managerlist"],',')
	      if not args[2] in cmns:
		socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager doesn't exist in list"))
	      else:
		cmns.remove(args[2])
		self.app.config["managerlist"] = ','.join(cmns)
		self.app.SaveConfig()
		socket.send("SAYPRIVATE %s %s\n" % ( args[0] , "Manager removed"))
	  if command == "CLIENTSTATUS" and len(args) == 2:
	    if getmod(int(args[1])) == 1:
	      cmns = tasbot.ParseConfig.parselist(self.app.config["admins"],',')
	      if not args[0] in cmns:
		cmns.append(args[0])
		self.app.config["admins"] = ','.join(cmns)
		self.app.SaveConfig()
		print purple+"** Added "+green+args[0]+purple+" to admin list"+normal
	def onload(self,tasc):
	  self.app = tasc.main
	def onloggedin(self,socket):
	  socket.send("JOIN autohost\n")

