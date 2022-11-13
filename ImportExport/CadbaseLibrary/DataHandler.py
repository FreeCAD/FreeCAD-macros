''' Here are functions for working with data (links, storage, files) '''

import os
import time
import json
import pathlib
from types import SimpleNamespace
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PySide import QtCore  # FreeCAD's PySide
from PySide2 import QtNetwork
import FreeCAD as app
from CadbaseLibrary.CdbsEvn import g_user_agent, g_response_path

def get_file(args):
    '''
    This function downloads and saves a file of args data to the user's local storage.
    Argument (args) for this function have a url and filepath (path/filename).
    '''
    t0 = time.time()
    url, filepath = args[0], args[1]

    if filepath.exists():
        logger(2, f'File "{filepath}" already exists and skipped.')
        return (filepath, time.time() - t0)

    manager = QtNetwork.QNetworkAccessManager()

    try:
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        request.setRawHeader(b'User-Agent', g_user_agent)
        reply = manager.get(request)
        loop = QtCore.QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
    except Exception as e:
        logger(1, f'Exception in download file: {e}')
    else:
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            response_bytes = reply.readAll()
            with filepath.open('wb') as f:
                f.write(response_bytes)
            return (filepath, time.time() - t0)
        else:
            logger(1, 'Error')

def download_parallel(args):
    t0 = time.time()
    results = ThreadPool(cpu_count() - 1).imap_unordered(get_file, args)

    for result in results:
        logger(4, f'path: "{result[0]}" time: {result[1]} s')

    logger(3, f'Total time: {time.time() - t0} s')

def parsing_gpl():
    logger(3, 'Data processing, please wait.')

    if g_response_path.exists():
        with g_response_path.open('rb', buffering=0) as f:
            x = json.loads(f.readall(),
                 object_hook=lambda d: SimpleNamespace(**d))

        if x.data:
            return x.data
        else:
            logger(1, 'Error occured:')

            for error in x.errors:
                logger(1, error.message)
    else:
        logger(1, 'No file with response')

    logger(1, 'Failed')


def remove_object(rm_object):
    ''' delete directory or file from local storage '''
    if rm_object.exists():
        if rm_object.is_dir():
            os.rmdir(rm_object)
        else:
            os.remove(rm_object)
        logger(4, f'"{rm_object}" removed')


def create_object_path(new_dir, object_info, object_type):
    ''' create a new object path '''
    if new_dir.exists() and not new_dir.is_dir():
        logger(1, f'Please remove the "{new_dir}" file for correct operation')
    else:
        if not new_dir.is_dir():
            os.mkdir(new_dir)
        new_info_file = new_dir / object_type
        try:
            with new_info_file.open('w') as f:
                f.write(json.dumps(object_info, default=lambda o: o.__dict__, indent=4))
                f.close()
        except Exception as e:
            logger(1, e)


def read_object_info(object_type, object):
    ''' read information about an object from a file '''
    with object_type.open('r') as data_file:
        object_info = json.loads(data_file.read(),
                                object_hook=lambda d: SimpleNamespace(**d))
        logger(4, f'Select {object}: {object_info.uuid}')
        data_file.close()
        return object_info

def logger(type, msg):
    ''' this function is used to shorten the code for logging '''
    match type:
        case 1:
            app.Console.PrintError(f'{msg}\n')
        case 2:
            app.Console.PrintWarning(f'{msg}\n')
        case 3:
            app.Console.PrintMessage(f'{msg}\n')
        case _:
            app.Console.PrintLog(f'{msg}\n')
