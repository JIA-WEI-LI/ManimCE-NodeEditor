# utils/logger.py
import logging
import os

DEBUG_MODE = True
ENABLE_FILE_LOG = False

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, 'nodeeditor.log')

LOG_FORMAT = '[%(levelname)s] %(name)s:%(lineno)d → %(message)s'
formatter = logging.Formatter(LOG_FORMAT)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

file_handler = None
if ENABLE_FILE_LOG:
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG if DEBUG_MODE else logging.INFO)

if not any(isinstance(h, logging.StreamHandler) for h in root_logger.handlers):
    root_logger.addHandler(console_handler)
if file_handler and not any(isinstance(h, logging.FileHandler) for h in root_logger.handlers):
    root_logger.addHandler(file_handler)

logging.getLogger("node_editor.node_editor_window.content.node_content_widget").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.core.edge").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.core.scene_history").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.core.node").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.core.scene").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.core.socket").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.graphics.graphics_edge").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.graphics.graphics_node").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.graphics.graphics_scene").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.graphics.graphics_socket").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.graphics.graphics_view").setLevel(logging.INFO)
logging.getLogger("node_editor.node_editor_window.ui.node_editor_window").setLevel(logging.INFO)
