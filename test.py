from pef import encoder,decoder
import os
import tempfile 



def test():
    width=2
    height=2
    pixels=['FF0000FF','00FF00FF','0000FFFF','FFFFFFFF'] # red, green, blue, white

    # creating temp file
    temp_file=tempfile.NamedTemporaryFile(delete=False, suffix='.pef')
    temp_path=temp_file.name
    temp_file.close() # need to close for encoder to be able to write

    try:
        encoder(width,height,pixels,temp_path)
        d_w,d_h,d_pixels=decoder(temp_path)
        assert d_w==width
        assert d_h==height
        assert d_pixels==pixels
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__=='__main__':
    test()
    print('\033[32mTest passed\033[0m')
    