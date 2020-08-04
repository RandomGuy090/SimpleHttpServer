#/usr/bin/python3
import socket, time, sys, os
from serv import *




def main():
	block = None
	arg = sys.argv
	ADDRESS, PORT = arguments(arg)


	images = ["png", "jpg", "jpeg", "bmp",
			  "gif", "webp", "svg", "mp3"]
	videos = ["webm", "mp4"]
	files = ["zip", ""]
	ser = Server(ADDRESS, PORT)
	while True:
		print(f"\n\nPort: {PORT}")
		clientsocket, address = ser.accept()
		method, loc = ser.readHeader()
		send = GETfunctions(clientsocket)

		

		if loc != "":
			if "." in loc:
				ext = loc.rsplit(".")[-1].lower()

				if ext in images:
					send.sendImg(loc, ext)
				elif ext == "html":
					send.sendHTML(loc)
				elif ext in videos:
					send.sendVideo(loc, ext)
				elif ext in files:
					send.sendFile(loc, ext)
				elif ext == "rar":
					send.sendFile(loc, "x-rar-compressed")
				elif ext == ".tar":
					send.sendFile(loc, "x-tar")
				elif ext == "ico":
					send.sendImg("favicon.jpg", "jpg")
				else:
					#send.notFound()
					send.sendText(loc)
			else:
				#send.notFound()
				send.sendDirecrory(loc)
		else:
			#send.sendHTML("index.html")	
			send.sendDirecrory(loc)
		
def arguments(arg):

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
		try:
			help = arg[arg.index("-h")+1]
		except:
			help = arg[arg.index("--help")+1]	


	return ADDRESS, int(PORT)


if __name__ == "__main__":
	main()
