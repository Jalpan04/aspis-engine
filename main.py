import sys
import traceback
from PySide6.QtWidgets import QApplication
from editor.app import MainWindow

def main():
    try:
        app = QApplication(sys.argv)
    except RuntimeError as e:
        print(f"Error initializing QApplication: {e}")
        print("Note: This application requires a graphical environment.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error initializing QApplication: {e}")
        traceback.print_exc()
        sys.exit(1)

    try:
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        print(f"Application crash: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
