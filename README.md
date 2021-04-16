# qmk OLED animation compressor
A short python script to compress .gif or image directories into looping C code for oled's with QMK firmware

**Warning!**

This will just give the C code for a looping animation. Code was made for an Elite C controller for QMK firmware and a 32x128 OLED. Currently vertical encoding only

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
--orientation <'vertical'/'horizontal'> orientation formatting of the oled, default is 'vertical'  **Currently only works with vertical**

```


## Dependancies and Tools:

PIL - https://pillow.readthedocs.io/en/stable/
Numpy - https://numpy.org/doc/stable/

## Credit to image to byte array code:

Image2cpp: https://javl.github.io/image2cpp/



## full example for moon.gif

Input:
```
python ./moon.gif --to-file=True
```
Output:
```
used RAM: 0
total RAM: 2500

------------------

//**************************************************
//* PLACE THESE VARIABLE DEFS AT BEGINNING OF FILE *
//**************************************************
#define ANIM_SIZE 352 // number of bytes in array, max is 1024 (minimize where possible)
#define IDLE_FRAMES 34 //number of total frames

//********************************************
//* Compression ratio:      9.621 to 1      *
//* Estimated PROGMEM Usage: 1244 bytes      *
//********************************************
static const char PROGMEM frame[ANIM_SIZE] = {
        0x2F, 0x17, 0x4B, 0xA5, 0x43, 0x01, 0x02, 0x01, 0x00, 0x81, 0x80, 0x80, 0xC0, 0xC0, 0xC0,
        0xC0, 0xC0, 0xC0, 0xC0, 0xC0, 0x90, 0x80, 0x81, 0x00, 0x01, 0x02, 0x01, 0x03, 0x05, 0x8B,
        0x17, 0x2F, 0x00, 0x00, 0x80, 0xE0, 0xF8, 0x9C, 0xC6, 0x66, 0x3F, 0x1B, 0x19, 0x09, 0x1F,
        0x17, 0x3F, 0x3F, 0x1F, 0x0F, 0x0F, 0x0F, 0x0F, 0x1D, 0xF9, 0xFB, 0xFE, 0x9E, 0x1C, 0xF8,
        0xE0, 0x80, 0x00, 0x00, 0x00, 0xFC, 0x87, 0x03, 0x01, 0x01, 0x0F, 0x04, 0x80, 0x80, 0x80,
        0x80, 0x40, 0x30, 0x3F, 0xBE, 0x86, 0xC4, 0xC4, 0xE6, 0xF8, 0xF1, 0xE0, 0xE0, 0xF0, 0xF9,
        0xAF, 0xCF, 0xFF, 0xFF, 0xFC, 0x00, 0x28, 0x10, 0x07, 0x1E, 0x30, 0x60, 0xC2, 0xC0, 0x82,
        0x07, 0x01, 0x13, 0x0C, 0x1C, 0x9D, 0xFC, 0xE7, 0x81, 0xC2, 0x83, 0x8F, 0xDF, 0xFF, 0xFF,
        0x7F, 0xBF, 0x7F, 0x27, 0x1F, 0x07, 0x00, 0x00, 0x50, 0xA0, 0x40, 0x82, 0x00, 0x00, 0x00,
        0x01, 0x03, 0x03, 0x04, 0x04, 0x45, 0x05, 0x0E, 0x0C, 0x0C, 0x0F, 0x07, 0x07, 0x05, 0x05,
        0x02, 0x83, 0x01, 0x10, 0x28, 0x10, 0x00, 0x80, 0x40, 0xA0, 0x2F, 0x4E, 0x5D, 0xBA, 0xBD,
        0x7A, 0x74, 0x78, 0xF4, 0xE8, 0xF4, 0xE8, 0xF0, 0xE8, 0xD0, 0xE8, 0xD0, 0xE8, 0xD0, 0xE8,
        0xF0, 0xE8, 0xF4, 0xE8, 0x74, 0x78, 0x74, 0xBA, 0xB5, 0x5A, 0x4D, 0x2E, 0x00, 0x08, 0x00,
        0x00, 0x00, 0x81, 0x01, 0x01, 0x02, 0x02, 0x02, 0x42, 0x05, 0x05, 0x05, 0x05, 0x25, 0x05,
        0x05, 0x05, 0x02, 0x02, 0x22, 0x02, 0x81, 0x01, 0x11, 0x10, 0x28, 0xC6, 0x28, 0x10, 0x08,
        0x40, 0x00, 0x00, 0x01, 0x02, 0x01, 0x00, 0x00, 0x00, 0x10, 0x00, 0x00, 0x00, 0x00, 0x80,
        0x40, 0x80, 0x00, 0x04, 0x00, 0x01, 0x00, 0x20, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x08,
        0x00, 0x60, 0x60, 0x70, 0x68, 0x70, 0x60, 0x60, 0x62, 0x60, 0x60, 0x60, 0x60, 0x60, 0x68,
        0x60, 0x60, 0x61, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x60, 0x61,
        0x60, 0x60, 0x60, 0x00, 0x00, 0x00, 0xF0, 0x00, 0x00, 0x00, 0x00, 0xF0, 0x50, 0x50, 0x50,
        0x00, 0xF0, 0x00, 0x00, 0x00, 0xF0, 0x00, 0xF0, 0x50, 0x50, 0x50, 0x00, 0xF0, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x03, 0x02, 0x02, 0x02, 0x00, 0x03, 0x02,
        0x02, 0x02, 0x00, 0x00, 0x01, 0x02, 0x01, 0x00, 0x00, 0x03, 0x02, 0x02, 0x02, 0x00, 0x03,
        0x02, 0x02, 0x02, 0x00, 0x00, 0x00, 0x00,
};

static const uint16_t PROGMEM cumsum_inds[IDLE_FRAMES+1] = {
        0, 3, 9, 11, 25, 47, 66, 81, 90, 94, 102, 107, 110, 111, 112,
        116, 118, 121, 130, 133, 138, 154, 160, 164, 169, 187, 210, 225, 236, 242,
        250, 252, 261, 266, 274,
};

static const uint16_t PROGMEM change_inds[274] = {
        15, 129, 234, 2, 3, 4, 127, 146, 214, 3, 234, 3, 29, 62, 63,
        87, 88, 89, 113, 114, 115, 197, 228, 229, 230, 2, 3, 4, 62, 63,
        87, 88, 89, 113, 114, 115, 137, 138, 139, 140, 141, 142, 143, 168, 169,
        170, 229, 113, 114, 115, 137, 138, 139, 140, 141, 142, 143, 166, 167, 168,
        169, 171, 196, 197, 198, 199, 138, 139, 166, 167, 168, 169, 170, 171, 196,
        197, 198, 199, 214, 229, 284, 196, 197, 198, 199, 218, 221, 228, 229, 230,
        196, 197, 199, 284, 29, 131, 219, 220, 221, 222, 223, 282, 219, 220, 221,
        222, 223, 131, 218, 221, 263, 269, 153, 154, 155, 269, 154, 225, 216, 245,
        263, 20, 238, 239, 240, 241, 242, 271, 272, 273, 154, 216, 225, 129, 153,
        154, 155, 245, 15, 20, 29, 129, 203, 214, 218, 221, 238, 239, 240, 241,
        242, 271, 272, 273, 15, 140, 214, 218, 221, 225, 20, 29, 140, 203, 2,
        3, 4, 20, 140, 131, 152, 153, 154, 178, 179, 180, 181, 182, 183, 184,
        205, 206, 207, 208, 224, 225, 269, 2, 3, 4, 152, 153, 154, 179, 180,
        181, 182, 183, 184, 202, 203, 204, 205, 206, 224, 232, 233, 234, 235, 269,
        20, 131, 178, 202, 203, 204, 205, 206, 207, 208, 231, 232, 233, 234, 235,
        20, 140, 208, 230, 231, 232, 233, 234, 235, 261, 282, 127, 146, 208, 230,
        232, 261, 127, 146, 239, 240, 241, 245, 272, 282, 127, 243, 20, 140, 216,
        239, 240, 241, 243, 245, 272, 20, 140, 214, 218, 221, 15, 129, 146, 214,
        216, 218, 221, 282,
};

static const char PROGMEM change_vals[274] = {
        0xC4, 0xA4, 0x00, 0x0B, 0x45, 0x03, 0x20, 0x27, 0x02, 0x05, 0x10, 0x45, 0x0B, 0x80, 0x40,
        0xF0, 0xF8, 0xFD, 0x99, 0xCE, 0x87, 0x01, 0x00, 0x01, 0x00, 0x4B, 0xA5, 0x43, 0x00, 0x00,
        0xE0, 0xF0, 0xF9, 0xF1, 0xFA, 0x9B, 0x83, 0xC4, 0xF4, 0x7D, 0x1F, 0x0F, 0x0F, 0xFE, 0xEF,
        0xF7, 0x00, 0x81, 0xC2, 0x83, 0x03, 0x84, 0xC4, 0x45, 0x05, 0x0E, 0x0C, 0xF4, 0xF8, 0xFC,
        0xFE, 0xE9, 0x38, 0x3F, 0x3F, 0x07, 0x04, 0x04, 0x74, 0x78, 0xF4, 0xE8, 0xF4, 0xE8, 0x30,
        0x79, 0x31, 0x01, 0x22, 0x01, 0x60, 0x48, 0x91, 0x01, 0x21, 0x01, 0x44, 0x01, 0x02, 0x01,
        0x00, 0x81, 0x01, 0x61, 0x8B, 0x80, 0x00, 0x10, 0x38, 0x10, 0x00, 0x64, 0x10, 0x28, 0x44,
        0x28, 0x10, 0x82, 0x11, 0xC6, 0x60, 0x60, 0x00, 0x10, 0x00, 0x68, 0x00, 0x00, 0x01, 0x00,
        0x62, 0x80, 0x80, 0x40, 0x20, 0x40, 0x80, 0x61, 0x62, 0x61, 0x10, 0x81, 0x40, 0xA0, 0x10,
        0x28, 0x10, 0x01, 0xC0, 0x90, 0x0B, 0xA4, 0x02, 0x02, 0x01, 0x44, 0x00, 0x80, 0x40, 0x80,
        0x00, 0x60, 0x61, 0x60, 0xC4, 0x05, 0x22, 0x11, 0xC6, 0x00, 0x80, 0x8B, 0x45, 0x42, 0x0B,
        0x45, 0x03, 0x90, 0x05, 0x80, 0x81, 0x50, 0x68, 0xF0, 0xF8, 0xF8, 0xEC, 0xF6, 0xEB, 0x75,
        0x1D, 0x0D, 0x07, 0x27, 0x00, 0x40, 0x60, 0x4B, 0xA5, 0x43, 0x01, 0x10, 0x28, 0xE8, 0xF0,
        0xE8, 0xF4, 0xE8, 0x74, 0x82, 0xE2, 0x75, 0x3D, 0x0F, 0x08, 0x1C, 0x07, 0x13, 0x01, 0x68,
        0x80, 0x82, 0xD0, 0x02, 0x42, 0x05, 0x05, 0x05, 0x05, 0x25, 0x60, 0x38, 0x1C, 0x1C, 0x02,
        0x90, 0x45, 0x05, 0x41, 0x00, 0x80, 0x00, 0x10, 0x00, 0x61, 0x60, 0x00, 0x07, 0x25, 0x01,
        0x00, 0x60, 0x20, 0x27, 0x00, 0x80, 0x00, 0x00, 0x60, 0x64, 0x00, 0x00, 0x80, 0x05, 0x01,
        0x80, 0x40, 0x80, 0x04, 0x01, 0x61, 0x90, 0x45, 0x02, 0x01, 0x44, 0xC0, 0xA0, 0x07, 0x22,
        0x81, 0x11, 0xC6, 0x60,
};

uint16_t index_start = 0;
uint16_t index_end = 0;
static void change_frame_bytewise(uint8_t frame_number){
// for n changes this frame, change those bytes by change_inds and change_vals
        index_start = pgm_read_word(cumsum_inds + (frame_number-1));
        index_end = pgm_read_word(cumsum_inds + (frame_number));
        if (index_start != index_end){  // if a change in buffer
                for (uint16_t i=index_start; i < index_end; i++){
                        oled_write_raw_byte(pgm_read_byte(change_vals + i), pgm_read_word(change_inds + i));
                }
        }
}


```


