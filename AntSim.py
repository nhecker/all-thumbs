# This CircuitPython is intened for TinyCircuits's Thumby, <https://thumby.us/>.
# It is heavily influenced by <https://en.wikipedia.org/wiki/Langton%27s_ant>.
# It is a simulation only, intended to create digital art; it has no controls.

import thumby
import random
from framebuf import FrameBuffer, MONO_HMSB, MONO_VLSB

thumby.display.setFPS(4) # for the viewer's pleasure
thumby.display.brightness(1) # for the battery's pleasure (++ if sim is dark)
antd = 0 # init ant direction (north)
buf = bytearray()
cells = []
wb = 72//8 # byte dimensions for BuildBuffer()
hb = 360//wb
antx = thumby.display.width//2 # init ant position (center)
anty = thumby.display.height//2
fbuffer = FrameBuffer(thumby.display.display.buffer, 72, 40, MONO_VLSB)

# Single-pixel cells are dumb and we should just use a buffer directly so
# that we don't have to call BuildBuffer() every frame. This is probably
# the first thing to optimize for huge efficiency gainz.
def InitCells(): # initializes the cells array with all 0s
    global cells
    for row in range(thumby.display.height):
        for col in range(thumby.display.width):
            cells.append(0)
InitCells()

def BuildBuffer(): # convert cells array to a buffer for display
    global buf
    buf = bytearray()
    gi=0
    for row in range(hb):
        for col in range(wb):
            nb = 0b0
            for i in range(8):
                nb |= (0b1*cells[gi]) << (i)
                gi+=1
            buf.append(nb)
    fbuffer.blit(FrameBuffer(buf, 72, 40, MONO_HMSB), 0, 0, 72,40) # draw board
    thumby.display.update() # flush the screenbuffer

def Simulate(): # simulates the ant in a grid of cells
    global antx
    global anty
    global antd
    global cells
    gi = anty*thumby.display.width + antx # gi is the index into cells array
    if cells[gi] == 0: # unexplored so mostly straight
        if random.randint(0,5) == 0:
            antd = random.randint(0,3)
        cells[gi] = 1
    else: # been here before, so more likely to explore elsewhere
        antd = random.randint(0,3)
        cells[gi] = 0
    if antd == 0: # move ant
        anty -= 1
    elif antd == 1:
        antx += 1
    elif antd == 2:
        anty += 1
    elif antd == 3:
        antx -= 1
    if antx < 0: # wrap ant
        antx = thumby.display.width-1
    elif antx >= thumby.display.width:
        antx = 0
    if anty < 0:
        anty = thumby.display.height-1
    elif anty >= thumby.display.height:
        anty = 0
    BuildBuffer()

while 1: # simulation screen loop
    Simulate()

