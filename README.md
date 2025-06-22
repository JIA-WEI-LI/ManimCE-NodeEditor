# ManimCE Node Editor — Visual Animation Creator

A PyQt5-based visual node editor designed to **simplify the creation of ManimCE animation videos**.  
This tool enables intuitive construction of animation sequences using nodes and connections, turning complex Manim scripting into a visual workflow.

---

## Project Goals & Progress

### ✅ Current Progress by Milestone

| Milestone                                            | Progress |
|-----------------------------------------------------|----------|
| 1. Basic Node Editor Features                        | 66%      |
| 2. Advanced Node Editor Features                     | 0%       |
| 3. Node Editor Packaging                             | 0%       |
| 4. Node Editor Embedded Window Integration           | 0%       |
| 5. Completion of Node Editor                         | 0%       |
| 6. Applying Multiple Styles for UI Design            | 0%       |
| 7. Basic Integration with ManimCE Logic              | 0%       |
| 8. Advanced Integration with ManimCE Logic           | 0%       |
| 9. Export as Standalone Application (APP/EXE)        | 0%       |
| 10. Dedicated Tutorial Website and Documentation (Bilingual) | 0%       |

---

## 🚀 Key Features

- Modular architecture with clear separation between core logic, graphics, and UI components  
- Color-coded socket types for intuitive connections  
- Smooth edge rendering supporting both Bezier curves and direct lines  
- Live edge updates upon node movement for seamless interaction  
- Configurable logging system with console and optional file outputs for easier debugging  

---

## 📂 Project Structure

```mermaid
classDiagram
    class Node {
        - Scene scene
        - str title
        - QDMNodeContentWidget content
        - QDMGraphicsNode graphicsNode
        - int socket_spacing = 22
        - List~Socket~ inputs
        - List~Socket~ outputs
        + pos() QPointF
        + setPos(x: int, y: int) void
        + setSocketPosition(index: int, position: str) List~int~
        + updateConnectedEdges(edge=None) void
    }

    class Edge {
        - Scene scene
        - Socket start_socket
        - Socket end_socket
        - QDMGraphicsEdge graphicsEdge
        + __init__(scene, start_socket, end_socket, edge_type=int) 
        + updatePositions()
        + remove_from_socket()
        + remove()
    }

    class Socket {
        - Node node
        - int index
        - int position
        - int socket_type
        - QDMGraphicsSocket graphicsSocket
        - Edge edge
        + __init__(node, index=int, position=int, socket_type=int)
        + getSocketPosition() List~int~
        + setConnectedEdge(edge)
        + hasEdge() bool
    }

    class Scene {
        - List~Node~ nodes
        - List~Edge~ edges
        - int scene_width = 64000
        - int scene_height = 64000
        - QDMGraphicsScene graphicsScene
        + __init__()
        + initUI()
        + addNode(node)
        + addEdge(edge)
        + removeNode(node)
        + removeEdge(edge)
    }

    class QDMGraphicsNode {
        - Node node
        - QDMNodeContentWidget content
        - QColor _title_color
        - QFont _title_font
        - int width = 180
        - int height = 240
        - float edge_size = 10.0
        - int title_height = 24
        - float _padding = 4.0
        - QPen _pen_default
        - QPen _pen_selected
        - QBrush _brush_title
        - QBrush _brush_background
        - QGraphicsTextItem title_item
        - QGraphicsProxyWidget graphicsContents
        + __init__(node, parent=None)
        + mouseMoveEvent(event)
        + title()
        + title(value)
        + boundingRect() QRectF
        + initUI()
        + initTitle()
        + initContent()
        + initSockets()
        + paint(painter, option, widget=None)
    }

    class QDMGraphicsEdge {
        - Edge edge
        - QColor _color
        - QColor _color_selected
        - QPen _pen
        - QPen _pen_selected
        - List~int~ posSource
        - List~int~ posDestination
        + __init__(edge, parent=None)
        + setSource(x: int, y: int)
        + setDestination(x: int, y: int)
        + paint(painter, option, widget=None)
        + updatePath()
    }

    class QDMGraphicsEdgeDirect {
        + updatePath()
    }

    class QDMGraphicsEdgeBezier {
        + updatePath()
    }

    QDMGraphicsEdgeDirect --|> QDMGraphicsEdge
    QDMGraphicsEdgeBezier --|> QDMGraphicsEdge

    class QDMGraphicsSocket {
        - float radius = 6.0
        - float outline_width = 1.0
        - List~QColor~ _colors
        - QColor _color_background
        - QColor _color_outline
        - QPen _pen
        - QColor _brush
        + __init__(parent=None, socket_type:int=1)
        + paint(painter, option, widget=None)
        + boundingRect() QRectF
    }

    class QDMGraphicsScene {
        - scene
        - int gridSize = 20
        - int gridSquares = 5
        - QColor _color_background = "#393939"
        - QColor _color_light = "#2f2f2f"
        - QColor _color_dark = "#292929"
        - QPen _pen_light
        - QPen _pen_dark
        - int scene_width = 64000
        - int scene_height = 64000
        + __init__(scene, parent=None)
        + setGraphicsScene(width, height)
        + drawBackground(painter, rect)
    }

    class QDMGraphicsView {
        - graphicsScene
        - float zoomInFator = 1.25
        - bool zoomClamp = False
        - int zoom = 5
        - int zoomStep = 1
        - list zoomRange = [0, 10]
        + __init__(graphicsScene, parent=None)
        + initUI()
        + mousePressEvent(event)
        + mouseReleaseEvent(event)
        + middleMouseButtonPress(event)
        + middleMouseButtonRelease(event)
        + leftMouseButtonPress(event)
        + leftMouseButtonRelease(event)
        + rightMouseButtonPress(event)
        + rightMouseButtonRelease(event)
        + wheelEvent(event)
    }

    class QDMNodeContentWidget {
        + __init__(node, parent=None)
        + initUI()
        - layout: QVBoxLayout
        - widget_label: QLabel
        - QTextEdit
    }

    class NodeEditorWindow {
        - str stylesheet_filename = "NodeEditor/NodeEditorWindow/qss/nodestyle.qss"
        - Scene scene
        - QGraphicsScene graphicsScene
        - QDMGraphicsView view
        - QVBoxLayout layout
        + __init__(parent=None)
        + initUI()
        + addNodes()
        + loadStylesheet(filename)
    }

    Node "1" --> "many" Socket : inputs, outputs
    Socket "1" --> "1" Node : node
    Socket "0..1" --> "0..1" Edge : edge
    Edge "1" --> "1" Scene : scene
    Edge "1" --> "1" Socket : start_socket
    Edge "0..1" --> "0..1" Socket : end_socket
    Scene "1" --> "many" Node : nodes
    Scene "1" --> "many" Edge : edges
    Node "1" --> "1" QDMNodeContentWidget : content
    Node "1" --> "1" QDMGraphicsNode : graphicsNode
    Socket "1" --> "1" QDMGraphicsSocket : graphicsSocket
    Edge "1" --> "1" QDMGraphicsEdge : graphicsEdge
    Scene "1" --> "1" QDMGraphicsScene : graphicsScene
    QDMGraphicsNode ..|> QGraphicsItem
    QDMGraphicsEdge ..|> QGraphicsPathItem
    QDMGraphicsSocket ..|> QGraphicsItem
    QDMGraphicsScene ..|> QGraphicsScene
    QDMGraphicsView ..|> QGraphicsView
    NodeEditorWindow "1" --> "1" Scene : scene
    NodeEditorWindow "1" --> "1" QDMGraphicsScene : graphicsScene
    NodeEditorWindow "1" --> "1" QDMGraphicsView : view
    NodeEditorWindow "1" --> "1" QDMNodeContentWidget : content
```

---

## 📺 Getting Started
```bash
git clone https://github.com/yourname/manimce-node-editor.git
cd manimce-node-editor
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python NodeEditor/node_editor_main.py
```

## 🎓 Learning Resources
* Official tutorial website coming soon, featuring detailed guides in both Chinese and English.

## 📄 License
[MIT License](./LICENSE)

## Additional suggestions:
* Add a "Contributing" section if you plan to open source or accept contributions.
* Add badges (build status, PyPI version, license) if you host the repo on GitHub.
* Add screenshots or GIFs of the editor UI to showcase it visually.
* Consider adding a "Known Issues" or "Roadmap" section for transparency.