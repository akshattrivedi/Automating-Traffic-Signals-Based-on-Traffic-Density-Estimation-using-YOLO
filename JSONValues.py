from darkflow.net.build import TFNet
import cv2

options = {"model": "cfg/run/yolo.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}

tfnet = TFNet(options)

imgcv = cv2.imread("./sample_img/traffic-congestion-1.jpg")
result = tfnet.return_predict(imgcv)

#print(result)
#print(type(result))
#print(type(result[0]))

carCount = 0
motorbikeCount = 0
truckCount = 0
busCount = 0
bicycleCount = 0

for i in range(len(result)):
	if result[i]['label'] == 'car':
		carCount = carCount + 1
	elif result[i]['label'] == 'motorbike':
		motorbikeCount = motorbikeCount + 1
	elif result[i]['label'] == 'truck':
		truckCount = truckCount + 1
	elif result[i]['label'] == 'bus':
		busCount = busCount + 1
	elif result[i]['label'] == 'bicycle':
		bicycleCount = bicycleCount + 1
for i in range(len(result)):
	print(result[i])



print()
print("=============================================")
print("Car:",carCount)
print("Motorbike:",motorbikeCount)
print("Truck:",truckCount)
print("Bus:",busCount)
print("Bicycle:",bicycleCount)
print("=============================================")

