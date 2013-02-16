'''
Created on Feb 16, 2013

@author: leonpo
'''

from SimpleCV import Camera, Color, Display
from time import sleep

cam = Camera(prop_set={'width':320,'height':240})
size = (cam.getImage().size())
disp = Display(size)

prev_center = None

while disp.isNotDone():
   input = cam.getImage()
   dist = input.colorDistance(Color.RED).invert().dilate(3).threshold(130)

   blobs = dist.findBlobs(minsize=500)

   if( blobs is not None ):
       blobs.draw(color=Color.GREEN, width=3)
       blobs.sortArea()
       center = (int(blobs[-1].minRectX()),
                 int(blobs[-1].minRectY()))

       # check of movement direction
       if prev_center is not None:
          if (prev_center[0] - center[0]) > 20:
              print "moved left"
          if (prev_center[0] - center[0]) < -20:
              print "moved right"

          if (prev_center[1] - center[1]) > 20:
              print "moved up"
          if (prev_center[1] - center[1]) <-20:
              print "moved down"
       prev_center = center
   dist.save(disp)
   sleep(.1)
