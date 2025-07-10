from pprint import pformat, PrettyPrinter
from sys import float_info
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from .node import Node
from .edge import Edge, EDGE_TYPE_BEZIER, EDGE_TYPE_DIRECT
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
        pp = PrettyPrinter(indent=4, width=100)
        logger.debug("\n  NODES\n%s\n", pp.pformat(sel_nodes))
        logger.debug("\n  EDGES\n%s\n", pp.pformat(sel_edges))
        logger.debug("\n  SOCKETS\n%s\n", pp.pformat(sel_sockets))

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
            self.scene.history.storeHistory("Cut out elements from scene", setModified=True)

        return data
    
    def deserializeFromClipboard(self, data):
        
        hashmap = {}

        # calculate mouse pointer - scene position
        view = self.scene.graphicsScene.views()[0]
        mouse_scene_pos = view.last_scene_mouse_pos

        # calcuate selected objects bbox and center
        min_x, max_x = float_info.max, float_info.min
        min_y, max_y = float_info.max, float_info.min
        for node_data in data['nodes']:
            x, y = node_data['pos_x'], node_data['pos_y']
            if x < min_x: min_x = x
            if x > max_x: max_x = x
            if y < min_y: min_y = y
            if y > max_y: max_y = y
        bbox_center_x = (min_x + max_x)/2
        bbox_center_y = (min_y + max_y)/2

        # calcuate tehe offset of the newly creating nodes
        offset_x = mouse_scene_pos.x() - bbox_center_x
        offset_y = mouse_scene_pos.y() - bbox_center_y

        # create each nodes
        for node_data in data['nodes']:
            new_node = Node(self.scene)
            new_node.deserialize(node_data, hashmap, restore_id=False)

            # readjust the new node's position
            pos = new_node.pos
            new_node.setPos(pos.x() + offset_x, pos.y() + offset_y)

        # create each edges
        if 'edges' in data:
            for edge_data in data['edges']:
                new_edge = Edge(self.scene)
                new_edge.deserialize(edge_data, hashmap, restore_id=False)

        # store history
        self.scene.history.storeHistory("Pasted elements in scene", setModified=True)