
import os, sys, socket, base64
class Server(object):

	HEADERSIZE = 1000
	CLIENTSOCKET = None
	PATH = None
	s = None


	def __init__(self, adress, port):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.bind((adress, port))
		self.s.listen(5)



	def accept(self): #accept connection
		try:
			self.CLIENTSOCKET, address = self.s.accept()
			print(f"<-->new connection from {address}<-->")
			return self.CLIENTSOCKET, address
		except Exception as e:
			print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}")
			print(sys.exc_info()[0])
			print("Error on accepting")
			return -1, -1

	def readHeader(self): 	#read received header
		try:
			recv = str(self.CLIENTSOCKET.recv(self.HEADERSIZE))
			print(recv[2:60])
			method = recv.rsplit(" ")[0][2:]
			loc = recv.rsplit(" ")[1][1:]
			return method, loc
		
		except Exception as e:
			print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}")
			print(sys.exc_info()[0])
			print("Error on receving")
			return -1, -1

	def kill(self):
		self.CLIENTSOCKET.close()



class GETfunctions(object):
	CLIENTSOCKET = None
	PATH = None
	
	
	def __init__(self, clientsocket, path=None):
		self.CLIENTSOCKET = clientsocket
		self.PATH = path

		print(f"@@+{self.PATH}")
	


	def notFound(self): #page not found
		header =f"HTTP/1.1 404 Not Found \n"
		print("XX 404 Not Found XX")
		header = header.encode("utf-8")
		self.CLIENTSOCKET.send(header)
		self.CLIENTSOCKET.close()



	def getLocation(self): #get locaton of running file
		path = __file__
		path = path[:-len(os.path.basename(__file__))]
		return path


	def listFiles(self, loc=None): #list files in directory with running file
		if self.PATH == None:
			self.PATH = self.getLocation()
			path = self.PATH
		else:
			path = self.PATH
		
		try:
			#files = os.listdir(path+loc);
			files = os.listdir(loc);
		except Exception as e:
			print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}") 
			files = os.listdir(path+loc);


		return files

		
	def sendHTML(self, loc): #send html page
		files = self.listFiles()
		
		if self.PATH == None:
			self.PATH = self.getLocation()
			path = self.PATH
		else:
			path = self.PATH
		loc = loc.rsplit("/")[-1]
		print(f":::: {loc}")
		print(files)
		try:			
			header =f"HTTP/1.1 200 OK\n"\
					f"Content-Type: text/html\n"\
					f"Accept-Charset: utf-8\n"\
					"Content-Length: "
			
			with open(path+loc,"r") as f:
				msg = f.read()
			send = header+str(len(msg))+"\n\n"+msg
			self.CLIENTSOCKET.send(bytes(send, "utf-8"))
			self.CLIENTSOCKET.close()

		except Exception as e:
			print(e)
			print(f"XX no page: {loc} XX")
			self.notFound()


	def sendImg(self, loc, ext): #send image 
		self.listFiles()
		if self.PATH == None:
			self.PATH = self.getLocation()
			path = self.PATH
		else:
			path = self.PATH
		print(loc)

		header = f"HTTP/1.1 200 OK\n"\
				 f"Content-Type: image/{ext}\n\n"	
		try:
			with open(self.PATH+loc,"rb") as f:
				msg = f.read()	
			header = header.encode("utf-8")
			send = header+msg
			
			self.CLIENTSOCKET.send(send)
			self.CLIENTSOCKET.close()
		
		except Exception as e:
			print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}")
			if loc.rsplit(".")[0] == "favicon":
				print(f"XX No image: {loc} XX")
				self.notFound()
				self.CLIENTSOCKET.close()
				return 0
					
			print(f"XX No image: {loc} XX")
			msg = f"XX No image: {loc} XX"
			send = f"{header}{len(str(msg))}\n\n{msg}"
			self.sendText(f"no image Found: {loc}")
			self.CLIENTSOCKET.close()
		


	def sendText(self, content="Hello world!"): #send text
		header =f"HTTP/1.1 200 OK\n"\
				f"Content-Type: text/plain\n"\
				f"Accept-Charset: utf-8\n"\
				"Content-Length: "
		try:
			try:
				with open(content,"r") as f:
					msg = f.read()
					send = header+str(len(msg))+"\n\n"+msg
			except Exception as e:
				content = self.PATH + content
				print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}")
				with open(content,"rb") as f:
					msg = f.read()
					send = header+str(len(msg))+"\n\n"+str(msg)
		
		except:
			send = header+str(len(content))+"\n\n"+content
		
		self.CLIENTSOCKET.send(bytes(send, "utf-8"))

	def sendVideo(self, loc, ext):
		self.listFiles()
		if self.PATH == None:
			self.PATH = self.getLocation()
			path = self.PATH
		else:
			path = self.PATH

		header = f"HTTP/1.1 200 OK\n"\
				 f"Content-Type: video/{ext}\n\n"	
		try:
			with open(loc,"rb") as f:
				msg = f.read()	
			header = header.encode("utf-8")
			send = header+msg
			
			self.CLIENTSOCKET.send(send)
			self.CLIENTSOCKET.close()
		
		except Exception as e:
			print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}")
			print(f"XX No image: {loc} XX")
			msg = f"XX No image: {loc} XX"
			send = f"{header}{len(str(msg))}\n\n{msg}"
			self.sendText(f"no image Video: {loc}")
			self.CLIENTSOCKET.close()

	def createHtml(self,loc, files):
		headHTML = """
			<!DOCTYPE html>
			<html>
			<head>
			<meta charset="UTF-8">
			<title>TITLE</title>
			<style type="text/css">
				.header{
					height: 10vh;
					width: 90vw;
					border-bottom-style: solid;
					border-bottom-width: 1px;
					border-bottom-color: #ff0000;
				}
			</style>
			</head>
			<body>
			<div class="header">
			<h1>HEADER</h1>
			</div>
			<div class="list">
			"""
		endHTML = """
					</div>
					</body>
					</html>
						"""
		headHTML = headHTML.replace("TITLE", f"{self.PATH}/{loc}")
		headHTML = headHTML.replace("HEADER", f"/{loc}")

		list = ""
		for file in files:
			list = list+ f'\n</br><a href="{loc.rsplit("/")[-1]}/{file}">{file}</a>'

			

		msg = f"{headHTML}  {list} {endHTML}"
		return msg


	def sendFile(self, loc, ext): #send file 
		self.listFiles()
		if self.PATH == None:
			self.PATH = self.getLocation()
			path = self.PATH
		else:
			path = self.PATH

		header = f"HTTP/1.1 200 OK\n"\
				 f"Content-Type: application/{ext}\n\n"	
		try:
			with open(loc,"rb") as f:
				msg = f.read()	
			header = header.encode("utf-8")
			send = header+msg
			
			self.CLIENTSOCKET.send(send)
			self.CLIENTSOCKET.close()
		
		except Exception as e:
			print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}")
			self.notFound()
			self.CLIENTSOCKET.close()


	def sendDirecrory(self, loc):
		try:
			files = self.listFiles(loc)
		except Exception as e:
			print(f"{e} /// line {sys.exc_info()[-1].tb_lineno}")
			files = self.listFiles()
			loc = "/"
			return -1

		
		if self.PATH == None:
			self.PATH = self.getLocation()
			path = self.PATH
		else:
			path = self.PATH
				
		header =f"HTTP/1.1 200 OK\n"\
				f"Content-Type: text/html\n"\
				f"Accept-Charset: utf-8\n"\
				"Content-Length: "
			
		msg = self.createHtml(loc, files)
		msg = msg.replace("//","/")
		send = header+str(len(msg))+"\n\n"+msg
		self.CLIENTSOCKET.send(bytes(send, "utf-8"))
		self.CLIENTSOCKET.close()



