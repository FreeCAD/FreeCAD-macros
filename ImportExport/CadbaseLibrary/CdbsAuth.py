''' This file contains one class for authorization on the CADBase platform '''

import json
from PySide import QtCore
from PySide2 import QtNetwork
import FreeCAD as app
from CadbaseLibrary.CdbsEvn import g_param, g_api_login, g_content_type

class CdbsAuth:
    ''' class for getting a token to access the CADBase platform '''

    def __init__(self, username, password):
        app.Console.PrintMessage('Getting a new token, please wait.\n')

        query = {'user': {'username': username, 'password': password}}

        self.do_request(query)

    def do_request(self, query):
        req = QtNetwork.QNetworkRequest(QtCore.QUrl(g_api_login))

        req.setRawHeader(b'Content-Type', g_content_type);

        body = json.dumps(query).encode('utf-8')
        self.nam = QtNetwork.QNetworkAccessManager()
        reply = self.nam.post(req, body)
        loop = QtCore.QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
        self.handle_response(reply)

    def handle_response(self, reply):
        global g_param

        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:
            response_bytes = reply.readAll()
            token = json.loads(str(response_bytes, 'utf-8'))
            g_param.SetString('auth-token', token['bearer'])

            app.Console.PrintMessage('Success\n')
        else:
            app.Console.PrintError(f'Error occured: {er}\n')
            app.Console.PrintError(reply.errorString() + '\n')
