import matplotlib.pyplot as plt
import matplotlib.animation as animation
import csv

plt.style.use('ggplot')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)

def animate(i):
    with open('output.csv', 'r') as csvFile:
        csvReader = csv.DictReader(csvFile)
        line_count = 0
        xar = []
        yar = []
        zar = []
        for row in csvReader: 
            if line_count == 0:
                line_count+=1
            x = f'{row["% Speed Adjusted"]}'
            y = f'{row["Max Subsystems Temp"]}'
            z = f'{row["Time"]}' #Added this to plot speed and temperature over time
            yar.append(float(y))
            xar.append(float(x))
            zar.append(z)
            
        ax1.clear()
        ax1.plot(xar,yar, 'o')
        plt.xlabel('Adjusted % Speed')
        plt.ylabel('Max Subsystems Temp recorded')
        plt.title('Subsystem Temperature VS Adjusted % Speed')
        csvFile.close()
ani = animation.FuncAnimation(fig, animate, interval=3000)
plt.show()