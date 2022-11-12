''' Global variables of the macro are collected here '''

import pathlib
from PySide.QtGui import QFileDialog, QApplication
import FreeCAD as app

g_param = app.ParamGet('User parameter:Plugins/cadbase_library')
g_api_login = 'https://api.cadbase.rs/login'
g_cdbs_api = 'https://api.cadbase.rs/graphql'
g_program_id = 42 # this is FreeCAD ID in CADBase
g_user_agent = b'Mozilla/5.0 (Macintosh; Intel Mac OS 10 12.3; rv:42.0) \
                Gecko/20100101 Firefox/42.0'
g_content_type = b'application/json'
g_ui_file = app.getUserMacroDir(True) + '/CadbaseLibrary/cadbase_library.ui'
g_ui_file_config = app.getUserMacroDir(True) + '/CadbaseLibrary/cadbase_library_config.ui'

if pathlib.Path(g_param.GetString('destination')).is_dir():
    g_library_path = g_param.GetString('destination')
else:
    folder_dialog = QFileDialog.getExistingDirectory(None,
        QApplication.translate('CADBaseLibrary',
        'Location of your existing CADBase library'))
    g_param.SetString('destination', folder_dialog.replace('\\', '/'))  # forward slashes apparently work on windows too
    g_library_path = g_param.GetString('destination')

# Please don't use this name as the name of files or folders in the CADBase Library folder.
g_response_path = pathlib.Path(g_library_path) / 'cadbase_response_file_2018'

if not g_param.GetString('api-url'):
    g_param.SetString('api-url', g_cdbs_api)

if not g_param.GetString('auth-token'):
    g_param.SetString('auth-token', '')
