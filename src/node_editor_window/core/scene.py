import os
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

class InvalidFile(Exception): pass

class Scene(Serializable):
    def __init__(self):
        super().__init__()
        self.nodes = []
        self.edges = []

        self.scene_width = 64000
        self.scene_height = 64000

        self._has_been_modified = False
        self._has_been_modified_listeners = []
        self._item_selected_listeners = []
        self._items_deselected_listeners = []

        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = SceneClipboard(self)

        self.graphicsScene.itemSelected.connect(self.onItemSelected)
        self.graphicsScene.itemsDeselected.connect(self.onItemsDeselected)

    def initUI(self):
        self.graphicsScene = QDMGraphicsScene(self)
        self.graphicsScene.setGraphicsScene(self.scene_width, self.scene_height)

    def onItemSelected(self):
        logger.info(" ~onItemSelected")

    def onItemsDeselected(self):
        logger.info(" ~onItemsDeselected")

    def isModified(self):
        return self.has_been_modified

    def getSelectedItems(self):
        return self.graphicsScene.selectedItems()

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

    def addItemSelectedListener(self, callback):
        self._item_selected_listeners.append(callback)

    def addItemsDeselectedListener(self, callback):
        self._items_deselected_listeners.append(callback)

    # custom flag to detect node or edge has been selected....
    def resetLastSelectedStates(self):
        for node in self.nodes:
            node.graphicsNode._last_selected_state = False
        for edge in self.edges:
            edge.graphicsEdge._last_selected_state = False


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
            try:
                data = json.loads(raw_data)
                self.deserialize(data)

                self.has_been_modified = False
            except json.JSONDecodeError:
                raise InvalidFile("%s is not a valid JSON file" % os.path.basename(filename))
            except Exception as e:
                logger.error(f"Error loading file {filename}: {e}")

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
            Node(self).deserialize(node_data, hashmap, restore_id)

        # Create Edge
        for edge_data in data['edges']:
            Edge(self).deserialize(edge_data, hashmap, restore_id)

        return True