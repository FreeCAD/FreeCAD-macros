"""This file contains functions for log, processing responses, working with files, and checking """

import os
import time
import json
import pathlib
from types import SimpleNamespace
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from PySide2 import QtCore, QtNetwork
import FreeCAD as App
import CadbaseLibrary.CdbsEvn as CdbsEvn


def logger(type_msg, msg):
    """ Processing the output of messages for the user
    and saving them to the log file, if it exists """
    if type_msg == 'error':
        App.Console.PrintError(f'{msg}\n')
    elif type_msg == 'warning':
        App.Console.PrintWarning(f'{msg}\n')
    elif type_msg == 'message':
        App.Console.PrintMessage(f'{msg}\n')
    else:
        App.Console.PrintLog(f'{msg}\n')
    # Save the message to the log file if there is a log file in the folder
    if CdbsEvn.g_log_file_path.is_file():
        log_file = open(CdbsEvn.g_log_file_path, 'a')
        log_file.write(f'\nConsole {type_msg} {time.time()}: {msg}')
        log_file.close()


def validation_uuid(target_uuid):
    """ Checking an uuid length. Return target UUID if valid
    or None if the uuid failed the test """
    if target_uuid and len(target_uuid) == CdbsEvn.g_len_uuid:
        return target_uuid
    return None


def handle_response(reply):
    er = reply.error()
    if er == QtNetwork.QNetworkReply.NoError:
        if reply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute) == 200:
            logger('message', 'Success')
            return reply.readAll()
        else:
            logger('error',
                   f'Failed, status code: {reply.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)}')
    else:
        logger('error', f'Error occurred: {er}')
        logger('error', f'{reply.errorString()}')


def get_file(args):
    """ Downloads and saves a file of args data to the user's local storage.
    Argument (args) for this function have url and filepath (path/filename). """
    t0 = time.time()
    url = args[0]
    filepath = args[1]
    if filepath.exists():
        logger('warning', f'File "{filepath}" already exists and skipped.')
        return filepath, time.time() - t0
    manager = QtNetwork.QNetworkAccessManager(None)
    try:
        request = QtNetwork.QNetworkRequest()
        request.setUrl(QtCore.QUrl(url))
        request.setRawHeader(b'User-Agent', CdbsEvn.g_user_agent)
        reply = manager.get(request)
        loop = QtCore.QEventLoop()
        reply.finished.connect(loop.quit)
        loop.exec_()
    except Exception as e:
        logger('error', f'Exception in download file: {e}')
    else:
        if reply.error() == QtNetwork.QNetworkReply.NoError:
            response_bytes = reply.readAll()
            with filepath.open('wb') as f:
                f.write(response_bytes)
        else:
            logger('error', f'Error: {reply.error()}')
    return filepath, time.time() - t0


def download_parallel(args):
    """ Running the file download function in parallel streams
    and keeps track of the total download time (if available) """
    t0 = time.time()
    results = ThreadPool(cpu_count() - 1).imap_unordered(get_file, args)
    for result in results:
        logger('log', f'path: "{result[0]}" time: {result[1]} s')
    logger('message', f'Total time: {time.time() - t0} s')


def parsing_gpl():
    """ Parsing data from file with a response into a namespace """
    logger('message', 'Data processing, please wait.')
    if not CdbsEvn.g_response_path.exists():
        logger('error', 'Not found file with response')
    try:
        with CdbsEvn.g_response_path.open('rb', buffering=0) as f:
            res = json.loads(f.readall(), object_hook=lambda d: SimpleNamespace(**d))
            if res.data:
                return res.data
            # if there is no data, tries to get an error message
            logger('error', 'Error occurred:')
            for error in res.errors:
                logger('error', error.message)
    except Exception as e:
        logger('error', f'Exception occurred while parsing the server response: {str(e)}')


def remove_object(rm_object: pathlib.Path):
    """ Removing directory or file from local storage """
    if not rm_object.exists():
        logger('log', f'No data found to delete')
        return
    # saving the previous server response to a log file, if it exists
    if rm_object == CdbsEvn.g_response_path and CdbsEvn.g_log_file_path.is_file():
        try:
            with open(CdbsEvn.g_response_path) as response_file:
                with open(CdbsEvn.g_log_file_path, 'a') as log_file:
                    log_file.write(f'\nResponse before {time.time()}:\n')
                    for line in response_file:
                        log_file.write(line)
            response_file.close()
            log_file.close()
        except Exception as e:
            logger('error', f'Exception occurred while trying to save old response: {str(e)}')
    if rm_object.is_dir():
        os.rmdir(rm_object)
    else:
        os.remove(rm_object)
    logger('log', f'"{rm_object}" removed')


def create_object_path(new_dir: pathlib.Path, object_info: str, object_type: str):
    """ Creating a new object path """
    if new_dir.is_file():
        logger('error', f'Please remove the "{new_dir}" file for correct operation')
        return
    if not new_dir.is_dir():
        os.mkdir(new_dir)
    new_info_file = new_dir / object_type
    try:
        with new_info_file.open('w') as f:
            f.write(json.dumps(object_info, default=lambda o: o.__dict__, indent=4))
            f.close()
    except Exception as e:
        logger('error', f'Exception occurred while trying to write the file: {str(e)}')


def read_object_info(info_file: pathlib.Path, select_object: str):
    """ Reading information about an object from a special file """
    try:
        with info_file.open('r') as data_file:
            object_info = json.loads(data_file.read(), object_hook=lambda d: SimpleNamespace(**d))
            logger('log', f'Select {select_object}: {object_info.uuid}')
            data_file.close()
    except Exception as e:
        logger('error', f'Exception when trying to read information from the file: {str(e)}')
    else:
        return object_info


def deep_parsing_gpl(target, try_dict=False):
    """ Parsing response data with SimpleNamespace by target key and then return structure """
    data = parsing_gpl()
    if not data:
        logger('log', f'Failed to parse gpl before deep parsing: {data}')
        return
    try:
        pre_result = getattr(data, target)
    except Exception as e:
        logger('warning', f'Received data about "{target}" is not suitable for processing: {e}')
        return
    if not try_dict:
        return pre_result
    # converting namespace to dict
    result = []
    for rd in pre_result:
        result.append(vars(rd))
    return result


def get_uuid(structure_data):
    """ Getting an uuid if it exists in the data. Returning None if not found uuid. """
    target_uuid = None
    logger('log', f'Structure data: {structure_data}')
    if not structure_data:
        logger('log', f'Not found data for uuid selection: {structure_data}')
        return
    vars_data = structure_data[0]
    logger('log', f'Structure vars: {vars_data}')
    # are the known fields that store the uuid of the object
    if vars_data.get('uuid'):
        target_uuid = vars_data.get('uuid')
    if vars_data.get('fileUuid'):
        target_uuid = vars_data.get('fileUuid')
    logger('log', f'Uuid of structure data: {target_uuid}')
    return validation_uuid(target_uuid)
