import pymysql
import tkinter as tk

def ConnectSql():
    conn = pymysql.connect(host="localhost",port=3306,user='root',password="123456")
    cur = conn.cursor()#生成游标对象
    return conn,cur

def Closesql(conn,cur):
    cur.close()
    conn.close()
    return

#根据页面具体内容，设定合适的页面大小和滚动条滚动范围
def generateWindow(root,type):
    #主页面且无用户登录
    if type=="M_no":
        canvas = tk.Canvas(root, bg="grey", width=800, height=600)
        canvas.place(x=0, y=0)
        myframe = tk.Frame(canvas)
        canvas.create_window((400, 300), window=myframe)
    #主页面有用户登录/搜索页面/浏览记录页面
    elif type=="M_yes" or type=="S" or type=="B":
        canvas = tk.Canvas(root, bg="grey", width=800, height=600, scrollregion=(0, 0, 800, 900))
        canvas.place(x=0, y=0)
        myframe = tk.Frame(canvas)
        vbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        vbar.place(x=780, y=40, width=20, height=600)
        vbar.configure(command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        canvas.create_window((390, 460), window=myframe)
    #电影信息页面
    elif type=="I":
        canvas = tk.Canvas(root, bg="grey", width=800, height=600, scrollregion=(0, 0, 800, 1000))
        canvas.place(x=0, y=0)
        myframe = tk.Frame(canvas)
        vbar = tk.Scrollbar(root, orient=tk.VERTICAL)
        vbar.place(x=780, y=40, width=20, height=600)
        vbar.configure(command=canvas.yview)
        canvas.configure(yscrollcommand=vbar.set)
        canvas.create_window((390, 500), window=myframe)
    return myframe