import os
import sys
import img_to_ascii
from PIL import Image
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QInputDialog, QLineEdit, QScrollArea, QFileDialog, QComboBox, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt


class InputWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initWindow()
	
	def initWindow(self):
		self.data = None
		self.ascii_image = None
		self.img = None
		self.setWindowTitle("IMG-to-ASCII")
		self.setGeometry(300, 300, 800, 600)
		layout = QVBoxLayout()
		horizontal_row = QHBoxLayout()
		
		self.btn_negative = QPushButton("Negative", self)
		self.btn_negative.setCheckable(True)
		self.btn_negative.clicked.connect(self.apply_neg_filter)
		horizontal_row.addWidget(self.btn_negative)
		layout.addLayout(horizontal_row)
		
		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		
		self.output_label = QLabel("Not provided", self)
		self.output_label.setFont(QFont("Courier New", 12))
		self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.output_label.setWordWrap(True)
		self.scroll_area.setWidget(self.output_label)	
		layout.addWidget(self.scroll_area)

		self.dropdown_conversions = QComboBox()
		self.dropdown_conversions.addItems(["average", "luminance", "desaturation", "decomposition_min", "decomposition_max"])
		self.dropdown_conversions.currentTextChanged.connect(self.get_conversion_input)
		layout.addWidget(self.dropdown_conversions)
		
		self.btn_input = QPushButton("Load image", self)
		self.btn_input.clicked.connect(self.load_image)
		layout.addWidget(self.btn_input)
		
		self.setLayout(layout)
		
	def apply_neg_filter(self):
		self.data = img_to_ascii.negative_filter(self.data)
		self.ascii_image = self.data.copy()
		self.output_label.setText(f'{img_to_ascii.print_ascii_chars(self.ascii_image, self.img)}')

		self.output_label.adjustSize()
		
	def get_conversion_input(self, conversion):
		print("Type:", conversion)
		if conversion:
			self.data = [self.img.getpixel((x,y)) for y in range(self.img.height) for x in range(self.img.width)]
			self.data = img_to_ascii.rgb_to_brightness(self.data, conversion)
			self.ascii_image = self.data.copy()
			self.output_label.setText(f'{img_to_ascii.print_ascii_chars(self.ascii_image, self.img)}')
			self.output_label.adjustSize()
		else:
			self.output_label.setText('No conversion type provided.')
			
	def load_image(self):
		filename = QFileDialog.getOpenFileName(self, self.tr("Select an image"), os.path.expanduser("~"), self.tr("Image Files (*.png *.jpg *.bmp)"))
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