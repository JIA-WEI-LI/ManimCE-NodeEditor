import logging
logger = logging.getLogger(__name__)

from ..graphics.graphics_edge import QDMGraphicsEdge

class SceneHistory():
    def __init__(self, scene):
        self.scene = scene

        self.history_stack = []
        self.history_current_step = -1
        self.history_limit = 16

    def undo(self):
        logger.debug("UNDO")

        if self.history_current_step > 0:
            self.history_current_step -= 1
            self.restoreHistory()

    def redo(self):
        logger.debug("REDO")

        if self.history_current_step + 1 < len(self.history_stack):
            self.history_current_step += 1
            self.restoreHistory()

    def restoreHistory(self):
        logger.debug(f"Restoring history ... current step: {self.history_current_step} {len(self.history_stack)}")
        self.restoreHistoryStamp(self.history_stack[self.history_current_step])

    def storeHistory(self, desc):
        logger.debug(f"Storing history ... current step: {self.history_current_step} {len(self.history_stack)}")
        hs = self.createHistoryStamp(desc)

        # if the pointer (self.history_current_step) is not at the end of history stack
        if self.history_current_step + 1 < len(self.history_stack):
            self.history_stack = self.history_stack[0: self.history_current_step+1]

        # history is outside of the limits
        if self.history_current_step + 1 >= self.history_limit:
            self.history_stack = self.history_stack[1:]
            self.history_current_step -= 1

        self.history_stack.append(hs)
        self.history_current_step += 1
        logger.debug(f"  -- setting step to: {self.history_current_step}")

    def createHistoryStamp(self, desc):
        sel_obj = {
            'nodes': [],
            'edges': []
        }
        for item in self.scene.graphicsScene.selectedItems():
            if hasattr(item, 'node'):
                sel_obj['nodes'].append(item.node.id)
            elif isinstance(item, QDMGraphicsEdge):
                sel_obj['edges'].append(item.edge.id)

        history_stamp = {
            'desc': desc,
            'snapshot': self.scene.serialize(),
            'selection': sel_obj,
        }
        return history_stamp
    
    def restoreHistoryStamp(self, history_stamp):
        logger.debug(f"RHS: {history_stamp['desc']}")

        self.scene.deserialize(history_stamp['snapshot'])

        for node_id in history_stamp['selection']['nodes']:
            for node in self.scene.nodes:
                if node.id == node_id:
                    node.graphicsNode.setSelected(True)
                    break

        for edge_id in history_stamp['selection']['edges']:
            for edge in self.scene.edges:
                if edge.id == edge_id:
                    edge.graphicsEdge.setSelected(True)
                    break