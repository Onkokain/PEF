# import os
# import sys
# import tkinter as tk

# from PIL import Image, ImageTk
# from pef import decoder
# from tkinter import filedialog
# class PEF_Viewer:
#     def __init__(self,root):
#         self.root=root
#         self.root.title('PEF Viewer')
#         self.root.geometry('800x600')

#         self.photo=None

#         toolbar=tk.Frame(root)
#         toolbar.pack(side=tk.TOP,
#         fill=tk.X,
#         padx=8,
#         pady=8
#         )

#         open_button=tk.Button(toolbar,text='Open .pef',
#         command=self.open
#         )
#         open_button.pack(side=tk.LEFT)

#         self.info=tk.Label(toolbar,text='No file opened')
#         self.info.pack(side=tk.LEFT,padx=12)

#         self.canvas=tk.Canvas(root,bg='#1e1e1e',
#         highlightthickness=0
#         )
#         self.canvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

#         self.root.bind("<Control-o>",lambda event: self.open())

#     def to_image(self,w,h,pixels):
#         img=Image.new('RGBA',(w,h))
#         i=0
#         for x in range(h):
#             for y in range(w):
#                 hex_pixel=pixels[i]
#                 r,g,b,a=int(hex_pixel[:2],16),int(hex_pixel[2:4],16),int(hex_pixel[4:6],16),int(hex_pixel[6:],16)
#                 img.putpixel((y,x),(r,g,b,a))
#                 i+=1
#         return img

#     def fit(self,image,max_w,max_h):
#         w,h=image.size
#         if w<=0 or h<=0:
#             return image
#         scale=min(max_w/w,max_h/h)
#         if scale>=1:
#             return image
#         new_w=max(1,int(w*scale))
#         new_h=max(1,int(h*scale))
#         return image.resize((new_w,new_h),Image.NEAREST)

#     def load(self,path):
#         try:
#             w,h,px=decoder(path)
#             image=self.to_image(w,h,px)
#         except Exception as e:
#             return

#         self.root.update_idletasks()
#         c_w=max(1,self.canvas.winfo_width())
#         c_h=max(1,self.canvas.winfo_height())
#         image=self.fit(image,c_w-20,c_h-20)

#         self.photo=ImageTk.PhotoImage(image)
#         self.canvas.delete('all')
#         self.canvas.create_image(c_w//2,c_h//2,image=self.photo)
        
#         name=os.path.basename(path)
#         self.info.config(text=f"{name} | {w}x{h}")
#         self.root.title(f"PEF Viewer - {name}")

#     def open(self):
#         path=filedialog.askopenfilename(
#             title='Open PEF Image',
#             filetypes=[("PEF Files","*.pef"),("All Files","*.*")]
#         )
#         if path:
#             self.load(path)
    
# def main():
#     root=tk.Tk()
#     app=PEF_Viewer(root)

#     if len(sys.argv)>1:
#         root.after(200, lambda: app.load(sys.argv[1]))

#     root.mainloop()

# if __name__=='__main__':
#     main()

import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QFileDialog, QLabel, QMainWindow, QScrollArea, QHBoxLayout, QWidget, QMessageBox, QPushButton, QSizePolicy, QVBoxLayout

from pef import decoder, encoder, load_image

color_palette = {
    "bg": "#0b0b0d",
    "panel": "#111114",
    "panel_alt": "#17171c",
    "line": "#24242b",
    "line_alt": "#2f3037",
    "text_dim": "#5b5c62",
    "text": "#8a8a92",
    "text_bright": "#e9e9ee",
}

def resource_path(name: str) -> str:
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

class ViewImage(QLabel):
    
    def __init__(self):
        super().__init__()
        self.base_pixmap = None
        self.setAlignment(Qt.AlignCenter)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setMinimumSize(700, 500)
        self.setText('No Image Loaded.')
        self.setStyleSheet(
            f"""background: {color_palette['panel']};
            color: {color_palette['text_bright']};
            border: 1px solid {color_palette['line']};
            """
        )
    
    def set_base_pixmap(self, pixmap):
        self.base_pixmap = pixmap
        self._refresh_scaled()

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._refresh_scaled()

    def _refresh_scaled(self):
        if not self.base_pixmap:
            return
        target = self.size()
        scaled = self.base_pixmap.scaled(target, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.setPixmap(scaled)

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = resource_path('logo-Pedro.png')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle('Pedro')
        self.resize(1200, 800)
        self.current_path = None

        root = QWidget()
        self.setCentralWidget(root)

        outer = QVBoxLayout(root)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(14)

        top = QHBoxLayout()
        top.setSpacing(10)

        self.open_btn = QPushButton('Open File')
        self.convert_btn = QPushButton('Convert to PEF')
        self.info_label = QLabel('No file opened.')

        # --- UPDATED LOGO SECTION ---
        self.logo_label = QLabel()
        self.logo_label.setScaledContents(False)

        logo_path = resource_path('logo-Pedro.png')
        if os.path.exists(logo_path):
            logo_pm = QPixmap(logo_path)
            if not logo_pm.isNull():
                scaled_logo = logo_pm.scaledToHeight(32, Qt.SmoothTransformation)
                self.logo_label.setPixmap(scaled_logo)
                self.logo_label.setFixedWidth(scaled_logo.width())

        top.addWidget(self.logo_label)
        top.addWidget(self.open_btn)
        top.addWidget(self.convert_btn)
        top.addStretch(1)
        top.addWidget(self.info_label)

        outer.addLayout(top)

        self.image_view = ViewImage()
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.image_view)
        outer.addWidget(scroll)

        self.open_btn.clicked.connect(self.open_pef_dialog)
        self.convert_btn.clicked.connect(self.convert_image_to_pef)

        # --- UPDATED STYLESHEET ---
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background: {color_palette['bg']};
            }}
            QWidget {{
                color: {color_palette['text_bright']};
                font-size: 13px;
                background: {color_palette['bg']};
            }}
            QScrollArea {{
                background: {color_palette['bg']};
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background: {color_palette['bg']};
            }}
            QLabel {{
                color: {color_palette['text_bright']};
                background: transparent;
            }}
            QPushButton {{
                background: {color_palette['panel_alt']};
                color: {color_palette['text_bright']};
                border: 1px solid {color_palette['line']};
                border-radius: 10px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }}
            QPushButton:hover {{
                background: {color_palette['line']};
                border-color: {color_palette['line_alt']};
            }}
            QPushButton:pressed {{
                background: {color_palette['line_alt']};
            }}
            """
        )
        
    def open_pef_dialog(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            'Open PEF',
            "",
            "PEF Files (*.pef);;All Files (*)",
        )

        if path:
            self.load_pef(path)
    
    def load_pef(self, path):
        try:
            w, h, px = decoder(path)
            img = self._pixels_to_qimage(w, h, px)
            pm = QPixmap.fromImage(img)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f"Failed to load PEF:\n{str(e)}")
            return

        self.current_path = path
        self.image_view.set_base_pixmap(pm)
        self.info_label.setText(f"{os.path.basename(path)} | {w}x{h}")

    def convert_image_to_pef(self):
        input_path, _ = QFileDialog.getOpenFileName(
            self,
            'Choose Image to Convert',
            "",
            'Images (*.png *.jpg *.jpeg *.bmp *.webp);;All files (*.*)',
        )

        if not input_path:
            return

        default_name = os.path.splitext(os.path.basename(input_path))[0] + '.pef'
        output_path, _ = QFileDialog.getSaveFileName(
            self,
            'Save PEF',
            default_name,
            'PEF Files (*.pef)',
        )

        if not output_path:
            return

        if not output_path.lower().endswith('.pef'):
            output_path += '.pef'
        
        try:
            w, h, px = load_image(input_path)
            encoder(w, h, px, output_path)
        except Exception as exc:
            QMessageBox.critical(self, "Convert failed", f"Could not convert image.\n\n{exc}")
            return

        QMessageBox.information(self, "Convert successful", f"Saved:\n{output_path}")
        self.load_pef(output_path)
    
    def _pixels_to_qimage(self, width, height, pixels):
        image = QImage(width, height, QImage.Format_RGBA8888)
        i = 0
        for y in range(height):
            for x in range(width):
                hp = pixels[i]
                r = int(hp[0:2], 16)
                g = int(hp[2:4], 16)
                b = int(hp[4:6], 16)
                a = int(hp[6:8], 16)
                image.setPixelColor(x, y, QColor(r, g, b, a))
                i += 1
        return image

def main():
    app = QApplication(sys.argv)
    app_icon = resource_path('logo-Pedro.png')
    if os.path.exists(app_icon):
        app.setWindowIcon(QIcon(app_icon))
    win = Main()

    if len(sys.argv) > 1:
        win.load_pef(sys.argv[1])

    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()