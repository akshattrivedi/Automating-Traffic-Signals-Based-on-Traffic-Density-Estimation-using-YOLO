import os
from django.shortcuts import render,redirect
from django.http import HttpResponse 
from app.forms import TrafficForm
from app.models import Traffic
from darkflow.net.build import TFNet
import cv2

def index(request): 

	if request.method == 'POST': 
		form = TrafficForm(request.POST, request.FILES) 

		if form.is_valid(): 
			form.save() 
			return redirect('results') 
	else: 
		form = TrafficForm() 
	return render(request, 'app/index.html', {'form' : form}) 


def results(request):
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


# Create your views here.
