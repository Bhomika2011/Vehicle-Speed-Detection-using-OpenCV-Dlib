#importing the necessary libraries
import cv2
import dlib
import time
import math

#Taking Cascade file from the local directory 
carCascade = cv2.CascadeClassifier('vech.xml')

#initializing the video capture object 
video = cv2.VideoCapture('carsVid.mp4')

#To get the location of the object 
WIDTH = 1280 #Width of the object
HEIGHT = 720 #height of the object

#To estimate the speed of the object using the previous and current location of the object 
#The formula is taken from the paper "Real-Time Object Tracking using Adaptive Correlation Filters"
#The formula is: speed = distance * fps * 3.6 
def estimateSpeed(location1, location2): #location1 and location2 are the previous and current location of the object
    d_pixels = math.sqrt(math.pow(location2[0] - location1[0], 2) + math.pow(location2[1] - location1[1], 2)) #distance in pixels
    ppm = 8.8 #Pixels per meter
    d_meters = d_pixels / ppm #Distance in meters
    fps = 18 #Frames per second
    speed = d_meters * fps * 3.6  #Speed in km/h
    return speed #returning the speed

#trackmultiobjects is the function which is used to detect the object in the video 
#The function takes the video object as input and returns the location of the object
#The function also returns the speed of the object 
def trackMultipleObjects(): #Tracking function
    rectangleColor = (0, 255, 0) #In BGR
    frameCounter = 0 #to count the number of frames
    currentCarID = 0 #to keep track of the carID
    fps = 0 #fps = frames per second

    carTracker = {} #Dictionary to store the carID and the location of the object
    carNumbers = {} #Dictionary to store the carID and the speed of the object
    carLocation1 = {} #Dictionary to store the carID and the previous location of the object
    carLocation2 = {} #Dictionary to store the carID and the current location of the object
    speed = [None] * 1000 #Initializing the speed array to None
    
    out = cv2.VideoWriter('out.mp4', cv2.VideoWriter_fourcc('M','P','4','V'), 10, (WIDTH, HEIGHT)) #Output video file
    
    while True: #Looping over the video using the video object
        start_time = time.time() #To calculate the fps
        rc, image = video.read() #Reading the video frame
        if type(image) == type(None): #If the video is over
            break

        image = cv2.resize(image, (WIDTH, HEIGHT)) #resize the image to the desired size
        resultImage = image.copy() #Copying the image to the resultImage

        frameCounter = frameCounter + 1 #Incrementing the frame counter
        carIDtoDelete = [] #List to store the carID which is not present in the current frame

        for carID in carTracker.keys(): #Looping over the carTracker dictionary
            trackingQuality = carTracker[carID].update(image)

            if trackingQuality < 7: #If the tracking quality is less than 7 then the car is not detected
                carIDtoDelete.append(carID) #Appending the carID to the carIDtoDelete list

        
        for carID in carIDtoDelete: #Looping over the carIDtoDelete list
            print("Removing carID " + str(carID) + ' from list of trackers. ') #Printing the carID which is not present in the current frame
            print("Removing carID " + str(carID) + ' previous location. ') #Printing the carID which is not present in the current frame
            print("Removing carID " + str(carID) + ' current location. ')
            carTracker.pop(carID, None)
            carLocation1.pop(carID, None)
            carLocation2.pop(carID, None)

        
        if not (frameCounter % 10): #Looping over the frameCounter variable 
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #Converting the image to grayscale
            cars = carCascade.detectMultiScale(gray, 1.1, 13, 18, (24, 24)) #Detecting the cars in the image

            for (_x, _y, _w, _h) in cars: #Looping over the cars detected in the image
                x = int(_x) #x = x coordinate of the car
                y = int(_y) # x and y are the coordinates of the top left corner of the car
                w = int(_w) #x, y, w, h are the coordinates of the cars
                h = int(_h) #x, y, w, h are the coordinates of the cars

                x_bar = x + 0.5 * w #Calculating the center of the car
                y_bar = y + 0.5 * h #Calculating the center of the car

                matchCarID = None #Initializing the matchCarID variable

                for carID in carTracker.keys(): #Looping over the carTracker dictionary
                    trackedPosition = carTracker[carID].get_position()

                    t_x = int(trackedPosition.left()) #Calculating the center of the car
                    t_y = int(trackedPosition.top())   #Calculating the center of the car
                    t_w = int(trackedPosition.width()) 
                    t_h = int(trackedPosition.height())

                    t_x_bar = t_x + 0.5 * t_w #Calculating the center of the car
                    t_y_bar = t_y + 0.5 * t_h #Calculating the center of the car
                    
                    #The formula is taken from the paper "Real-Time Object Tracking using Adaptive Correlation Filters"
                    if ((t_x <= x_bar <= (t_x + t_w)) and (t_y <= y_bar <= (t_y + t_h)) and (x <= t_x_bar <= (x + w)) and (y <= t_y_bar <= (y + h))): 
                        matchCarID = carID 

                if matchCarID is None: 
                    print(' Creating new tracker' + str(currentCarID)) 

                    tracker = dlib.correlation_tracker() 
                    tracker.start_track(image, dlib.rectangle(x, y, x + w, y + h))

                    carTracker[currentCarID] = tracker 
                    carLocation1[currentCarID] = [x, y, w, h]

                    currentCarID = currentCarID + 1

        for carID in carTracker.keys(): #Looping over the carTracker dictionary
            trackedPosition = carTracker[carID].get_position()

            t_x = int(trackedPosition.left()) #Calculating the center of the car
            t_y = int(trackedPosition.top())
            t_w = int(trackedPosition.width())
            t_h = int(trackedPosition.height())

            cv2.rectangle(resultImage, (t_x, t_y), (t_x + t_w, t_y + t_h), rectangleColor, 4) #Drawing the rectangle around the car

            carLocation2[carID] = [t_x, t_y, t_w, t_h] #Storing the current location of the car

        end_time = time.time() #Calculating the time taken to detect the car

        if not (end_time == start_time): #Calculating the frames per second
            fps = 1.0/(end_time - start_time)

        for i in carLocation1.keys(): #Looping over the carLocation1 dictionary
            if frameCounter % 1 == 0: #Looping over the frameCounter variable
                [x1, y1, w1, h1] = carLocation1[i] #Storing the previous location of the car
                [x2, y2, w2, h2] = carLocation2[i] #Storing the current location of the car

                carLocation1[i] = [x2, y2, w2, h2] #Storing the current location of the car

                if [x1, y1, w1, h1] != [x2, y2, w2, h2]: #Checking if the car has moved
                    if (speed[i] == None or speed[i] == 0) and y1 >= 275 and y1 <= 285: #Checking if the car is in the road
                        speed[i] = estimateSpeed([x1, y1, w1, h1], [x1, y2, w2, h2]) #Estimating the speed of the car

                    if speed[i] != None and y1 >= 180: #Checking if the car is in the road
                        cv2.putText(resultImage, str(int(speed[i])) + "km/h", (int(x1 + w1/2), int(y1-5)), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 100) ,2) 

        cv2.imshow('result', resultImage) #Showing the result image

        out.write(resultImage) #Writing the result image to the output video

        if cv2.waitKey(1) == 27: #Checking if the user has pressed the ESC key
            break #Breaking the loop

    
    cv2.destroyAllWindows() #Destroying all the windows
    out.release() #Releasing the output video

#Calling the trackMultipleObjects function
if __name__ == '__main__': 
    trackMultipleObjects() #Calling the trackMultipleObjects function
