REQUIREMENTS:
	PYTHON 2.7
	LIBRARIES:
		OpenCV2
			numpy
			cython
		Pymunk
		Pygame
	640x480 web cam

How to make it work:
-Disable auto exposure on your webcam
-Find a place with plenty of space and a lot of (preferably)white light
-In frame during play there should be no:
	-Reflective objects: Glass, mirrors, varnished wood, oily keyboards...
	- light sources in direct view
	- Any objects close enough for you to cast your shadow on them during play
-Your background should be a different colour to yourself. 
-To launch the game use the command: `python level*.py`
-When the game starts you should be out of frame to allow the program to take a picture of your background.
-If you need to take another picture of the background press the space bar while out of frame.

Gameplay:
Get the big ball to the red circle.
You will find that you can't interact with all objects.
Your shadow will not be rendered in a purple region

https://www.youtube.com/watch?v=XDNIO3I7HYI&feature=youtu.be

Made by:
a1670074 Matthew Budimir
