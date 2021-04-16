# -*- coding: utf-8 -*-
"""
Created on Sun Apr 11 13:52:52 2021

@author: amab
"""

# Convert image to bytes
import PIL.Image as Image
import numpy as np
import io 
import os

directory = './fuji_2/'
flist = os.listdir(directory)

def convert_flist_2_carr(file_list, directory, w=32,h=88):
    
    return [im2carr(file_list[x],directory,w=w,h=h) for x in range(0,len(file_list))]
    
def im2carr(file,directory,w=32,h=88 ):
    im = np.array(Image.open(  (directory + file) ))
    return convert_to_carr(im,w=w,h=h)
    
def convert_to_carr(im_arr,w=32,h=88  ):
    
    data = im_arr.flatten()
    
    output_str = ""
    output_index = 0

    
    screenheight = h
    screenwidth = w
    thresh = 50
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
            
            
strs = convert_flist_2_carr(flist,directory )
strs.append(strs[0])

def compress_strs(strs):
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



cumsum_lens = [0,] +  np.cumsum(change_lens).tolist()
ind = 0


newlines = []

newlines.append('//********************************************')
#newlines.append('//* Estimated     RAM usage: %i / 2500 bytes * '%cumsum_memory)
newlines.append('//* Estimated PROGMEM Usage: %i bytes       *' %prog_mem)
newlines.append('//********************************************')

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
str1 = 'static const ' + cum_typestr + ' PROGMEM cumsum_inds[IDLE_FRAMES+1] = {'
newlines.append(str1)
newlines.append(  ( '\t' +  str(cumsum_lens)[1:-1]) )
newlines.append('};')
newlines.append(' ')

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


