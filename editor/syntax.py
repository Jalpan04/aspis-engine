from PySide6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor, QFont
from PySide6.QtCore import QRegularExpression

class PythonHighlighter(QSyntaxHighlighter):
    def __init__(self, document):
        super().__init__(document)
        
        self.highlighting_rules = []
        
        # Keywords
        keyword_format = QTextCharFormat()
        keyword_format.setForeground(QColor("#569cd6")) # Blue
        keyword_format.setFontWeight(QFont.Bold)
        keywords = [
            "def", "class", "if", "else", "elif", "while", "for", "return", 
            "import", "from", "as", "try", "except", "pass", "None", "True", "False",
            "and", "or", "not", "in", "is", "lambda", "global", "with"
        ]
        for word in keywords:
            pattern = QRegularExpression(f"\\b{word}\\b")
            self.highlighting_rules.append((pattern, keyword_format))
            
        # Decorators
        decorator_format = QTextCharFormat()
        decorator_format.setForeground(QColor("#dcdcaa")) # Yellowish
        self.highlighting_rules.append((QRegularExpression("@[A-Za-z0-9_]+"), decorator_format))
        
        # Strings (Single and Double quotes)
        string_format = QTextCharFormat()
        string_format.setForeground(QColor("#ce9178")) # Orange/Red
        self.highlighting_rules.append((QRegularExpression("\".*\""), string_format))
        self.highlighting_rules.append((QRegularExpression("'.*'"), string_format))
        
        # Comments
        comment_format = QTextCharFormat()
        comment_format.setForeground(QColor("#6a9955")) # Green
        self.highlighting_rules.append((QRegularExpression("#[^\n]*"), comment_format))
        
        # Numbers
        number_format = QTextCharFormat()
        number_format.setForeground(QColor("#b5cea8")) # Light Green
        self.highlighting_rules.append((QRegularExpression("\\b[0-9]+\\b"), number_format))
        
        # Class names
        class_format = QTextCharFormat()
        class_format.setForeground(QColor("#4ec9b0")) # Teal
        class_format.setFontWeight(QFont.Bold)
        self.highlighting_rules.append((QRegularExpression("\\bclass\\s+([A-Za-z0-9_]+)"), class_format))
        
        # Function names
        func_format = QTextCharFormat()
        func_format.setForeground(QColor("#dcdcaa")) # Yellow
        self.highlighting_rules.append((QRegularExpression("\\bdef\\s+([A-Za-z0-9_]+)"), func_format))

    def highlightBlock(self, text):
        for pattern, format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), format)
