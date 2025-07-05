import logging
logger = logging.getLogger(__name__)

class SceneClipboard():
    def __init__(self, scene):
        self.scene = scene

    def serializeSelected(self, delete:bool = False):
        return {}
    
    def deserializeFromClipboard(self, data):
        logger.debug("")
        logger.debug("deserialization from clipboard, data: " + data)