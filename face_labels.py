# -*- coding: utf-8 -*
import os,h5py,cv2,sys,shutil
import numpy as np
from xml.dom.minidom import Document
rootdir="./wider_face"
save_dir = "./wider_face_voc"
convet2yoloformat=True
convert2vocformat=True
resized_dim=(48, 48)
 
#最小取20大小的脸，并且补齐
minsize2select=20
usepadding=True
 
datasetprefix="/media/data/YC_DATA/mydata/wider_face"#
datasetprefix_voc="/media/data/YC_DATA/mydata/wider_face_voc"# 
def convertimgset(img_set="train"):
    imgdir=rootdir+"/WIDER_"+img_set+"/images"
    gtfilepath=rootdir+"/wider_face_split/wider_face_"+img_set+"_bbx_gt.txt"
    imagesdir=save_dir+"/images"
    vocannotationdir=save_dir+"/Annotations"
    labelsdir=save_dir+"/labels"
    if not os.path.exists(imagesdir):
        os.mkdir(imagesdir)
    if convet2yoloformat:
        if not os.path.exists(labelsdir):
            os.mkdir(labelsdir)
    if convert2vocformat:
        if not os.path.exists(vocannotationdir):
            os.mkdir(vocannotationdir)

    if not os.path.exists(save_dir+"/ImageSets"):
        os.mkdir(save_dir+"/ImageSets")
    if not os.path.exists(save_dir+"/ImageSets/Main"):
        os.mkdir(save_dir+"/ImageSets/Main")

    index=0
    f_txt=open(save_dir+"/"+img_set+".txt","w")
    f_main=open(save_dir+"/ImageSets/Main/"+img_set+".txt",'w')
    with open(gtfilepath,'r') as gtfile:
        while(True ):#and len(faces)<10
            filename=gtfile.readline()[:-1]
            if(filename==""):
                break;

#            sys.stdout.write("\r"+str(index)+":"+filename+"\t\t\t")
#            sys.stdout.flush()
            imgpath=imgdir+"/"+filename
            img=cv2.imread(imgpath)
            if not img.data:
                break;
            imgheight=img.shape[0]
            imgwidth=img.shape[1]
            maxl=max(imgheight,imgwidth)
            paddingleft=(maxl-imgwidth)>>1
            paddingright=(maxl-imgwidth)>>1
            paddingbottom=(maxl-imgheight)>>1
            paddingtop=(maxl-imgheight)>>1
            saveimg=cv2.copyMakeBorder(img,paddingtop,paddingbottom,paddingleft,paddingright,cv2.BORDER_CONSTANT,value=0)
            showimg=saveimg.copy()
            numbbox=int(gtfile.readline())
            bboxes=[]
            for i in range(numbbox):
                line=gtfile.readline()
                line=line.split()
                line=line[0:4]               
                if(int(line[3])<=0 or int(line[2])<=0):
                    continue
                x=int(line[0])+paddingleft
                y=int(line[1])+paddingtop
                width=int(line[2])
                height=int(line[3])
                bbox=(x,y,width,height)
                x2=x+width
                y2=y+height
                #face=img[x:x2,y:y2]
                if width>=minsize2select and height>=minsize2select:
                    bboxes.append(bbox)
                    cv2.rectangle(showimg,(x,y),(x2,y2),(0,255,0))
                    #maxl=max(width,height)
                    #x3=(int)(x+(width-maxl)*0.5)
                    #y3=(int)(y+(height-maxl)*0.5)
                    #x4=(int)(x3+maxl)
                    #y4=(int)(y3+maxl)
                    #cv2.rectangle(img,(x3,y3),(x4,y4),(255,0,0))
                else:
                    cv2.rectangle(showimg,(x,y),(x2,y2),(0,0,255))              
            filename=filename.replace("/","_")
            if len(bboxes)==0:
#                print "warrning: no face"
                continue 
            cv2.imwrite(imagesdir+"/"+filename,saveimg)
	    imgfilepath = datasetprefix_voc + "/images/"+filename
	    f_main.write(filename+'\n')
	    f_txt.write(imgfilepath+'\n')	
            if convet2yoloformat:
                height=saveimg.shape[0]
                width=saveimg.shape[1]
                txtpath=labelsdir+"/"+filename
                txtpath=txtpath[:-3]+"txt"
                ftxt=open(txtpath,'w')  
                for i in range(len(bboxes)):
                    bbox=bboxes[i]
                    xcenter=(bbox[0]+bbox[2]*0.5)/width
                    ycenter=(bbox[1]+bbox[3]*0.5)/height
                    wr=bbox[2]*1.0/width
                    hr=bbox[3]*1.0/height
                    txtline="0 "+str(xcenter)+" "+str(ycenter)+" "+str(wr)+" "+str(hr)+"\n"
                    ftxt.write(txtline)
                ftxt.close()
            if convert2vocformat:
                xmlpath=vocannotationdir+"/"+filename
                xmlpath=xmlpath[:-3]+"xml"
                doc = Document()
                annotation = doc.createElement('annotation')
                doc.appendChild(annotation)
                folder = doc.createElement('folder')
                folder_name = doc.createTextNode('widerface')
                folder.appendChild(folder_name)
                annotation.appendChild(folder)
                filenamenode = doc.createElement('filename')
                filename_name = doc.createTextNode(filename)
                filenamenode.appendChild(filename_name)
                annotation.appendChild(filenamenode)
                source = doc.createElement('source')
                annotation.appendChild(source)
                database = doc.createElement('database')
                database.appendChild(doc.createTextNode('wider face Database'))
                source.appendChild(database)
                annotation_s = doc.createElement('annotation')
                annotation_s.appendChild(doc.createTextNode('PASCAL VOC2007'))
                source.appendChild(annotation_s)
                image = doc.createElement('image')
                image.appendChild(doc.createTextNode('flickr'))
                source.appendChild(image)
                flickrid = doc.createElement('flickrid')
                flickrid.appendChild(doc.createTextNode('-1'))
                source.appendChild(flickrid)
                owner = doc.createElement('owner')
                annotation.appendChild(owner)
                flickrid_o = doc.createElement('flickrid')
                flickrid_o.appendChild(doc.createTextNode('yanyu'))
                owner.appendChild(flickrid_o)
                name_o = doc.createElement('name')
                name_o.appendChild(doc.createTextNode('yanyu'))
                owner.appendChild(name_o)
                size = doc.createElement('size')
                annotation.appendChild(size)
                width = doc.createElement('width')
                width.appendChild(doc.createTextNode(str(saveimg.shape[1])))
                height = doc.createElement('height')
                height.appendChild(doc.createTextNode(str(saveimg.shape[0])))
                depth = doc.createElement('depth')
                depth.appendChild(doc.createTextNode(str(saveimg.shape[2])))
                size.appendChild(width)
                size.appendChild(height)
                size.appendChild(depth)
                segmented = doc.createElement('segmented')
                segmented.appendChild(doc.createTextNode('0'))
                annotation.appendChild(segmented)
                for i in range(len(bboxes)):
                    bbox=bboxes[i]
                    objects = doc.createElement('object')
                    annotation.appendChild(objects)
                    object_name = doc.createElement('name')
                    object_name.appendChild(doc.createTextNode('face'))
                    objects.appendChild(object_name)
                    pose = doc.createElement('pose')
                    pose.appendChild(doc.createTextNode('Unspecified'))
                    objects.appendChild(pose)
                    truncated = doc.createElement('truncated')
                    truncated.appendChild(doc.createTextNode('1'))
                    objects.appendChild(truncated)
                    difficult = doc.createElement('difficult')
                    difficult.appendChild(doc.createTextNode('0'))
                    objects.appendChild(difficult)
                    bndbox = doc.createElement('bndbox')
                    objects.appendChild(bndbox)
                    xmin = doc.createElement('xmin')
                    xmin.appendChild(doc.createTextNode(str(bbox[0])))
                    bndbox.appendChild(xmin)
                    ymin = doc.createElement('ymin')
                    ymin.appendChild(doc.createTextNode(str(bbox[1])))
                    bndbox.appendChild(ymin)
                    xmax = doc.createElement('xmax')
                    xmax.appendChild(doc.createTextNode(str(bbox[0]+bbox[2])))
                    bndbox.appendChild(xmax)
                    ymax = doc.createElement('ymax')
                    ymax.appendChild(doc.createTextNode(str(bbox[1]+bbox[3])))
                    bndbox.appendChild(ymax)
                f=open(xmlpath,"w")
                f.write(doc.toprettyxml(indent = ''))
                f.close()     
            #cv2.imshow("img",showimg)
            #cv2.waitKey()
            index=index+1
    f_txt.close()
    f_main.close() 
 
 
def convertdataset():
    img_sets=["train","val"]
    for img_set in img_sets:
        convertimgset(img_set)
 
if __name__=="__main__":
    convertdataset()
    shutil.move(save_dir+"/"+"train.txt",save_dir+"/"+"trainval.txt")
    shutil.move(save_dir+"/"+"val.txt",save_dir+"/"+"test.txt")
    shutil.move(save_dir+"/ImageSets/Main/"+"train.txt",save_dir+"/ImageSets/Main/"+"trainval.txt")
    shutil.move(save_dir+"/ImageSets/Main/"+"val.txt",save_dir+"/ImageSets/Main/"+"test.txt")
