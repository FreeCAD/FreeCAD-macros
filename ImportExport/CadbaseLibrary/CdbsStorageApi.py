""" Functionality for processing requests to the storage (S3) of CADBase platform """

from PySide2 import QtCore, QtNetwork
from PySide2.QtCore import QFile
import CadbaseLibrary.DataHandler as DataHandler


class CdbsStorageApi:
    """ Sending a file to CADBase storage and handling response (empty response - good case) """

    def __init__(self, presigned_url, file_path):
        DataHandler.logger('message', 'Preparing for upload file...')
        self.presigned_url = presigned_url
        self.file_path = file_path
        self.nam = QtNetwork.QNetworkAccessManager(None)
        self.do_request()

    def do_request(self):
        file = QFile(self.file_path.absolute().as_posix())
        if not file.open(QtCore.QIODevice.OpenModeFlag.ReadOnly):
            DataHandler.logger('message', f'Can not read file...')
            return
        try:
            request = QtNetwork.QNetworkRequest()
            request.setUrl(QtCore.QUrl(self.presigned_url))
            reply = self.nam.put(request, file)
            loop = QtCore.QEventLoop()
            DataHandler.logger('message', f'Upload file...')
            reply.finished.connect(loop.quit)
            loop.exec_()
        except Exception as e:
            DataHandler.logger('error', f'Exception in upload file: {e}')
        else:
            response_bytes = DataHandler.handle_response(reply)
            DataHandler.logger('log', f'Upload file, response bytes: {response_bytes}')
