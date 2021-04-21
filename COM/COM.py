from .cgiserver import runServer, getMimeType
import logging as log
from .htmlhelpers import fileRead
#from .data import dataa
import threading, os

class Communication:
    def __init__(self, data, port):
        self.data = data
        self.port = port
        self.__isServerRunning = False
        self.runThread = threading.Thread(target=self.__Run, args=())
        self.commands = []
        self.thisPath = os.path.dirname(os.path.abspath(__file__)) + os.sep

    def __Run(self):
        runServer(self.port, {
            "": self.__home,
            "/": self.__home,
            # 'json': processJSONRequest,
            # 'button': processButton
            "console": self.__console,
            "console/data.js": self.__dataJS,
            "console/send": self.consoleSend,
            "console/script.js": self.__scriptJS,
            "console/commands.js": self.__commands,
            "console/w3schools.css": self.__w3schoolsCSS
        })

    def __home(self, request, response):
        s = ''
        for key, value in request.query.items():
            s += f'{key}:{value}<br>'
        response.buildResult('<h2>Params:</h2>' + s + "<br><a href='console'>Console</a><script>document.title = 'Server'</script>")


    def __console(self, request, response):
        response.buildResult(fileRead(self.thisPath+'consolePage/console.html'))


    def __dataJS(self, request, response):
        response.buildResult("var data = " + str(self.data), getMimeType("data.js"))

    def __scriptJS(self, request, response):
        response.buildResult(fileRead(self.thisPath+'consolePage/script.js'), getMimeType("script.js"))

    def __w3schoolsCSS(self, request, response):
        response.buildResult(fileRead(self.thisPath+'consolePage/w3schools.css'), getMimeType("w3schools.css"))

    def __commands(self, request, response):
        result = "var commands = []"
        if len(self.commands) > 0:
            #result = "var commands = " + str(self.commands)
            result = "send('Readed_0')"
        response.buildResult(result, getMimeType("commands.js"))

    def consoleSend(self, request, response):
        text = request.query["text"]

        if text.find("Readed_") > -1 and len(self.commands) > 0:
            #print(int(text.replace("Readed_", "")))
            del self.commands[int(text.replace("Readed_", ""))]

        response.buildResult(fileRead(self.thisPath+'consolePage/consoleSend.html'), getMimeType("consoleSend.html"))
        self.__onReceive(text)

    def __onReceive(self, text):
        #print("Receiving text: "+text)
        self.onReceive(text)

    def onReceive(self, text):
        pass

    def __send(self, text):
        #print("Sending text: "+text)
        self.commands.append(text)

    def reloadConsole(self):
        if not self.commands.__contains__("document.location.reload()"):
            self.__send("document.location.reload()")

    def run(self):
        if not self.__isServerRunning:
            self.__isServerRunning = True
            self.runThread.start()
        else:
            print(f"Server is already running at port {self.port}, url is: http://localhost:{self.port}/")
