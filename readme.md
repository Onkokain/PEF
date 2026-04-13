# PEF (Picture Efficient Format)

PEF (.pef) is a custom image extension I built using python and PIP. It converts a png/jpg image into hexcodes and translated them one pixel at a time to form a complete image.

---

## Overview

PEF is a simple binary image format that stores:

- Image width & height
- Raw RGBA pixel data (1 byte per channel with a total of 4 channels)

This project includes:
- Encoder (`PNG/JPG → PEF`)
- Decoder (`PEF → raw pixels`)
- Converter (`PEF → PNG`)
-Demo GUI Viewer (built with Tkinter)

---

## Features

-  Custom binary image format (`.pef`)
-  Lossless RGBA storage (I mean there is no compression yet so expect about a 6-11x file size increase.. yikes..)
-  Encode images into `.pef`
-  Decode `.pef` files
-  Convert back to PNG
-  Lightweight GUI viewer
-  Input validation & error handling

---

##  Project Structure

```
pef.py            # Core encoder/decoder logic
viewer.py         # Tkinter GUI viewer
main.py           # Example usage (also the conversion script)
```

---

##  How the Format Works

### File Structure

```
[ Header ][ Width ][ Height ][ Pixel Data ]

Header      → 4 bytes  → b'PEF\x00'
Width       → 4 bytes  → Big-endian integer
Height      → 4 bytes  → Big-endian integer
Pixel Data  → 4 bytes per pixel (RGBA)
```

Each pixel:
```
R (1 byte) | G (1 byte) | B (1 byte) | A (1 byte)
```

---

## Installation

### Requirements

- Python 3.x
- Pillow

Install dependencies:

```bash
pip install pillow
```

---



##  Testing

Basic test included (currently commented out):

```python
# Run encoder → decoder → verify integrity
```

Uncomment the `test()` function to validate correctness of the implemented logic.

---

## Limitations

- No compression (as stated before, file sizes can be larger than expected)
- No metadata support
- No color profiles
- Slower for large images (since it's based on pure Python loops, switching to rust soon maybe idk)

---

##  Future Improvements

- [ ] Add compression (RLE / zlib)
- [ ] Support metadata (EXIF-like)
- [ ] Optimize pixel processing (NumPy)
- [ ] CLI tool support
- [ ] Switch to rust

---

##  Why This Project?

I watched a guy on youtube do the same thing and I thought it'd be a fun project to try out. I also learned the following from this project:

- Binary file formats
- Image encoding/decoding
- Byte-level data handling
- GUI development with Tkinter

---

## License

MIT License — free to use, modify, and distribute.



