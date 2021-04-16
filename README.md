# qmk OLED animation compressor
A short python script to compress .gif or image directories into looping C code for oled's with QMK firmware

**Warning!**

This will just give the C code for a looping animation. Code was made for an Elite C controller for QMK firmware and a 32x128 OLED.

### Purpose: 

Saving animation frames to flash memory or RAM for oled's is costly and limits the amount of frames you can animate with. This code will automatically calculate the changes needed to compress an animation into the following (hopefully smaller) amount of information in flash memory. It takes N frames and will make the following:

* Base frame -  one frame to write once to the OLED
* cumsum_inds - a list of cumulative sum changes per frame, ie ```cumsum_inds[i] - cumsum_inds[i-1] ``` = amount of bytes to change per frame i.
* change_inds - index in the byte array of the changes
* change_vals - byte value to change at index

**Warning** this may take more memory in flash based on the nature of the animation, lots of changes per frame = more changes to store in flash. Worst case scenario would be frames that flash completely black or white. 

This will provide the C code to paste into QMK .C firmware, keymap.c or <name of keyboard>.c
  
The code is called via change_frame_bytewise(frame_number), note if you change frames out of order it will break the animation, as it only updates the bites from frame -i to frame i.

### Example usage:  

```python  oled_animation_to_c.py <directory w/ images named in sequence or .gif>```

### Arguments:

```
--to-file <boolean> save the output to a textfile, default is false
--output-fname <string> output filename , default is oled_anim_outc.txt
--orientation <'vertical'/'horizontal'> orientation formatting of the oled, default is 'vertical'

```


## Dependancies and Tools:

PIL - https://pillow.readthedocs.io/en/stable/
Numpy - https://numpy.org/doc/stable/

## Credit to image to byte array code:

Image2cpp: https://javl.github.io/image2cpp/

