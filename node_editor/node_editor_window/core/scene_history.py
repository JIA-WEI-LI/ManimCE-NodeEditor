import logging
logger = logging.getLogger(__name__)

class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 8

    def undo(self):
        logger.debug("UNDO")

    def redo(self):
        logger.debug("REDO")

    def restoreHistory(self):
        logger.debug(f"Restoring history ... current step: {self.history_current_step:%d} {len(self.history_stack)}")
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])

    def storeHistory(self, desc):
        logger.debug(f"Storing history ... current step: {self.history_current_step} {len(self.history_stack)}")
        hs = self.createHistoryStamp(desc)

    def createHistoryStamp(self, desc):
        return desc
    
    def restoreHistoryStamp(self, history_stamp):
        logger.debug(f"RHS: {history_stamp}")