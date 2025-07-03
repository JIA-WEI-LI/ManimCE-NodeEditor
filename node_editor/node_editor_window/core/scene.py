import json
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from .node import Node
from .edge import Edge
from ..graphics.graphics_scene import QDMGraphicsScene
from ..serialization.serialzable import Serializable

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self.initUI()

    def initUI(self):
        self.graphicsScene = QDMGraphicsScene(self)
        self.graphicsScene.setGraphicsScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes:
            self.nodes.remove(node)

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

    def saveToFile(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))
        logger.debug(f"saving to {filename} was successful")

    def loadFromFile(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)

    def serialize(self):
        nodes, edges = [], []
        for node in self.nodes: nodes.append(node.serialize())
        for edge in self.edges: edges.append(edge.serialize())
        return OrderedDict([
            ('id', self.id),
            ('scene_width', self.scene_width),
            ('scene_height', self.scene_height),
            ('nodes', nodes),
            ('edges', edges),
        ])
    
    def deserialize(self, data, hashmap={}):
        logger.debug(f"deserializating data: {data}")

        self.clear()

        hashmap= {}

        # Create Node
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap)

        # Create Edge
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap)

        return True