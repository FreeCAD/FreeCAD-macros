""" Functionality for processing requests to the CADBase platform """

import json
from PySide2 import QtCore, QtNetwork
import CadbaseLibrary.CdbsEvn as CdbsEvn
import CadbaseLibrary.DataHandler as DataHandler


def parsing_response(reply):
    response_bytes = DataHandler.handle_response(reply)
    if response_bytes:
        DataHandler.remove_object(CdbsEvn.g_response_path)  # deleting old a response if it exists
        with CdbsEvn.g_response_path.open('wb') as file:
            file.write(response_bytes)
        DataHandler.logger('message', 'Successful processing request')
    else:
        DataHandler.logger('error', 'Failed processing request')


class CdbsApi:
    """ Sending a request to the CADBase API and processing the response """

    def __init__(self, query):
        DataHandler.logger('message', 'Getting data...')
        self.nam = QtNetwork.QNetworkAccessManager(None)
        self.do_request(query)

    def do_request(self, query):
        try:
            request = QtNetwork.QNetworkRequest()
            request.setUrl(QtCore.QUrl(CdbsEvn.g_cdbs_api))
            auth_header = 'Bearer ' + CdbsEvn.g_param.GetString('auth-token', '')
            request.setRawHeader(b'Content-Type', CdbsEvn.g_content_type)
            request.setRawHeader(b'Authorization', auth_header.encode())
            body = json.dumps(query).encode('utf-8')
            DataHandler.logger('log', f'Query include body: {body}')
            reply = self.nam.post(request, body)
            loop = QtCore.QEventLoop()
            reply.finished.connect(loop.quit)
            loop.exec_()
        except Exception as e:
            DataHandler.logger('error', f'Exception when trying to sending the request: {e}')
        else:
            parsing_response(reply)
