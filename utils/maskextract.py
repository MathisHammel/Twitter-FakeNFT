# This script generates an alpha mask based on the actual hexagon shape.
# It is based on a screenshot, so we need to process the edge to have smooth transparency and avoid aliasing
# This is done by checking the amount of blue in the pixels near the edge (near green pixels)

from PIL import Image

mask = Image.open('newmask_raw.png')
res = Image.new('RGBA', mask.size, (0, 0, 0, 255))

for x in range(mask.size[0]):
    if not x%10: print(x)
    for y in range(mask.size[1]):
        if mask.getpixel((x,y)) == (0,255,0):
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if 0 <= x+dx < mask.size[0] and 0 <= y+dy < mask.size[1]:
                        r,g,b = mask.getpixel((x+dx, y+dy))
                        if b >= 245: b = 255
                        res.putpixel((x+dx, y+dy), (0, 0, 0, b))

res.save('newmask_full.png')
res.resize((400,400)).save('newmask.png')
