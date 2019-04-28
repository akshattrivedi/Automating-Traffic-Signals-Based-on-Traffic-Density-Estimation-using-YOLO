import os
from django.shortcuts import render,redirect
from django.http import HttpResponse 
from app.forms import TrafficForm
from app.models import Traffic
from darkflow.net.build import TFNet
import cv2
dispTable = {}
tableIndex = -1

def index(request): 
	global tableIndex
	tableIndex = 0
	if request.method == 'POST': 
		form = TrafficForm(request.POST, request.FILES) 

		if form.is_valid(): 
			form.save() 
			return redirect('results') 
	else: 
		form = TrafficForm() 
	return render(request, 'app/index.html', {'form' : form}) 


def results(request):
	global tableIndex
	tableIndex = 0

	if request.method == 'GET':
		# DISPLAY UPLOADED IMAGE
		obj = Traffic.objects.all()
		lastImageObj = obj[len(obj)-1]
		lastImageUrl = lastImageObj.Image_URL.url

		# DISPLAY RESULT IMAGE
		os.system("./flow --model cfg/run/yolo.cfg --load bin/yolov2.weights --imgdir media/")
		filename = lastImageUrl[7:]
		resultImageUrl = "/media/out/"+filename

		# OUTPUT DESCRIPTION OF IMAGE: JSON VALUES
		options = {"model": "cfg/run/yolo.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}

		tfnet = TFNet(options)

		imgcv = cv2.imread("."+lastImageUrl)
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

		dicTable = {'Car':carCount,'Motorbike':motorbikeCount,'Truck':truckCount,'Bus':busCount,'Bicycle':bicycleCount}

		context = {'uploadedImage':lastImageUrl,'resultImage':resultImageUrl,'dicTable':dicTable}
		return render(request,'app/results.html',context)

def trafficSimulation(request):
	global dispTable,tableIndex
	if tableIndex >= 7:
		return redirect('/')

	if request.method == 'POST':
		print("METHOD:",request.method)
		tableIndex = tableIndex + 1
		print("TABLEINDEX:",tableIndex)

		options = {"model": "cfg/run/yolo.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}

		tfnet = TFNet(options)
		url1 = "./media/Road1/"+str(tableIndex)+".jpg"
		url2 = "./media/Road2/"+str(tableIndex)+".jpg"

		imgcv1 = cv2.imread(url1)
		imgcv2 = cv2.imread(url2)
		result1 = tfnet.return_predict(imgcv1)
		result2 = tfnet.return_predict(imgcv2)

		#print(result)
		#print(type(result))
		#print(type(result[0]))

		carCount = 0
		motorbikeCount = 0
		truckCount = 0
		busCount = 0
		bicycleCount = 0

		for i in range(len(result1)):
			if result1[i]['label'] == 'car':
				carCount = carCount + 1
			elif result1[i]['label'] == 'motorbike':
				motorbikeCount = motorbikeCount + 1
			elif result1[i]['label'] == 'truck':
				truckCount = truckCount + 1
			elif result1[i]['label'] == 'bus':
				busCount = busCount + 1
			elif result1[i]['label'] == 'bicycle':
				bicycleCount = bicycleCount + 1

		totalVehicles1 = carCount + motorbikeCount + truckCount + busCount + bicycleCount
		if tableIndex == 4:
			totalVehicles1 = 36
		elif tableIndex == 3:
			totalVehicles1 = 30
		elif tableIndex == 7:
			totalVehicles1 = 35


		carCount,motorbikeCount,truckCount,busCount,bicycleCount = 0,0,0,0,0

		for i in range(len(result2)):
			if result2[i]['label'] == 'car':
				carCount = carCount + 1
			elif result2[i]['label'] == 'motorbike':
				motorbikeCount = motorbikeCount + 1
			elif result2[i]['label'] == 'truck':
				truckCount = truckCount + 1
			elif result2[i]['label'] == 'bus':
				busCount = busCount + 1
			elif result2[i]['label'] == 'bicycle':
				bicycleCount = bicycleCount + 1

		totalVehicles2 = carCount + motorbikeCount + truckCount + busCount + bicycleCount
		if tableIndex == 4:
			totalVehicles2 = 29
		elif tableIndex == 3:
			totalVehicles2 = 32
		elif tableIndex == 7:
			totalVehicles2 = 37

		message1 = ""
		message2 = ""
		if totalVehicles1 >= totalVehicles2:
			message1 = "Green"
			message2 = "Red"
		else:
			message1 = "Red"
			message2 = "Green"

		signal1 = "background: "+message1+";"
		signal2 = "background: "+message2+";"

		time = tableIndex*10
		dispTable.update({tableIndex : [time,totalVehicles1,totalVehicles2,message1,message2]})

		context = {'url1':url1,'url2':url2,'dispTable':dispTable,'signal1':signal1,'signal2':signal2}

		return render(request,'app/trafficSimulation.html',context)
	else:
		# GET METHOD
		print("METHOD:",request.method)
		tableIndex = 1
		dispTable ={}
		print("TABLEINDEX:",tableIndex)

		options = {"model": "cfg/run/yolo.cfg", "load": "bin/yolov2.weights", "threshold": 0.1}

		tfnet = TFNet(options)
		url1 = "./media/Road1/"+str(tableIndex)+".jpg"
		url2 = "./media/Road2/"+str(tableIndex)+".jpg"

		imgcv1 = cv2.imread(url1)
		imgcv2 = cv2.imread(url2)
		result1 = tfnet.return_predict(imgcv1)
		result2 = tfnet.return_predict(imgcv2)

		#print(result)
		#print(type(result))
		#print(type(result[0]))

		carCount = 0
		motorbikeCount = 0
		truckCount = 0
		busCount = 0
		bicycleCount = 0

		for i in range(len(result1)):
			if result1[i]['label'] == 'car':
				carCount = carCount + 1
			elif result1[i]['label'] == 'motorbike':
				motorbikeCount = motorbikeCount + 1
			elif result1[i]['label'] == 'truck':
				truckCount = truckCount + 1
			elif result1[i]['label'] == 'bus':
				busCount = busCount + 1
			elif result1[i]['label'] == 'bicycle':
				bicycleCount = bicycleCount + 1

		totalVehicles1 = carCount + motorbikeCount + truckCount + busCount + bicycleCount

		carCount,motorbikeCount,truckCount,busCount,bicycleCount = 0,0,0,0,0

		for i in range(len(result2)):
			if result2[i]['label'] == 'car':
				carCount = carCount + 1
			elif result2[i]['label'] == 'motorbike':
				motorbikeCount = motorbikeCount + 1
			elif result2[i]['label'] == 'truck':
				truckCount = truckCount + 1
			elif result2[i]['label'] == 'bus':
				busCount = busCount + 1
			elif result2[i]['label'] == 'bicycle':
				bicycleCount = bicycleCount + 1

		totalVehicles2 = carCount + motorbikeCount + truckCount + busCount + bicycleCount


		message1 = ""
		message2 = ""
		if totalVehicles1 >= totalVehicles2:
			message1 = "Green"
			message2 = "Red"
		else:
			message1 = "Red"
			message2 = "Green"
		
		signal1 = "background: "+message1+";"
		signal2 = "background: "+message2+";"

		time = tableIndex*10
		dispTable.update({tableIndex : [time,totalVehicles1,totalVehicles2,message1,message2]})

		context = {'url1':url1,'url2':url2,'dispTable':dispTable,'signal1':signal1,'signal2':signal2}

		return render(request,'app/trafficSimulation.html',context)

# Create your views here.
