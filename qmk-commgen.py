import QMK_KC
import re
from tkinter import Tk
r=Tk()
r.withdraw()
comb=[]             #combined layer ready for output
fill="-------"      #top and bottom fill lines
fill2="------+"     #middle row fill lines
laystart=False      #has the program found a layer start
layers=0            #how many layers
KClayers=[]         #array of all KClines
KClines=[]          #list if all KC on line
nl="\n"
#open keymap file
inpt=open("keymap.c","r")
inpList=inpt.readlines()
#add all lines of keymap to allin var and close
inpt.close()
file=open("comment.txt","w+")
for line in inpList:
    line=line.replace("\n","")
    #remove whitespace and new lines
    line=line.replace(" ","")
    if line.count(")")==1 and line.count("(")==0 and laystart==True:
        #if it is the end of a layer
        laystart=False
        #add layer to KClayers
        KClayers.append(KClines)
        KClines=[]
        layers+=1
    elif laystart==True:
        #if it part of keymap add it to KC lines
        KClines.append(line)
    elif re.search("LAYOUT",line):
        laystart=True
assert len(KClayers)>0,"+- No keymap Found -+"
assert layers==len(KClayers),"+- Layer Error -+"
print("Successfully imported layers")
lyrcount=layers
for layer in range(0,len(KClayers)):
    lyrcount-=1
    for num in range(0,len(KClayers[layer])):
        #define current layer
        crtln=(KClayers[layer][num])
        if crtln.endswith(",")==False:
            crtln=crtln+","
        colm=crtln.count(',')
        crtln=" * ,"+crtln
        #run it through my module see QMK_KC.py
        fixed=QMK_KC.repl(crtln)
        comb.append(fixed)
        lines=len(comb)
    file.write(nl)
    #Output to comment.txt
    file.write("/*"+nl)
    colm2=colm-1
    file.write(" * ,------"+(fill*colm2)+"."+nl)
    for num in range(0,lines):
        file.write(comb[num]+nl)
        if lines>1 and num<(lines-1):
            file.write(" * |"+(fill2*colm2)+"------|"+nl)
    file.write(" * `------"+(fill*colm2)+"'"+nl)
    file.write(" */"+nl)
    print("Layer "+str(layer+1)+" done")
    #empty the combined list
    comb=[]
file.close()
#ask if clipboard
if QMK_KC.yesno("Enable paste to Clipboard")==True:
    opclp=open("comment.txt","r")
    clip=opclp.read()    
    r.clipboard_clear()
    r.clipboard_append(clip)
    r.update()
    r.destroy()
    print("Added to Clipboard")
print("Done printing Keymap")
