#/usr/bin/python3
import socket, time, sys, os
from serv import *




def main():
	block = None
	arg = sys.argv
	ADDRESS, PORT, PATH = arguments(arg)
	add = ""

	images = ["png", "jpg", "jpeg", "bmp",
			  "gif", "webp", "svg", "mp3"]
	videos = ["webm", "mp4"]
	files = ["zip"]
	ser = Server(ADDRESS, PORT)
	while True:
		print(f"\n\nPort: {PORT}")
		clientsocket, address = ser.accept()
		method, loc = ser.readHeader()
		send = GETfunctions(clientsocket, PATH)

		add = f"{PATH}{loc}"
		print(f"***{add}  ++")
		

		if loc != "":
			if "." in loc:


				ext = loc.rsplit(".")[-1].lower()

				if ext in images:
					print("sendimg")
					send.sendImg(loc, ext)
				elif ext == "html":
					print("sendHTML")
					send.sendHTML(loc)
				elif ext in videos:
					print("sendVideo")
					send.sendVideo(loc, ext)
				elif ext in files:
					print("sendFile")
					send.sendFile(loc, ext)
				elif ext == "rar":
					print("sendFile")
					send.sendFile(loc, "x-rar-compressed")
				elif ext == ".tar":
					send.sendFile(loc, "x-tar")
				elif ext == "ico":
					print("sendImg")
					send.sendImg("favicon.jpg", "jpg")
				elif loc.rsplit("/")[-1][0] == ".":
					print("sendDirecrory")
					ret = send.sendDirecrory(loc)
					if ret == -1:
						print("sendText")
						send.sendText(loc)
				else:
					#send.notFound()
					print("sendDirecroryy")
					ret = send.sendDirecrory(loc)
					if ret == -1:
						print("sendTextt")
						send.sendText(loc)
			else:
				try:
					print("sendDirecroryyy")
					ret = send.sendDirecrory(loc)
					if ret == -1:
						print("sendTexttt")
						send.sendText(loc)

				except:					
					print("sendFile")
					sednd.sendFile(loc)
				#send.notFound()
		else:
			print("sendDirecrory")
			#send.sendHTML("index.html")	
			send.sendDirecrory(loc)
		
def arguments(arg):

	helpTmp="""
-a --address 		set address
-p --port 		set port
-P --path 		set path
	"""

	if "-a" in arg or "--address" in arg:
		try:
			ADDRESS = arg[arg.index("-a")+1]
		except:
			ADDRESS = arg[arg.index("--address")+1]
	else:
		ADDRESS = "127.0.0.1"
	
	if "-p" in arg or  "--port" in arg:
		try:
			PORT = arg[arg.index("-p")+1]
		except:
			PORT = arg[arg.index("--port")+1]
	else:
		PORT = "8080"
	if "-h" in arg or "--help" in arg:
		print(helpTmp)
		sys.exit(0)

	if "-P" in arg or "--path" in arg:
		try:
			PATH = arg[arg.index("--port")+1]
		except:
			PATH = arg[arg.index("-P")+1]
		if PATH[-1] != "/" or PATH[-1] != "\\":
			PATH = PATH+"/"
	else:
		PATH = None



	return ADDRESS, int(PORT), PATH


if __name__ == "__main__":
	main()
