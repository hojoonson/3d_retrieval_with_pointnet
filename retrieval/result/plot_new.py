import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob
import os
import shutil

txtlist=glob.glob("./*.txt")

Num_of_Result=10

targetwidth=100

for element in txtlist:


    print(element)
    print("="*50)
    f=open(element,'r')
    content=f.readlines()
    

    Query_num=0
 
    for line in content:
        if line!="\n":
            line=line[:-2]
            if line.split(" ")[0]!="Most":
                Query_num+=1
    

    result_count=0
    next_valid=1
    count=0
    
    rows=Query_num
    cols=Num_of_Result+1
    """
    fig.subplots_adjust(left = 0.49,  # the left side of the subplots of the figure
            right = 0.5,   # the right side of the subplots of the figure
            bottom = 0.49,  # the bottom of the subplots of the figure
            top = 0.5,     # the top of the subplots of the figure,
            hspace=1, wspace=0)
    """
    count==0
    for line in content:
        if line!="\n":
            line=line[:-2]
            if line.split(" ")[0]!="Most" and next_valid==1:
                directory = 'images/3D_Retrieval_Result_new/'+element.split(".")[1][1:] + f'/query_{count+1}'
                os.makedirs(directory)
                query_model_id=line.split(" ")[0]
                print("Query "+str(count+1)+" : "+query_model_id)
                #PLOT Query
                shutil.copy2("/home/hojoonson/projects/3D_retrieval/pointnet/part_seg/PartAnnotation/02691156/expert_verified/seg_img/"+query_model_id+".png", directory+f'/query_{query_model_id}.png')
                result_count=0
                count+=1
            if line.split(" ")[0]=="Most" and result_count<Num_of_Result:
                img=cv2.imread("/home/hojoonson/projects/3D_retrieval/pointnet/part_seg/PartAnnotation/02691156/expert_verified/seg_img/"+line.split(":")[1].split(" ")[0]+".png")
                shutil.copy2("/home/hojoonson/projects/3D_retrieval/pointnet/part_seg/PartAnnotation/02691156/expert_verified/seg_img/"+line.split(":")[1].split(" ")[0]+".png", directory+f'/rank{result_count+1}_{query_model_id}.png')
                result_count+=1
                next_valid=0
            if result_count==Num_of_Result:
                next_valid=1

    print("Total # of Query Models : "+str(Query_num))
    print("="*50)
    
