from pdf2image import convert_from_path 
from PIL       import Image

import pytesseract
import os 

PATH  = os.path.dirname( __file__ )

def writeFile(): 

    EXCLUDE_LIST = [ 'metros', 'metro', 'Lt', 'm²', 'mg ', 'cm', 'm?', 'g ', 'Metros', 'Metro', 'mls', 'ml' ] 

    FILES = [] 
    NOME  = []

    for _, _, file_in in os.walk( PATH+'\\PDF_TO_CONVERT' ):
        FILES.append( file_in )

    pytesseract.pytesseract.tesseract_cmd = PATH + '\\utils\\Tesseract-OCR\\tesseract.exe'
    PATH_POPPLER                          = PATH + '\\utils\\poppler-21.03.0\\Library\\bin'

    for pdf_file in FILES[0] : 

        PATH_IMG = PATH + '\\PDF_TO_CONVERT\\' + pdf_file 
        PDF      = convert_from_path( PATH_IMG, dpi=200, poppler_path = PATH_POPPLER )

        for ind, page in enumerate( PDF ):
            out = pytesseract.image_to_string( page )   
            out = out.split('\n')

            for n_line, line in enumerate( out ): 
                if  'Itens:' in line: 
                    begin = n_line+1
                try:
                    if 'R$' in line[:2]:
                        end = n_line
                except:
                    continue
            
            for line in out[ begin : end ]:
                line = line.split('R$')
                if '  ' in line[0]:
                    line[0] = line[0].replace('  ',' ')
                if ',' in line[0]:
                    line[0] = line[0].replace(',', '.' )
                for exclude in EXCLUDE_LIST: 
                    if exclude in line[0]:
                        line[0] = line[0].replace(exclude, '')

                
                NOME.append(line[0])
                print( line[0] )
    
    print( NOME )
    with open(PATH + '\\LISTA_COMPLETA.txt', 'w') as f:
        for i in range(len(NOME)):
            f.write( NOME[i] + '\n'  )

#writeFile() 

LIST = [] 

def readFile():
    with open(PATH + "\\LISTA_COMPLETA.txt", 'r') as f: 
        for line in f.readlines():
            line = line.split(' ')
            if line != '':
                for _ in range(len(line)): 
                    m = line.pop()
                    if m == '':
                        continue
                    else:
                        try:
                            if float(m) :
                                quan = float(m)  
                                break
                        except:
                            continue
                aux = ''
                for nibble in line:
                    aux += nibble + ' '
                nome = aux 
                LIST.append( [nome, quan] )

    return LIST

from collections import Counter 

LIST = readFile() 
LIST = sorted( LIST, key = lambda nome : nome[0] )

NAME = [] 
QUAN = []
for n, q in LIST: 
    NAME.append(n)
    QUAN.append(q)

ALL_UNIQUE_NAMES = Counter( NAME )

NEW_LIST = [] 

for name in ALL_UNIQUE_NAMES: 
    quan = 0 
    for n, q in zip( NAME, QUAN ) : 
        if name == n: 
            quan += q 

    NEW_LIST.append( [name, quan] )    

with open( PATH + '\\final.csv', 'w') as f:
    for n, q in NEW_LIST:
        f.write( n + ' ; ' + str(q) + '\n')

print( NEW_LIST )