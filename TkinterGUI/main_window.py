import tkinter as tk
import GlobalFun
import threading
import TkinterGUI.metaFrame
import TkinterGUI.browseFootprints
global Images
import TkinterGUI.metaButtons
Images=[]

# 导航栏Frame(指向metaButtons)
# 无用户登录时显示请先登录Label、热门电影Frame
# 有用户登录时显示热门电影Frame、离线推荐Frame、在线推荐Frame

class Main_window():

    def __init__(self,root,movieid,userid):
        self.movieid = movieid
        self.userid = userid
        self.root = root

        #主页面分为无用户登录和有用户登录的情况
        if userid is None:
            self.window = GlobalFun.generateWindow(self.root,"M_no")
        else:
            self.window = GlobalFun.generateWindow(self.root, "M_yes")

        #导航栏布局
        navbar_Frame = tk.Frame(self.root, width=800, height=40)
        navbar_Frame.pack_propagate(False)
        navbar_Frame.place(x=0,y=0,anchor="nw")
        #主页面类型的导航栏
        TkinterGUI.metaButtons.NavigationBar(self.root,self.window,navbar_Frame,self.movieid,self.userid,type="M")

        #无用户登录的主页
        if userid is None:
            tk.Label(self.window,text="RecSystem Failed :(\nPlease login or register first",font=('',20))\
                .grid(row=0,column=0,rowspan=6,pady=50)
            tk.Label(self.window, text='Hot Movies',font=("",15)).grid(row=7,column=0)
            self.hotmovieFrame = tk.Frame(self.window)
            self.hotmovieFrame.grid(row=8,column=0,sticky=tk.N) # 放置热门电影
            self.hotmovie()
            tk.Label(self.window).grid(row=9, column=0,pady=50)
        #有用户登录的主页
        else:
            #放置热门电影
            tk.Label(self.window, text='Hot Movies',font=('',15)).grid(row=1,column=0)
            self.hotmovieFrame = tk.Frame(self.window)
            self.hotmovieFrame.grid(row=2,column=0,rowspan=3)
            self.hotmovie()

            #放置基于SVD的离线推荐
            tk.Label(self.window, text='\nOffline RecSys Based on SVD',font=('',15)).grid(row=6,column=0)
            self.offline_rec_svdFrame = tk.Frame(self.window,width=800,height=150)
            self.offline_rec_svdFrame.grid(row=7,column=0,rowspan=3)
            self.offline_rec_svd()

            #放置基于ALS的离线推荐
            tk.Label(self.window, text='\nOffline RecSys Based on ALS',font=('',15)).grid(row=10,column=0)
            self.offline_rec_alsFrame = tk.Frame(self.window)
            self.offline_rec_alsFrame.grid(row=11,column=0,rowspan=3)
            self.offline_rec_als()

            #放置在线推荐
            tk.Label(self.window,text="\nOnline RecSys",font=('',15)).grid(row=15,column=0)
            self.online_rec_Frame = tk.Frame(self.window)
            self.online_rec_Frame.grid(row=17,column=0,rowspan=3)
            self.online_rec()

    def hotmovie(self):
        conn,cur = GlobalFun.ConnectSql()
        #查询被打分次数最多的电影，选前五作为热门电影
        cur.execute('select movieid,count(1) from movierecommender.ratings group by movieid order by count(1) desc limit 5;')
        data = cur.fetchall()#拿到最热门的5部电影
        GlobalFun.Closesql(conn,cur)
        for tup in data:
            t = threading.Thread(target=self.job,args=(self.hotmovieFrame,tup[0]))
            t.start()

    def offline_rec_svd(self):
        conn, cur = GlobalFun.ConnectSql()
        cur.execute(
            'select recommendid from movierecommender.offline_recommend_svd where userid={} order by predictScore desc limit 5;'.format(self.userid))
        data = cur.fetchall()  # 拿到离线用户推荐信息
        GlobalFun.Closesql(conn, cur)
        print(data)
        print(len(data))
        if len(data) == 0:
            tk.Label(self.offline_rec_svdFrame,text="Sorry T^T\nI haven't know you a long time\nGive me some time to recommend for you!",font=('',20)).pack(side='bottom')
        else:
            for tup in data:
                t = threading.Thread(target=self.job, args=(self.offline_rec_svdFrame, tup[0]))
                t.start()


    def offline_rec_als(self):
        conn, cur = GlobalFun.ConnectSql()
        cur.execute(
            'select recommendid from movierecommender.offline_recommend_als where userid={} order by predictScore desc limit 5;'.format(self.userid))
        data = cur.fetchall()  # 拿到离线用户推荐信息
        GlobalFun.Closesql(conn, cur)
        print(data)
        print(len(data))
        if len(data) > 0:
            for tup in data:
                t = threading.Thread(target=self.job, args=(self.offline_rec_alsFrame, tup[0]))
                t.start()

    def online_rec(self):
        conn, cur = GlobalFun.ConnectSql()
        cur.execute(
            'select movieid from movierecommender.online_recommend where userid = {} limit 5;'.format(
                self.userid))
        data = cur.fetchall()  # 拿到离线用户推荐信息
        GlobalFun.Closesql(conn, cur)
        print(data)
        print(len(data))
        for tup in data:
            t = threading.Thread(target=self.job, args=(self.online_rec_Frame, tup[0]))
            t.start()

    def job(self, Frame, movieid):
        temp = TkinterGUI.metaFrame.metaFrame(movieid, self.userid, Frame, self.window, self.root)
        Images.append(temp.tk_image)
        temp.frm.pack(side='left')


