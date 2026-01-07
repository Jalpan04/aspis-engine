from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QFileSystemModel, QTreeView

class AssetBrowser(QWidget):
    def __init__(self, project_root):
        super().__init__()
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        self.header = QLabel("Asset Browser")
        self.header.setStyleSheet("font-weight: bold; padding: 5px; background: #2b2b2b;")
        self.layout.addWidget(self.header)

        self.model = QFileSystemModel()
        self.model.setRootPath(project_root)
        self.model.setNameFilters(["*.png", "*.jpg", "*.jpeg", "*.scene.json", "*.py", "*.prefab"])
        self.model.setNameFilterDisables(False) # Hide files that don't match
        
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        self.tree.setRootIndex(self.model.index(project_root))
        
        self.tree.setDragEnabled(True)
        
        # Hide standard columns we might not want (Size, Type, Date)
        # self.tree.hideColumn(1)
        # self.tree.hideColumn(2)
        
        self.layout.addWidget(self.tree)
