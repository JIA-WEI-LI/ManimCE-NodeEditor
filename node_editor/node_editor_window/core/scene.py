import json
import logging
logger = logging.getLogger(__name__)
from collections import OrderedDict

from .node import Node
from .edge import Edge
from .scene_history import SceneHistory
from .scene_clipboard import SceneClipboard
from ..graphics.graphics_scene import QDMGraphicsScene
from ..serialization.serializable import Serializable

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._has_been_modified_listeners = []

        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

    @property
    def has_been_modified(self):
        return self._has_been_modified
    @has_been_modified.setter
    def has_been_modified(self, value):
        if not self._has_been_modified and value:
            self._has_been_modified = value

            # call all registered listeners
            for callback in self._has_been_modified_listeners:
                callback()

        self._has_been_modified = value

    def addHasBeenModifiedListener(self, callback):
        self._has_been_modified_listeners.append(callback)

    def initUI(self):
        self.graphicsScene = QDMGraphicsScene(self)
        self.graphicsScene.setGraphicsScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes: self.nodes.remove(node)
        else: logger.warning(f"  WARNING!\n    Scene::removeNode wanna remove Node: {node} from self.nodes but it's not in the list.")

    def removeEdge(self, edge):
        if edge in self.edges: self.edges.remove(edge)
        else: logger.warning(f"  WARNING!\n    Scene::removeEdge wanna remove Edge: {edge} from self.edges but it's not in the list.")

    def clear(self):
        while len(self.nodes) > 0:
            self.nodes[0].remove()

        self.has_been_modified = False

    def saveToFile(self, filename):
        with open(filename, 'w') as file:
            file.write(json.dumps(self.serialize(), indent=4))
            logger.debug(f"saving to {filename} was successful")

            self.has_been_modified = False

    def loadFromFile(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            raw_data = file.read()
            data = json.loads(raw_data)
            self.deserialize(data)

            self.has_been_modified = False

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
    
    def deserialize(self, data, hashmap={}, restore_id:bool = True):
        logger.debug(f"deserializating data: {data}")
        self.clear()
        hashmap= {}

        if restore_id: self.id = data['id']

        # Create Node
        for node_data in data['nodes']:
            Node(self).deserialize(node_data, hashmap)

        # Create Edge
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap)

        return True