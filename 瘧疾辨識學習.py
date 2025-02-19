'''
瘧疾辨識學習.py

用來學習辨識不同感染程度的紅血球
'''

from PIL import Image, ImageTk
import ttkbootstrap as ttk
import random

PLASMODIUM_TYPES = ("vivax","falciparum","malariae","ovale")
PLASMODUIM_STAGES = ("ring","trophozoite","pre schizont","post schizont","microgametocyte","macrogemetocyte")

CHOP_X = (112,464,819,1208,1580)
CHOP_Y = (131,418,753,1066,1401,1726,2023)

try:
    cell_photo = Image.open("assets.jpg")

except:
    import sys
    input("尚未匯入素材")
    sys.exit()

class App:
    def __init__(self) -> None:

        self.root = ttk.Window(title="瘧疾感染紅血球薄片辨識學習",themename="darkly",size=(600,600),resizable=(False,False))
        self.root.position_center()
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12))
        self.start_playing()
        self.root.mainloop()
    
    def start_playing(self) -> None:
        
        self.question_number = 1
        self.question_number_var = ttk.StringVar()
        self.question_number_var.set(f"第{self.question_number}題")

        self.correct_number = 0
        
        self.game_page = ttk.Frame(master=self.root)
        self.game_page.pack()
        self.question_number_label = ttk.Label(master=self.game_page,textvariable=self.question_number_var)
        self.question_number_label.pack()

        self.image = ttk.Label(master=self.game_page)
        self.image.pack(pady=10)

        answer_frame = ttk.Frame(master=self.game_page)
        answer_frame.pack(pady=20)

        ttk.Label(master=answer_frame,text="物種:").grid(row=0,column=0,padx=10)
        self.species_var = ttk.StringVar()
        species_box = ttk.Combobox(master=answer_frame,values=PLASMODIUM_TYPES,state=ttk.READONLY,textvariable=self.species_var)
        species_box.grid(row=0,column=1,padx=10,pady=10)

        ttk.Label(master=answer_frame,text="成長階段:").grid(row=1,column=0,padx=10)
        self.stage_var = ttk.StringVar()
        stage_box = ttk.Combobox(master=answer_frame,values=PLASMODUIM_STAGES,state=ttk.READONLY,textvariable=self.stage_var)
        stage_box.grid(row=1,column=1,padx=10,pady=10)

        self.check_btn = ttk.Button(master=self.game_page,text="確認",command=self.check_answer)
        self.check_btn.pack(pady=10)

        self.next_question()
    
    def next_question(self) -> None:
        using_species_index = random.randint(0,len(PLASMODIUM_TYPES)-1)
        using_stage_index = random.randint(0,len(PLASMODUIM_STAGES)-1)

        self.using_species = PLASMODIUM_TYPES[using_species_index]
        self.using_stage = PLASMODUIM_STAGES[using_stage_index]
        using_crop_zone = (CHOP_X[using_species_index],CHOP_Y[using_stage_index],CHOP_X[using_species_index+1],CHOP_Y[using_stage_index+1])
        using_image = cell_photo.crop(using_crop_zone)
        self.image.image = ImageTk.PhotoImage(using_image)  #keep track
        self.image.config(image=self.image.image)

        self.species_var.set("請選擇")
        self.stage_var.set("請選擇")
    
    def check_answer(self) -> None:

        self.check_btn.config(state=ttk.DISABLED)
        
        if self.species_var.get() == self.using_species and self.stage_var.get() == self.using_stage:
            self.correct_number += 1
            self.show_answer_and_hide(True)
        
        else:
            self.show_answer_and_hide(False)
    
    def show_answer_and_hide(self,is_true_answer):
        self.tooltip = ttk.Toplevel(overrideredirect=True,size=(500,150))
        self.tooltip.position_center()
        self.root.after(ms=2000,func=self.go_next)

        if is_true_answer:
            ttk.Label(master=self.tooltip,text="正確!",font="Helvetica 18").pack(padx=20,pady=10)
        
        else:
            ttk.Label(master=self.tooltip,text="錯誤!",font="Helvetica 18").pack(padx=20,pady=10)
            ttk.Label(master=self.tooltip,text=f"正確答案是:{self.using_species}的{self.using_stage} stage",font="Helvetica 12").pack(padx=20,pady=10)
    
    def go_next(self) -> None:

        self.tooltip.destroy()

        self.check_btn.config(state=ttk.NORMAL)
        self.question_number += 1
        self.question_number_var.set(f"第{self.question_number}題")
        self.next_question()

App()