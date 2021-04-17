# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 13:52:52 2021

@author: amab
"""

import argparse

# Convert image to bytes
import PIL.Image as Image
from PIL import ImageSequence
import numpy as np
import io 
import os
import warnings

parser = argparse.ArgumentParser(description='Convert a directory of images to compressed C code for OLED animations')
parser.add_argument('--to-file', dest='save_file',
                     default=0,
                    help='save the output to a text file?')

parser.add_argument('--output-fname', dest='out_fname', 
                    default='oled_anim_outc.txt',
                    help='output text filename if to-file is true')

parser.add_argument('--orientation', dest='ori', 
                    default='vertical',
                    help='orientation formatting of the oled')

parser.add_argument('directory', type=str,help='Directory of images (.PNG) to convert')
args = parser.parse_args()
directory = args.directory
ori = args.ori

tofile = args.save_file
outfname = args.out_fname



class ViableImageError(Exception):
    """exception for when images are not uniform size

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ImageConsistencyError(Exception):
    """exception for when images are not uniform size

    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message




def check_image_dir(directory):
    '''
    make sure the image directory is fine to use

    Parameters
    ----------
    directory : string
        directory of an folder with images to convert.

    Raises
    ------
    IOError
        In/out error.
    ViableImageError
        no viable images found.
    ImageConsistencyError
        images are not the same size.

    Returns
    -------
    flist : list
        list of file paths to the images fine.

    '''
    flist = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".png"):
                 flist.append(os.path.join(root, file))
    
    if len(flist) < 0:
        try:
            raise IOError
        except IOError as exc:
            raise ViableImageError('Found no png files within this directory: ', directory) from exc
    h = []
    w = []
    modes = []
    for file in flist:
        ii = Image.open(  file )
        h.append(ii.height)
        w.append(ii.width)


    if len(set(h)) >1 or len(set(w)) > 1:
        try:
            raise IOError
        except IOError as exc:
            raise ImageConsistencyError('Images in the directory are not a consistent size: ', directory) from exc
    
    return flist
    

if directory[-4:] == '.gif':
    img = Image.open(directory)
    frames =[np.array(frame.copy().convert('RGBA').getdata(),dtype=np.uint8).reshape(frame.size[1],frame.size[0],4) for frame in ImageSequence.Iterator(img)]

else:
    flist = check_image_dir(directory)

def convert_gif_2_carr(frames,  w=32,h=88,thresh=50):
    return [convert_to_carr(frames[x],w=w,h=h, thresh=thresh) for x in range(0,len(frames))]

def convert_flist_2_carr(file_list, w=32,h=88,thresh=50):
    return [im2carr(file_list[x],w=w,h=h, thresh=thresh) for x in range(0,len(file_list))]
    
def im2carr(file,w=32,h=88,thresh=50 ):
    im = np.array(Image.open(  file ).convert('RGBA')   )
    return convert_to_carr(im,w=w,h=h,thresh=thresh)
    

def convert_to_carr(im_arr,w=32,h=88,thresh=50):
    if ori.lower() == 'vertical':
        return convert_to_carr_vert(im_arr,w=32,h=88,thresh=50)
    if ori.lower() == 'horizontal':
        return convert_to_carr_horz(im_arr,w=32,h=88,thresh=50)

def convert_to_carr_horz(im_arr,w=32,h=88,thresh=50):
    data = im_arr.flatten()
    output_str = ""
    output_index = 0
    screenheight = h
    screenwidth = w   
    byteIndex = 7
    number = 0
    k= 0
    for i in range(0,len(data),4):
        avg = (data[i] + data[i+1] + data[i+2])/3
        if avg > thresh:
            number+= np.power(2,byteIndex)
        byteIndex -=1 
        
        if (  (i !=0) and ((int(i/4)+1)%w)   )   or (i == len(data) - 4):
            bytIndex=-1
        
        if byteIndex < 0:
            byteset = np.base_repr(number,base=16)
            
            while len(byteset) < 2:
                byteset = '0' + byteset
            byteset = '0x' + byteset
            if k != 0:
                output_str = (output_str + ', ' + byteset )
            else: 
                output_str = byteset
                k+=1
            output_index += 1     
            number = 0
            byteIndex=7
    return output_str
        
        


def convert_to_carr_vert(im_arr,w=32,h=88,thresh=50  ):
    '''
    converts a PIL image np array to a C byte array

    Parameters
    ----------
    im_arr : PIL numpy array of an image
        image data to convert.
    w : width, int, optional
        width of the images, autodetected. The default is 32.
    h : height, int, optional
        height of the images, autodetected. The default is 88.

    Returns
    -------
    output_str : TYPE
        DESCRIPTION.

    '''
    
    data = im_arr.flatten()
    
    output_str = ""
    output_index = 0

    
    screenheight = h
    screenwidth = w
    
    k = 0
    for p in range(0,int(np.ceil(screenheight)/8 )):
        for x in range(0,screenwidth ):
            byteIndex = 7
            number = 0
            
            for y in range(7,-1,-1):
                index = ((p*8)+y)*(screenwidth*4) + x*4
                avg = (data[index] + data[index+1] + data[index+2])/3
                
                
                
                if avg > thresh:
                    number+= np.power(2,byteIndex)
                byteIndex -=1
                
            byteset = np.base_repr(number,base=16)
            
            while len(byteset) < 2:
                byteset = '0' + byteset
            byteset = '0x' + byteset
            if k != 0:
                output_str = (output_str + ', ' + byteset )
            else: 
                output_str = byteset
                k+=1
            output_index += 1

    return output_str
            
# make all the byte strings here  

if directory[-4:] == '.gif':
    strs = convert_gif_2_carr(frames )
else:
    strs = convert_flist_2_carr(flist )
         

strs.append(strs[0])

def compress_strs(strs):
    '''
    

    Parameters
    ----------
    strs : list of c arrays as strings
         c arrays as strings to compress .

    Returns
    -------
    base_arr : list
        list of bytes for the base array.
    changes : list
        byte change indexes per frame.
    changes_values : TYPE
        byte change values per frame.

    '''
    base_arr = strs[0].replace(' ','').split(',')
    changes = []
    changes_values = []
    
    for i in range(1,len(strs) ):
        str_list2 = strs[i].replace(' ','').split(',')
        str_list1 = strs[i-1].replace(' ','').split(',')
        changes.append([x for x in range(len(str_list2)) if str_list2[x] != str_list1[x]] )
        changes_values.append([str_list2[x] for x in range(len(str_list2)) if str_list2[x] != str_list1[x]] )
    return base_arr, changes,changes_values
    
    
frame0, changes,changes_values = compress_strs(strs)

change_lens = [len(x) for x in changes]
max_change = max([len(x) for x in changes])

change_array= np.zeros([len(changes),max_change])
for i in range(len(changes)):
    while len(changes[i]) < max_change:
        changes[i] = changes[i] + [-1,]
    change_array[i,:] = changes[i]



for i in range(len(changes_values)):
    while len(changes_values[i]) < max_change:
        changes_values[i] = changes_values[i] + ['0x1F',]
    
changes_str_flat = [item for sublist in changes_values for item in sublist]
changes_str_to_paste = ' ,'.join(changes_str_flat)

    
anim_size = len(strs[0].replace(' ','').split(','))
n_frames = len(change_lens)
total_mem = n_frames*max_change*2 + anim_size + n_frames*2 + max_change*n_frames
max_mem = 2500



frame0, changes,changes_values = compress_strs(strs)
change_lens = [len(x) for x in changes]
change_inds_flat = [item for sublist in changes for item in sublist]
change_vals_flat = [item for sublist in changes_values for item in sublist]


raw_mem_size = (len(strs)-1)*len(frame0)


cumsum_memory = 0
prog_mem = 0

if len(change_inds_flat) < 254:
    cum_typestr = 'uint8_t'
    prog_mem += (n_frames+1) 
else:
    prog_mem += (n_frames+1)*2 
    cum_typestr = 'uint16_t'


if max(change_inds_flat) < 254:
    inds_typestr = 'uint8_t'
    prog_mem += len(change_vals_flat) + len(change_vals_flat)  + len(frame0)
else:
    prog_mem += 2*len(change_vals_flat) + len(change_vals_flat) + len(frame0)
    inds_typestr = 'uint16_t'


#add all the C code text to paste here, auto change types based on sizes

if prog_mem > 7500:
    warnings.warn('This will take %i bytes in flash memory, this likely will not compile into hex as it is too big for pro-microcontoller.'%prog_mem)

print(' ')
print(' ')

cumsum_lens = [0,] +  np.cumsum(change_lens).tolist()
ind = 0


newlines = []
newlines.append('//**************************************************')
#newlines.append('//* Estimated     RAM usage: %i / 2500 bytes * '%cumsum_memory)
newlines.append('//* PLACE THESE VARIABLE DEFS AT BEGINNING OF FILE *')
newlines.append('//**************************************************')

newlines.append('#define ANIM_SIZE %i // number of bytes in array, max is 1024 (minimize where possible)' %len(frame0))
newlines.append('#define IDLE_FRAMES %i //number of total frames'% (len(strs)-1))
newlines.append(' ')
newlines.append('//********************************************')
#newlines.append('//* Estimated     RAM usage: %i / 2500 bytes * '%cumsum_memory)
newlines.append('//* Compression ratio:      %1.3f to 1      *' % (raw_mem_size/prog_mem))
newlines.append('//* Estimated PROGMEM Usage: %i bytes      *' %prog_mem)
newlines.append('//********************************************')


# BASE FRAME
str1 = 'static const char PROGMEM frame[ANIM_SIZE] = {'
newlines.append(str1)
kind = 0
tmpstr = '\t'
for i in range(len(frame0)):
 

    tmpstr = tmpstr + frame0[i] + ', '
    kind += 1
    if kind == 15:
        newlines.append(tmpstr)
        tmpstr = '\t'
        kind = 0
        
newlines.append(tmpstr)        
newlines.append('};')    
newlines.append(' ')

# Cumulative sum , how many changes per frame
str1 = 'static const ' + cum_typestr + ' PROGMEM cumsum_inds[IDLE_FRAMES+1] = {'
newlines.append(str1)
kind = 0
tmpstr = '\t'
for i in range(len(cumsum_lens)):
 

    tmpstr = tmpstr + str(cumsum_lens[i]) + ', '
    kind += 1
    if kind == 15:
        newlines.append(tmpstr)
        tmpstr = '\t'
        kind = 0
newlines.append(tmpstr)       
newlines.append('};')
newlines.append(' ')
     

# Change index locations 
str1 = 'static const ' + inds_typestr + ' PROGMEM change_inds[%i] = {'%len(change_inds_flat)
newlines.append(str1)
kind = 0
tmpstr = '\t'
for i in range(len(change_inds_flat)):
 

    tmpstr = tmpstr + str(change_inds_flat[i]) + ', '
    kind += 1
    if kind == 15:
        newlines.append(tmpstr)
        tmpstr = '\t'
        kind = 0
        
newlines.append(tmpstr)       
newlines.append('};')
newlines.append(' ')

# Change values 
str1 = 'static const char PROGMEM change_vals[%i] = {'%len(change_vals_flat)
newlines.append(str1)
kind = 0
tmpstr = '\t'
for i in range(len(change_vals_flat)):
 

    tmpstr = tmpstr + str(change_vals_flat[i]) + ', '
    kind += 1
    if kind == 15:
        newlines.append(tmpstr)
        tmpstr = '\t'
        kind = 0
        
newlines.append(tmpstr)
newlines.append('};')
newlines.append(' ')
newlines.append(  (cum_typestr+  ' index_start = 0;'))
newlines.append((cum_typestr+  ' index_end = 0;'))


# Loop code here

total_frames = len(strs)+1

if total_frames > 254:
    newlines.append('static void change_frame_bytewise(uint16_t frame_number){   ')
else:
    newlines.append('static void change_frame_bytewise(uint8_t frame_number){   ')

newlines.append('// for n changes this frame, change those bytes by change_inds and change_vals')
newlines.append( '\tindex_start = pgm_read_word(cumsum_inds + (frame_number-1));')
newlines.append('\tindex_end = pgm_read_word(cumsum_inds + (frame_number));')

newlines.append('\tif (index_start != index_end){  // if a change in buffer')
newlines.append( ('\t\tfor ('+ cum_typestr + ' i=index_start; i < index_end; i++){'))
newlines.append('\t\t\toled_write_raw_byte(pgm_read_byte(change_vals + i), pgm_read_word(change_inds + i));')
newlines.append('\t\t}')       
newlines.append('\t}')    
newlines.append('}')    
newlines.append(' ')

print('used RAM: %i' % cumsum_memory)
print('total RAM: 2500 ')
print(' ')
print('------------------')
print(' ')

for x in newlines:
    print(x)


# save to file if needed
if tofile:
    with open(outfname, 'w') as f:
        f.writelines("%s\n" % st for st in newlines)

