#coding: UTF-8
import sys
#sys.path.append('../Rcb4Lib') #Rcb4Libの検索パスを追加
from Rcb4BaseLib import Rcb4BaseLib            #Rcb4BaseLib.pyの中のRcb4BaseLibが使えるように設定
rcb4 = Rcb4BaseLib()      #rcb4をインスタンス(定義)
import time                   #timeが使えるように宣言
import uuid

import numpy as np
import h5py
import scipy.io
# Load joint angle traj
mytraj = scipy.io.loadmat('qtraj.mat');
t=np.array(mytraj["t_traj"])
q=np.array(mytraj["q_traj"])
print(np.size(t))

# Indices from DH to servo traj
# q_i[0]=q[22-1, k];
# q_i[1:4]=q[23-1: 25, k];
# q_i[4:7]=q[26-1: 28, k];
# q_i[7:12]=q[8-1: 12, k];
# q_i[12:17]=q[14-1: 18, k];
q_ind=[22, 23,24,25, 26,27,28, 8,9,10,11,12, 14,15,16,17,18]
q_ind = [i - 1 for i in q_ind]

### Servo rotation traj
from sim2kondo import jointdata
[n,q_id,q_sio,q2dir,q_trim]=jointdata()
#print(q_trim)

#% Frequency
dt_min=15/1000; #%15 ms

t_i = 1  # 1 sec

pos_trim=0*q_trim; #% Pos for servo

#%%% Pose for Unit angle of rotation
def q2pos(q_i):
    return np.multiply(8000/np.deg2rad(270)*q2dir,(q_i-q_trim));


# Trim values of servos
ics=np.zeros(n)
servo_trim=np.zeros(n, dtype=int)
servo_pos=np.zeros(n, dtype=int)
for i in range (0,n):
    cmd = rcb4.ServoData(q_id[i], q_sio[i], 1)
    ics[i]=cmd.icsNum2id()        #q_id[i] * 2 + (q_sio[i] - 1)
    servo_trim[i]=7500#cmd#[1][2]
    #print(servo_trim[i])



#Find Servo pose for trajectory
# Name, GUID, X, Y, Width, Height, Text, BackColorText, MotionFlag, BaseName, Description, Group, ConnectedGuids, ConnectTypes, Motion, Hint = posdata
posdata=[] # array to store all pose data
# GUID, X1, Y1, X2, Y2, ConnectMode= lindata
lindata=[] # Create Line data for connect nodes
linguid=[] # GUIDs of lines
Lim= 700 # 500x500 grid
X=10
Y=10
dXY=30
w=26
h=26
q_i=np.zeros(n)
t_i=0 # 1 sec
frm=1
dt=dt_min*frm
k=0
while t_i<=t[0,len(t[0,:])-1]:
    for i in range(0,n):
        q_i[i]=np.interp(t_i, t[0,:],q[q_ind[i], :])
    pos_i = q2pos(q_i)
    pos_i = np.round(pos_i)
    #t_i = t_i + t[0,k]-t[0,k-1]  # dt sec
    servo_pos = servo_trim + pos_i.astype(int)
    #print(pos_i)
    #frm = (t[0,k]-t_i) / dt_min
    servo_data = []
    for i in range(0,n):
        servo_data.append(rcb4.ServoData(q_id[i], q_sio[i], servo_pos[i]))
    cmd = rcb4.runConstFrameServoCmd(servo_data, frm)
    #print(cmd[1])
    poshex=(f'{cmd[1][0]:02X}')
    for i in cmd[1][1:]:
        poshex=poshex+(f' {i:02X}')
    #print(poshex)
    if (X+w/2)>Lim:
        Y=Y+dXY
        X=10
    X1 = int(X + w / 2)
    Y1 = int(Y + h / 2)
    if (X + dXY + w / 2) > Lim:
        X2 = int(10 + w / 2)
        Y2 = int(Y + dXY +h/2)
    else:
        X2 = X1 + dXY
        Y2 = int(Y + h/2)
    linguid.append(uuid.uuid4())
    if k==0:
        mylin=[f'{linguid[k]}', X1, Y1, X2, Y2, 'Normal']
        lindata.append(mylin)
        mypos=[f'P{k + 1}', f'{uuid.uuid4()}', X, Y, w, h, f'P{k + 1}', 'WhiteSmoke', 'Start', 'Pos', 'Servo Position','Position', f'{linguid[k]}', 'BeginConnect', poshex, f'Frame = {frm}']
    elif t_i+dt>t[0,len(t[0,:])-1]:
        mypos=[f'P{k+1}',f'{uuid.uuid4()}',X,Y,w,h,f'P{k+1}','WhiteSmoke','None','Pos','Servo Position','Position',f'{linguid[k-1]}','EndConnect',poshex,f'Frame = {frm}']
    else:
        mylin=[f'{linguid[k]}', X1, Y1, X2, Y2, 'Normal']
        lindata.append(mylin)
        linguid.append(uuid.uuid4())
        mypos=[f'P{k+1}',f'{uuid.uuid4()}',X,Y,w,h,f'P{k+1}','WhiteSmoke','None','Pos','Servo Position','Position',f'{linguid[k-1]},{linguid[k]}','EndConnect,BeginConnect',poshex,f'Frame = {frm}']
    posdata.append(mypos)
    X=X+dXY
    t_i=t_i+dt
    k=k+1

