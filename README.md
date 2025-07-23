<!-- Language Switch -->
<p align="right">
  🌐 <strong>Language：</strong>
  <a href="./README.md">English</a> &nbsp;| &nbsp;
  <a href="./README.zh-TW.md">繁體中文</a>
</p>

# ManimCE Node Editor — Visual Animation Creator

[![Version](https://img.shields.io/badge/version-v0.2.0.dev9-orange)](#)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](#)
[![Qt](https://img.shields.io/badge/Qt-PyQt5-blue)](#)
[![License](https://img.shields.io/github/license/JIA-WEI-LI/ManimCE-NodeEditor?color=blue)](./LICENSE)
![Size](https://img.shields.io/github/repo-size/JIA-WEI-LI/ManimCE-NodeEditor?color)

[![Development](https://img.shields.io/badge/status-in%20development-yellow)](#)
[![GitHub issues](https://img.shields.io/github/issues/JIA-WEI-LI/ManimCE-NodeEditor)](https://github.com/JIA-WEI-LI/ManimCE-NodeEditor/issues)


A PyQt5-based visual node editor designed to **simplify the creation of ManimCE animation videos**. This tool provides an intuitive, node-based interface for building animation logic, aiming to reduce the need for low-level scripting in Manim.

> [!WARNING]
> This project is still under development and is not yet complete

---

## 📈 Project Goals & Milestones

### ✅ Current Progress by Milestone

| Milestone                                            | Progress |
|-----------------------------------------------------|----------|
| 1. Basic Node Editor Features                        | ✅ 100%     |
| 2. Advanced Node Editor Features                     | ✅ 100%   |
| 3. Node Editor Packaging                             | ❌ 0%      |
| 4. Node Editor Embedded Window Integration           | 🚀 70%       |
| 5. Completion of Node Editor                         | ❌ 0%       |
| 6. Applying Multiple Styles for UI Design            | ❌ 0%       |
| 7. Basic Integration with ManimCE Logic              | ❌ 0%       |
| 8. Advanced Integration with ManimCE Logic           | ❌ 0%       |
| 9. Export as Standalone Application (APP/EXE)        | ❌ 0%       |
| 10. Dedicated Tutorial Website and Documentation (Bilingual) | ❌ 0%       |

## 🚀 Key Features

- Modular architecture with clear separation between core logic, graphics, and UI components  
- Color-coded socket types for intuitive connections  
- Smooth edge rendering supporting both Bezier curves and direct lines  
- Live edge updates upon node movement for seamless interaction  
- Configurable logging system with console and optional file outputs for easier debugging  


## 💼 Technical Stack

* Python 3.12+
* PyQt5 (>= 5.15.9)
* ManimCE (planned integration)
* QGraphicsScene / QGraphicsView framework
* Custom serialization/deserialization system

<!-- ## 📺 Getting Started
```bash
git clone https://github.com/Magicsoldier19/manimce-node-editor.git
cd manimce-node-editor
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python NodeEditor/node_editor_main.py
``` -->

## 🎓 Learning Resources
Official tutorial website is under development and will provide:

* Full-featured bilingual guides (English & Traditional Chinese)
* Video tutorials and interactive examples
* Custom theme documentation and extensibility tips

## 🔼 Planned Improvements

### UI/UX Enhancements
* Theme switching
* Context menus
* Drag-and-drop node creation
### Export Capabilities
* Convert node graph to ManimCE code
* Preview animations inside editor
* Export `.py` and video files directly

## 🔻 Roadmap & Tags
*  `v0.0.1` ：  🎯 Basic node editing complete
*  `v0.0.2` ：  🔁 Advanced logic, edge types, and serialization
  
### 📦 Current Version
**`v0.0.3.dev4`** – Under active development  

## 📄 License
[MIT License](./LICENSE)