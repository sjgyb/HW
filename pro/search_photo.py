# -*- coding: utf-8 -*-  
import cv2  
import numpy as np  
from find_obj import filter_matches,explore_match
import os

def match(pic1,pic2):
    img1 = cv2.imread(pic1, 0)  # queryImage  
    img2 = cv2.imread(pic2, 0)  # trainImage  
    sift = cv2.SIFT()  
    kp1, des1 = sift.detectAndCompute(img1, None)  
    kp2, des2 = sift.detectAndCompute(img2, None)  
    # 蛮力匹配算法,有两个参数，距离度量(L2(default),L1)，是否交叉匹配(默认false)  
    bf = cv2.BFMatcher()  
    #返回k个最佳匹配  
    matches = bf.knnMatch(des1, des2, k=2)  
    # cv2.drawMatchesKnn expects list of lists as matches.  
    #opencv2.4.13没有drawMatchesKnn函数，需要将opencv2.4.13\sources\samples\python2下的common.py和find_obj文件放入当前目录，并导入  
    p1, p2, kp_pairs = filter_matches(kp1, kp2, matches)  
    explore_match('find_obj', img1, img2, kp_pairs)  # cv2 shows image
    return len(kp_pairs)


def search_photo(target):
    film_id="1"
    max_match=0
    root="films_pictures"
    for root, dirnames, filenames in os.walk(root):
        for filename in filenames:
            try:
                path = os.path.join(root, filename)          
                match_num=match(path,target)          
                if match_num>max_match:
                    max_match=match_num
                    film_id=filename
            except Exception, e:
                print "Fail:", e
    film_id=film_id.split("_")[0]
    print film_id
    dictionary = {}
    file = open('index1_film.txt', 'r')
    for line in file.readlines():      
        line = line[0:-1]
        if '\t' in line: 
            list = line.split('\t')
            dictionary[list[0]] = list[4]
    file.close()
    name= dictionary[str(film_id)]
    print name
    print max_match
    return name
    
          
                
