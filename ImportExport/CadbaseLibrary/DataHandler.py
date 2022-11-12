''' Here are functions for working with data (links, storage, files) '''

import os
import time
import json
import pathlib
from types import SimpleNamespace
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PySide import QtCore
from PySide2 import QtNetwork
import FreeCAD as app
from CadbaseLibrary.CdbsEvn import g_user_agent, g_response_path

def get_file(args):
    t0 = time.time()
    url, filepath = args[0], args[1]
    manager = QtNetwork.QNetworkAccessManager()

    try:
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        request.setRawHeader(b'User-Agent', g_user_agent)
        reply = manager.get(request)
        loop = QtCore.QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
    except Exception as e:
        app.Console.PrintError(f'Exception in download file: {e}\n')
    else:
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            response_bytes = reply.readAll()
            with filepath.open('wb') as f:
                f.write(response_bytes)
            return (filepath, time.time() - t0)
        else:
            app.Console.PrintError('Error\n')

def download_parallel(args):
    t0 = time.time()
    results = ThreadPool(cpu_count() - 1).imap_unordered(get_file, args)

    for result in results:
        app.Console.PrintLog(f'path: "{result[0]}" time: {result[1]} s\n')

    app.Console.PrintMessage(f'Total time: {time.time() - t0} s\n')

def parsing_gpl():
    app.Console.PrintMessage('Data processing, please wait.\n')

    if g_response_path.exists():
        with g_response_path.open('rb', buffering=0) as f:
            x = json.loads(f.readall(), object_hook=lambda d: \
                        SimpleNamespace(**d))

        if x.data:
            return x.data
        else:
            app.Console.PrintError('Error occured:\n')

            for error in x.errors:
                app.Console.PrintError(error.message + '\n')
    else:
        app.Console.PrintError('No file with response\n')

    app.Console.PrintError('Failed\n')


def remove_object(rm_object):
    ''' delete directory or file from local storage '''
    if rm_object.exists():
        if rm_object.is_dir():
            os.rmdir(rm_object)
        else:
            os.remove(rm_object)
        app.Console.PrintLog(f'"{rm_object}" removed\n')


def create_object_path(new_dir, object_info, object_type):
    ''' create a new object path '''
    if new_dir.exists() and not new_dir.is_dir():
        app.Console.PrintError(f'Please remove the "{new_dir}" file for correct operation\n')
    else:
        if not new_dir.is_dir():
            os.mkdir(new_dir)
        new_info_file = new_dir / object_type
        try:
            with new_info_file.open('w') as f:
                f.write(json.dumps(object_info, default=lambda o: o.__dict__, indent=4))
                f.close()
        except Exception as e:
            app.Console.PrintError(f'{e}\n')


def read_object_info(object_type, object):
    ''' read information about an object from a file '''
    with object_type.open('r') as data_file:
        object_info = json.loads(data_file.read(),
                                object_hook=lambda d: SimpleNamespace(**d))
        app.Console.PrintLog(f'Select {object}: {object_info.uuid}\n')
        data_file.close()
        return object_info
