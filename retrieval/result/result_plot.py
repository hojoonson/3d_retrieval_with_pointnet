import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import glob

txtlist=glob.glob("./*.txt")

Num_of_Result=10

targetwidth=100

for element in txtlist:
    print(element)
    print("="*100)
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
    
    fig = plt.figure(figsize=(6*(Num_of_Result+1),4*Query_num))
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
                print("-"*100)
                query_model_id=line.split(" ")[0]
                print("Query "+str(count+1)+" : "+query_model_id)
                print("-"*100)

                #PLOT Query
                img=cv2.imread("/home/hojoonson/projects/3D_retrieval/pointnet/part_seg/PartAnnotation/02691156/expert_verified/seg_img/"+query_model_id+".png")
                height,width=img.shape[0],img.shape[1]
                img=cv2.resize(img,(300,200),interpolation=cv2.INTER_AREA)
                ax = fig.add_subplot(rows, cols, count*(Num_of_Result+1)+1)
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                ax.set_title("Query "+str(count+1),y=-0.05,fontweight='bold')
                ax.axis("off")
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)
                ax.title.set_fontsize(40)
                autoAxis = ax.axis()
                rec = plt.Rectangle((-16.5,213.5),328.5,-219.5,fill=False,lw=5)
                rec = ax.add_patch(rec)
                rec.set_clip_on(False)
                
                result_count=0
                count+=1
            if line.split(" ")[0]=="Most" and result_count<Num_of_Result:
                print(line.split(":")[1].split(" ")[0])
                #PLOT Result
                img=cv2.imread("/home/hojoonson/projects/3D_retrieval/pointnet/part_seg/PartAnnotation/02691156/expert_verified/seg_img/"+line.split(":")[1].split(" ")[0]+".png")
                height,width=img.shape[0],img.shape[1]
                img=cv2.resize(img,(300,200),interpolation=cv2.INTER_AREA)
                ax = fig.add_subplot(rows, cols, (count-1)*(Num_of_Result+1)+1+result_count+1)
                ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                ax.set_title("Rank "+str(result_count+1),y=-0.05,fontweight='bold')
                ax.axis("off")
                ax.axes.get_xaxis().set_visible(False)
                ax.axes.get_yaxis().set_visible(False)
                ax.title.set_fontsize(40)
                
                if result_count==0:
                    autoAxis = ax.axis()
                    rec = plt.Rectangle((-16.5,213.5),328.5+312*(Num_of_Result-1)+156,-219.5,fill=False,lw=5)
                    rec = ax.add_patch(rec)
                    rec.set_clip_on(False)
                result_count+=1
                next_valid=0
            if result_count==Num_of_Result:
                next_valid=1
    
    fig.tight_layout()
    #print(element.split(".")[1][1:]+'.eps')
    #fig.savefig("./images/3D_Retrieval_Result/"+element.split(".")[1][1:]+'.eps',format='eps',dps=500)
    fig.savefig("./images/3D_Retrieval_Result/"+element.split(".")[1][1:]+'.png',dps=500)

    f.close()
    print("Total # of Query Models : "+str(Query_num))
    print("="*100)
    
