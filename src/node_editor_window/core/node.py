from typing import List
import pprint
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from .socket import Socket, LEFT_TOP, RIGHT_TOP, LEFT_BOTTOM, RIGHT_BOTTOM
from ..graphics.graphics_node import QDMGraphicsNode
from ..content.node_content_widget import QDMNodeContentWidget
from ..serialization.serializable import Serializable

class Node(Serializable):
    def __init__(self, scene, title:str = "Undefined Node", inputs:List = [], outputs:List = []):
        super().__init__()
        self._title = title
        self.scene = scene

        self.content = QDMNodeContentWidget(self)
        self.graphicsNode = QDMGraphicsNode(self)
        self.title = title

        self.scene.addNode(self)
        self.scene.graphicsScene.addItem(self.graphicsNode)

        self.socket_spacing = 22

        # Create sockets for inputs and outputs
        self.inputs = []
        self.outputs = []
        counter = 0

        for item in inputs:
            socket = Socket(
                node=self, 
                index=counter, 
                position=LEFT_BOTTOM, 
                socket_type=item,
                multi_edges=False)
            counter += 1
            self.inputs.append(socket)

        counter = 0
        for item in outputs:
            socket = Socket(
                node=self, 
                index=counter, 
                position=RIGHT_TOP, 
                socket_type=item,
                multi_edges=True)
            counter += 1
            self.outputs.append(socket)

    def __str__(self):
        return "< Node %s ... %s >" % (hex(id(self))[2:5], hex(id(self))[-3:]) + " Title: %s" % self.title

    @property
    def pos(self):
        return self.graphicsNode.pos()       # QPonintF
    def setPos(self, x: int, y: int):
        self.graphicsNode.setPos(x, y)

    @property
    def title(self):
        return self._title
    @title.setter
    def title(self, value):
        self._title = value
        self.graphicsNode.title = self._title

    def setSocketPosition(self, index: int, position: str):
        x = 0 if position in (LEFT_TOP, LEFT_BOTTOM) else self.graphicsNode.width
        if position in (LEFT_BOTTOM, RIGHT_BOTTOM):
            y = (self.graphicsNode.height
            - self.graphicsNode.edge_size
            - self.graphicsNode._padding
            - index * self.socket_spacing)
        else:
            y = (self.graphicsNode.title_height 
            + self.graphicsNode.edge_size 
            + self.graphicsNode._padding 
            + index * self.socket_spacing)

        return [x, y]
    
    def updateConnectedEdges(self, edge=None):
        for socket in self.inputs + self.outputs:
            # if socket.hasEdge():
            for edge in socket.edges:
                edge.updatePositions()

    def remove(self):
        logger.debug(f"> Remove Node {self}")
        logger.debug(f" - remove all edge from sockets")
        for socket in (self.inputs + self.outputs):
            # if socket.hasEdge():
            for edge in socket.edges:
                logger.debug(f"     - removing from socket: {socket} edge: {edge}")
                edge.remove()
        logger.debug(f" - remove graphicsNode")
        self.scene.graphicsScene.removeItem(self.graphicsNode)
        self.graphicsNode = None
        logger.debug(f" - remove node from scene")
        self.scene.removeNode(self)
        logger.debug(f" - everythings was done.")

    def serialize(self):
        inputs, outputs = [], []
        for socket in self.inputs: inputs.append(socket.serialize())
        for socket in self.outputs: outputs.append(socket.serialize())
        return OrderedDict([
            ('id', self.id),
            ('title', self.title),
            ('pos_x', self.graphicsNode.scenePos().x()),
            ('pos_y', self.graphicsNode.scenePos().y()),
            ('inputs', inputs),
            ('outputs', outputs),
            ('content', self.content.serialize())
        ])
    
    def deserialize(self, data, hashmap={}, restore_id:bool = True):
        try:
            if restore_id: self.id = data['id']
            hashmap[data['id']] = self

            self.setPos(data['pos_x'], data['pos_y'])
            self.title = data['title']

            data['inputs'].sort(key=lambda socket: socket['index'] + socket['position']*10000)
            data['outputs'].sort(key=lambda socket: socket['index'] + socket['position']*10000)

            self.inputs = []
            for socket_data in data['inputs']:
                new_socket = Socket(
                    node=self,
                    index=socket_data['index'],
                    position=socket_data['position'],
                    socket_type=socket_data['socket_type']
                )
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.inputs.append(new_socket)

            self.outputs = []
            for socket_data in data['outputs']:
                new_socket = Socket(
                    node=self,
                    index=socket_data['index'],
                    position=socket_data['position'],
                    socket_type=socket_data['socket_type']
                )
                new_socket.deserialize(socket_data, hashmap, restore_id)
                self.outputs.append(new_socket)

            logger.debug(pprint.pformat(hashmap))
        except KeyError as e: logger.error(f"KeyError: {e} in Node.deserialize with data: {data}")
        
        return True