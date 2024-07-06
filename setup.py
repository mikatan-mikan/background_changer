
from tkinter import Tk,Canvas,messagebox,NW,SE,ttk,BooleanVar
from shutil import copy,rmtree,copytree
from os import path,makedirs
from subprocess import run
from threading import Thread 
from uuid import uuid4
from json import dump
from PIL import ImageTk,Image

exec_path = ""

class progress_bar():
    def __init__(self) -> None:
        self.progress_false = Image.new("RGBA",(1,5),(64,64,64,255))
        self.progress_true = Image.new("RGBA",(1,3),(255,165,0,255))
        self.progress_true_buffer = 1
        self.letter_y = 110
        self.letter_offset_x = 0
        self.bar_size = 512
        self.side_image_size = 256
        self.now_progress = 0
    def set_property(self,letter: str,per: float) -> None:
        self.set_text(letter = letter)
        self.set_bar(per = per)
    def set_bar(self,per: float) -> None:
        """
        進捗バーを進める

        per     : 進捗度(per)
        """
        # percentから512段階に直す
        draw_area = per * 5.12 if per * 5.12 <= 512 else 512
        # すでに塗り終えたところから目標地点まで塗る
        for draw in range(self.now_progress,int(draw_area + 1)):
            self.canvas.create_image(self.side_image_size + 14 + draw + 1,self.side_image_size / 2 + self.progress_true_buffer,image = self.progress_true,anchor = NW)
        self.now_progress = draw
    def set_text(self,letter: str,delete: bool = True) -> None:
        """
        進捗バーの上部に状態を表示する

        leter   : 表示する文字
        delete  : 過去の文字の削除(存在しない場合はerr)
        """
        if delete:
            self.canvas.delete(self.put_letter)
        self.put_letter = self.canvas.create_text(self.side_image_size + self.bar_size - self.letter_offset_x,self.letter_y,text = letter,anchor = SE)
    def create(self,title: str,icon: str,image: str,window: Tk) -> None:
        """
        title   : ウィンドウの名前
        icon    : ウィンドウのアイコンパス
        image   : ウィンドウの左側に表示する画像のパス
        window  : TkまたはToplevelのインスタンス 但し、初期状態で呼び出す
        """
        def set_img(img) -> None:
            # __init__で読み込んだ画像をtkinter上に乗せるために変換
            self.progress_false = ImageTk.PhotoImage(image = self.progress_false)
            self.progress_true = ImageTk.PhotoImage(image = self.progress_true)
            # imgを読み込み、貼り付ける
            self.image = Image.open(fp=img)
            self.image = ImageTk.PhotoImage(image = self.image)
            self.canvas.create_image(0,0,image = self.image,anchor = NW)
            #初期状態の進捗バーを作成(灰色の横512 + 2px)
            for bar_draw_place in range(self.bar_size + 2):
                self.canvas.create_image(self.side_image_size + 14 + bar_draw_place,self.side_image_size / 2,image = self.progress_false,anchor = NW)
        self.root = window
        self.root.title(title)
        self.root.iconbitmap(icon)
        self.canvas = Canvas(self.root,width=self.side_image_size + 14 + self.bar_size + 2 + 5,height=self.side_image_size)
        self.canvas.pack()
        set_img(image)
        self.set_text(letter = "",delete = False)

class main:
    def install(self):
        import os

        global exec_path
        def create_short_cut(frm: path,to: path,name: path,icon: path):
            import comtypes.client
            #リンク先のファイル名
            target_file=frm
            #ショートカットを作成するパス
            save_path=to
            #WSHを生成
            wsh=comtypes.client.CreateObject("wScript.Shell",dynamic=True)
            #ショートカットの作成先を指定して、ショートカットファイルを開く。作成先のファイルが存在しない場合は、自動作成される。
            short=wsh.CreateShortcut(save_path)
            #以下、ショートカットにリンク先やコメントといった情報を指定する。
            #リンク先を指定
            short.TargetPath=target_file
            #コメントを指定する
            short.Description=name
            #引数を指定したい場合は、下記のコメントを解除して、引数を指定する。
            #short.arguments="/param1"
            #アイコンを指定したい場合は、下記のコメントを解除してアイコンのパスを指定する。
            short.IconLocation=icon
            #作業ディレクトリを指定したい場合は、下記のコメントを解除してディレクトリのパスを指定する。
            #short.workingDirectory="c:\\test\\"
            #ショートカットファイルを作成する
            short.Save()
        #ファイルをコピー
        self.progress.set_property("実行ファイルをコピー...",20.0)
        dumps_dir = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer')
        if not path.exists(dumps_dir):
            makedirs(dumps_dir)
        try:
            copy("./main.exe",f"{dumps_dir}\\main.exe")
        except:
            messagebox.showerror("エラー","実行ファイルのコピーに失敗しました。\nmain.exeが存在しない、又は現在起動中です")


        self.progress.set_property(letter = "常時実行ファイルのコピー...",per=40.0)
        if not path.exists(f"{dumps_dir}\\assets\\picture"):
            makedirs(f"{dumps_dir}\\assets\\picture")
        rmtree(f"{dumps_dir}\\assets\\picture")
        copytree("./assets/picture",f"{dumps_dir}\\assets\\picture")
        try:
            copy("./assets/main_pg/main.exe",f"{dumps_dir}/background_changer.exe")
        except:
            messagebox.showerror("エラー","実行ファイルのコピーに失敗しました。\n./assets/main_pg/main.exeが存在しない、又は現在起動中です")
            
        self.progress.set_property(letter = "ディレクトリ及びファイルの生成...",per=50.0)
        add_dir = path.expandvars(r'%LOCALAPPDATA%\MG_mikan\background_changer')
        try:
            rmtree(add_dir+'\\'+'picture')
        except:
            pass
        if path.exists(add_dir) == False:
            makedirs(add_dir)
        if path.exists(add_dir+'\\'+'picture') == False:
            makedirs(add_dir+'\\'+'picture')
        with open (f"{add_dir}\\config.json","w") as f:
            save_json_list = [[{"time":"99:00","path":f"{uuid4()}","mode":"change"}]]# [{"time": "99:00","path": "486e6eb1-7fc7-4d12-9cd7-a4f151575864","mode": "change"}]
            dump(save_json_list,f)
        

        if self.button_data[0]:
            self.progress.set_property(letter = "ショートカットを生成中...",per=70.0)
            create_short_cut(os.path.expanduser("%LOCALAPPDATA%\\MG_mikan\\background_changer\\main.exe"),os.path.expanduser("~\\Desktop\\background changer.lnk"),"background changer",f"{add_dir}\\assets\\picture\\icon\\mg.ico")

        self.progress.set_property(letter = "スタートアップに登録中",per=80.0)
        create_short_cut(f"{dumps_dir}/background_changer.exe",os.getenv('APPDATA') + r"\Microsoft\Windows\Start Menu\Programs\Startup\background changer.lnk","background changer",f"{add_dir}\\assets\\picture\\icon\\mg.ico")

        if self.button_data[1]:
            self.progress.set_property(letter = "アプリケーションメニューに登録中",per=90.0)
            create_short_cut(f"{dumps_dir}/main.exe",os.getenv('APPDATA') + r"\Microsoft\Windows\Start Menu\Programs\background changer.lnk","background changer",f"{add_dir}\\assets\\picture\\icon\\mg.ico")

        self.progress.set_property(letter = "完了",per=100.0)
        messagebox.showinfo("完了","インストールが終了しました。\nDeskTopにショートカットを作成しました。\nbackgroud changerを起動します")
        exec_path = dumps_dir
        self.root.destroy()
    def start_process(self):
        self.button_data = [self.short_bln.get(),self.menu_bln.get()]
        self.canvas.destroy()
        self.progress.create("BackGround Changer SetUp","./assets/picture/icon/haguruma.ico","./assets/picture/icon/logo_gradation.png",self.root)
        Thread(target = self.install).start()
    def set_obj(self):
        self.image = Image.open(fp="./assets/picture/icon/logo_gradation.png")
        self.image = ImageTk.PhotoImage(image = self.image)
        self.canvas.create_image(0,0,image = self.image,anchor = NW)
        # チェックONにする
        self.short_bln = BooleanVar()
        self.short_bln.set(True)
        self.menu_bln = BooleanVar()
        self.menu_bln.set(True)
        self.short_cut_button = ttk.Checkbutton(self.root,text="デスクトップにショートカットを作成する",variable=self.short_bln)
        self.short_cut_button.place(x = 200,y = 180)
        self.menu_cut_button = ttk.Checkbutton(self.root,text="アプリケーションメニューに表示する",variable=self.menu_bln)
        self.menu_cut_button.place(x = 200,y = 200)
        self.start_button = ttk.Button(self.root,text = "インストール",command=self.start_process)
        self.start_button.place(x = 300,y = 230)
    def main(self):
        self.root = Tk()
        self.progress = progress_bar()
        self.root.title("BackGround Changer Installer")
        self.root.iconbitmap("./assets/picture/icon/haguruma.ico")
        self.canvas = Canvas(self.root,width=400,height=256)
        self.canvas.pack()
        self.set_obj()
        self.root.mainloop()


def run_back_soft():
    global exec_path
    run(f"{exec_path}/background_changer.exe")
def run_main_soft():
    global exec_path
    run(f"{exec_path}/main.exe")

if __name__ == "__main__":
    main_ = main()
    main_.main()
    Thread(target = run_back_soft).start()
    Thread(target = run_main_soft).start()