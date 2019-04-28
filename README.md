# Automating-Traffic-Signals-Based-on-Traffic-Density-Estimation-using-YOLO
Automating the traffic signal timings using images of vehicles near the crossroads with traffic signals using YOLO (You Only Look Once) and implemented on Python-Django Web Framework.

## Usage

* Download YOLOv2 Weights: http://bit.ly/YOLOv2Weights
* Copy 'yolov2.weights' to 'bin/' folder
* Setup YOLO
```
$ python3 setup.py build_ext --inplace
```

* Run YOLO for image directory
```
$ ./flow --model cfg/run/yolo.cfg --load bin/yolov2.weights --imgdir sample_img/
```

* Retrieve JSON Values of objects inside the image with labels alongwith dimensions of the bounding box and confidence values.
```
$ python3 JSONValues.py
```

* HELP with YOLO options
```
$ ./flow --help
```

* Run the YOLO model on the Python-DJANGO website
```
$ python3 manage.py runserver
```

* There are two methods to run YOLO. Open Browser Type: localhost:8000

* Upload any image on index page and find out number of vehicles belonging to different classes like Car, Motorbike, Truck, Bus, Bicycle
* Run Traffic Simulation for an interval of 10 seconds by using the button 'Traffic Simulation' button on the index page.
