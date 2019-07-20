import random
import sched, time
import sys
import datetime
import csv

message = input("Enter number of subsystems: ")
print("Assuming that we have three fans in robot..")
maximumFanSpeed = [1000.0, 2000.0, 3000.0] #This can be changed and % max speed has nothing to do with these values
dataFrequency = 3 #Seconds

with open('output.csv', 'w') as output:
    fileWriter = csv.writer(output)
    fileWriter.writerow(["Maximum Fan Speeds", "Adjusted Fan Speeds", "Max Subsystems Temp", "% Speed Adjusted", "Time"])
    output.close()

def dataGenerator(sc):
    temperature = []
    with open( 'livedata.txt', 'a+') as f:
        for numOfSystems in range(1, int(message)+1):
            temperature.append(random.uniform(1,100))
        print("Generated Subsystem temperature values: %s" % temperature)
        for item in temperature:
             f.write("%s " % item)
        f.write("\n")
        f.close()
        del temperature[:]
    
def controlFans():
    graph_data = open('livedata.txt','r').read()
    lines = graph_data.split('\n')[-2]
    line = lines.split(' ')
    del line[-1]
    print("Highest temperature reading:")
    print(max(float(x) for x in line))
    adjustFanSpeed(max(float(x) for x in line))

def adjustFanSpeed(latestMaxTemp):
    with open('output.csv', 'a+') as output:
        fileWriter = csv.writer(output)
        if (25 <= latestMaxTemp <= 75):
            adjustedSpeedPercent = ((latestMaxTemp - 25.0) * 1.6) + 20 #Linear Interpolation
            adjustedSpeed = [ element*adjustedSpeedPercent/100 for element in maximumFanSpeed ] 
        elif (latestMaxTemp < 25):
            adjustedSpeed = [ element*0.2 for element in maximumFanSpeed ] 
            adjustedSpeedPercent = 20
        elif (latestMaxTemp > 75):
            adjustedSpeed = maximumFanSpeed
            adjustedSpeedPercent = 100
        fileWriter.writerow([maximumFanSpeed, adjustedSpeed, latestMaxTemp, adjustedSpeedPercent, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    
def main():
    try:
        while True:
            s = sched.scheduler(time.time, time.sleep)
            s.enter(dataFrequency, 1, dataGenerator, (s,))
            s.run()
            controlFans()

    except KeyboardInterrupt:
        print("Interrupt signal sent")

if __name__ == "__main__":
    main()