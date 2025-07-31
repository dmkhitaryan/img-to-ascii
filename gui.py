import os
import sys
import img_to_ascii
from PIL import Image
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QInputDialog, QLineEdit, QScrollArea, QFileDialog
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class InputWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initWindow()
	
	def initWindow(self):
		self.img = None
		self.setWindowTitle("IMG-to-ASCII")
		self.setGeometry(300, 300, 400, 250)
		layout = QVBoxLayout()
		
		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		
		self.output_label = QLabel("Not provided", self)
		self.output_label.setFont(QFont("Courier New", 12))
		self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.output_label.setWordWrap(True)
		self.scroll_area.setWidget(self.output_label)	
		layout.addWidget(self.scroll_area)
		
		
		self.btn_text = QPushButton("Input conversion type", self)
		self.btn_text.clicked.connect(self.get_conversion_input)
		layout.addWidget(self.btn_text)
		
		self.btn_input = QPushButton("Load image", self)
		self.btn_input.clicked.connect(self.load_image)
		layout.addWidget(self.btn_input)
		
		self.setLayout(layout)
		
	def get_conversion_input(self):
		conversion, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter your conversion type:', QLineEdit.EchoMode.Normal, "")
		if ok and conversion:
			
			data = [self.img.getpixel((x,y)) for y in range(self.img.height) for x in range(self.img.width)]
			data = img_to_ascii.rgb_to_brightness(data, conversion)
			self.output_label.setText(f'{img_to_ascii.print_ascii_chars(data, self.img)}')
			self.output_label.adjustSize()
		elif not ok:
			self.output_label.setText('Input cancelled.')
		else:
			self.output_label.setText('No conversion type provided.')
			
	def load_image(self):
		filename = QFileDialog.getOpenFileName(self, self.tr("Select an image"), os.path.expanduser("~"), self.tr("Image Files (*.png *.jpg *.bmp)"))
		print("----------------")
		print(filename)
		print("----------------")
		self.img = Image.open(filename[0])
		self.img = self.img.resize((75,75))
		print(f"Successfully loaded image!\nImage size: {self.img.width} x {self.img.height}")
		

def main():
    app = QApplication(sys.argv)
    test = InputWindow()
    test.show()
    sys.exit(app.exec())
                        
if __name__ == '__main__':
    main()