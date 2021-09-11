import math

class Point:
    def __init__(self, x, y):
            self.x = x
            self.y = y


class Line:
    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint

    #線分の長さを返す
    def getLength(self):
        return ((self.startPoint.x - self.endPoint.x)**2 + (self.startPoint.y - self.endPoint.y)**2)**0.5
    
    #線分の傾きを返す
    def getSlope(self):
        if self.startPoint.x - self.endPoint.x==0:
            return None
        return (self.startPoint.y - self.endPoint.y)/(self.startPoint.x - self.endPoint.x)


class QuadrilateralShape:
    def __init__(self, lineAB, lineBC, lineCD, lineDA):
        self.lineAB = lineAB
        self.lineBC = lineBC
        self.lineCD = lineCD
        self.lineDA = lineDA
    
    #四角形の名称を返す
    def getShapeType(self):
        if not self.isQuadrangle():
            return "not a quadrilateral"  
        elif self.lineAB.getLength()==self.lineBC.getLength()==self.lineCD.getLength()==self.lineDA.getLength():
            if self.getAngle("BAD")==90:
                return "square（正方形）"
            else:
                return "rhombus（ひし形）"
        elif self.lineAB.getLength()==self.lineCD.getLength() and self.lineBC.getLength()==self.lineDA.getLength():
            if self.getAngle("BAD")==90:
                return "rectangle（長方形）"
            elif self.isInner360():
                return "parallelogram（平行四辺形）"
        elif (self.getAngle("BAD")+self.getAngle("ABC")==180 or self.getAngle("ABC")+self.getAngle("BCD")==180) and self.isInner360():
            return "trapezoid（台形）"
        elif (self.lineAB.getLength()==self.lineBC.getLength() and self.lineCD.getLength()==self.lineDA.getLength()) or (self.lineBC.getLength()==self.lineCD.getLength() and self.lineDA.getLength()==self.lineAB.getLength()):
            return "kite（凧）"
        return "other（その他）"
    
    #図形が四角形か判断
    def isQuadrangle(self):
        if self.lineAB.getLength()==0 or self.lineBC.getLength()==0 or self.lineCD.getLength()==0 or self.lineDA.getLength()==0:
             return False
        elif self.getAngle("BAD")==0 or self.getAngle("ABC")==0 or self.getAngle("BCD")==0 or self.getAngle("CDA")==0 or self.getAngle("BAD")==180 or self.getAngle("ABC")==180 or self.getAngle("BCD")==180 or self.getAngle("CDA")==180: 
            return False
        return True
    
    #四角形の内角が360度か判断
    def isInner360(self):
        return self.getAngle("BAD")+self.getAngle("ABC")+self.getAngle("BCD")+self.getAngle("CDA")==360
 
    #四角形の周囲の長さを返す
    def getPerimeter(self):
        return round(self.lineAB.getLength() + self.lineBC.getLength() + self.lineCD.getLength() + self.lineDA.getLength(), 2)

    #四角形の面積を返す
    def getArea(self):
        if self.isInner360():
            triangleABC=self.lineAB.getLength() * self.lineBC.getLength() * math.sin(math.radians(self.getAngle("ABC"))) / 2
            triangleCDA=self.lineCD.getLength() * self.lineDA.getLength() * math.sin(math.radians(self.getAngle("ADC"))) / 2
            return round(triangleABC+triangleCDA, 2)
        else:
            return None

    #BAD、ABC、ADC、BCDの角度を返す
    def getAngle(self, angleString):
        if angleString=="BAD" or angleString=="DAB":
            degree = self.getDegree(self.lineAB.endPoint.x, self.lineAB.endPoint.y, self.lineDA.endPoint.x, self.lineDA.endPoint.y, self.lineCD.endPoint.x, self.lineCD.endPoint.y)
        elif angleString=="ABC" or angleString=="CBA":
            degree = self.getDegree(self.lineDA.endPoint.x, self.lineDA.endPoint.y, self.lineAB.endPoint.x, self.lineAB.endPoint.y, self.lineBC.endPoint.x, self.lineBC.endPoint.y)
        elif angleString=="BCD" or angleString=="DCB":
            degree = self.getDegree(self.lineAB.endPoint.x, self.lineAB.endPoint.y, self.lineBC.endPoint.x, self.lineBC.endPoint.y, self.lineCD.endPoint.x, self.lineCD.endPoint.y)
        elif angleString=="ADC" or angleString=="CDA":
            degree = self.getDegree(self.lineDA.endPoint.x, self.lineDA.endPoint.y, self.lineCD.endPoint.x, self.lineCD.endPoint.y, self.lineBC.endPoint.x, self.lineBC.endPoint.y)
        else:
            print("未定義です")
            degree = None
        return degree

    #3点の角度を返す
    def getDegree(self, x1, y1, x2Base, y2Base, x3, y3):
        innerProduct=(x1 - x2Base)*(x3 - x2Base) + (y1 - y2Base)*(y3 - y2Base)
        vec21Length = math.sqrt((x1 - x2Base)**2 + (y1 - y2Base)**2)
        vec23Length = math.sqrt((x3 - x2Base)**2 + (y3 - y2Base)**2)
        if vec21Length==0 or vec23Length==0:
            return None
        cos = innerProduct/(vec21Length*vec23Length)
        return round(math.degrees(math.acos(cos)), 3)

    #四角形を描写、(座標が整数、内角が45°、90°、135°のいずれかの時に描写可能)
    def draw(self):
        #----------------------描写ツール------------------------
        #マップを生成
        def createMap(lineList):
            height = max(lineList[0].endPoint.y, lineList[1].endPoint.y, lineList[2].endPoint.y, lineList[3].endPoint.y) + 2
            width = max(lineList[0].endPoint.x, lineList[1].endPoint.x, lineList[2].endPoint.x, lineList[3].endPoint.x) + 2
            Map=[["　　"]*width for y in range(height)]
            return Map

        #第1象限に平行移動
        def moveQuadrant1(lineList):
            yMin=min(lineList[0].endPoint.y, lineList[1].endPoint.y, lineList[2].endPoint.y, lineList[3].endPoint.y)
            xMin=min(lineList[0].endPoint.x, lineList[1].endPoint.x, lineList[2].endPoint.x, lineList[3].endPoint.x)
            if yMin<0:
                for index in range(0,len(lineList)):
                    lineList[index].startPoint.y+=abs(yMin)
                    lineList[index].endPoint.y+=abs(yMin)
            if xMin<0:
                for index in range(0,len(lineList)):
                    lineList[index].startPoint.x+=abs(xMin)
                    lineList[index].endPoint.x+=abs(xMin)
            return lineList
        
        #線分の傾きから特定の辺に置き換える
        def changeToSides(line, Map):
            startX = min(line.startPoint.x, line.endPoint.x) + 1
            startY = min(line.startPoint.y, line.endPoint.y) + 1
            endX = max(line.startPoint.x, line.endPoint.x) + 1
            endY = max(line.startPoint.y, line.endPoint.y) + 1
            if line.getSlope()==0:
                for x in range(startX, endX):
                    if len(Map)-2==line.startPoint.y:
                        Map[line.startPoint.y + 1][x]="﹍　"
                    else:
                        Map[line.startPoint.y][x]="﹉　"
            elif line.getSlope()==None:
                for y in range(startY, endY):
                    if len(Map[0])-2==line.startPoint.x:
                        Map[y][line.startPoint.x + 1]="｜　"
                    else:
                        Map[y][line.startPoint.x]="｜　"
            elif line.getSlope()==1:
                moveX=0
                for y in range(startY,endY):
                    Map[y][startX + moveX]="／　"
                    moveX+=1       
            elif line.getSlope()==-1:
                startX = max(line.startPoint.x, line.endPoint.x)
                endX = min(line.startPoint.x, line.endPoint.x)
                moveX=0
                for y in range(startY,endY):
                    Map[y][startX + moveX]="＼　"
                    moveX-=1
            return Map
        
        #マップを表示、(Map[y][x]は第1象限の(x,y)と対応)
        def printMap(Map):
            for MapY in reversed(Map):
                for MapX in MapY:
                    print(MapX, end="")
                print()
        
        #図形が描写に対応しているか判断
        def canPrintMap():
            if self.getShapeType()=="not a quadrilateral":
                return False
            for line in [self.lineAB, self.lineBC, self.lineCD, self.lineDA]:
                if line.getSlope()!=0 and line.getSlope()!=-1 and line.getSlope()!=1 and line.getSlope()!=None:
                    return False
                elif line.endPoint.x%1!=0 or line.endPoint.y%1!=0:
                    return False
            return True
        #---------------------------------------------------------

        #---ここから本処理---
        if canPrintMap():
            lineList=moveQuadrant1([self.lineAB, self.lineBC, self.lineCD, self.lineDA])
            Map=createMap(lineList)
            for line in lineList:
                Map=changeToSides(line, Map)
            printMap(Map)
        else:
            print("この図形は描写に非対応です")
  
    #四角形の情報を全て表示
    def printAllInfo(self):
        print("図形：" + self.getShapeType())
        if self.getShapeType()=="not a quadrilateral":
            print("四角形ではないため、情報は表示できません")
        else:
            print("面積：" + str(self.getArea()) + "\n"+
                  "周囲の長さ：" + str(self.getPerimeter()) + "\n"+
                  "角BAD：" + str(self.getAngle("BAD")) + "°　" + "角ABC：" + str(self.getAngle("ABC")) + "°\n"+
                  "角BCD：" + str(self.getAngle("BCD")) + "°　" + "角ADC：" + str(self.getAngle("ADC")) + "°")
            self.draw()
        print()


# テストケース
# square（正方形）
# 　　﹍　﹍　﹍　﹍　　
# ｜　　　　　　　　　｜
# ｜　　　　　　　　　｜
# ｜　　　　　　　　　｜
# ｜　　　　　　　　　｜
# 　　﹉　﹉　﹉　﹉　　
lineAB = Line(Point(0,0), Point(4,0))
lineBC = Line(Point(4,0), Point(4,4))
lineCD = Line(Point(4,4), Point(0,4))
lineDA = Line(Point(0,4), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# square（正方形）
# 　　﹍　﹍　﹍　﹍　﹍　　　
# ｜　　　　　　　　　　　｜
# ｜　　　　　　　　　　　｜
# ｜　　　　　　　　　　　｜
# ｜　　　　　　　　　　　｜
# ｜　　　　　　　　　　　｜
# 　　﹉　﹉　﹉　﹉　﹉　　　
lineAB = Line(Point(0,0), Point(-5,0))
lineBC = Line(Point(-5,0), Point(-5,-5))
lineCD = Line(Point(-5,-5), Point(0,-5))
lineDA = Line(Point(0,-5), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# square（正方形）
# 　　　　／　＼　　　　　
# 　　／　　　　　＼　　　
# 　　＼　　　　　／　　　
# 　　　　＼　／　　　　　
lineAB = Line(Point(2,0), Point(4,2))
lineBC = Line(Point(4,2), Point(2,4))
lineCD = Line(Point(2,4), Point(0,2))
lineDA = Line(Point(0,2), Point(2,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# rectangle（長方形）
# 　　﹍　﹍　﹍　﹍　﹍　
# ｜　　　　　　　　　　　｜
# ｜　　　　　　　　　　　｜
# ｜　　　　　　　　　　　｜
# 　　﹉　﹉　﹉　﹉　﹉　
lineAB = Line(Point(0,0), Point(5,0))
lineBC = Line(Point(5,0), Point(5,3))
lineCD = Line(Point(5,3), Point(0,3))
lineDA = Line(Point(0,3), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# rectangle（長方形）
# 　　　　／　＼　　　　　　　
# 　　／　　　　　＼　　　　　
# 　　＼　　　　　　　＼　　　
# 　　　　＼　　　　　　　＼　
# 　　　　　　＼　　　　　／　
# 　　　　　　　　＼　／　　　　
lineAB = Line(Point(0,4), Point(4,0))
lineBC = Line(Point(4,0), Point(6,2))
lineCD = Line(Point(6,2), Point(2,6))
lineDA = Line(Point(2,6), Point(0,4))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# rhombus（ひし形）
lineAB = Line(Point(0,0), Point(5,0))
lineBC = Line(Point(5,0), Point(8,4))
lineCD = Line(Point(8,4), Point(3,4))
lineDA = Line(Point(3,4), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# parallelogram(平行四辺形)
# 　　　　　　﹍　﹍　﹍　﹍　　
# 　　　　／　　　　　　　／　　
# 　　／　　　　　　　／　　　　
# 　　﹉　﹉　﹉　﹉　　
lineAB = Line(Point(0,0), Point(4,0))
lineBC = Line(Point(4,0), Point(6,2))
lineCD = Line(Point(6,2), Point(2,2))
lineDA = Line(Point(2,2), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# parallelogram(平行四辺形)
# 　　　　　　　
# 　　　　／　｜
# 　　／　　　｜
# ｜　　　　　｜
# ｜　　　　　｜
# ｜　　　／　　
# ｜　／　
lineAB = Line(Point(0,0), Point(2,2))
lineBC = Line(Point(2,2), Point(2,6))
lineCD = Line(Point(2,6), Point(0,4))
lineDA = Line(Point(0,4), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# trapezoid(台形)
# 　　　　　　﹍　﹍　　　　　　
# 　　　　／　　　　　＼　　　　
# 　　／　　　　　　　　　＼　　
# 　　﹉　﹉　﹉　﹉　﹉　﹉　　
lineAB = Line(Point(0,0), Point(6,0))
lineBC = Line(Point(6,0), Point(4,2))
lineCD = Line(Point(4,2), Point(2,2))
lineDA = Line(Point(2,2), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# trapezoid(台形)
# 　　　　　　　　／　｜
# 　　　　　　／　　　｜　　
# 　　　　／　　　／　　　　　
# 　　／　　　／　　　　　　　
# 　　﹉　﹉　
lineAB = Line(Point(0,0), Point(2,0))
lineBC = Line(Point(2,0), Point(4,2))
lineCD = Line(Point(4,2), Point(4,4))
lineDA = Line(Point(4,4), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# trapezoid(台形)
# 　　﹍　﹍　　　　　　
# ｜　　　　　＼　　　　
# ｜　　　　　　　＼　　
# 　　﹉　﹉　﹉　﹉　　
lineAB = Line(Point(0,0), Point(4,0))
lineBC = Line(Point(4,0), Point(2,2))
lineCD = Line(Point(2,2), Point(0,2))
lineDA = Line(Point(0,2), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# trapezoid(台形)
# 　　　　　　　　／｜
# 　　　　　　／　　｜
# 　　　　／　　　　｜
# 　　／　　　　　　｜
# 　　＼　　　　　／　 
# 　　　　＼　／　　　　
lineAB = Line(Point(2,0), Point(4,2))
lineBC = Line(Point(4,2), Point(4,6))
lineCD = Line(Point(4,6), Point(0,2))
lineDA = Line(Point(0,2), Point(2,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# kite（凧）
lineAB = Line(Point(2,0), Point(5,2))
lineBC = Line(Point(5,2), Point(2,4))
lineCD = Line(Point(2,4), Point(0,2))
lineDA = Line(Point(0,2), Point(2,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# other（その他）
lineAB = Line(Point(0,0), Point(4,2))
lineBC = Line(Point(4,2), Point(6,5))
lineCD = Line(Point(6,5), Point(2,2))
lineDA = Line(Point(2,2), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# other（その他）
# ｜　＼　　　　　／　｜　
# ｜　　　＼　／　　　｜　
# ｜　　　／　＼　　　｜　
# ｜　／　　　　　＼　｜　
lineAB = Line(Point(0,0), Point(4,4))
lineBC = Line(Point(4,4), Point(4,0))
lineCD = Line(Point(4,0), Point(0,4))
lineDA = Line(Point(0,4), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# other（その他）
# 　　　　　　　　　　／　｜　
# ｜　＼　　　　　／　　　｜　
# ｜　　　＼　／　　　　　｜　
# ｜　　　／　＼　　　　　｜　
# ｜　／　　　　　＼　　　｜　
# 　　　　　　　　　　＼　｜　
lineAB = Line(Point(0,1), Point(5,6))
lineBC = Line(Point(5,6), Point(5,0))
lineCD = Line(Point(5,0), Point(0,5))
lineDA = Line(Point(0,5), Point(0,1))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# not a quadrilateral
lineAB = Line(Point(0,0), Point(0,1))
lineBC = Line(Point(0,1), Point(1,1))
lineCD = Line(Point(1,1), Point(0,0))
lineDA = Line(Point(0,0), Point(0,0))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()

# not a quadrilateral
lineAB = Line(Point(1,1), Point(2,2))
lineBC = Line(Point(2,2), Point(3,3))
lineCD = Line(Point(3,3), Point(4,4))
lineDA = Line(Point(4,4), Point(1,1))
quadrilateral = QuadrilateralShape(lineAB, lineBC, lineCD, lineDA)
quadrilateral.printAllInfo()