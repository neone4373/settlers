import psycopg2 as pg
from pylab import *
from matplotlib.collections import LineCollection
import time,random,numpy as np
post = { "DB" : 'postgres',
  "User" : 'pybot',
  "Pass": 'pybot',
  "Host": 'localhost',
  "Port": 5432}
"""

"""
class Hexing:

  def __init__(self):
    #As with all good __init__ functions this calls the initial
    # conditions for the class
    self.blankVariables()
    self.randomizeBoard()
    self.resDicts()
    self.hexCoordinates(self.hexSize)
    self.writeKey(self.nodeList)
    self.boardSeed()

  #####################
  # Initial Functions #
  #####################

  def randomizeBoard(self):
    #Sets up a random board, and adds a dictionary for hex 
    # by roll and roll by hex
    self.randMap = [0,1,1,1,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5]
    random.shuffle(self.randMap)
    self.rollDict = {}
    self.hexDict = {2: [0], 3: [0,0], 4: [0,0], 
        5: [0,0], 6: [0,0], 7: [0,0], 8: [0,0], 
        9: [0,0], 10: [0,0], 11: [0,0], 12: [0]}
    fe = 0
    randN = [2,3,3,4,4,5,5,6,6,8,8,9,9,10,10,11,11,12]
    for qq in self.randMap:
      random.shuffle(randN)
      if qq == 0:
        self.rollDict[fe] = 7
        self.hexDict[7] = fe
      else:
        mm = randN.pop()
        self.rollDict[fe] = mm
        if self.hexDict[mm][0] == 0:
          self.hexDict[mm][0] = fe
        else:
          self.hexDict[mm][1] = fe
      fe += 1

  def blankVariables(self):
    #initializes class variables used in multiple functions
    self.hexNames = []
    self.ptList = []
    self.nodeArray = np.zeros((54,6), dtype=int)
    for x in range(self.nodeArray.shape[0]):
      self.nodeArray[x][0] = x + 1
    #print self.nodeArray
    self.nodeList = [
      (1,1,0,0), (2,1,0,0), (3,1,4,0), (4,1,4,5), (5,1,2,5),(6,1,2,0),(7,2,0,0), 
      (8,2,5,6),(9,2,3,6),(10,2,3,0),(11,3,0,0),(12,3,6,7),(13,3,7,0),(14,3,0,0), 
      (15,4,0,0),(16,4,8,0),(17,4,8,9),(18,4,5,9),(19,5,9,10),(20,5,6,10),(21,6,10,11), 
      (22,6,7,11),(23,7,11,12),(24,7,12,0),(25,7,0,0),(26,8,0,0),(27,8,0,0),(28,8,13,0), 
      (29,8,9,13),(30,9,13,14),(31,9,10,14),(32,10,14,15),(33,10,11,15),(34,11,15,16), 
      (35,11,12,16),(36,12,16,0),(37,12,0,0),(38,12,0,0),(39,13,0,0),(40,13,17,0), 
      (41,13,14,17),(42,14,17,18),(43,14,15,18),(44,15,18,19),(45,15,16,19),(46,16,19,0), 
      (47,16,0,0),(48,17,0,0),(49,17,0,0),(50,17,18,0),(51,18,0,0),(52,18,19,0),
      (53,19,0,0), (54,19,0,0)        
      ]
    self.nodeKey = np.zeros((54,4), dtype=int)
    self.hexSize = 80
    self.seed = []
    self.rolls = []
    self.topNodes = []

  def resDicts(self):
    #Dictionaries for the resources
    self.resDct = {0:'desert',1:'brick',2:'wheat',3:'sheep',4:'wood',5:'rock'}
    self.resCDct = {0:'yellow',1:'red',2:'orange',3:'gray',4:'green',5:'black'}
    #print self.hexDict; print self.rollDict
    
  def hexCoordinates(self,hexSize):
    #This names and routes the coordinates for 19 hexes to self.hexName
    xMargin = hexSize
    xOffset = hexSize * (.75)
    yOffset = hexSize/2
    t = hexSize/2
    for i in range(19):
      if i < 3:
        self.hexNames += [[
          i+1,
          (xOffset * 0 + xMargin, yOffset + hexSize+hexSize*i),
          hexSize,
          (xOffset * 0 + xMargin + t, yOffset + hexSize+hexSize*i + t)
          ]]
      elif i < 7:
        self.hexNames += [[
          i+1,
          (xOffset * 1 + xMargin, yOffset + hexSize/2 + hexSize*(i-3)),
          hexSize,
          (xOffset * 1 + t + xMargin, yOffset + hexSize/2 + hexSize*(i-3) + t)]]
      elif i < 12:
        self.hexNames += [[
          i+1,
          (xOffset * 2 + xMargin, yOffset + hexSize*(i-7)),
          hexSize,
          (xOffset * 2 + t + xMargin, yOffset + hexSize*(i-7) + t)]]
      elif i < 16:
        self.hexNames += [[
          i+1,
          (xOffset * 3 + xMargin, yOffset + hexSize/2 + hexSize*(i-12)),
          hexSize,
          (xOffset * 3 + t + xMargin, yOffset + hexSize/2 + hexSize*(i-12) + t)]]
      elif i < 19:
        self.hexNames += [[
          i+1,
          (xOffset * 4 + xMargin, yOffset + hexSize+hexSize*(i-16)),
          hexSize,
          (xOffset * 4 + t + xMargin, yOffset + hexSize+hexSize*(i-16) + t)]]
      else:
        pass

  def writeKey(self,nK):
    a = 0
    for x in nK:
      b = 0
      for y in x:
        self.nodeKey[a][b] = y
        b += 1
      a += 1
    #print "nodeKey",x,y; print self.nodeKey

  def boardSeed(self):
    for rr in range(19):
      self.seed += [(rr+1,self.randMap[rr],self.resDct[self.randMap[rr]],self.rollDict[rr])]


  ##################
  #Active Functions#
  ##################

  def hexIt(self,h):
    #this function is used to set the points for each hex for drawing purposes
    name = h[0]
    origin = h[1]
    size = h[2]
    oneseg = size/4
    twoseg = oneseg*2	# same as size/2

    # Get the x and y from the tuple
    orgx = origin[0]
    orgy = origin[1]
    
    # Create a new one
    return  [[ 
    (orgx, orgy + twoseg),
    (orgx + oneseg, orgy),
    (orgx + oneseg + twoseg, orgy),
    (orgx + size , orgy + twoseg),
    (orgx + oneseg + twoseg, orgy + size),
    (orgx + oneseg, orgy + size),
    (orgx, orgy + twoseg)]]

  def drawHexs(self,hn, mp = []):
    #As the name suggest this function draws and labels the board
    # and hexes.
    x = arange(len(hn))
    if mp == []:
      mp = self.randMap
    # We need to set the plot limits, they will not autoscale
    fig=Figure() 
    '''can=FigureCanvasBase(fig)
    can.set_window_title("Figure?")
    fig.set_canvas(can)'''
    fig.set_size_inches(12,9,forward=False)
    ax = axes()
    #ax.set_figure(fig)
    ax.set_xlim((0,6 * self.hexSize))
    ax.set_ylim((0,6 * self.hexSize))
    pid=1
    spaceList = []
    for z in hn:
      for pts in self.hexIt(z)[0]:
        if pts not in spaceList:
          spaceList += [pts]
          self.ptList += [(pid,pts)]
          propP = dict( alpha=0.25, color='blue' )
          propH = dict( alpha=0.25, color='grey' )
          propL = dict( alpha=0.5, color=self.resCDct[mp[z[0]-1]])
          ax.text(pts[0],pts[1],str(pid),
            horizontalalignment='center',
            verticalalignment='center',
            **propP
            )   
          #print pid,self.nodeArray[pid-1][0]
          for xx in [1,2,3,4,5]:
            h = self.hexSize
            wt = h/20
            lft = pts[0] + xx * wt - h/4
            bt = pts[1]-wt
            htV = self.nodeArray[pid-1][xx]
            #print htV,len(self.rolls)
            ht = round((h*(3./4))*(float(htV)/len(self.rolls)))
            propB = dict( alpha=0.5,color = self.resCDct[xx])
            #print "pid,xx,node"
            #print pid,xx,
            ax.bar(left=lft,
              bottom=bt,
              height=ht,
              width=wt,
              #align='center',
              linewidth = 0,
              **propB)
          pid += 1
      # colors is sequence of rgba tuples
      # linestyle is a string or dash tuple. Legal string values are
      #          solid|dashed|dashdot|dotted.  The dash tuple is (offset, onoffseq)
      #          where onoffseq is an even length tuple of on and off ink in points.
      #          If linestyle is omitted, 'solid' is used
      # See matplotlib.collections.LineCollection for more information
      line_segments = LineCollection(self.hexIt(z), # Make a sequence of x,y pairs
                                      linewidths    = (0.5,1,1.5),
                                      linestyles = 'solid',
                                      **propH)
      line_segments.set_array(x)
      ax.add_collection(line_segments)
      #print z[0], self.randMap[z[0]-1]
      #prints the hex label
      text = self.resDct[mp[z[0]-1]]+"\n"+str(self.rollDict[z[0]-1])
      ax.text(z[3][0],z[3][1],text,
          horizontalalignment='center',
          verticalalignment='center',
          **propL)  

    #fig = gcf()
    #axcb = fig.colorbar(line_segments)
    self.drawHist(ax,self.rolls,self.hexSize)
    self.drawTop(ax,self.hexSize,self.topNodes,10,self.nodeKey)
    ax.set_title('Resource Distribution After '+str(len(self.rolls))+' Rolls')
    sci(line_segments) # This allows interactive changing of the colormap.'''
    show()
    raw_input("Press enter to continue")
    close()
    #for kk in self.ptList:
    #  print kk[1]

  def drawHist(self,a,r,h):
    propBar = dict( alpha=0.5,color = 'blue')
    propText = dict( alpha=0.5,color = 'black',size=8)
    propTitle = dict( alpha=0.5,color = 'black',size=10)
    bt = h/4
    l = 6*h*(5./8)
    wt = h/5
    a.text(l+wt*5,bt+h/2,'Roll Distribution %',
      horizontalalignment='center',
      verticalalignment='bottom',
        **propTitle)
    for zz in [2,3,4,5,6,7,8,9,10,11,12]:  
      lft = l + (zz-2)*(wt)
      N = r.count(zz)
      ht = 50*(N / float(len(r)/2))
      txt = str(100*N / len(r))
      a.bar(left=lft,bottom=bt,
        height=ht,width=wt,
        align='center',
        linewidth = 0,
        **propBar)
      a.text(lft,ht+bt+h/20,txt,
        horizontalalignment='center',
        verticalalignment='bottom',
        **propText)
      a.text(lft,bt - h/40,zz,
        horizontalalignment='center',
        verticalalignment='top',
        **propText)

  def drawTop(self,a,h,l,n,k):
    propText = dict( alpha=0.5,color = 'black',size=8)
    propTitle1 = dict( alpha=0.5,color = 'blue',size=10)
    propTitle2 = dict( alpha=0.5,color = 'green',size=8)
    bt = h*6 - h/20
    lft = h/8
    txt1 = "Top " + str(n) + " Nodes"
    txt2 = "Rolls Node Numbers"
    a.text(lft,bt,txt1,
      horizontalalignment='left',
      verticalalignment='top',
      **propTitle1)
    a.text(lft,bt-h*(3./16),txt2,
      horizontalalignment='left',
      verticalalignment='top',
      **propTitle2)
    #print l
    #print self.rollDict
    for c in range(n):
      dn = (c + 1) * (h/8) + h/4
      o = h/20
      t = h*(9./32) 
      l1 = lft + o
      l2 = lft + o + t 
      l3 = lft + o + 2 * t
      a.text(l1,bt - dn,str(l[c][0]),
        horizontalalignment='left',
        verticalalignment='top',
        **propText)
      a.text(l2,bt - dn,str(l[c][1]),
        horizontalalignment='left',
        verticalalignment='top',
        **propText)
      nPair = ""
      #print l[c][1],k
      for q in k[l[c][1]-1,1:]:
        #print q, self.rollDict[q-1]
        if q > 0:
          nPair += str(self.rollDict[q-1]) + " "
      a.text(l3,bt - dn,str(nPair),
        horizontalalignment='left',
        verticalalignment='top',
        **propText)

  def writeNode(self,lst):
    #This fuction writes the node table to the settlers schema
    # Connect to an existing database
    conn = pg.connect(
        "dbname=" + post["DB"] + " user=" + post["User"] + " password=" + post["Pass"])

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Execute a command: this creates a new table
    cur.execute("drop table if exists settlers.node;")


    # Execute a command: this creates a new table
    cur.execute(
        "CREATE TABLE settlers.node (id serial PRIMARY KEY, x_coordinate integer, y_coordinate integer);")

    # Pass data to fill a query placeholders and let Psycopg perform
    # the correct conversion (no more SQL injections!)
    for j in lst:
      cur.execute(
          "INSERT INTO settlers.node (x_coordinate , y_coordinate) VALUES (%s, %s)",j[1])

    # Query the database and obtain data as Python objects
    cur.execute("SELECT * FROM settlers.node;")
    print cur.fetchone()
    #Out: (1, 100, "abc'def")

    # Make the changes to the database persistent
    conn.commit()

    # Close communication with the database
    cur.close() 
    conn.close()

  def writeAdjHex(self):
    #This writes the adjhex table to the settlers database
    nodeKey = self.nodeKey
    '''    [
        (1,1,0,0), (2,1,0,0), (3,1,4,0), (4,1,4,5), (5,1,2,5),(6,1,2,0),(7,2,0,0),
        (8,2,5,6),(9,2,3,6),(10,2,3,0),(11,3,0,0),(12,3,6,7),(13,3,7,0),(14,3,0,0),
        (15,4,0,0),(16,4,8,0),(17,4,8,9),(18,4,5,9),(19,5,9,10),(20,5,6,10),(21,6,10,11),
        (22,6,7,11),(23,7,11,12),(24,7,12,0),(25,7,0,0),(26,8,0,0),(27,8,0,0),(28,8,13,0),
        (29,8,9,13),(30,9,13,14),(31,9,10,14),(32,10,14,15),(33,10,11,15),(34,11,15,16),
        (35,11,12,16),(36,12,16,0),(37,12,0,0),(38,12,0,0),(39,13,0,0),(40,13,17,0),
        (41,13,14,17),(42,14,17,18),(43,14,15,18),(44,15,18,19),(45,15,16,19),(46,16,19,0),
        (47,16,0,0),(48,17,0,0),(49,17,0,0),(50,17,18,0),(51,18,0,0)(52,18,19,0),(53,19,0,0),
        (54,19,0,0)        
      ]'''
    '''for jj in nodeKey:
      print jj'''

    conn = pg.connect(
        "dbname=" + post["DB"] + " user=" + post["User"] + " password=" + post["Pass"])
    cur = conn.cursor()
    cur.execute("drop table if exists settlers.adjhex;")

    cur.execute(
        "CREATE TABLE settlers.adjhex (id serial PRIMARY KEY, node_id integer, hex_id1 integer, hex_id2 integer, hex_id3 integer);")

    for j in nodeKey:
      cur.execute(
          "INSERT INTO settlers.adjhex (node_id, hex_id1, hex_id2, hex_id3) VALUES (%s, %s, %s, %s)",j)

    cur.execute("SELECT * FROM settlers.adjhex;")
    print cur.fetchone()
    conn.commit()
    cur.close() 
    conn.close()

  def fetchMapPG(self):
    #Pulls the adjhex table from the database and saves it as a list
    conn = pg.connect(
        "dbname=" + post["DB"] + " user=" + post["User"] + " password=" + post["Pass"])
    cur = conn.cursor()
    cur.execute("SELECT * FROM settlers.adjhex")
    self.writeMap(cur.fetchall())
    #print self.nodeKey
    #print type(self.nodeKey), self.nodeKey
    cur.close()
    conn.close()

  def randDices(self):
    #A simple die fucntion returns the sum of two fair 6-sided dice
    die = [1,2,3,4,5,6]
    return float(random.choice(die)+random.choice(die))

  def roll(self,N):
    #This fucntion acts to tell the program what resources are 
    # added where when dice are rolled
    times = 0
    #print self.nodeKey
    #print self.rollDict
    #print self.hexDict
    while times < N:
      dice = self.randDices()
      #print times,dice,rolls
      self.rolls += [int(dice)]
      ndKey = self.nodeKey[:,1:]
      #print ndKey
      #print "roll",dice; print "hex",ff.hexDict[dice]; 
      #print "resource",ff.resDct[ff.randMap[ff.hexDict[dice][0]]],ff.resDct[ff.randMap[ff.hexDict[dice][1]]]
      a1,a2 = [],[]
      if dice in (2,12):
        a = np.where(ndKey == ff.hexDict[dice][0]+1)[0]
        b = [ff.randMap[ff.hexDict[dice][0]]] * 6
      elif dice == 7:
        a = []
        b = []
      else:
        a1 = np.where(ndKey == ff.hexDict[dice][0]+1)[0]
        a2 = np.where(ndKey == ff.hexDict[dice][1]+1)[0]
        a = np.hstack((a1,a2))
        b = [ff.randMap[ff.hexDict[dice][0]]] * 6 + [ff.randMap[ff.hexDict[dice][1]]] * 6

      #print dice,a,"a1,a2",len(a1),len(a2),a1,a2; #print a[0]; 
      #print ff.hexDict[dice]
      for ll in range(len(a)):
        #print ndKey[a[ll]][0],b[ll]
        self.nodeArray[a[ll]][b[ll]] += 1
      times += 1
    
    #print "rolls", len(self.rolls); print self.rolls


  def printSeed(self,s):
    print "hex rN type roll"
    for zz in s:
      print zz

  def printResults(self,r):
    print "node br wh sh wd rk";print r

  def nodeRank(self,node):
    for x in node:
      self.topNodes += [(np.sum(x[1:]),x[0])]
      self.topNodes.sort(reverse=True)
    #print self.topNodes
    #print node

ff = Hexing()
ff.printSeed(ff.seed)
ff.roll(200)
#ff.printResults(ff.nodeArray)
ff.nodeRank(ff.nodeArray)
ff.drawHexs(ff.hexNames)



#ff.writeKey()
#for tt in range(10):
#  print(ff.randDice())
#print ff.hexNames
#print ff.hexIt(ff.hexNames[0])
#ff.writeAdjHex()

#print ff.ptList 
#ff.writeNode(ff.ptList)



'''

'''
