''' This file stores GraphQL requests for CADbase platform '''

from CadbaseLibrary.CdbsEvn import g_program_id

class QueriesApi:
    ''' class contains queries for the CADBase (using GraphQL API) '''

    def fav_components():
        return {'query': '''{
          components (args: {
            favorite: true
          }) {
            uuid
            name
            ownerUser {
              uuid
              username
            }
            imageFile {
              uuid
              filename
              downloadUrl
            }
          }
        }'''}

    def component_modifications(object_uuid):
        return {'query': f'''{{
          componentModifications (args: {{
            componentUuid: "{object_uuid}"
          }}) {{
            uuid
            modificationName
          }}
        }}'''}

    def target_fileset(object_uuid):
        return {'query': f'''{{
          componentModificationFilesets (args: {{
            modificationUuid: "{object_uuid}"
            programIds: {g_program_id}
          }}) {{
            uuid
          }}
        }}'''}

    def fileset_files(object_uuid):
        return {'query': f'''{{
          componentModificationFilesetFiles (args: {{
            filesetUuid: "{object_uuid}"
          }}) {{
            uuid
            filename
            downloadUrl
          }}
        }}'''}
