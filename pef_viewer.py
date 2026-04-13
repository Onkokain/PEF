import os
import sys
import tkinter as tk

from PIL import Image, ImageTk
from pef import decoder
from tkinter import filedialog
class PEF_Viewer:
    def __init__(self,root):
        self.root=root
        self.root.title('PEF Viewer')
        self.root.geometry('800x600')

        self.photo=None

        toolbar=tk.Frame(root)
        toolbar.pack(side=tk.TOP,
        fill=tk.X,
        padx=8,
        pady=8
        )

        open_button=tk.Button(toolbar,text='Open .pef',
        command=self.open
        )
        open_button.pack(side=tk.LEFT)

        self.info=tk.Label(toolbar,text='No file opened')
        self.info.pack(side=tk.LEFT,padx=12)

        self.canvas=tk.Canvas(root,bg='#1e1e1e',
        highlightthickness=0
        )
        self.canvas.pack(side=tk.TOP,fill=tk.BOTH,expand=True)

        self.root.bind("<Control-o>",lambda event: self.open())

    def to_image(self,w,h,pixels):
        img=Image.new('RGBA',(w,h))
        i=0
        for x in range(h):
            for y in range(w):
                hex_pixel=pixels[i]
                r,g,b,a=int(hex_pixel[:2],16),int(hex_pixel[2:4],16),int(hex_pixel[4:6],16),int(hex_pixel[6:],16)
                img.putpixel((y,x),(r,g,b,a))
                i+=1
        return img

    def fit(self,image,max_w,max_h):
        w,h=image.size
        if w<=0 or h<=0:
            return image
        scale=min(max_w/w,max_h/h)
        if scale>=1:
            return image
        new_w=max(1,int(w*scale))
        new_h=max(1,int(h*scale))
        return image.resize((new_w,new_h),Image.NEAREST)

    def load(self,path):
        try:
            w,h,px=decoder(path)
            image=self.to_image(w,h,px)
        except Exception as e:
            return

        self.root.update_idletasks()
        c_w=max(1,self.canvas.winfo_width())
        c_h=max(1,self.canvas.winfo_height())
        image=self.fit(image,c_w-20,c_h-20)

        self.photo=ImageTk.PhotoImage(image)
        self.canvas.delete('all')
        self.canvas.create_image(c_w//2,c_h//2,image=self.photo)
        
        name=os.path.basename(path)
        self.info.config(text=f"{name} | {w}x{h}")
        self.root.title(f"PEF Viewer - {name}")

    def open(self):
        path=filedialog.askopenfilename(
            title='Open PEF Image',
            filetypes=[("PEF Files","*.pef"),("All Files","*.*")]
        )
        if path:
            self.load(path)
    
def main():
    root=tk.Tk()
    app=PEF_Viewer(root)

    if len(sys.argv)>1:
        app.load(sys.argv[1])

    root.mainloop()

if __name__=='__main__':
    main()
