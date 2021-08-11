Objective : Generate a GIF generated with 10 PPM pictures, Each representing a pi Monte carolo Simulation

We generate a point in the [-1,1]x[-1,1] square. If his distance to (0,0) is inferieur to 1, we increment by one a counter (initialized to 0). By multiplying by 4 and by dividing by the number of point of the simulation, we estimate the value of pi.
We do an homothety to each point so that the point is in the [0, size]x[0,size] square (of integer cordinates). We then write it on the ppm file. We do this 10 times, In Each PPM picture, we add 10% percents of the number of poins of the simulation.

Team : Solo

Time Spent : ~ 30 hours

Technologies used:
- Python, pylint
- Libraries : numpy, random, sys, subprocess

Mathematics :
- Monte-Carlo, Homothety