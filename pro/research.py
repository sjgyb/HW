#coding=utf8
import cv2  
import numpy as np
from find_obj import filter_matches,explore_match
import _1
from _1 import *
from collections import defaultdict 
from operator import itemgetter
import web
import face_recognition
from web import form
import urllib2
import sys, os, lucene,pickle
from java.io import File
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
from org.apache.lucene.search import SortField
from org.apache.lucene.search import Sort
import jieba
reload(sys)
sys.setdefaultencoding('utf8')
f=open('train.pkl','rb')
train=pickle.load(f)
print train
f.close()
f=open('W.pkl','rb')
W=pickle.load(f)
f.close()
urls = (
    '/(js|css|img)/(.*)','static', 
    '/', 'log',
    '/movie_rate(.*)','movie_rate',
    '/movie_comment(.*)', 'movie_comment',
    '/a(.*)','actor',
    '/c(.*)','catgory',
    '/p(.*)','photo',
    '/r(.*)','recommend'
)

user_id=''
render = web.template.render('templates') # your templates

login = form.Form(
    form.Textbox('keyword'),
    form.Button('Search'),
    
)

def func1(genre,year):
    vm_env.attachCurrentThread()
    lists=[]
    query = BooleanQuery()
    if genre!="111":  
        item=QueryParser(Version.LUCENE_CURRENT, "genre",analyzer).parse(genre)
        query.add(item, BooleanClause.Occur.MUST)
    if year!="111":
        item=QueryParser(Version.LUCENE_CURRENT, "year",analyzer).parse(year)
        query.add(item, BooleanClause.Occur.MUST)
    sf=SortField("score",SortField.Type.STRING,True)
    s=Sort(sf)
    scoreDocs = searcher1.search(query, 20,s).scoreDocs
    for scoreDoc in scoreDocs:
        movie=[]
        doc = searcher1.doc(scoreDoc.doc)
        movie.append(doc.get("url"))
        movie.append(doc.get("picture"))
        movie.append(doc.get("title"))
        movie.append(doc.get("score"))
        movie.append(doc.get("genre"))
        movie.append(doc.get("stars"))
        movie.append(doc.get("comments"))
        lists.append(movie)
    return lists
        

def func2(name):
    vm_env.attachCurrentThread()
    lists=[]
    query = BooleanQuery()
    
    item = QueryParser(Version.LUCENE_CURRENT, "name",analyzer).parse(name)
    query.add(item, BooleanClause.Occur.MUST)
    scoreDocs = searcher2.search(query, 20).scoreDocs
    for scoreDoc in scoreDocs:
        list=[]
        doc = searcher2.doc(scoreDoc.doc)
        list.append(doc.get("picture"))
        list.append(doc.get("url"))
        list.append(doc.get("name"))
        lists.append(list)
    return lists
def searchface(imgpath):
    f=open('index2_stars.txt','r')
    doc={}
    for i in f.readlines():
        l=i.split()
        t=[]
        t.append(l[1])
        t.append(l[2])
        t.append(l[3])
        doc[l[0]]=t
    path=os.path.abspath('stars_faces')
    imglist=[]
    labels=[]
    r=[]
    for filename in os.listdir(path):
        labels.append(filename)
        img=os.path.join('stars_faces/',filename)
        new_image=face_recognition.load_image_file(img);
        imglist.append(new_image)
    unknown_image = face_recognition.load_image_file(imgpath);
    encodinglist=[]
    for i in imglist:
        newencoding=face_recognition.face_encodings(i)[0]
        encodinglist.append(newencoding)
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces(encodinglist, unknown_encoding )
    for i in range(0, len(results)):
        if results[i] == True:
            r.append(doc[labels[i]])
    return r
  
def search_kw(kw,mode):
    vm_env.attachCurrentThread()
    lists=[]
    l=jieba.cut(kw)
    query = BooleanQuery()
    for i in l:
        ii = QueryParser(Version.LUCENE_CURRENT, "introduction",analyzer).parse(i)
        query.add(ii, BooleanClause.Occur.MUST)
    if mode:
        sf=SortField("score",SortField.Type.STRING,True)
        s=Sort(sf)
    else:
        sf=SortField("comments",SortField.Type.FLOAT,True)
        s=Sort(sf)
    scoreDocs = searcher1.search(query, 20,s).scoreDocs
    for scoreDoc in scoreDocs:
        movie=[]
        doc = searcher1.doc(scoreDoc.doc)
        ####
        movie.append(doc.get("url"))
        movie.append(doc.get("picture"))
        movie.append(doc.get("title"))
        movie.append(doc.get("score"))
        movie.append(doc.get("genre"))
        movie.append(doc.get("stars"))
        movie.append(doc.get("comments"))
        #####
        lists.append(movie)
   
    return lists
def search_id(mv_id):
    vm_env.attachCurrentThread()
    lists=[]
    query = BooleanQuery()
    clause = QueryParser(Version.LUCENE_CURRENT, "id",analyzer).parse(mv_id)
    query.add(clause, BooleanClause.Occur.MUST)
    scoreDocs = searcher1.search(query,1).scoreDocs
    for scoreDoc in scoreDocs:
        movie=[]
        doc = searcher1.doc(scoreDoc.doc)
        ####
        movie.append(doc.get("url"))
        movie.append(doc.get("picture"))
        movie.append(doc.get("title"))
        movie.append(doc.get("score"))
        movie.append(doc.get("genre"))
        movie.append(doc.get("stars"))
        movie.append(doc.get("comments"))
        #####
        lists.append(movie)
    
    return lists 

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
  
            path = os.path.join(root, filename)          
            match_num=match(path,target)          
            if match_num>max_match:
                max_match=match_num
                film_id=filename
            
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

      
class static:
    def GET(self, media, file):
        f = open(media+'/'+file, 'r')
        return f.read()

class log:
    def GET(self):
        return render.log()


class movie_rate:
    def GET(self,src):
        data=web.input()
        if src=='_s':
            return render.movie_rate([])
        else:
            return render.movie_rate(search_kw(data.kw,1))

class movie_comment:
    def GET(self,src):
        data=web.input()
        if src=='_s':
            return render.movie_comment([])
        else:
            return render.movie_comment(search_kw(data.kw,0))
        

class catgory:
    def GET(self,src):
        if src=='_s':
            return render.catgory([])
        else:
            data = web.input()
            return render.catgory(func1(data.genre,data.year))
    

class actor:
    def GET(self,src):
        data = web.input()
        if src=='_s':
            return render.actor([])
        elif data.type=='1':
            return render.actor(func2(data.kw))
        else:
            return render.actor(searchface(data.kw))

class photo:
    def GET(self,src):
        data=web.input()
        if src=='_s':
            return render.photo([])
        else:
            print search_photo(data.kw)
            return render.photo(search_id(search_photo(data.kw)))

class recommend:
    def GET(self,src):
        if src=='_log':
            data=web.input()
            global user_id
            user_id=data.logname
        global W
        global train
        rank = dict()
        ru=train[user_id] 
        for i, pi in ru.items(): 
            
            for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:10]:
                if j in ru: 
                    continue
                if j not in rank.keys():
                    rank[j]=0
                rank[j] += float(pi) * wj
        lists=[]
        for mv_id,s in sorted(rank.items(), key=itemgetter(1), reverse=True):
            lists+=search_id(mv_id)
        return render.recommend(lists)

if __name__ == "__main__":
    
    
    
    app = web.application(urls, globals())
    app.run()
