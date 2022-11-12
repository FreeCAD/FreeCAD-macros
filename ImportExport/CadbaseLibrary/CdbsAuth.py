''' This file contains one class for authorization on the CADBase platform '''

import json
from PySide import QtCore  # FreeCAD's PySide
from PySide2 import QtNetwork
import FreeCAD as app
from CadbaseLibrary.CdbsEvn import g_param, g_api_login, g_content_type
from CadbaseLibrary.DataHandler import logger

class CdbsAuth:
    ''' class for getting a token to access the CADBase platform '''

    def __init__(self, username, password):
        logger(3, 'Getting a new token, please wait.')

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
        er = reply.error()

        if er == QtNetwork.QNetworkReply.NoError:
            response_bytes = reply.readAll()
            token = json.loads(str(response_bytes, 'utf-8'))
            g_param.SetString('auth-token', token['bearer'])

            logger(3, 'Success')
        else:
            logger(1, f'Error occured: {er}')
            logger(1, reply.errorString())
