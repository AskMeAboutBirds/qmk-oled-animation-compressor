# qmk OLED animation compressor
A short python script to compress .gif or image directories into looping C code for oled's qith QMK firmware

**Warning!**

This will just give the C code for a looping animation. Code was made for an Elite C controller for QMK firmware and a 32x128 OLED.

Purpose: 

Example usage:  

```python  oled_animation_to_c.py <directory w/ images named in sequence>```

Arguments:

```
--to-file <boolean> save the output to a textfile, default is false
--output-fname <string> output filename , default is oled_anim_outc.txt
--orientation <'vertical'/'horizontal'> orientation formatting of the oled, default is 'vertical'

```
