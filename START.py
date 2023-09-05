import tkinter as tk
import GlobalVar
import TkinterGUI.main_window

#项目入口
if __name__ == "__main__":
    #加载主页面的窗体
    Root = GlobalVar.BigWindow
    screenWidth, screenHeight = Root.maxsize()
    cen_x = (screenWidth - 800) / 2
    cen_y = (screenHeight - 600) / 2
    Root.geometry('800x600+%d+%d'% (cen_x, cen_y))
    Root.title("Film Recommendation System")
    Root.resizable(False, False)
    #无登录用户情况
    TkinterGUI.main_window.Main_window(Root,1,None)
    #2号用户登录情况
    #TkinterGUI.main_window.Main_window(Root,1,2)
    Root.mainloop()

