from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QTreeWidget, QTreeWidgetItem, 
    QPushButton, QHBoxLayout
)
from PySide6.QtCore import Qt
from editor.editor_state import EditorState
from shared.scene_schema import GameObject
from dataclasses import asdict

class HierarchyPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.setMinimumWidth(160)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Compact toolbar
        toolbar = QHBoxLayout()
        toolbar.setContentsMargins(4, 4, 4, 4)
        toolbar.setSpacing(4)
        
        add_btn = QPushButton("+ Add")
        add_btn.setFixedHeight(20)
        add_btn.clicked.connect(self.add_new_object)
        toolbar.addWidget(add_btn)
        toolbar.addStretch()
        
        toolbar_widget = QWidget()
        toolbar_widget.setLayout(toolbar)
        layout.addWidget(toolbar_widget)

        # Tree
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        self.tree.setIndentation(12)
        self.tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree.customContextMenuRequested.connect(self.show_context_menu)
        self.tree.currentItemChanged.connect(self.on_selection_changed)
        layout.addWidget(self.tree)

        # Connect signals
        self.state = EditorState.instance()
        self.state.scene_loaded.connect(self.refresh)

    def refresh(self):
        self.tree.clear()
        scene = self.state.current_scene
        if not scene:
            return

        for obj in scene.objects:
            item = QTreeWidgetItem(self.tree)
            name = obj.get("name", "Unnamed")
            active = obj.get("active", True)
            
            if active:
                item.setText(0, name)
            else:
                item.setText(0, f"[x] {name}")
                item.setForeground(0, Qt.gray)
            
            item.setData(0, Qt.UserRole, obj.get("id"))
    
    def on_selection_changed(self, current, previous):
        if current:
            obj_id = current.data(0, Qt.UserRole)
            if self.state.selected_object_id != obj_id:
                self.state.select_object(obj_id)
        else:
            self.state.select_object(None)

    def show_context_menu(self, position):
        item = self.tree.itemAt(position)
        if not item:
            return
        
        from PySide6.QtWidgets import QMenu
        menu = QMenu(self)
        
        save_prefab_action = menu.addAction("Save as Prefab")
        save_prefab_action.triggered.connect(lambda: self.save_prefab(item))
        
        menu.exec(self.tree.viewport().mapToGlobal(position))

    def save_prefab(self, item):
        obj_id = item.data(0, Qt.UserRole)
        obj = self.state.get_object_by_id(obj_id)
        if not obj:
            return
            
        from PySide6.QtWidgets import QFileDialog, QMessageBox
        import json
        import os
        
        # Default filename = object name
        safe_name = "".join(c for c in obj.get("name", "prefab") if c.isalnum() or c in (' ', '_', '-')).strip()
        
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Prefab",
            os.path.join(self.state.project_root, "assets", f"{safe_name}.prefab"),
            "Prefab Files (*.prefab)"
        )
        
        if path:
            print(f"Attempting to save prefab to: {path}")
            try:
                with open(path, 'w') as f:
                    json.dump(obj, f, indent=2)
                print(f"Saved prefab to {path}")
                
                # Notify asset browser to refresh
                self.state.scene_loaded.emit() 
                
            except Exception as e:
                print(f"Error saving prefab: {e}")
                QMessageBox.critical(self, "Error", f"Failed to save prefab:\n{e}")

    def add_new_object(self):
        scene = self.state.current_scene
        if not scene:
            return
        
        new_obj = GameObject.create("New Object")
        
        # Try to spawn at canvas center
        from editor.canvas import SceneCanvas
        # Find canvas widget through parent
        main_window = self.window()
        if main_window:
            canvas = main_window.findChild(SceneCanvas)
            if canvas:
                cx, cy = canvas.get_canvas_center()
                new_obj.components["Transform"]["position"] = [cx, cy]
        
        scene.add_object(new_obj)
        self.refresh()
        self.state.select_object(new_obj.id)
