from tkinter import PhotoImage, messagebox, ttk,Tk,Canvas,filedialog,Toplevel,VERTICAL,Frame,RIGHT,Y,LEFT,BOTH#,Scrollbar
from uuid import uuid4
from PIL import ImageTk,Image
from os import path,getcwd


# version情報
# version v 1.0 : リリースバージョン
# version v 1.1 : インストーラーの改善
# version v 1.2 : サイドバーの追加
#                  (情報が空で登録した場合に常駐プログラムがエラーを出す問題の修正)
__version__ = "r 1.2"

class Tooltip:
    def __init__(self, widget, text, method):
        self.widget = widget
        self.text = text
        self.method = method
        if method[0] == "tag":
            self.widget.tag_bind(method[1],"<Enter>", self.enter)
            self.widget.tag_bind(method[1],"<Leave>", self.leave)
        elif method[0] == "def":
            self.widget.bind("<Enter>", self.enter)
            self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        x = y = 0
        if self.method[0] == "def":
            x, y, cx, cy = self.widget.bbox("insert")
        elif self.method[0] == "tag":
            x, y, cx, cy = self.widget.bbox(self.method[1])
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        self.tw = Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = ttk.Label(self.tw, text=self.text, justify='left',
                      background="#ffffff", relief='solid', borderwidth=1,
                      )
        label.pack(ipadx=1)

    def leave(self, event=None):
        if self.tw:
            self.tw.destroy()

class main:
    def __init__(self) -> None:
        self.main_frame = []
        self.time_entry = []
        self.path_entry = []
        self.get_path_button = []
        self.sumple_image = []
        self.sumple_image_x_length = []
        self.put_count = 0
        self.time_and_pic = [[],[]]
        self.Main_App = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer')
        self.header_img = Image.new("RGB",(500,50),(255,255,255))
        #self.Main_App = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer')
    def view_usecase(self):
        #ブラウザを開く
        from webbrowser import open as open_webbrowser
        self.url = 'https://github.com/mikatan-mikan/backgroud_changer/blob/main/README.md'
        open_webbrowser(self.url)
    def pressed(self,event):
        try:
            self.put_obj()
        except: pass
        finally:
            for i in range(len(self.sumple_image)):
                try:
                    item_id = self.canvas.find_withtag(f"sumple_image{i}")
                    x, y = self.canvas.coords(item_id)
                    if abs((x)-event.x)<=self.sumple_image_x_length[i] and abs((y) -event.y)<=20:
                        self.canvas.delete(f"sumple_image{i}")
                        self.path_entry[i].delete(0,len(self.path_entry[i].get()))
                except:continue
    def get_path(self,button_num):
        def nest():
            self.path = filedialog.askopenfilename()
            if self.path == "":
                pass
            else:
                self.path_entry[button_num].delete(0,len(self.path_entry[button_num].get()))
                self.path_entry[button_num].insert(0,self.path)
                self.sumple_image[button_num] = Image.open(self.path)
                self.sumple_image[button_num] = self.sumple_image[button_num].resize((int(40 * (self.sumple_image[button_num].size[0] / self.sumple_image[button_num].size[1])),40))
                self.sumple_image_x_length[button_num] = int(self.sumple_image[button_num].size[0] / 2)
                self.sumple_image[button_num] = ImageTk.PhotoImage(self.sumple_image[button_num])
                self.canvas.delete(f"sumple_image{button_num}")
                self.canvas.create_image(390 , button_num * 40 + 40, image=self.sumple_image[button_num],tags=f"sumple_image{button_num}")
        return nest
    def put_obj_fir(self):
        # self.header_img = ImageTk.PhotoImage(image = self.header_img)
        # self.canvas.create_line(500,0,500,240,fill="black")
        self.tip = Tooltip(self.canvas, "クリックして背景画像を追加",["tag","add_button"])
        # self.logo_img = Image.open(f"{self.Main_App}\\assets\\picture\\icon\\logo_gradation_left.png")
        # self.logo_img = self.logo_img.resize((150,150))
        # self.logo_img = ImageTk.PhotoImage(self.logo_img)
        # self.canvas.create_image(650, 0, image=self.logo_img,tags="header")
        # self.canvas.create_image(0, 0, image=self.header_img,tags="header")
    def put_obj(self):
        def save():
            from json import dump
            from os import path,makedirs
            from shutil import copy,rmtree
            save_json_list = []
            dic = []
            dumps_dir = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer')
            #dumps_dir = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer')
            rmtree(dumps_dir+'\\'+'picture')
            if path.exists(dumps_dir) == False:
                makedirs(dumps_dir)
            if path.exists(dumps_dir+'\\'+'picture') == False:
                makedirs(dumps_dir+'\\'+'picture')
            self.time_and_pic[0].clear()
            self.time_and_pic[1].clear()
            for i in range(len(self.time_entry)):
                if self.time_entry[i].get() == "":
                    continue
                self.time_and_pic[0].append(self.time_entry[i].get())
                self.time_and_pic[0][-1] = float(self.time_and_pic[0][-1].replace(":","."))
                self.time_and_pic[1].append(self.path_entry[i].get())
            #バブルソート
            #self.time_and_pic = sorted(self.time_and_pic,key = self.time_and_pic[0])
            change = True
            while change:
                change = False
                for i in range(len(self.time_and_pic[0]) - 1):
                    if self.time_and_pic[0][i] > self.time_and_pic[0][i + 1]:
                        self.time_and_pic[0][i], self.time_and_pic[0][i + 1] = self.time_and_pic[0][i + 1], self.time_and_pic[0][i]
                        self.time_and_pic[1][i], self.time_and_pic[1][i + 1] = self.time_and_pic[1][i + 1], self.time_and_pic[1][i]
                        change = True
            for i in range(len(self.time_entry)):
                self.time_and_pic[0][i] = format(self.time_and_pic[0][i],'.2f')

            with open(f"{dumps_dir}/config.json","w") as pic_file:
                cnt = 0
                for i in range(len(self.time_and_pic[0])):
                    if self.time_and_pic[1][i] == "" or self.time_and_pic[0][i] == "":
                        continue
                    copy(self.time_and_pic[1][i],f"{dumps_dir}/picture/{path.basename(self.time_and_pic[1][i])}")
                    self.time_and_pic[0][i] = str(self.time_and_pic[0][i]).replace(".",":")
                    if i >= 1 and self.time_and_pic[0][i - 1] == self.time_and_pic[0][i]:#2枚目以降であつ一枚前の画像と現在の画像の表示時刻が同じなら
                        dic.append({"time":self.time_and_pic[0][i],"path":f"{dumps_dir}\\picture\\{path.basename(self.time_and_pic[1][i])}"})
                    else:
                        if cnt > 0:
                            cnt = 0
                            save_json_list.append(dic)
                        cnt += 1
                        dic = [{"time":self.time_and_pic[0][i],"path":f"{dumps_dir}\\picture\\{path.basename(self.time_and_pic[1][i])}"}]
                if dic != []:
                    save_json_list.append(dic)
                save_json_list.append([{"time":"99:00","path":f"{uuid4()}","mode":f"{self.mode_box.get()}"}])
                dump(save_json_list,pic_file,indent=4)
            messagebox.showinfo("完了","保存しました\n画像の切り替えは60秒ごとにチェックされます")
        class view_set():
            def __init__(self):
                self.time_list = []
                self.path_list = []
                self.image_list = []
                self.change_y = 5
            def read_json(self):
                from json import load
                from os import path
                self.time_list = []
                self.path_list = []
                self.image_list = []
                json_path = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer\config.json')
                #json_path = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer\config.json')
                with open(json_path,"r") as json_file:
                    json_list = load(json_file)
                for i in range(len(json_list)-1):
                    self.image_list.append([])
                    for j in range(len(json_list[i])):
                        self.time_list.append(json_list[i][j]["time"])
                        self.path_list.append(json_list[i][j]["path"])
                        self.image_list[i].append(Image.open(json_list[i][j]["path"]))
                        self.image_list[i][j] = self.image_list[i][j].resize((int(128 * (self.image_list[i][j].size[0] / self.image_list[i][j].size[1])),128))
                        self.image_list[i][j] = ImageTk.PhotoImage(self.image_list[i][j])
            def put_obj(self):
                additional_num = 0
                for i in range(5):
                    self.canvas.create_text(100 + (i )* 512,30,text="変更時刻",font=("",10))
                    self.canvas.create_text(350 + (i )* 512,30,text="画像",font=("",10))
                for i in range(len(self.image_list)):
                    for j in range(len(self.image_list[i])):
                        self.canvas.create_image(350 + ((i + j + additional_num) // self.change_y )* 512,((i + j + additional_num) % self.change_y)*128+120,image=self.image_list[i][j],tags=f"sumple_image{i}")
                        if j > 0:
                            additional_num += 1
                for i in range(len(self.time_list)):
                    self.canvas.create_text(100 + (i // self.change_y )* 512,(i % self.change_y)*128+120,text=self.time_list[i],font=("",10))
            def main(self):
                self.read_json()
                self.root = Toplevel()
                self.root.title("現在の設定")
                wid_size , hei_size = ((len(self.time_list) // self.change_y )+ 1 )* 512 , 512 + 256 if len(self.time_list) >= 5 else len(self.time_list) * 128 + 120
                self.canvas = Canvas(self.root,width=wid_size,height=hei_size)
                self.canvas.pack()
                self.put_obj()
                self.root.mainloop()
        self.put_count += 1
        self.main_frame.append(Frame(self.canvas))
        self.update_window(self.put_count)
        # self.root.geometry(f"700x{100 + self.put_count * 40}")
        try:
            self.plus_image = PhotoImage(file=f"{getcwd()}/assets/picture/button/plus_button.png")
        except:
            self.plus_image = PhotoImage(file=f"{self.Main_App}/assets/picture/button/plus_button.png")
        # 背景をrootのbgと同様に
        ttk.Label(text = "\n   切り替え時刻    |   画像のファイルパス                     |                                |    選択画像          ").place(x = 0,y = 0)
        # self.time_entry.append(ttk.Spinbox(self.canvas,format='%1:2f',from_="0:00",to="24:00",width=5))
        # 先頭に空白
        ttk.Label(self.main_frame[-1],text="").pack(padx = 10,side='left')
        self.time_entry.append(ttk.Entry(self.main_frame[-1],width=5))
        self.time_entry[self.put_count - 1].pack(padx = 10,side='left')
        self.time_entry[self.put_count - 1].insert(0,"0:00")
        self.path_entry.append(ttk.Entry(self.main_frame[-1],width=25))
        self.path_entry[self.put_count - 1].pack(padx = 10,side='left')
        self.sumple_image.append(0)
        self.sumple_image_x_length.append(0)
        self.get_path_button.append(ttk.Button(self.main_frame[-1],text='参照',command=self.get_path(self.put_count - 1)))
        self.get_path_button[self.put_count - 1].pack(padx = 10,side = 'left')
        try:
            self.tip.leave()
        except:pass
        self.canvas.delete("add_button")
        #登録上限数
        if self.put_count < float('inf'):
            self.canvas.create_image(440,self.put_count * 40 - 15,image=self.plus_image,anchor='nw',tag='add_button')
            self.bind()
        if self.put_count == 1:
        #     self.save_button.place_forget()
        #     self.view_set_button.place_forget()
        #     self.mode_box.place_forget()
        # else :
            self.save_button = ttk.Button(self.root,text='設定を保存する',command=save)
            self.view_set_button = ttk.Button(self.root,text='現在の設定を見る',command=view_set().main)
            modes = ("rand","change")
            self.mode_box = ttk.Combobox(self.root, height=3,values=modes,state="readonly",width=10)
            self.mode_box.current(1)
            self.save_button.place(x=600,y=150 + 30)
            self.view_set_button.place(x=600,y=150 + 60)
            self.mode_box.place(x=600,y=152)
            self.view_usecase_button = ttk.Button(self.root,text='使用方法',command=self.view_usecase)
            self.view_usecase_button.place(x=520,y=150 + 60)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        #一番下までスクロール
        self.canvas.yview_scroll(100, "units")

    def update_window(self,num):
        self.canvas.create_window(0,num * 40 - 10 - 2, window=self.main_frame[num], anchor='nw')
        self.main_frame[num].update_idletasks()
    def bind(self):
        def on_scroll(event):
            scroll_amount = -1 * event.delta // 120
            self.canvas.yview_scroll(scroll_amount, "units")
        self.canvas.bind("<MouseWheel>", on_scroll)
        self.canvas.tag_bind("add_button","<Button-1>",self.pressed)
    def update_scroll_region(self,event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.ybar.set(0.0,1.0)
    def main(self):
        self.root = Tk()
        self.root.title('background changer')
        self.root.geometry('700x250+0+0')
        #サイズを固定
        self.root.resizable(False,False)
        #アイコン
        try:
            self.root.iconbitmap(f"{getcwd()}/assets/picture/icon/mg.ico")
        except:
            self.root.iconbitmap(f"{self.Main_App}/assets/picture/icon/mg.ico")
        self.canvas = Canvas(self.root,width=500,height=100,borderwidth=0,highlightthickness=0)
        

        self.ybar = ttk.Scrollbar(self.canvas, orient=VERTICAL)
        self.ybar.pack(side=RIGHT, fill=Y,padx=200)
        self.ybar.config(command=self.canvas.yview)
        self.canvas.config(yscrollcommand=self.ybar.set)
        self.main_frame.append(Frame(self.canvas))
        self.update_window(0)
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind("<Configure>", self.update_scroll_region)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.put_obj_fir()
        self.put_obj()
        self.root.mainloop()

if __name__ == "__main__":
    main_pg = main()
    main_pg.main()