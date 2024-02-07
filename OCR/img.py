import os 
PATH  = os.path.dirname( __file__ )

from PIL import Image
img = Image.open( os.path.join( PATH + 'img.jpg' ) ) 

import pytesseract 
pytesseract.pytesseract.tesseract_cmd = os.path.join( PATH, 'utils', 'Tesseract-OCR', 'tesseract.exe' ) 

ret = pytesseract.image_to_string( img ) 
print( ret.replace( '\n', ' ' )   )
