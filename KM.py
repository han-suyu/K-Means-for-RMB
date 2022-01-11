from PIL import Image, ImageStat
import sys
import os
import random
from datetime import datetime
import math
import shutil


Pic = []        # 存放n个图片的路径
mean_Pic = []   # 存放代表n个图片的n个点


# 将同类图片移动到同名文件夹下，方便检查。（注意：第二次运行时，要把这4个文件夹先删除）
def Move(Clust):
    # 定义 路径+文件夹名
    dest1 = os.getcwd() + '//1//'       # os.getcwd()的作用是读取现在的根目录路径
    dest2 = os.getcwd() + '//2//'
    dest3 = os.getcwd() + '//3//'
    dest4 = os.getcwd() + '//4//'

    # 根据 路径+文件夹名 ，创建文件夹
    os.makedirs(dest1)
    os.makedirs(dest2)
    os.makedirs(dest3)
    os.makedirs(dest4)
   

    # 移动到对应的文件夹中
    for i in Clust[0]:
        print('第1类',Pic[i])
        shutil.copy(Pic[i], dest1)
    for i in Clust[1]:
        print('第2类',Pic[i])
        shutil.copy(Pic[i], dest2)
    for i in Clust[2]:
        print('第3类',Pic[i])
        shutil.copy(Pic[i], dest3)
    for i in Clust[3]:
        print('第4类',Pic[i])
        shutil.copy(Pic[i], dest4)
    return






# 更新簇心。      # 这里的做法不是取物理位置中的最中心的位置，而是取一个中间值，这个中间值所代表的图片可能在样本集中不存在，但他不影响程序的运行，并且效果会更好一些
def FindNewCentroid(lst):
    sum = 0
    for i in range(len(lst)):
        sum = sum + mean_Pic[lst[i]]    # 累加像素值
    return sum / len(lst)               # 求平均






# K-means算法
def KM(m1, m2, m3,m4, Clust):
    # 计算样本中其他的每个点分别到这四个初始点的欧氏距离
    distTo_m1 , distTo_m2 , distTo_m3 , distTo_m4 = [],[],[],[]

    for i in range(len(mean_Pic)):  # 遍历样本中的点
        distTo_m1.append(math.sqrt((m1-mean_Pic[i])**2))    # 计算这个点到簇中心 m1 的距离
        distTo_m2.append(math.sqrt((m2-mean_Pic[i])**2))    # 计算这个点到簇中心 m2 的距离
        distTo_m3.append(math.sqrt((m3-mean_Pic[i])**2))    # 计算这个点到簇中心 m3 的距离
        distTo_m4.append(math.sqrt((m4-mean_Pic[i])**2))    # 计算这个点到簇中心 m4 的距离
      

    # 把这些样本点归类：归到离他最近的那个簇中心点所在的簇中
    clusters = [[],[],[],[],[]]

    for i in range(len(mean_Pic)):
        if distTo_m1[i] <= distTo_m2[i] and distTo_m1[i] <= distTo_m3[i] and distTo_m1[i] <= distTo_m4[i] :     # 距 m1 最近，归到第一个簇中
            clusters[0].append(i)

        elif distTo_m2[i] <= distTo_m1[i] and distTo_m2[i] <= distTo_m3[i] and distTo_m2[i] <= distTo_m4[i]:    # 距 m2 最近，归到第二个簇中
            clusters[1].append(i)

        elif distTo_m3[i] <= distTo_m2[i] and distTo_m3[i] <= distTo_m1[i] and distTo_m3[i] <= distTo_m4[i] :   # 距 m3 最近，归到第三个簇中
            clusters[2].append(i)

        elif distTo_m4[i] <= distTo_m1[i] and distTo_m4[i] <= distTo_m2[i] and distTo_m4[i] <= distTo_m3[i] :   # 距 m4 最近，归到第三个簇中
            clusters[3].append(i)

      




    # 判断是否还有图片没有被归类好
    if(clusters == Clust):  # 如果所有的点所处的类都和上一轮没有变化，说明已经聚类好了，停止迭代，把同类的图片复制到同名文件夹中
        Move(Clust)         # 图片移动
        return
    else:                   # 还有图片没有被归类好，更新簇心，继续迭代
        # 更新每个簇的中心
        m1 = FindNewCentroid(clusters[0])
        m2 = FindNewCentroid(clusters[1])
        m3 = FindNewCentroid(clusters[2])
        m4 = FindNewCentroid(clusters[3])

        KM(m1, m2, m3,m4, clusters)   # 继续迭代




def main():
    path = os.getcwd() + '//picture//'
    for filename in os.listdir(path):
        if filename.endswith('.jpg'):
            im_file = path + filename
           
            Pic.append(im_file)   # 存储样本图像的路径信息

            # 使用PIL的ImageStat的工具，将每张图像转化为一个值
            im = Image.open(im_file)        # 打开图像
            stat = ImageStat.Stat(im)       # 将图像转化为ImageStat格式
            mean_Pic.append(stat.mean[0])   # 使用ImageStat中的mean方法，将第一层上的像素值加和求平均。
            # 此时存入mean_Pic的是点值。n个图像就有n个值，以后就把这些点值送入K-means算法中
    # print(mean_Pic)



    # 从这些点中选出四个点作为初始化簇的中心。现在的策略是4等分，选每一份末尾处的点作为初始点
    j = len(mean_Pic) // 4  # 四等分

    m1 = mean_Pic[j-1]      # 第一个初始化簇的中心
    m2 = mean_Pic[j*2-1]    # 第二个初始化簇的中心
    m3 = mean_Pic[j*3-1]    # 第三个初始化簇的中心
    m4 = mean_Pic[j*4-1]    # 第四个初始化簇的中心


    KM(m1, m2, m3,m4, [[],[],[],[]])    # 将这四个点和四个簇（初始为空）送入K-means算法中




if __name__ == '__main__':
    '''
    K-means目的：将一堆离散的点在不改变他们物理位置（坐标）的情况下，按照欧氏距离聚成若干个簇


    K-means思想：首先在一堆离散点中随机选出k个点作为初始化簇的中心（即本身），然后计算样本中其他的每个点分别到这几个簇中心的距离，全部计算完成之后，将每个样本点归到与他最近的那个簇中心所在的类中，一轮完成
                现在会有k个簇，但原来那k个点不一定还是这k个簇的中心位置，所以就需要更新一下簇心，使簇心位于每个簇的中心位置
                簇心更新完后，原来计算的相互之间的欧氏距离会被打乱，现在就需要重新计算，这就需要第二轮...
                ...
                一直这样迭代下去，直到簇中的点都不再发生变动，程序可以停止，此时的k个簇，就是最终的结果。



    K-means图像聚类的思路：
                这里聚类的对象不再是离散点，而是图像。
                现在的思路就是把每一张图像看成一个点。怎么转化呢？
                我们知道每张图片是由RGB三个通道组成的，每个通道可以看作是一层、一个二维的矩阵，那么三层的RGB图像实质上就是一个堆叠起来的三维矩阵，每一个像素点上都有自上而下的三个值
                我们现在使用第一个通道（也可以使用第二、三个或求均值），即取第一层上的像素值，将这些像素值累加起来求平均，用这个值来代表整个RGB图像。
                这样就将一堆图像转化成了一堆离散的点，再使用同样的思路使用上述的K-means算法，即可完成图像聚类

    '''

    main()   # 现在只支持4类，如果想增多，可以简单修改代码，以支持任意多种类