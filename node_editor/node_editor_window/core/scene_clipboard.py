from pprint import pformat
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from ..graphics.graphics_edge import QDMGraphicsEdge

class SceneClipboard():
    def __init__(self, scene):
        self.scene = scene

    def serializeSelected(self, delete:bool = False):
        logger.debug(" -- COPT TO CLIPBOARD -- ")

        sel_nodes, sel_edges, sel_sockets = [], [], {}

        # sort edges and nodes
        for item in self.scene.graphicsScene.selectedItems():
            if hasattr(item, 'node'):
                sel_nodes.append(item.node.serialize())
                for socket in (item.node.inputs + item.node.outputs):
                    sel_sockets[socket.id] = socket
            elif isinstance(item, QDMGraphicsEdge):
                sel_edges.append(item.edge)

        # debug
        logger.debug("\n  NODES\n     \n%s\n", pformat(sel_nodes))
        logger.debug("\n  EDGES\n     \n%s\n", pformat(sel_edges))
        logger.debug("\n  SOCKETS\n     \n%s\n", pformat(sel_sockets))

        # remove all edges which aree not connected to a node in our list
        edges_to_remove = []
        for edge in sel_edges:
            if edge.start_socket.id in sel_sockets and edge.end_socket.id in sel_sockets:
                pass
            else:
                logger.debug(f"edge {edge} is not connected with both sides")
                edges_to_remove.append(edge)
        for edge in edges_to_remove:
            sel_edges.remove(edge)

        # make final list of edges
        edges_final = []
        for edge in sel_edges:
            edges_final.append(edge.serialize())

        data = OrderedDict([
            ('nodes', sel_nodes),
            ('edges', edges_final),
        ])

        # if CUT(aka deleted) remove selected items
        if delete:
            self.scene.graphicsScene.views()[0].deleteSelected()

        return data
    
    def deserializeFromClipboard(self, data):
        logger.debug(f"deserialization from clipboard, data: {data}")