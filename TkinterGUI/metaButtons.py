#将所有主页上涉及到的按钮统一在这个模块中
#一共是分为4种页面
# IMBS
# I：电影信息页
# M：推荐主页
# B：用户浏览页
# S：搜索页面

import TkinterGUI.browseFootprints
import TkinterGUI.main_window
import TkinterGUI.movieInfo_window
import TkinterGUI.search_window
import RecommendationAlogrithm.OnlineRecommend
import tkinter as tk
import GlobalVar
import GlobalFun
import tkinter.messagebox

# 对登录/登出按钮设置属性和方法
class Login_register_Button():
    def __init__(self,root , window ,nagvibar, movieid , userid ,type="M"):
        self.movieid = movieid
        self.userid = userid
        self.window = window #当前的主幕布
        self.nagvibar = nagvibar#当前的小幕布
        self.root = root #窗口根目录
        self.type = type #确定所在的页面种类，方便刷新页面"M" "B" "I"

        #设置用户登录/登出按钮，已登录设置logout，未登录设置登录login
        s = tk.StringVar()
        if self.userid is None:
            s.set('Login | Register')
        else:
            s.set('Logout')
        self.Button = tk.Button(self.nagvibar,textvariable=s,command=self.trigger)

    def trigger(self):
        if self.userid is None:
            self.login()
        else:
            #开启毁灭模式
            print("I am destroying the Main_Frame")
            print('Prepare to create a new window')
            self.userid = None
            self.update()#刷新页面
            print('Well Done!')

    # 设置登录的弹出窗口
    def login(self):
        # 获得弹窗控件
        self.window_sign_up = tk.Toplevel(self.root)
        screenWidth, screenHeight = self.window_sign_up.maxsize()
        cen_x = (screenWidth - 460) / 2
        cen_y = (screenHeight - 350) / 2
        self.window_sign_up.geometry("460x350+%d+%d"% (cen_x, cen_y))
        self.window_sign_up.title('Login | Register')

        self.name = tk.StringVar()
        self.name.set("1~610")
        tk.Label(self.window_sign_up,text="UserId:").place(x=50,y=57)
        tk.Entry(self.window_sign_up,textvariable=self.name).place(x=103,y=57)

        self.password = tk.StringVar()
        tk.Label(self.window_sign_up,text="Password:").place(x=34,y=117)
        tk.Entry(self.window_sign_up,textvariable=self.password,show='*').place(x=103,y=117)

        #温馨提示
        tk.Label(self.window_sign_up,text="The recorded userId is from 1 to 610\n"
                                          "Password is identical to  userId\n"
                                          "If you want to register a new user,\n"
                                          "please start from 611.",justify='left').place(x=103,y=166)
        tk.Button(self.window_sign_up,text="Login | Register",command=self.comfirm).place(x=282,y=253)

    # 判断userid是否异常
    def comfirm(self):
        try:
            name = eval(self.name.get())
        except:
            tk.messagebox.showerror(message="The user name must be integer")
            self.login()
            return
        if not isinstance(name,int):
            tk.messagebox.showerror(message="The user name must be integer")
            self.login()
            return
        conn,cur = GlobalFun.ConnectSql()
        cur.execute("select password from movierecommender.users where userid={}".format(self.name.get()))
        data = cur.fetchall()
        if len(data)==0:
            #记录新用户
            cur.execute("insert into movierecommender.users values({},{})".format(self.name.get(),self.password.get()))
            conn.commit()
            tk.messagebox.showinfo(message="Welcome :>\nNew User:{}".format(self.name.get()))
            self.window_sign_up.destroy()
            self.userid = eval(self.name.get())

            #触发online_recommend添加上新用户的推荐列表

            ##############################################
            RecommendationAlogrithm.OnlineRecommend.insertnewuser(self.userid)
            self.update()#刷新页面
        else:
            #data形式:((....))
            if data[0][0] == self.password.get():
                tk.messagebox.showinfo(message="Welcome :D\n User:{}".format(self.name.get()))
                self.window_sign_up.destroy()
                self.userid = eval(self.name.get())
                self.update()
            else:
                tk.messagebox.showerror(message="Sorry :<\nThe password is wrong")
                self.login()

    def update(self):
        self.window.destroy()
        if self.type == "M" or self.type == "B":
            TkinterGUI.main_window.Main_window(self.root, self.movieid, self.userid)
        elif self.type == "I":
            TkinterGUI.movieInfo_window.movieinfo_window(self.root, self.movieid, self.userid)
        else:
            TkinterGUI.search_window.Search_window(self.root,self.movieid,self.userid)

# 对搜索按钮设置属性和方法
class Search_Button():
    def __init__(self , root , window , nagvibar, movieid, userid):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar#当前的小幕布
        self.window = window  # 当前的主幕布
        self.root = root  # 窗口根目录
        self.Button = tk.Button(self.nagvibar, text="Search", command=self.turn2search)

    def turn2search(self):
        self.window.destroy()
        TkinterGUI.search_window.Search_window(self.root, self.movieid, self.userid)
        print('Well Done!')

# 对返回主页按钮设置属性和方法
class Main_window_Button():
    def __init__(self , root , window , nagvibar, movieid, userid):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar#当前的小幕布
        self.window = window  # 当前的主幕布
        self.root = root  # 窗口根目录
        self.Button = tk.Button(self.nagvibar, text="Main Window", command=self.turn2main)

    def turn2main(self):
        self.window.destroy()
        TkinterGUI.main_window.Main_window(self.root, self.movieid, self.userid)
        print('Well Done!')

# 对浏览记录按钮设置属性和方法
class Browse_Button():
    def __init__(self , root , window ,nagvibar, movieid, userid):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar#当前的小幕布
        self.window = window  # 当前的幕布
        self.root = root  # 窗口根目录
        self.Button = tk.Button(self.nagvibar, text="BrowseFootprints", command=self.turn2Browse)

    def turn2Browse(self):
        self.window.destroy()
        TkinterGUI.browseFootprints.BrowseFootprints(self.root, self.movieid, self.userid)
        print('Well Done!')

# 导航栏显示类，根据窗体的页面类型，设置按钮的布局；根据用户的登录状态，设置显示的文字
class NavigationBar():
    def __init__(self , root , window , nagvibar, movieid, userid , type):
        self.movieid = movieid
        self.userid = userid
        self.nagvibar = nagvibar
        self.window = window  # 当前的幕布
        self.root = root  # 窗口根目录
        self.type = type

        if userid is not None:#在登陆状态
            tk.Label(self.nagvibar, text=' Welcome user No:{} ! ٩(๑❛ᴗ❛๑)۶'.format(self.userid), font=('', 15)).pack(side='left')
            tk.Label(self.nagvibar, text=' ').pack(side="right")
            Login_register_Button(self.root, self.window, self.nagvibar, self.movieid, self.userid,
                                  self.type).Button.pack(side="right")
            tk.Label(self.nagvibar, text=' ').pack(side="right")
            if self.type == "I" or self.type == "M" or self.type == "S":
                Browse_Button(self.root,self.window,self.nagvibar,self.movieid,self.userid).Button.pack(side="right")
                tk.Label(self.nagvibar, text=' ').pack(side="right")
            if self.type == "I" or self.type == "B" or self.type == "S":
                Main_window_Button(self.root,self.window,self.nagvibar,self.movieid,self.userid).Button.pack(side='right')
                tk.Label(self.nagvibar, text=' ').pack(side="right")
            if self.type != 'S':
                Search_Button(self.root, self.window, self.nagvibar, self.movieid, self.userid).Button.pack(
                    side="right")
                tk.Label(self.nagvibar, text=' ').pack(side="right")

        else:#非登陆状态
            tk.Label(self.nagvibar, text=' ').pack(side="right")
            Login_register_Button(self.root, self.window, self.nagvibar, self.movieid, self.userid,
                                  self.type).Button.pack(side="right")
            tk.Label(self.nagvibar, text=' ').pack(side="right")
            if self.type == "I" or self.type == "S":
                Main_window_Button(self.root, self.window,self.nagvibar, self.movieid, self.userid).Button.pack(side="right")
                tk.Label(self.nagvibar, text=' ').pack(side="right")
            if self.type != 'S':
                Search_Button(self.root, self.window,self.nagvibar, self.movieid, self.userid).Button.pack(side="right")
                searchcontent = tk.StringVar()
                tk.Label(self.nagvibar, text=' ').pack(side="right")

# 用于测试
if __name__ == "__main__":
    Root = GlobalVar.BigWindow
    Root.geometry('800x900')
    Frame = tk.Frame(Root,width=800,height=20,bg='black')
    Frame.pack_propagate(False)
    Frame.pack()
    # a = Login_register_Button(Root,Frame,1,1,type='B')
    NavigationBar(Root, Frame,Frame, 1, 1, type='I')
    # a = NavigationBar(Root, Frame, 1, None, type='B')

    Root.mainloop()
