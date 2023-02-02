""" Functionality for processing requests to the storage of CADBase platform """

import os
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
from CadbaseLibrary.CdbsApi import CdbsApi
from CadbaseLibrary.CdbsStorageApi import CdbsStorageApi
from CadbaseLibrary.QueriesApi import QueriesApi
import CadbaseLibrary.DataHandler as DataHandler


class CdbsStorage:
    """
    The class functions determine which files are suitable for uploading to the CADBase storage,
    request data for uploading files, and call functions to upload files to storage.
    """

    def __init__(self, arg):
        """ Validation the modification uuid and creating variables for next parsing data """
        DataHandler.logger('message', 'Preparing for uploading files...')
        self.modification_uuid = arg[0]
        self.last_clicked_dir = arg[1]  # set directory from which files will be pushed
        if not os.path.isdir(self.last_clicked_dir):
            DataHandler.logger('warning', 'To upload files, you must select the modification folder')
            return
        DataHandler.logger('log', f'Modification uuid: {self.modification_uuid}')
        if not DataHandler.validation_uuid(self.modification_uuid):
            DataHandler.logger('warning', 'To upload files, you must select a modification '
                                          '(so that the macro can determine the target set of files)')
            return
        self.upload_filenames = []  # filenames for upload to the CADBase storage
        self.delete_files = []  # uuids of old files on the CADBase storage
        self.completed_files = []  # uuid of successfully uploaded files
        self.fileset_uuid = None
        self.new_fileset = False
        self.processing_manager()
        DataHandler.logger('message', 'Upload completed')

    def processing_manager(self):
        """ Manager sending files to the storage: defines the uuid for fileset,
        calls the functions for processing, loading and confirm successful uploading files """
        DataHandler.logger('log', 'Getting fileset uuid...')
        # getting the uuid of a set of files for FreeCAD
        CdbsApi(QueriesApi.target_fileset(self.modification_uuid))
        self.fileset_uuid = \
            DataHandler.get_uuid(DataHandler.deep_parsing_gpl('componentModificationFilesets', True))
        DataHandler.logger('log', f'Fileset uuid: {self.fileset_uuid}')
        if not self.fileset_uuid:
            DataHandler.logger('log', 'Create a new set of files for FreeCAD')
            CdbsApi(QueriesApi.register_modification_fileset(self.modification_uuid))
            self.fileset_uuid = DataHandler.deep_parsing_gpl('registerModificationFileset')
            self.new_fileset = True
        if not DataHandler.validation_uuid(self.fileset_uuid):
            DataHandler.logger('warning', 'Error occurred while getting the uuid of the file set')
            return
        if self.fileset_uuid:
            self.define_files()
        if self.upload_filenames:
            # trying to upload files and save a count of successful uploads
            count_up_files = self.upload()
            if not count_up_files:
                DataHandler.logger('warning', 'Error occurred while confirming the upload of files, '
                                              'the files were not uploaded to correctly')
                return
        else:
            DataHandler.logger('warning', 'No files found for upload')
            return
        if count_up_files > 0:
            DataHandler.logger('message', f'Success upload {count_up_files} files to CADBase storage')
            if self.delete_old_files:
                DataHandler.logger('log', 'Files in the CADBase storage have been updated successfully')
        # clear data that will no longer be used
        self.upload_filenames.clear()
        self.delete_files.clear()
        self.completed_files.clear()

    def define_files(self):
        """ Determine files to upload to CADBase storage: getting files from local and remote storage,
        identify duplicates and compare hashes """
        local_files = []  # files from local storage
        # files from the local storage that are not in the CADBase storage
        DataHandler.logger('log', f'Last clicked dir: {self.last_clicked_dir}')
        for path in os.listdir(self.last_clicked_dir):
            # check if current path is a file and skip if the file with technical information
            if os.path.isfile(os.path.join(self.last_clicked_dir, path)) and not path.endswith('modification'):
                local_files.append(path)
        DataHandler.logger('log', f'Local files: {local_files}')
        if not local_files:
            return  # no potential files for uploads found
        cloud_files = []  # files from CADBase storage
        cloud_filenames = []  # filenames of CADBase storage files
        if not self.new_fileset:
            # get file list with hash from CADBase storage
            CdbsApi(QueriesApi.fileset_files(self.fileset_uuid))
            cloud_files = DataHandler.deep_parsing_gpl('componentModificationFilesetFiles', True)
        for cf in cloud_files:
            cloud_filenames.append(cf.get('filename'))  # selecting cloud filenames for validation with locale files
        DataHandler.logger('log', f'Cloud filenames: {cloud_filenames}')
        dup_files = []  # files which are in the local and CADBase storage
        for l_filename in local_files:
            if not self.new_fileset and l_filename in cloud_filenames:
                DataHandler.logger('log', f'The local file "{l_filename}" has a cloud version')
                # save the name of the (old) file for hash check
                dup_files.append(l_filename)
            else:
                DataHandler.logger('log', f'Local file "{l_filename}" does not have a cloud version')
                # save the name of the new file to upload
                self.upload_filenames.append(l_filename)  # add new files to upload
        DataHandler.logger('message', f'New files to upload:{self.upload_filenames}')
        self.parsing_duplicate(dup_files, cloud_files)

    def parsing_duplicate(self, dup_files, cloud_files):
        """ Compare hash for local and CADBase storage files, add files for update if hash don't equally """
        import pathlib
        try:
            from blake3 import blake3
        except Exception as e:
            DataHandler.logger('error', f'Blake3 import error: {e}')
            DataHandler.logger('warning', 'Warning: for compare hashes need install `blake3`. '
                                          'Please try to install it with: `pip install blake3` or some other way.')
            return
        for df in dup_files:
            cloud_file = next(item for item in cloud_files if item['filename'] == df)
            if not cloud_file['hash']:
                DataHandler.logger('warning', f'File hash "{df}" from CADBase not found, this file is skipped.')
                continue
            local_file_hash = ''
            local_file_path = pathlib.Path(self.last_clicked_dir) / df
            if not local_file_path.is_file():
                DataHandler.logger('warning', f'Warning: {df} is not file and skipped')
                break
            try:
                file = local_file_path.open('rb', buffering=0)
                local_file_hash = blake3(file.read()).hexdigest()
                file.close()
            except Exception as e:
                DataHandler.logger('error', f'Error calculating hash for local file {local_file_hash}: {e}')
                break
            DataHandler.logger('log', f'Hash file {df}:\n{local_file_hash} (local)\n{cloud_file["hash"]} (cloud)')
            # check the hash if it exists for both files
            if local_file_hash and cloud_file['hash'] and local_file_hash != cloud_file['hash']:
                self.upload_filenames.append(df)
                self.delete_files.append(cloud_file['uuid'])

    def upload(self):
        """ Getting information (file IDs, pre-signed URLs) to upload files to CADBase storage
        and calling the function to upload files in parallel """
        DataHandler.logger('message', f'Selected files to upload: {self.upload_filenames}')
        CdbsApi(QueriesApi.upload_files_to_fileset(self.fileset_uuid, self.upload_filenames))
        args = DataHandler.deep_parsing_gpl('uploadFilesToFileset', True)  # data for uploading by each file
        if not args:
            return 0
        # data for uploading files to storage received
        DataHandler.logger('message', f'Uploading files to storage (this can take a long time)')
        self.upload_parallel(args)
        if not self.completed_files:
            DataHandler.logger('log', f'Failed to upload files')
            return 0
        # at least some files were uploaded successfully
        CdbsApi(QueriesApi.upload_completed(self.completed_files))
        res = DataHandler.deep_parsing_gpl('uploadCompleted')
        DataHandler.logger('log', f'Upload completed: {res}')
        return res

    def put_file(self, arg: dict):
        """ Uploading a file via presigned URL to the CADBase storage """
        t0 = time.time()
        filename = arg.get('filename')
        file_path = self.last_clicked_dir / filename
        if CdbsStorageApi(arg.get('uploadUrl'), file_path):
            DataHandler.logger('log', f'Completed upload: "{filename}"')
            self.completed_files.append(arg.get('fileUuid'))
        return filename, time.time() - t0

    def upload_parallel(self, args: list):
        """ Asynchronous calling of the function of uploading files to the CADBase storage
        in several threads (if available) """
        t0 = time.time()
        results = ThreadPool(cpu_count() - 1).imap_unordered(self.put_file, args)
        for result in results:
            DataHandler.logger('log', f'Filename: "{result[0]}" time: {result[1]} s')
        DataHandler.logger('message', f'Total time: {time.time() - t0} s')

    @property
    def delete_old_files(self):
        """ Deleting obsolete files from CADBase storage """
        if self.delete_files:
            CdbsApi(QueriesApi.delete_files_from_fileset(self.fileset_uuid, self.delete_files))
            res = DataHandler.deep_parsing_gpl('deleteFilesFromFileset')
            DataHandler.logger('log', f'Delete files from fileset: {res}')
            return res
        return False
