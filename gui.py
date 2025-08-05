import os
import sys
import img_to_ascii
from PIL import Image
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QInputDialog, QLineEdit, QScrollArea, QFileDialog, QComboBox, QHBoxLayout, QCheckBox 
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtCore import Qt, QEvent

# TODO:
# 1. Tidy up the code a bit?
# 2. Write a README.

class InputWindow(QWidget):
	def __init__(self):
		super().__init__()
		self.initWindow()
	
	def initWindow(self):
		self.isRed, self.isGreen, self.isBlue = False, False, False
		self.font_size = 12
		self.data = None
		self.ascii_image = None
		self.img = None
		self.setWindowTitle("IMG-to-ASCII")
		self.setGeometry(300, 300, 800, 600)
		
		self.default_rgb = QColor(255, 255, 255)

		layout = QVBoxLayout()
		h_layout = QHBoxLayout()
		
		checkbox_layout = QVBoxLayout()
		self.checkbox_red = QCheckBox(text = "Red")
		self.checkbox_green = QCheckBox(text = "Green")
		self.checkbox_blue = QCheckBox(text = "Blue")
		self.checkbox_red.setEnabled(False)
		self.checkbox_green.setEnabled(False)
		self.checkbox_blue.setEnabled(False)
		checkbox_layout.addWidget(self.checkbox_red)
		checkbox_layout.addWidget(self.checkbox_green)
		checkbox_layout.addWidget(self.checkbox_blue)
		self.checkbox_red.stateChanged.connect(lambda state, cb_red = self.checkbox_red : self.onStateChanged(cb_red))
		self.checkbox_green.stateChanged.connect(lambda state, cb_green = self.checkbox_green : self.onStateChanged(cb_green))
		self.checkbox_blue.stateChanged.connect(lambda state, cb_blue = self.checkbox_blue : self.onStateChanged(cb_blue))

		self.btn_negative = QPushButton("Negative", self)
		self.btn_negative.setCheckable(True)
		self.btn_negative.setEnabled(False)
		self.btn_negative.clicked.connect(self.apply_neg_filter)
		
		h_layout.addWidget(self.btn_negative)
		h_layout.addLayout(checkbox_layout)
		
		self.scroll_area = QScrollArea()
		self.scroll_area.setWidgetResizable(True)
		
		self.output_label = QLabel("Not provided", self)
		self.output_label.setFont(QFont("Courier New", self.font_size))
		self.output_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
		self.output_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
		self.output_label.setWordWrap(True)
		self.scroll_area.setWidget(self.output_label)
		self.scroll_area.installEventFilter(self)
		layout.addLayout(h_layout)
		layout.addWidget(self.scroll_area)

		self.dropdown_conversions = QComboBox()
		self.dropdown_conversions.addItems(["average", "luminance", "desaturation", "decomposition_min", "decomposition_max"])
		self.dropdown_conversions.currentTextChanged.connect(self.get_conversion_input)
		self.dropdown_conversions.setEnabled(False)
		layout.addWidget(self.dropdown_conversions)
		
		self.btn_input = QPushButton("Load image", self)
		self.btn_input.clicked.connect(self.load_image)
		layout.addWidget(self.btn_input)
		
		self.setLayout(layout)

	def onStateChanged(self, button):
		match button.text():
			case "Red":
				self.isRed = not self.isRed
			case "Green":
				self.isGreen = not self.isGreen
			case "Blue":
				self.isBlue = not self.isBlue
			case _:
				return
		R = self.default_rgb.red() * self.isRed
		G = self.default_rgb.green() * self.isGreen
		B = self.default_rgb.blue() * self.isBlue
		self.output_label.setStyleSheet(f"color: rgb({R}, {G}, {B});")
			
	def eventFilter(self, source, event):
		if source == self.scroll_area and event.type() == QEvent.Type.Wheel:
			if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
				self.zoom_with_wheel(event)
				return True
			else:
				return False
			
		return super().eventFilter(source, event)
	
	def zoom_with_wheel(self, event):
		diff = event.angleDelta().y()

		if diff > 0:
			self.zoom_text_in()
		elif diff < 0: 
			self.zoom_text_out()
		
		event.ignore()

	def zoom_text_in(self):
		if self.font_size <= 48:
			self.font_size += 2
			self.update_font_size()

	def zoom_text_out(self):
		if self.font_size >= 4:
			self.font_size -= 2
			self.update_font_size()
			
	def update_font_size(self):
		self.output_label.setFont(QFont("Courier New", self.font_size))

	def apply_neg_filter(self):
		if self.data is not None:
			self.data = img_to_ascii.negative_filter(self.data)
			self.ascii_image = self.data.copy()
			self.output_label.setText(f'{img_to_ascii.print_ascii_chars(self.ascii_image, self.img)}')
			self.output_label.adjustSize()
		return
		
	def get_conversion_input(self, conversion):
		print("Type:", conversion)
		if conversion:
			try:
				self.data = [self.img.getpixel((x,y)) for y in range(self.img.height) for x in range(self.img.width)]
				self.data = img_to_ascii.rgb_to_brightness(self.data, conversion)
				self.ascii_image = self.data.copy()
				self.output_label.setText(f'{img_to_ascii.print_ascii_chars(self.ascii_image, self.img)}')
				self.output_label.adjustSize()
			except AttributeError:
				return
		else:
			self.output_label.setText('No conversion type provided.')
			
	def load_image(self):
		filename = QFileDialog.getOpenFileName(self, self.tr("Select an image"), os.path.expanduser("~"), self.tr("Image Files (*.png *.jpg *.bmp)"))
		try:
			self.img = Image.open(filename[0])
			self.img = self.img.resize((min(self.img.width, 1366), min(self.img.height, 768)))
			print(f"Successfully loaded image!\nImage size: {self.img.width} x {self.img.height}")

			if (not self.btn_negative.isEnabled()):
				self.btn_negative.setEnabled(True)
				self.dropdown_conversions.setEnabled(True)
				self.checkbox_red.setEnabled(True)
				self.checkbox_green.setEnabled(True)
				self.checkbox_blue.setEnabled(True)
		except FileNotFoundError:
			return
				
def main():
		app = QApplication(sys.argv)
		test = InputWindow()
		test.show()
		sys.exit(app.exec())
												
if __name__ == '__main__':
		main()