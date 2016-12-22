'''
����������������������������������������������������������������������
��                                 ��
��          INP�ļ���ȡ            ��
��                                 ��
��          Qi He                  ��
��                                 ��
��          Tsinghua University    ��
��                                 ��
��          2016                   ��
����������������������������������������������������������������������
'''



#----------�����ļ�λ��------------
import sys,os
path = sys.path[0]
filename = input('Please input your filename:\n')
location = path[2:].replace('\\','/') + '/' + filename + '.inp'
#location = '/Users/Administrator/Desktop/INP/8H_8.inp'
read = open(location,'r')


#----------�������----------------
#��ʱ����
i = 0
j = 0
k = 0
l = 0
#��ȡ�ļ�
readline = 1    #����������ɹ����������while��䣩
line = []       #�ļ�����


#-----------�����ļ���line-----------
while readline:
    readline=read.readline()
    line.append(readline[:-1])  #ɾ�����Ļس�����
    i = i+1
read.close
line_len = len(line)            #INP�ļ�ȫ����


#-----------��ȡ�����ؼ���λ��-------

#�ؼ���λ����Ϣ
keylocation = [0 for x in range(line_len)] 

for i in range(0,line_len-1):
    if line[i].find('*Part')!=-1:           #'Part'--1
        keylocation[i] = 1
    if line[i].find('*Node')!=-1:           #'Node'--2
        keylocation[i] = 2
    if line[i].find('*Element')!=-1:        #'Element'--3
        keylocation[i] = 3
    if line[i].find('*Material')!=-1:
        keylocation[i] = 5
    if line[i].find('*Boundary')!=-1:
        keylocation[i] = 6
    #�������ӹؼ���---------

j = 0
for i in range(0,line_len-1):
    if keylocation[i] == 3:
        j = 1
        continue
    if j == 1:
        if line[i+1][:1] == '*':
            keylocation[i] = 4            #ÿ��element����λ��--4
            j = 0
#print (keylocation)        

keynum = max(keylocation)    #�ؼ��ָ���
keyloc = [[] for x in range(keynum)]          
for i in range(0,line_len-1):
    for j in range(0,keynum):
        if keylocation[i] == (j+1):
            keyloc[j].append(i)
            
partnum = len(keyloc[0])     #PART����
#print(keyloc)


#-----------��ȡ�̶��߽���Ϣ-------------
i = 0
j = 0
k = 0
boundary = []
b_line = line[keyloc[5][0]+1]
b_set = b_line[:b_line.find(',')]
#print(b_set)
for i in range(line_len):
    if line[i].find('*Nset, nset='+b_set)!=-1:
        j = 1
        continue
    if j==1:
        temp = line[i]
        while temp.find(',')!=-1:
            boundary.append(int(temp[:temp.find(',')]))
            temp = temp[temp.find(',')+1:]
        boundary.append(int(temp))
        if line[i+1].find('*')!=-1:
            j = 0
            
#print(boundary)    
        
#-----------��ȡNODE��Ϣ-------------
def readnode(beg,end):
    
    #�ڵ���Ϣ
    node_num = []   #NODE��Ϣ-node���
    node_xyz = []   #NODE��Ϣ-�ڵ�xyz����
    #��ʱ����
    i = 0
    j = 0
    
    for i in range(beg,end+1):
    
        nodeline = line[i][line[i].find(',')+1:]        #'          -5.,          -5.,          10.' in 8H
        node_num.append(int(line[i][:line[i].find(',')]))
        node_xyz.append([])                             #Ϊ����������������ʼ��
        
        while nodeline.find(',') != -1 :
            loc = nodeline.find(',')                    #�ҳ�','��λ��
            node_xyz[j].append(float(nodeline[:loc]))
            nodeline = nodeline[loc+1:]
        node_xyz[j].append(float(nodeline[:]))
        j = j + 1
    
    return node_num,node_xyz
    
    
#-----------��ȡELEMENT��Ϣ-------------
def readelement(beg,end):
    
    #��Ԫ��Ϣ
    element_num = []    #ELEMENT��Ϣ-element���
    element_name = []   #ELEMENT��Ϣ-element����
    element_node = []   #ELEMENT��Ϣ-��Ԫ�ڵ��
    #��ʱ����
    i = 0
    j = 0
    
    for i in range(beg,end+1):
    
        elementline = line[i][line[i].find(',')+1:]    #' 10, 11, 14, 13,  1,  2,  5,  4' in 8H
        element_num.append(int(line[i][:line[i].find(',')]))
        element_node.append([])                        #Ϊ����������������ʼ��
        
        while elementline.find(',') != -1 :
            loc = elementline.find(',')                #�ҳ�','��λ��
            element_node[j].append(int(elementline[:loc]))
            elementline = elementline[loc+1:]
        element_node[j].append(int(elementline[:]))
        j = j + 1
    
    return element_num,element_node
    

#-----------��ȡPART����-------------
def readpartname(beg):
    
    partname = line[beg][line[beg].find('name')+5:]
    return partname


#-----------��ȡELEMENT����----------
def readelementname(beg):
    
    elementname = line[beg][line[beg].find('type')+5:]
    return elementname
    
    
#-----------��ȡMATERIAL����----------
def readmaterial(beg):
    
    material = [[] for x in range(3)] 
    density = line[beg+2]
    elastic = line[beg+4]
    material[0] = line[beg][line[beg].find('name')+5:]
    material[1] = float(density[:density.find(',')])
    material[2].append(float(elastic[:elastic.find(',')]))
    material[2].append(float(elastic[elastic.find(',')+1:]))
    return material
    
#-----------��ȡPART��Ϣ-------------

#������Ϣ     
partname = readpartname(keyloc[0][0])

node = readnode(keyloc[1][0]+1,keyloc[2][0]-1)

node_b = []         #Node_Boundary
for i in range(len(node[0])):
    if node[0][i] in boundary:
        node_b.append([1,1,1,0,0,0])
    else:
        node_b.append([0,0,0,0,0,0])
        
element = [[] for x in range(len(keyloc[2]))]
for i in range(0,len(keyloc[2])):
    element[i].append(readelementname(keyloc[2][i]))
    element[i].append(readelement(keyloc[2][i]+1,keyloc[3][i]))
    
material = []
for i in range(0,len(keyloc[4])):
    material.append(readmaterial(keyloc[4][i]))

'''    
for i in range(len(keyloc[2])):
    if element[i][0] == 'C3D8R' or element[i][0] == 'S4R':
        for j in range(len(keyloc[4])):
            if material[j][0] == 'CONCRETE':
                element[i].append(material[j])
    elif element[i][0] == 'B31':
        for j in range(len(keyloc[4])):
            if material[j][0] == 'ALUMINUM':
                element[i].append(material[j])
    elif element[i][0] == 'C3D8R':
        for j in range(len(keyloc[4])):
            if material[j][0] == 'CONCRETE':
                element[i].append(material[j])        
'''
                
#-----------���INSTANCE��Ϣ-------------
filename = input('Please input your filename(FOR INSTANCE):\n')
location = path[2:].replace('\\','/') + '/' + filename + '.inp'
read = open(location,'r')

#��ȡ�ļ�
readline = 1    #����������ɹ����������while��䣩
line = []       #�ļ�����

#�����ļ���line
while readline:
    readline=read.readline()
    line.append(readline[:-1])  #ɾ�����Ļس�����
    i = i+1
read.close
line_len = len(line)            #INP�ļ�ȫ����

for i in range(line_len):
    if line[i].find('** PART INSTANCE: Part-Pier-1')!=-1: 
        j = 1
        continue
    if j==1 and line[i].find('*Nset')!=-1:
        C3D8_pier = int(line[i-1][:line[i-1].find(',')])
        break

print(C3D8_pier)

#-----------������϶�Ӧ��Ԫ��Ϣ-------------
material_e = [['floor'],['Pier'],['SupportBeam'],['RiverBank'],['Cables']] 
for i in range(len(keyloc[4])):
    if material[i][0] == 'STEEL':
        material_e[4].append(material[i])
        for i in range(len(keyloc[2])):
            if element[i][0] == 'T3D2':
                material_e[4].append([element[i][1][0][0],element[i][1][0][-1]])
    elif material[i][0] == 'ALUMINUM':
        material_e[2].append(material[i])
        for i in range(len(keyloc[2])):
            if element[i][0] == 'B31':
                material_e[2].append([element[i][1][0][0],element[i][1][0][-1]]) 
    elif material[i][0] == 'GRANITE':
        material_e[3].append(material[i])
        for i in range(len(keyloc[2])):
            if element[i][0] == 'C3D8R':
                material_e[3].append([C3D8_pier+1,element[i][1][0][-1]]) 
    elif material[i][0] == 'CONCRETE':
        material_e[0].append(material[i])
        material_e[1].append(material[i])
        for i in range(len(keyloc[2])):
            if element[i][0] == 'C3D8R':
                material_e[1].append([element[i][1][0][0],C3D8_pier])
            elif element[i][0] == 'S4R':
                material_e[0].append([element[i][1][0][0],element[i][1][0][-1]])
material_e[0].append([500,200,1])
material_e[2].append([2,0.1])
material_e[4].append([0.25])
                
print(material_e)  


#-----------���LOAD��Ϣ ����ID��6ά-------------
load_floor = 58e6/(material_e[0][2][1]-material_e[0][2][0]+1)
load_pier = 348e6/(material_e[1][2][1]-material_e[1][2][0]+1)
load_supportbeam = 27.868e6/(material_e[2][2][1]-material_e[2][2][0]+1)
load_riverbank = 346.25e6/(material_e[3][2][1]-material_e[3][2][0]+1)
load_cables = 0
load_e = [load_floor,load_pier,load_supportbeam,load_riverbank,load_cables]
ID_6 = [[0,0,1],[1,1,1],[0,0,0],[1,1,1],[1,1,1]]
#print(load)

load = [0 for x in range(len(node[0])+1)]    #��load[1]��ʼ����node[0]
for i in range(len(keyloc[2])):
    for j in range(len(element[i][1][0])):
        e_num = element[i][1][0][j]
        e_node = element[i][1][1][j]
        for s in range(len(material_e)):
            if material_e[s][2][0] <= e_num <= material_e[s][2][1]:
                for k in e_node:
                    load[k] = load[k] + load_e[s]
                    for p in range(3):
                        node_b[k-1][p+3]=node_b[k-1][p+3]+ID_6[s][p]
                        if node_b[k-1][p+3]==2:
                            node_b[k-1][p+3] = 1
                     


                    
#print(load)                    
                
              
#-----------���PART��Ϣ-------------

print('������������������������' + str(i+1) + '��Ԫ����������������������')
print('-------------��������---------------')
print(partname)
print('\n')     #����
print('-------------�ڵ���---------------')
print(node[0])
print('\n')
print('-------------�ڵ�����---------------')
print(node[1])
print('\n')
print('-------------ID����---------------')
print(node_b)
print('\n')

for i in range(len(keyloc[2])):
    
    print('-------------��Ԫ����---------------')
    print(element[i][0])
    print('\n')
    print('-------------��Ԫ���---------------')
    print(element[i][1][0])
    print('\n')
    print('-------------��Ԫ�ڵ�---------------')
    print(element[i][1][1])
    print('\n')

for i in range(len(keyloc[4])):
    
    print('-------------��������---------------')
    print(material[i][0])
    print('\n')
    print('-------------�ܶ�---------------')
    print(material[i][1])
    print('\n')
    print('-------------����---------------')
    print(material[i][2])
    print('\n')
    
print('����������������������������������������������������������')
print('\n'*5)


#-----------���PART��Ϣ���ļ�-------------   
location_write = path[2:].replace('\\','/') + '/' + 'Bridge' + '.inp' 
inp = open(location_write, 'w')

#��������
inp.write('Bridge' + '\n')

#����ڵ��
inp.write('%5d'*4%(len(node[0]),len(keyloc[2]),1,1) + '\n')

#����ڵ���Ϣ
for i in range(len(node[0])):
    inp.write('%5d'*7%(node[0][i],node_b[i][0],node_b[i][1],node_b[i][2],node_b[i][3],node_b[i][4],node_b[i][5]))
    inp.write('%10.3f'*3%(node[1][i][0],node[1][i][1],node[1][i][2]))
    inp.write('%5d'%0 + '\n')
    
#���ϡ��洢��Ϣ
#inp.write('%5d'%())

#���������Ϣ
inp.write('%5d'*2%(1,len(node[0]))+'\n')
for i in range(len(node[0])):
    inp.write('%5d'*2%(node[0][i],3))
    inp.write('%10.2e'%(-load[i+1]) + '\n')

#���뵥Ԫ��Ϣ
for i in range(len(keyloc[2])):
    if element[i][0] == 'C3D8R':
        inp.write('%5d'*3%(4,len(element[i][1][0]),2) + '\n')
        inp.write('%5d'%1 + '%10.3e'%(material_e[1][1][2][0]) + '%10.3f'%(material_e[1][1][2][1]) + '\n')
        inp.write('%5d'%2 + '%10.3e'%(material_e[3][1][2][0]) + '%10.3f'%(material_e[3][1][2][1]) + '\n')
        for j in range(len(element[i][1][0])):
            el_num = j+1
            el_node = element[i][1][1][j]
            inp.write('%5d'*9%(el_num,el_node[0],el_node[1],el_node[2],el_node[3],el_node[4],el_node[5],el_node[6],el_node[7]))
            if el_num < C3D8_pier :
                inp.write('%5d'*2%(1,0) + '\n')
            else:
                inp.write('%5d'*2%(2,0) + '\n')
    elif element[i][0] == 'S4R':
        inp.write('%5d'*3%(7,len(element[i][1][0]),1) + '\n')
        inp.write('%5d'%1 + '%10.3e'%(material_e[0][1][2][0]) + '%10.3f'%(material_e[0][1][2][1]) + '\n')
        for j in range(len(element[i][1][0])):
            el_num = j+1
            el_node = element[i][1][1][j]
            inp.write('%5d'*5%(el_num,el_node[0],el_node[1],el_node[2],el_node[3]))
            inp.write('%5d'%(1) + '%10.1e'%(1.0) + '%5d'%(0) + '\n')
    elif element[i][0] == 'B31':
        inp.write('%5d'*3%(5,len(element[i][1][0]),1) + '\n')
        inp.write('%5d'%1 + '%10.3e'%(material_e[2][1][2][0]) + '%10.3e'%(2.60030e10) + '%10.3f'%(0.76))
        inp.write('%10.3e'%(0.4853333) + '%10.3e'%(0.4853333) + '%10.3e'%(0.4853333))
        inp.write('%10.3e'%(0.9170666) + '%10.3e'%(0.9170666) + '%10.3e'%(0.9170666) + '\n')
        for j in range(len(element[i][1][0])):
            el_num = j+1
            el_node = element[i][1][1][j]
            inp.write('%5d'*3%(el_num,el_node[0],el_node[1]))
            inp.write('%5d'%(1) + '%5d'%(0) + '\n')
    elif element[i][0] == 'T3D2':
        inp.write('%5d'*3%(1,len(element[i][1][0]),1) + '\n')
        inp.write('%5d'%1 + '%10.3e'%(material_e[4][1][2][0]) + '%10.3f'%(0.25) + '\n')
        for j in range(len(element[i][1][0])):
            el_num = j+1
            el_node = element[i][1][1][j]
            inp.write('%5d'*3%(el_num,el_node[0],el_node[1]))
            inp.write('%5d'%(1) + '%5d'%(0) + '\n')
    elif element[i][0] == 'CPS4R':
        inp.write('%5d'*3%(1,len(element[i][1][0]),1) + '\n')
        inp.write('%5d'%1 + '%10.3e'%(material_e[4][1][2][0]) + '%10.3f'%(0.25) + '\n')
        for j in range(len(element[i][1][0])):
            el_num = j+1
            el_node = element[i][1][1][j]
            inp.write('%5d'*3%(el_num,el_node[0],el_node[1]))
            inp.write('%5d'%(1) + '%5d'%(0) + '\n')
    
inp.write('stop')
            
inp.close()    
    
    
    
    
    
    
    
    
    