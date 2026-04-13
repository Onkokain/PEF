# making a custom image extension :3

from PIL import Image


def encoder(width,height,pixels,path): #RGBA as a hash is supported with 4 channels
    with open(path,'wb') as file:
        if width*height!=len(pixels) or width<=0 or height<=0 or any(len(pixel)!=8 for pixel in pixels):
            raise ValueError('Invalid input')
        file.write(b'PEF\x00') # defining the extension type
        file.write(width.to_bytes(4,'big')) # 'big' so that the order remains the same
        file.write(height.to_bytes(4,'big'))
        for pixel in pixels:
            r,g,b,a=int(pixel[:2],16),int(pixel[2:4],16),int(pixel[4:6],16),int(pixel[6:8],16)
            file.write(r.to_bytes(1,'big'))
            file.write(g.to_bytes(1,'big'))
            file.write(b.to_bytes(1,'big'))
            file.write(a.to_bytes(1,'big'))

def decoder(path):
    with open(path,'rb') as file:
        if file.read(4)!=b'PEF\x00':
            raise ValueError('Not a valid PEF file')
        w_b=file.read(4)
        if len(w_b)!=4:
            raise ValueError('Invalid width data')
        h_b=file.read(4)
        if len(h_b)!=4:
            raise ValueError('Invalid height data')
        width=int.from_bytes(w_b,'big')
        height=int.from_bytes(h_b,'big')

        pixels=[] # empty list

        total=width*height # total referring to total number of pixels

        for _ in range(total):
            r_b=file.read(1)
            if len(r_b)!=1:
                raise ValueError('Invalid pixel data')
            g_b=file.read(1)
            if len(g_b)!=1:
                raise ValueError('Invalid pixel data')
            b_b=file.read(1)
            if len(b_b)!=1:
                raise ValueError('Invalid pixel data')
            a_b=file.read(1)
            if len(a_b)!=1:
                raise ValueError('Invalid pixel data')

            r_int=int.from_bytes(r_b,'big')
            g_int=int.from_bytes(g_b,'big')
            b_int=int.from_bytes(b_b,'big')
            a_int=int.from_bytes(a_b,'big')


            # 0 as padding, 2 as size, X as uppercase hex
            r=format(r_int,'02X') 
            g=format(g_int,'02X')
            b=format(b_int,'02X')
            a=format(a_int,'02X')

            hexcode=r+g+b+a
            pixels.append(hexcode)


        return width,height,pixels



def load_image(path):
    # coverting PNG/JPG to PEF
    image=Image.open(path)
    image=image.convert('RGBA')

    width,height=image.size
    pixels=[]

    for x in range(height):
        for y in range(width):
            r,g,b,a=image.getpixel((y,x))
            hex_pixel=f'{r:02X}{g:02X}{b:02X}{a:02X}'
            pixels.append(hex_pixel)
    return width,height,pixels

def save_image(width,height,pixels,path):
    # converting PEF to PNG
    image=Image.new('RGBA',(width,height))
    i=0
    for x in range(height):
        for y in range(width):
            hex_pixel=pixels[i]
            r,g,b,a=int(hex_pixel[:2],16),int(hex_pixel[2:4],16),int(hex_pixel[4:6],16),int(hex_pixel[6:8],16)
            image.putpixel((y,x),(r,g,b,a))
            i+=1
    image.save(path)