"""
This file stores GraphQL requests for CADbase platform.
Contains queries for the CADBase (using GraphQL API).
"""

import json
import CadbaseLibrary.CdbsEvn as CdbsEvn


class QueriesApi:
    @staticmethod
    def fav_components():
        return dict(query='''query {
                  components (args: {
                    favorite: true
                  }) {
                    uuid
                    name
                    ownerUser {
                      uuid
                      username
                    }
                  }
                }''')

    def component_modifications(object_uuid: str):
        return dict(query=f'''query {{
                  componentModifications (args: {{
                    componentUuid: "{object_uuid}"
                  }}) {{
                    uuid
                    modificationName
                  }}
                }}''')

    def target_fileset(object_uuid: str):
        return dict(query=f'''query {{
                  componentModificationFilesets (args: {{
                    modificationUuid: "{object_uuid}"
                    programIds: {CdbsEvn.g_program_id}
                  }}) {{
                    uuid
                  }}
                }}''')

    def fileset_files(object_uuid):
        return dict(query=f'''query {{
                  componentModificationFilesetFiles (args: {{
                    filesetUuid: "{object_uuid}"
                  }}) {{
                    uuid
                    hash
                    filename
                    downloadUrl
                  }}
                }}''')

    def register_modification_fileset(modification_uuid):
        return dict(query=f'''mutation {{
                    registerModificationFileset (args: {{
                        modificationUuid: "{modification_uuid}"
                        programId: {CdbsEvn.g_program_id}
                    }})
                }}''')

    def upload_files_to_fileset(fileset_uuid, filenames):
        return dict(query=f'''mutation {{
                  uploadFilesToFileset (args: {{
                    filesetUuid: "{fileset_uuid}"
                    filenames: {json.dumps(filenames)}
                  }}) {{
                    fileUuid
                    filename
                    uploadUrl
                  }}
                }}''')

    def upload_completed(file_uuids: list):
        return dict(query=f'''mutation {{
                  uploadCompleted (fileUuids: {json.dumps(file_uuids)})
                }}''')

    def delete_files_from_fileset(fileset_uuid, file_uuids: list):
        return dict(query=f'''mutation {{
                  deleteFilesFromFileset (args: {{
                    filesetUuid: "{fileset_uuid}"
                    fileUuids: {json.dumps(file_uuids)}
                  }})
                }}''')
