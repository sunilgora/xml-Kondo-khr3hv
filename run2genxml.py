import xml.etree.ElementTree as ET
import copy
import numpy as np
class Pos:
  def __init__(self, posdata):
    Name, GUID, X, Y, Width, Height, Text, BackColorText, MotionFlag, BaseName, Description, Group, ConnectedGuids, ConnectTypes, Motion, Hint = posdata
    self.Name = Name
    self.GUID = GUID
    self.X = X
    self.Y = Y
    self.Width = Width
    self.Height = Height
    self.Text = Text
    self.BackColorText = BackColorText
    self.MotionFlag = MotionFlag
    self.BaseName = BaseName
    self.Description = Description
    self.Group = Group
    self.ConnectedGuids = ConnectedGuids
    self.ConnectTypes = ConnectTypes
    self.Motion = Motion
    self.Hint = Hint

class Lin:
  def __init__(self, lindata):
    GUID, X1, Y1, X2, Y2, ConnectMode= lindata
    self.GUID = GUID
    self.X1 = X1
    self.Y1 = Y1
    self.X2 = X2
    self.Y2 = Y2
    self.ConnectMode = ConnectMode

def postag(myroot,pos): #pos = [Name, GUID, X, Y, ]
    Activity=myroot.find("Activities")
    ActivityData=ET.SubElement(Activity,"anyType")
    ActivityData.set('xsi:type',"ActivityData")
    Name=ET.SubElement(ActivityData,"Name")
    Name.text=f"{pos.Name}"
    GUID=ET.SubElement(ActivityData,"GUID")
    GUID.text=f"{pos.GUID}"
    Location=ET.SubElement(ActivityData,"Location")
    X=ET.SubElement(Location,"X")
    X.text=f"{pos.X}"
    Y=ET.SubElement(Location,"Y")
    Y.text=f"{pos.Y}"
    Size=ET.SubElement(ActivityData,"Size")
    Width=ET.SubElement(Size,"Width")
    Width.text=f"{pos.Width}"
    Height=ET.SubElement(Size,"Height")
    Height.text=f"{pos.Height}"
    Text=ET.SubElement(ActivityData,"Text")
    Text.text=f"{pos.Text}"
    BackColorText = ET.SubElement(Activity, "BackColorText")
    BackColorText.text = f"{pos.BackColorText}"
    MotionFlag=ET.SubElement(ActivityData,"MotionFlag")
    MotionFlag.text=f"{pos.MotionFlag}"
    BaseName=ET.SubElement(ActivityData,"BaseName")
    BaseName.text=f"{pos.BaseName}"
    Description=ET.SubElement(ActivityData,"Description")
    Description.text=f"{pos.Description}"
    Group=ET.SubElement(ActivityData, "Group")
    Group.text = f"{pos.Group}"
    ConnectedGuids=ET.SubElement(ActivityData, "ConnectedGuids")
    ConnectedGuids.text = f"{pos.ConnectedGuids}"
    ConnectTypes=ET.SubElement(ActivityData, "ConnectTypes")
    ConnectTypes.text = f"{pos.ConnectTypes}"
    ProgramCode=ET.SubElement(ActivityData,"ProgramCode")
    Motion=ET.SubElement(ProgramCode,"anyType")
    Motion.set('xsi:type',"xsd:string")
    Motion.text=f"{pos.Motion}"
    Hint=ET.SubElement(ActivityData,"Hint")
    Hint.text=f"{pos.Hint}"
    return myroot

def linetag(myroot,lin): #lin = [GUID, X1, Y1, X2,Y2]
    Line=myroot.find("Lines")
    LineData=ET.SubElement(Line,"anyType")
    LineData.set('xsi:type',"LineData")
    GUID=ET.SubElement(LineData,"GUID")
    GUID.text=f"{lin.GUID}"
    Path=ET.SubElement(LineData,"Path")
    Point1=ET.SubElement(Path,"Point")
    X1=ET.SubElement(Point1,"X")
    X1.text=f"{lin.X1}"
    Y1=ET.SubElement(Point1,"Y")
    Y1.text=f"{lin.Y1}"
    Point2 = ET.SubElement(Path, "Point")
    X2 = ET.SubElement(Point2, "X")
    X2.text = f"{lin.X2}"
    Y2 = ET.SubElement(Point2, "Y")
    Y2.text = f"{lin.Y2}"
    ConnectMode=ET.SubElement(LineData, "ConnectMode")
    ConnectMode.text = f"{lin.ConnectMode}"
    return myroot


tree = ET.parse('sampleMotion.xml')
root = tree.getroot()

#print(ET.tostring(root, encoding='utf8').decode('utf8'))
"""
# Modify Connecting Lines
for tag1 in root.findall("Lines"):
    for tag2 in tag1.findall("anyType"):
        for tag in tag2.findall("GUID"):
            #print(tag)
            tag.text = None

# Modify Pose
for tag1 in root.findall("Activities"):
    for tag2 in tag1.findall("anyType"):
        for tag in tag2.findall("GUID"):
            print(tag)
            tag.text = None
"""

myroot=ET.Element(root.tag) # Create top/root element
myroot.text=root.text
myroot.set('xmlns:xsd',"http://www.w3.org/2001/XMLSchema")
myroot.set('xmlns:xsi',"http://www.w3.org/2001/XMLSchema-instance")
# Find element to copy
copyelements=["Name","Size","GridSize","BackColorText"]
for elem in copyelements:
    member = root.find(elem)
    # Create a copy and # Append the copy
    myroot.append(copy.copy(member))
# Include elements for lines and activities
newelements=["Lines","Activities"]
for elem in newelements:
    ET.SubElement(myroot,elem)

#Motion=10 AF ..
#Name, GUID, X,Y,Size,Width,Height,Text,BackColorText,MotionFlag,BaseName,Description,Group,ConnectedGuids,ConnectTypes,ProgramCode,Motion,Hint
import khr3hvwalk  # Generate motion data and line data
posdata=khr3hvwalk.posdata
#filedata = np.load('servodata.npz')
#posdata=filedata['v1']
#posdata=[]
#posdata.append(["P1", "5e6bdc74-40a3-4e46-840c-d68d29e83be5", 100,100, 64,48,"P1","WhiteSmoke","Start","Pos","(servo position)","Position","","","2B 10 3D F3 3F 00 00 0C C4 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 4C 1D 27","Frame=100"])
for data in posdata:
    pos=Pos(data) #Name, GUID, X,Y,Size,Width,Height,Text,BackColorText,MotionFlag,BaseName,Description,Group,ConnectedGuids,ConnectTypes,ProgramCode,Motion,Hint
    myroot=postag(myroot,pos)

#GUID, X1,Y1,X2,Y2,ConnectedMode
lindata=khr3hvwalk.lindata
#lindata=[]
#lindata.append(["5e6bdc74-40a3-4e46-840c-d68d29e83be5", 0,0, 64,48,"Normal"])
for data in lindata:
    lin=Lin(data) #Name, GUID, X,Y,Size,Width,Height,Text,BackColorText,MotionFlag,BaseName,Description,Group,ConnectedGuids,ConnectTypes,ProgramCode,Motion,Hint
    myroot=linetag(myroot,lin)

print(ET.tostring(myroot, encoding='utf8', xml_declaration=False).decode('utf8'))

mytree= ET.ElementTree(myroot) # Create xml file
mytree.write('MotionWrite.xml', encoding='utf8', xml_declaration=False) # Save file
