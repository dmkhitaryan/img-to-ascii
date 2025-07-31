import sys
import img_to_ascii
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QInputDialog, QLineEdit, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class InputWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initWindow()
	
	def initWindow(self):
		self.setWindowTitle("IMG-to-ASCII")
		self.setGeometry(300, 300, 400, 250)
		layout = QVBoxLayout()
		
		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		
		self.output_label = QLabel("Not provided", self)
		self.output_label.setFont(QFont("Courier New", 12))
		self.output_label.setAlignment(Qt.AlignCenter)
		self.output_label.setWordWrap(True)
		self.scroll_area.setWidget(self.output_label)	
		layout.addWidget(self.scroll_area)
		
		
		self.btn_text = QPushButton("Input conversion type", self)
		self.btn_text.clicked.connect(self.get_conversion_input)
		layout.addWidget(self.btn_text)
		
		self.setLayout(layout)
		
	def get_conversion_input(self):
		conversion, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your conversion type:', QLineEdit.Normal, "")
		if ok and conversion:
			
			data = [img_to_ascii.img.getpixel((x,y)) for y in range(img_to_ascii.img.height) for x in range(img_to_ascii.img.width)]
			data = img_to_ascii.rgb_to_brightness(data, conversion)
			self.output_label.setText(f'{img_to_ascii.print_ascii_chars(data)}')
			self.output_label.adjustSize()
		elif not ok:
			self.output_label.setText('Input cancelled.')
		else:
			self.output_label.setText('No conversion type provided.')

def main():
    app = QApplication(sys.argv)
    test = InputWindow()
    test.show()
    sys.exit(app.exec_())
                        
if __name__ == '__main__':
    main()