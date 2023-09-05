import requests
from PIL import Image,ImageTk
import io
from lxml import etree
import re
import tkinter as tk
import tkinter.messagebox
import GlobalFun
import time
import RecommendationAlogrithm.OnlineRecommend

def get_movie_url(movieid):
    '''
    :param movieid:
    :return: url_imdbid
    根据movieid得到对应的网页链接
    '''
    #抓取movieid对应的imdbid
    conn, cur = GlobalFun.ConnectSql()
    cur.execute("select imdbid from movierecommender.links where movieId = {}".format(movieid))
    imdbid = str(cur.fetchall()[0][0])
    GlobalFun.Closesql(conn,cur)
    #0114709
    imdbid = "0" * (7 - len(imdbid)) + imdbid
    print(imdbid)
    url_imdbid = "http://www.imdb.com/title/tt{}/".format(imdbid)
    return url_imdbid

def get_src(url,movieId):
    """
    :param url:
    :return: src,title,date,genres
    根据网页连接和数据库，抓取电影海报地址，电影名称，电影上映时间，电影类型
    """
    html = requests.get(url)
    bs = etree.HTML(html.text)
    src = bs.xpath('//link[@rel="image_src"]/@href')[0]
    conn,cur = GlobalFun.ConnectSql()
    sql = "select title,genres from movierecommender.movies where movieid = {}".format(movieId)
    cur.execute(sql)
    data = cur.fetchall()
    text = bs.xpath('//script[@type="application/ld+json"]')[0].text
    briefinfo = re.findall('^.*?"description": "(.*?)",\n  "date',text,flags=re.S)[0].strip(', "')
    title = re.findall('(.*)\(', data[0][0])[0].strip(' ')
    date = re.findall('\((\d*)\)', data[0][0])[0].strip(' ')
    genres_list = data[0][1].strip('\r').split('|')
    genres = "\n".join(genres_list)
    GlobalFun.Closesql(conn,cur)
    return src,title,date,genres,briefinfo

def resize(w, h, w_box, h_box, pil_image):
    '''resize a pil_image object so it will fit into a box of size w_box times h_box,but retain aspect ratio'''
    f1 = 1.0 * w_box / w
    f2 = 1.0 * h_box / h
    factor = min([f1, f2])
    width = int(w * factor)
    height = int(h * factor)
    return pil_image.resize((width, height), Image.ANTIALIAS)

def get_image(src,w_box=80,h_box=120):
    html = requests.get(src).content
    data_stream = io.BytesIO(html)
    pil_image = Image.open(data_stream)  # 转成pil格式的图片
    w, h = pil_image.size
    pil_image_resized = resize(w, h, w_box, h_box, pil_image)
    tk_image = ImageTk.PhotoImage(pil_image_resized)  # 转tk_image
    return tk_image

def destroy(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def get_score(userid,movieid):
    conn, cur = GlobalFun.ConnectSql()
    # 获取用户打分信息
    sql = "select rating,timestamp from movierecommender.ratings where movieid={} and userid={};".format(movieid,userid)
    cur.execute(sql)
    data = cur.fetchall()
    GlobalFun.Closesql(conn,cur)
    return data

# 未评分部分GUI
class rating_frame():
    def __init__(self,window,type,userid,movieid):
        self.window = window
        self.type = type
        self.Content = tk.StringVar()
        self.Rating_Frame = tk.Frame(self.window)
        self.Entry = tk.Spinbox(self.Rating_Frame, from_=1, to=5, textvariable=self.Content,width=5)
        self.Entry.pack(side="left")
        tk.Label(self.Rating_Frame, text=' ').pack(side="left")
        self.B = tk.Button(self.Rating_Frame, text="rate",command=self.rate)
        self.B.pack(side="left")
        self.Rating_Frame.place(x=110,y=360,anchor="nw")
        self.userid=userid
        self.movieid=movieid

    def rate(self):
        try:
            Score = eval(self.Content.get())
            userid=self.userid
            movieid=self.movieid
            if isinstance(Score,int) and Score <= 5 and Score >= 0:
                timestamp=int(time.time())
                rate_score = Score
                conn, cur = GlobalFun.ConnectSql()
                if self.type == "edit":
                    sql = "update movierecommender.ratings set userid={},movieid={},rating={},timestamp={} where userid={} and movieid={};".format(userid, movieid,Score, timestamp,userid, movieid,Score)
                else:
                    sql = "insert into movierecommender.ratings values({},{},{},{});".format(userid, movieid,Score, timestamp)
                cur.execute(sql)
                conn.commit()
                GlobalFun.Closesql(conn,cur)
                tk.messagebox.showinfo(title="successed!", message="Thank you for your rating!",command=destroy(self.Rating_Frame))
                self.Rating_Frame.destroy()
                print('problem is destroy')
                rated_frame(self.window,rate_score,timestamp,userid,movieid)
                print('prolem is trigger')
                #触发在线推荐名单的改变
                print("userid is",userid,"movieid is ",movieid)
                RecommendationAlogrithm.OnlineRecommend.updateonline(userid, movieid)
                print('prolem is here')
            else:
                tk.messagebox.showwarning(title="failed!",message="sorry,the score must be an integer from 1 to 5\nplease modify and rate again.")
                self.Content.set(3)
        except:
            tk.messagebox.showwarning(title="failed!",message="sorry,\nit has something wrong with the program\nplease modify and rate again.")
            self.Content.set(3)

class rated_frame():
    def __init__(self,window,userrate,ratetime,userid,movieid):
        self.window = window
        self.Rated_Frame = tk.Frame(self.window)
        self.L = tk.Label(self.Rated_Frame,text="Your Rate:{}\ttime:{}".format(userrate,time.strftime("%Y-%m-%d %H:%M",time.localtime(ratetime))))
        self.L.pack()
        self.B = tk.Button(self.Rated_Frame,text="modify",command=self.modify)
        self.B.pack()
        self.Rated_Frame.place(x=40,y=360,anchor="nw")
        self.userid=userid
        self.moiveid=movieid

    def modify(self):
        self.Rated_Frame.destroy()
        rating_frame(self.window,"edit",self.userid,self.moiveid)

# 用户已登录情况的电影信息页的分数区域
class basedFrame():
    def __init__(self,window,userid,moiveid):
        self.window = window
        self.userid = userid
        self.movieid = moiveid
        data = get_score(self.userid,self.movieid)
        # 用户未评分
        if len(data) == 0:
            rating_frame(self.window,"insert",self.userid,self.movieid)
        # 用户已评分
        else:
            timestamp, userrate = data[0][1], data[0][0]
            rated_frame(self.window,userrate,timestamp,self.userid,self.movieid)

def get_similar_movie_list(movieId,type="ALS"):
    conn, cur = GlobalFun.ConnectSql()
    if type == "SVD":
        sql = "select similarId,similarDegree from movierecommender.movie_similar_svd where movieId={} order by similarDegree desc limit 5;".format(movieId)
    else:
        sql = "select similarId,similarDegree from movierecommender.movie_similar_als where movieId={} order by similarDegree desc limit 5;".format(movieId)
    cur.execute(sql)
    data = cur.fetchall()
    return data
