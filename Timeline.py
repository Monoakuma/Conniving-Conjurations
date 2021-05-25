import PyQt5
import sys
import random
import math
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import Qt

PointItem = QtWidgets.QGraphicsPixmapItem
Mosaic = QtGui.QPixmap
Brush = QtGui.QBrush
Pen = QtGui.QPen
Color = QtGui.QColor
Stage = QtWidgets.QGraphicsScene
GetRekt = QtWidgets.QGraphicsRectItem
RRR = 15
class Main(QtWidgets.QMainWindow):
    def __init__(self):
        Timeloop = Loop(10)
        super().__init__()
        self.resize(17*65,15*60)
        self.setWindowTitle("[[[ T I M E L I N E ]]]")
        self.Ecosystem = Ecosystem(17*65,15*60,parent=self)
        self.show()
class Ecosystem(QtWidgets.QGraphicsView):
    def __init__(self,w,h,parent=None):
        self.stage = Stage(0, 0, w, h, parent)
        super(Ecosystem, self).__init__(self.stage, parent)
        self.setAlignment(Qt.AlignBaseline)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.horizontalScrollBar().disconnect()
        self.verticalScrollBar().disconnect()
        self.setGeometry(0,0,w,h)
        self.resize(w, h)
        self.setStyleSheet('''
            QWidget{
                background-color: black;
                border-style: outset;
                border-width: 10px;
                border-color: rgb(255,174,50);
            }
        ''')
        self.Food = []
        self.Hunters = []
        self.Herbivores = []
        self.Carnivores = []
        self.dims=w,h
        for food in range(random.randint(5,40)):
            self.Food.append(Food((random.randrange(0,w),random.randrange(0,h))))
            self.stage.addItem(self.Food[food])
            self.Food[food].show()
        for hunter in range(random.randint(1,30)):
            vore = "herbivore"
            if vore == "herbivore":
                self.Herbivores.append(Hunter(vore,self.Food,random.randrange(0,w),random.randrange(0,h)))
                self.Hunters.append(self.Herbivores[-1])
            elif vore == "carnivore":
                self.Carnivores.append(Hunter(vore,self.Herbivores,random.randrange(0,w),random.randrange(0,h)))
                self.Hunters.append(self.Carnivores[-1])
            self.stage.addItem(self.Hunters[hunter])
            self.Hunters[hunter].show()
        self.tick = QtCore.QTimer(self)
        self.tick.timeout.connect(self.timestep)
        self.tick.start(10)
    def timestep(self):
        print(f"Herbivores:{len(self.Herbivores)}| Carnivores:{len(self.Carnivores)}| Food:{len(self.Food)}")
        for hunter in self.Hunters:
            for food in hunter.Food:
                if hunter.xy[0]<=food.xy[0]+RRR and hunter.xy[0]>=food.xy[0] and hunter.xy[1]<=food.xy[1]+RRR and hunter.xy[1]>=food.xy[1]:
                    hunter.food+=5
                    food.food-=5
            hunter.move()
            hunter.food-=1
            if hunter.food>=200:
                if hunter.voretype == "herbivore":
                    self.Herbivores.append(Hunter(hunter.voretype,hunter.Food,hunter.xy[0],hunter.xy[1]))
                    self.Hunters.append(self.Herbivores[-1])
                elif hunter.voretype == "carnivore":
                    self.Carnivores.append(Hunter(hunter.voretype,hunter.Food,hunter.xy[0],hunter.xy[1]))
                    self.Hunters.append(self.Carnivores[-1])
                self.stage.addItem(self.Hunters[-1])
                self.Hunters[-1].show()
            elif hunter.food<=-50:
                self.stage.removeItem(hunter)
                if hunter.voretype == "herbivore":
                    self.Herbivores.remove(hunter)
                elif hunter.voretype == "carnivore":
                    self.Carnivores.remove(hunter)
                self.Hunters.remove(hunter)
        for food in self.Food:
            if food.food<=0:
                self.stage.removeItem(food)
                self.Food.remove(food)
            elif food.food>=100:
                if random.randint(1,100)>95:
                    if len(self.Food)<150:
                        self.Food.append(Food((random.randrange(0,self.dims[0]),random.randrange(0,self.dims[1]))))
                        self.stage.addItem(self.Food[-1])
                        self.Food[-1].show()
                        food.food-=40
                food.food=100
            else:
                food.food+=1
        if random.randint(1,1000)==2: #Mutation
            if len(self.Herbivores)>0:
                mutator = random.choice(self.Herbivores)
                #self.Herbivores.remove(mutator)
                #self.Carnivores.append(mutator)
                #mutator.voretype = "carnivore"
                #mutator.Food = self.Herbivores
class Food(GetRekt):
    def __init__(self, xy):
        super(Food, self).__init__()
        self.xy = xy
        self.food=15
        self.setRect(self.xy[0],self.xy[1],RRR,RRR)
        self.setBrush(Brush(Color(0,255,0)))
class Hunter(GetRekt):
    def __init__(self, vore,food, x,y):
        super(Hunter, self).__init__()
        self.xy = [x,y]
        self.Food = food
        self.food=20
        self.setRect(self.xy[0],self.xy[1],RRR,RRR)
        self.voretype = vore #herbivore/carnivore

    def move(self):
        if self.voretype == "herbivore":
            self.setBrush(Brush(Color(255,0,0)))
        elif self.voretype == "carnivore":
            self.setBrush(Brush(Color(255,0,255)))
        pos = self.xy
        try:
            dest = self.Food[0].xy
            for food in self.Food:
                if math.sqrt((pos[0]-food.xy[0])**2+(pos[1]-food.xy[1])**2)<math.sqrt((pos[0]-dest[0])**2+(pos[1]-dest[1])**2):
                    dest = food.xy
            dist = random.randint(1,10)
            if pos[0]<dest[0]:
                self.xy[0]+=dist
                self.moveBy(+dist,0)
            elif pos[0]>dest[0]:
                self.xy[0]-=dist
                self.moveBy(-dist,0)
            if pos[1]<dest[1]:
                self.xy[1]+=dist
                self.moveBy(0,+dist)
            if pos[1]>dest[1]:
                self.xy[1]-=dist
                self.moveBy(0,-dist)
        except IndexError:
            self.moveBy(random.randrange(-10,10),random.randrange(-10,10))

class Loop():
    """A Loop is a series of events within a length that can be reversed to create small scale time travel.

    Mechanical Theory:
    In a game such as Braid or Life is Strange, the player can reverse time to some extent, but the mechanical limit is how far back.
    The underlying system seems quite simple actually, for every movement you record that movement and then when you want to travel back, you
    read the movements in reverse, until you reach the beginning of the list, at which point you begin recording again."""

    def __init__(self, length):
        self.length = length
        self.timeline = [] #timelines *must* be ordered chronologically.
    def addEvent(self,event):
        self.timeline.append(event)
        if len(self.timeline)>self.length:
            del self.timeline[0]
    def back(self):
        return(self.timeline.pop(-1)) #returns the newest event, allowing for backwards reading of the timeline
if __name__ == '__main__':

    app = QApplication(sys.argv)
    gui = Main()

sys.exit(app.exec_())
