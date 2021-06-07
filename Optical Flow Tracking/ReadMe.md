Optical Flow Tracking

In this project, you'll use the Lucas Kanade algorithm to track an object from one frame to another. 

the following example command:
 
python3 hw3.py --boundingBox 304,329,106,58  middlebury/Army/frame07.png middlebury/Army/frame14.png 
 
The output of this command was:

tracked object to have moved [13.859762   -0.09457114] to (317.85977, 328.90543)
 
If you're running locally or set up x-tunneling while ssh'd into tux, you can visualize the results with the --visualize flag:
 
 python3 hw3.py --visualize --boundingBox 304,329,106,58  middlebury/Army/frame07.png middlebury/Army/frame14.png 
 
 This will show the bounding box on the first image and it's tracked location on the second image:
