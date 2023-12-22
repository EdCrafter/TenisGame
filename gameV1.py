import sys
import random
from PIL import Image, ImageDraw , ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW, Menu, Toplevel,Label, Button\
     , messagebox, StringVar, IntVar , Entry, Checkbutton, Scale, Listbox,DoubleVar
import time

class Cons:
    BOARD_WIDTH = 1200
    BOARD_HEIGHT = 600
    DELAY = 5
    BALL_SIZE = 100
    RACKET_SIZE_Y = 180
    RACKET_SIZE_X = 117
    BALL_SPEED_FACTOR =1
    BALL_SPEED = 0.045
    PLAYER1_NAME ="Гравець 1"
    PLAYER2_NAME ="Гравець 2"
    button_width = 20

class WelcomeScreen(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Гра в теніс")
        self.geometry("600x370")
        self.initWelcome()

    def initWelcome(self):
        # Create a canvas for the background
        self.canvas = Canvas(self, width=600, height=370)
        self.canvas.pack()

        center_color = (255, 255, 255)  # Белый центр
        outer_color = (0, 0, 255)  # Синий на краях
        self.bg_image = self.create_radial_gradient_image(600, 370, center_color, outer_color)
        
        self.bg_canvas_image = self.canvas.create_image(0, 0, image=self.bg_image, anchor=NW, tag="background")
        self.configure(bg="white")
        self.draw_text_on_canvas(x=245, y=60)
        # Add other widgets with absolute positioning

        start_button = Button(self, text="Старт", width=Cons.button_width, command=self.start_game,bg="green3")
        start_button.place(x=230, y=80)
        config_button = Button(self, text="Налаштування", width=Cons.button_width, command=self.configure_game,bg="yellow")
        config_button.place(x=230, y=120)
        rules_button = Button(self, text="Правила гри", width=Cons.button_width, command=self.show_rules,bg="yellow")
        rules_button.place(x=230, y=160)
        help_button = Button(self, text="Допомога", width=Cons.button_width, command=self.show_help,bg="yellow")
        help_button.place(x=230, y=200)
        info_button = Button(self, text="Інформація", width=Cons.button_width, command=self.show_info,bg="yellow")
        info_button.place(x=230, y=240)
        exit_button = Button(self, text="Вихід", width=Cons.button_width, command=self.exit_game,bg="red")
        exit_button.place(x=230, y=280)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def start_game(self):
        self.destroy()
        # Start the game here
        self.master.start_game()

    def configure_game(self):
        #self.destroy()
        settings_window = SettingsWindow(self)

    def show_rules(self):
        rules_text = """
        Правила гри "Теніс":

        1. Гравці: Грають два гравці, один проти одного.

        2. М'яч та ракетки: В грі використовується м'яч та дві ракетки.

        3. Мета гри: Мета гравців - забити м'яч у поле супротивника так, щоб суперник не міг його відбити.

        4. Початок гри: М'яч починає рух з центра корта у поле супротивника.

        5. Відбиття: Гравці чергуються відбивати м'яч ракеткою. Це робиться так, щоб м'яч перетнув сітку і відразу вражав у поле супротивника.

        6. Отримання очок: Гравець отримує очко, якщо суперник не може відбити м'яч .

        7. Гейм : Гейм виграє той гравець, який першим досягне певної кількості очок. 

            
        """
        messagebox.showinfo("Game Rules", rules_text)

    def show_help(self):
        info_text = """
        Клавіші <W>,<S> рухають гравця зліва вверх і вниз ;
        Клавіші <Up>,<Down> (стрілка вверх і вниз) рухають 
        гравця cправа вверх і вниз ;
        Клавіша <Space> (пробіл) викликає меню паузи ;
        """
        messagebox.showinfo("Help", info_text)
    def show_info(self):
        info_text = """
        Це проста гра створена на tkinter.
        Розробив студент 2го курсу - Жердєв Едуард.
        """
        messagebox.showinfo("Game Info", info_text)
    def exit_game(self):
        # Destroy all windows and exit the application
        self.master.master.destroy()
    def on_close(self):
        # Custom method to handle window close event
        # Destroy both the current window and the main window
        self.destroy()
        self.master.master.destroy()
    def draw_text_on_canvas(self,x, y):
        line_length = 15
        self.canvas.create_line(x,y,x,y-2*line_length,x+line_length,y-line_length*2,\
            x-line_length,y-line_length*2, width=5, fill="gold")
        x+=3*line_length
        y-=2
        self.canvas.create_line(x,y,x-line_length,y,x-line_length,y-line_length,\
            x,y-line_length,x-line_length,y-line_length,x-line_length,y-2*line_length \
            ,x,y-2*line_length,width=5, fill="fuchsia")
        x+=line_length
        y+=2
        self.canvas.create_line(x,y,x,y-2*line_length,x,y-line_length,x+line_length,y-line_length,\
            x+line_length,y-2*line_length ,x+line_length,y,width=5, fill="chartreuse")
        x+=2*line_length
        self.canvas.create_line(x,y,x,y-2*line_length,width=5, fill="orange")
        y-=3*line_length
        self.canvas.create_oval(x - 4, y - 3, x + 4, y + 5, fill="orange", outline="blue")
        y+=3*line_length-2
        x+=2*line_length
        self.canvas.create_line(x,y,x-line_length,y,x-line_length,y-2*line_length\
            ,x,y-2*line_length,width=5, fill="red")

    def create_radial_gradient_image(self,width, height, center_color, outer_color):
        image = Image.new("RGB", (width, height))
        draw = ImageDraw.Draw(image)

        center_x, center_y = width // 2, height // 2

        for y in range(height):
            for x in range(width):
                distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
                radius = min(center_x, center_y)
                if distance <= radius:
                    ratio = distance / radius
                    r = int(center_color[0] + (outer_color[0] - center_color[0]) * ratio)
                    g = int(center_color[1] + (outer_color[1] - center_color[1]) * ratio)
                    b = int(center_color[2] + (outer_color[2] - center_color[2]) * ratio)
                else:
                    r, g, b = outer_color
                draw.point((x, y), fill=(r, g, b))

        return ImageTk.PhotoImage(image)

        

class Board(Canvas):
    def __init__(self, tennis_instance, master):
        super().__init__(master, width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT, highlightthickness=0)
        self.is_paused = False
        self.initGame()
        self.pack()
        self.last_time = time.time()
        self.tennis_instance = tennis_instance
        self.game_over_screen = None
        self.pause_menu = None

    def initGame(self):
        self.inGame = True
        self.ballMoveX = 2
        self.ballMoveY = -2
        self.ball_speed = 60
        self.goal1 = 0
        self.goal2 = 0
        self.racket1X = Cons.BOARD_WIDTH * 0.08
        self.racket1Y = (Cons.BOARD_HEIGHT-Cons.RACKET_SIZE_Y)/2
        self.racket2X = Cons.BOARD_WIDTH * 0.92 - Cons.RACKET_SIZE_X
        self.racket2Y = self.racket1Y  # Начальная позиция второй ракетки
        self.ball_scale = 1.0
        self.ball_width = Cons.BALL_SIZE
        self.ball_height = Cons.BALL_SIZE
        self.ball_paused = False
        self.original_ball_speed = Cons.BALL_SPEED
        # Начальный угол вращения мяча
        self.rotation_angle = 0
        # Скорость вращения мяча (в градусах на тик)
        self.rotation_speed = -2

        self.loadImages()
        self.createObjects()
        self.getRecord()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(Cons.DELAY, self.onTimer)

    def loadImages(self):
        try:
            self.iball = Image.open("./img/ball.png")
            self.original_iball = Image.open("./img/ball.png")
            self.original_ball_image = ImageTk.PhotoImage(self.original_iball)

            self.iball = self.original_iball
            self.iball = self.original_iball.resize((Cons.BALL_SIZE, Cons.BALL_SIZE), resample=Image.LANCZOS)
            self.ball_image = self.original_ball_image

            self.original_iracket = Image.open("./img/racket.png")
            self.original_racket_image = ImageTk.PhotoImage(self.original_iracket)

            self.iracket = self.original_iracket
            self.racket_image = ImageTk.PhotoImage(self.iracket)
            self.iracket2 = self.iracket.transpose(Image.FLIP_LEFT_RIGHT)  # Переворачиваем изображение
            self.racket2_image = ImageTk.PhotoImage(self.iracket2)
            self.ibg = Image.open("./img/bg.png")
            self.bg_image = ImageTk.PhotoImage(self.ibg)
            self.igoal1 = Image.open("./img/goal1.png")
            self.goal1_image = ImageTk.PhotoImage(self.igoal1)
            self.igoal2 = Image.open("./img/goal2.png")
            self.goal2_image = ImageTk.PhotoImage(self.igoal2)

        except IOError as e:
            print(e)
            sys.exit(1)

    def createObjects(self):
        self.create_image(0, 0, image=self.bg_image, anchor=NW, tag="background")


        
        try:
            self.create_text(
                500, 30, text="{0}".format(self.goal1),
                tag="goal1_text", fill="green2",font=("Arial", 50),
            )
        except Exception as e:
                print(f"Error : {e}")

        self.create_text(
            Cons.BOARD_WIDTH-500, 30, text="{0}".format(self.goal2),
            tag="goal2_text", fill="red",font=("Arial", 50),
        )
        self.racket1 = self.create_image(
            self.racket1X, self.racket1Y, image=self.racket_image,
            anchor=NW, tag="racket1",
        )
        self.racket2 = self.create_image(
            self.racket2X, self.racket2Y, image=self.racket2_image,
            anchor=NW, tag="racket2"
        )
        self.goal1_image_id = self.create_image(
            0, 0, image=self.goal1_image,
            anchor=NW, tag="goal1_image"
        )
        self.itemconfig(self.goal1_image_id, state="hidden")
        self.goal2_image_id = self.create_image(
            Cons.BOARD_WIDTH-96, 0, image=self.goal2_image,
            anchor=NW, tag="goal2_image"
        )
        self.itemconfig(self.goal2_image_id, state="hidden")
        self.ball = self.create_image((Cons.BOARD_WIDTH-Cons.BALL_SIZE)/2,(Cons.BOARD_HEIGHT-Cons.BALL_SIZE)/2, image=self.ball_image, anchor=NW, tag="ball")   

    def onKeyPressed(self, e):
        key = e.keysym
        
        if not self.is_paused :
            W_CURSOR_KEY = "w"
            if key == W_CURSOR_KEY:
                self.move_racket_up("racket1")

            S_CURSOR_KEY = "s"
            if key == S_CURSOR_KEY:
                self.move_racket_down("racket1")
            UP_CURSOR_KEY = "Up"
            if key == UP_CURSOR_KEY:
                self.move_racket_up("racket2")

            DOWN_CURSOR_KEY = "Down"
            if key == DOWN_CURSOR_KEY:
                self.move_racket_down("racket2")
            SPACE_KEY = "space"
            if key == SPACE_KEY:
                self.toggle_pause()

    def onTimer(self):
        current_time = time.time()
        if not self.is_paused:
            self.drawScore()
            elapsed_time = current_time - self.last_time
            if (not self.ball_paused):
                self.move_ball(elapsed_time)
            self.rotate_ball()
            self.ball_speed += self.original_ball_speed
            

        self.last_time = current_time
        self.after(Cons.DELAY, self.onTimer)

    def move_ball(self,elapsed_time):
        ball_coords = self.bbox(self.ball)
        racket1_coords = self.bbox(self.racket1)
        racket2_coords = self.bbox("racket2")
        if ball_coords:
            ballLeft = ball_coords[0]
            ballTop = ball_coords[1]
            ballRight = ball_coords[2]
            ballBottom = ball_coords[3]
        if racket1_coords:
            racket1Left = racket1_coords[0]
            racket1Top = racket1_coords[1]
            racket1Right = racket1_coords[2]
            racket1Bottom = racket1_coords[3]
        if racket2_coords:
            
            racket2Left = racket2_coords[0]
            racket2Top = racket2_coords[1]
            racket2Right = racket2_coords[2]
            racket2Bottom = racket2_coords[3]

        if (
            self.ballMoveX > 0 and 
            ballRight >= racket2Left+30 and 
            ballBottom >= racket2Top+30 and 
            ballTop <= racket2Bottom-30 and 
            ballLeft <= racket2Right-Cons.RACKET_SIZE_X/2
        ):
            self.resize_ball(1, 0)
            self.resize_racket(2,1)
            self.ballMoveX = random.randint(10,30)/10
            self.ballMoveY = 4 - self.ballMoveX
            self.ballMoveX = -self.ballMoveX
            if (racket2Top+Cons.RACKET_SIZE_Y*3/4>ballBottom):
                self.ballMoveY = -self.ballMoveY
        if (
            self.ballMoveX < 0 and 
            ballRight >= racket1Left-Cons.RACKET_SIZE_X*3/4 and 
            ballBottom >= racket1Top+30 and 
            ballTop <= racket1Bottom-30 and
            ballLeft <= racket1Right-30
        ):
            self.resize_ball(1, 0)
            self.resize_racket(1,1)
            self.ballMoveX = -random.randint(10,30)/10
            self.ballMoveY = 4 + self.ballMoveX
            self.ballMoveX = -self.ballMoveX
            if (racket1Top+Cons.RACKET_SIZE_Y/2>ballBottom):
                self.ballMoveY = -self.ballMoveY
        if self.ballMoveX > 0 and ballRight > Cons.BOARD_WIDTH:
            self.goal1+=1
            # Уменьшаем размеры мяча при ударе о стенку
            self.resize_ball(1,0)
            self.saveBallMoveX = self.ballMoveX
            self.saveBallMoveY = self.ballMoveY
            self.ballMoveX =0
            self.ballMoveY = 0
            for i in range(3):
                self.after(200*2*i, lambda player=2: self.scoring_goal_show(player)) 
            self.after(1200, self.move_ball_after_delay)
        if self.ballMoveX < 0 and ballLeft < 0:
            self.goal2+=1
            self.resize_ball(1,0)
            self.saveBallMoveX = self.ballMoveX
            self.saveBallMoveY = self.ballMoveY
            self.ballMoveX =0
            self.ballMoveY = 0
            for i in range(3):
                self.after(200*2*i, lambda player=1: self.scoring_goal_show(player)) 
            self.after(1200, self.move_ball_after_delay)
        if self.ballMoveY < 0 and ballTop < 0:
            self.resize_ball(0,1)
            self.ballMoveY = -self.ballMoveY
        if self.ballMoveY > 0 and ballTop > Cons.BOARD_HEIGHT - Cons.BALL_SIZE:
            self.resize_ball(0,1)
            self.ballMoveY = -self.ballMoveY
        # Изменяем размеры мяча, указывая все четыре координаты
        move_distance_x = self.ballMoveX *self.ball_speed* elapsed_time
        move_distance_y = self.ballMoveY *self.ball_speed* elapsed_time

        self.move(self.ball, move_distance_x, move_distance_y)


    def move_racket_up(self, racket):
        if racket == "racket1":
            racket_coords = self.bbox(self.racket1)
            if racket_coords[1] > 15:
                self.move(racket, 0, -15)
                
        else: 
            racket_coords = self.bbox(self.racket2)
            if racket_coords[1] > 15:
                self.move(racket, 0, -15)

    def move_racket_down(self, racket):
        if racket == "racket1":
            racket_coords = self.bbox(self.racket1)
            if racket_coords[3] < Cons.BOARD_HEIGHT - 15:
                self.move(racket, 0, 15)
        else: 
            racket_coords = self.bbox(self.racket2)
            if racket_coords[3] < Cons.BOARD_HEIGHT - 15:
                self.move(racket, 0, 15)

    def rotate_ball(self):
        # Увеличиваем угол вращения
        self.rotation_angle += self.rotation_speed
        
        if self.rotation_angle <= 0:
            self.rotation_angle += 360  # Ограничение угла до 360 градусов

        # Создаем вращенное изображение мяча
        rotated_ball = self.rotate_image(self.iball, self.rotation_angle)
        self.ball_image = ImageTk.PhotoImage(rotated_ball)
        
        # Обновляем изображение мяча
        self.itemconfig(self.ball, image=self.ball_image)

    def rotate_image(self, image, angle):
        # Вращение изображения на заданный угол
        return image.rotate(angle)
    def reset_ball_size(self):
        # Восстанавливаем оригинальное изображение мяча
        self.iball = self.original_iball.resize((Cons.BALL_SIZE, Cons.BALL_SIZE), resample=Image.LANCZOS)
        self.ball_image = ImageTk.PhotoImage(self.iball)
        self.itemconfig(self.ball, image=self.ball_image)
        self.ball_paused = False

    def resize_ball(self, x, y):
        self.rotation_angle -= self.rotation_speed
        self.ball_paused = True
        if x < 15 and y < 15:
            if x:
                x += 4
            if y:
                y += 4
            self.iball = self.iball.resize((Cons.BALL_SIZE - x, Cons.BALL_SIZE - y), resample=Image.LANCZOS)
            self.ball_image = ImageTk.PhotoImage(self.iball)
            self.itemconfig(self.ball, image=self.ball_image)
            self.after(Cons.DELAY, self.resize_ball, x, y)
        else:
            self.reset_ball_size()
    def reset_racket_size(self,t):
        # Восстанавливаем оригинальное изображение мяча
        self.iracket = self.original_iracket.resize((Cons.RACKET_SIZE_X, Cons.RACKET_SIZE_Y), resample=Image.LANCZOS)
        if (t==1):
            self.racket_image = ImageTk.PhotoImage(self.iracket)
            self.itemconfig(self.racket1, image=self.racket_image)
        else:
            self.iracket2 = self.iracket.transpose(Image.FLIP_LEFT_RIGHT) 
            self.racket2_image = ImageTk.PhotoImage(self.iracket2)
            self.itemconfig(self.racket2, image=self.racket2_image)
            self.move(self.racket2,-14,0)

    def resize_racket(self, t,x):
        if x < 15 :
            if x:
                x += 2
            if t==1:
                self.iracket = self.iracket.resize((Cons.RACKET_SIZE_X - x,Cons.RACKET_SIZE_Y), resample=Image.LANCZOS)
                self.racket_image = ImageTk.PhotoImage(self.iracket)
                self.itemconfig(self.racket1, image=self.racket_image)
            else :
                self.move(self.racket2,2,0)
                self.iracket2 = self.iracket2.resize((Cons.RACKET_SIZE_X - x,Cons.RACKET_SIZE_Y), resample=Image.LANCZOS) 
                self.racket2_image = ImageTk.PhotoImage(self.iracket2)
                self.itemconfig(self.racket2, image=self.racket2_image)
            
            self.after(Cons.DELAY, self.resize_racket,t, x)
            
        else:
            self.reset_racket_size(t)
    def drawScore(self):
        # Check if goal1_text and goal2_text already exist, create if not
        goal1_text = self.find_withtag("goal1_text")
        goal2_text = self.find_withtag("goal2_text")
        record_text = self.find_withtag("record_text")
        if (self.ball_speed>self.record):
            self.record = int(self.ball_speed)
        if not goal1_text:
            self.create_text(500, 30, text="{0}".format(self.goal1), tag="goal1_text", fill="green2", font=("Arial", 50))

        if not goal2_text:
            self.create_text(Cons.BOARD_WIDTH-500, 30, text="{0}".format(self.goal2), tag="goal2_text", fill="red", font=("Arial", 50))

        if not record_text:
            self.create_text(170, 30, text="Record : {0}".format(self.record), tag="record_text", fill="yellow", font=("Arial", 16))
        # Update the text of the existing items
        self.itemconfig("goal1_text", text="{0}".format(self.goal1))
        self.itemconfig("goal2_text", text="{0}".format(self.goal2))
        self.itemconfig("record_text", text="Record : {0}".format(self.record))
        if self.goal1 >= 3 or self.goal2 >= 3:
            self.game_over()
    def getRecord(self):
        self.record = 0
        self.current_encoding = 'utf-8'
        with open("records.txt", 'r', encoding=self.current_encoding) as file:
            lines = file.readlines()
        line = lines[0].strip()
        if line:
            self.record = int(line.strip())
    def setRecord(self):
        self.current_encoding = 'utf-8'
        with open("records.txt", "r+", encoding=self.current_encoding) as file:
            file.seek(0)
            file.writelines(f"{self.record}")

    def onSpaceKeyPressed(self, e):
        if not self.is_paused:
            self.is_paused = True
            self.pause_callback()
    def move_ball_after_delay(self):
        # Перемещаем мяч в новые координаты
        self.coords(self.ball, (Cons.BOARD_WIDTH-Cons.BALL_SIZE)/2,(Cons.BOARD_HEIGHT-Cons.BALL_SIZE)/2)
        # Запускаем функцию начала движения через некоторое время
        self.after(1000, self.start_ball_movement)

    def start_ball_movement(self):
        self.ballMoveX = self.saveBallMoveX
        self.ballMoveY = self.saveBallMoveY
        self.ballMoveX = -self.ballMoveX
    def scoring_goal_show(self, player):
        if player == 1:
            self.itemconfig(self.goal1_image_id, state="normal")
            self.after(200, lambda: self.scoring_goal_hidden(1))
        else:
            self.itemconfig(self.goal2_image_id, state="normal")
            self.after(200, lambda: self.scoring_goal_hidden(2))

    def scoring_goal_hidden(self, player):
        if player == 1:
            self.itemconfig(self.goal1_image_id, state="hidden")
        else:
            self.itemconfig(self.goal2_image_id, state="hidden")
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.show_pause_menu()
        else:
            self.hide_pause_menu()

    def show_pause_menu(self):
        # Отображение меню паузы
        self.pause_menu = PauseMenu(self.master, self.resume_game,self.return_to_welcome_screen)
        self.master.bind("<space>", lambda event: self.resume_game())

    def hide_pause_menu(self):
        # Скрытие меню паузы
        if self.pause_menu:
            self.pause_menu.destroy()
            self.pause_menu = None
        self.master.bind("<space>", lambda event: self.toggle_pause())

    def resume_game(self):
        self.toggle_pause()
    def game_over(self):
        self.setRecord()
        x=0
        self.is_paused = True
        if (self.goal2 == 3):
            x=2
        
        self.game_over_screen = GameOverScreen(self.master, self.return_to_welcome_screen,x)

    def return_to_welcome_screen(self):
        # Reset game variables and return to the welcome screen
        self.goal1 = 0
        self.goal2 = 0
        self.is_paused = True
        self.tennis_instance.return_to_welcome_screen()
        super().destroy() 
           
class PauseMenu(Toplevel):
    def __init__(self, master, resume_callback,return_callback):
        super().__init__(master)
        self.title("Пауза")
        self.geometry("170x150")
        self.resume_callback = resume_callback
        self.return_callback = return_callback
        self.initMenu()
    
    def initMenu(self):
        label = Label(self, text="Меню паузи")
        label.pack(padx=10, pady=10)
        return_button = Button(self, width=Cons.button_width, text="Перейти на головну", command=self.return_callback,bg="gold")
        return_button.pack(pady=10)
        # Добавьте другие элементы меню по вашему усмотрению

        resume_button = Button(self, width=Cons.button_width, text="Продовжити", command=self.resume_callback,bg="green3")
        resume_button.pack(pady=10)    
        self.protocol("WM_DELETE_WINDOW", self.on_close)      
    def on_close(self):
        self.resume_callback()
        self.destroy()
class GameOverScreen(Toplevel):
    def __init__(self, master, return_callback,x):
        super().__init__(master)
        self.title("Game Over")
        self.return_callback = return_callback
        self.initGameOver(x)

    def initGameOver(self,x):
        label = Label(self, text="Гра Закінчилась", font=("Arial", 22, "bold"),fg="blue2",bg="yellowgreen")
        label.pack(pady=20)
        self.configure(bg="yellowgreen")
        if (x == 2):
            Cons.PLAYER1_NAME,Cons.PLAYER2_NAME = Cons.PLAYER2_NAME,Cons.PLAYER1_NAME
        label = Label(self, text="Вітаю!!!\n"+str(Cons.PLAYER1_NAME)+" виходить переможцем,\n"+str(Cons.PLAYER2_NAME)+" програв.",\
             font=("Arial", 18),bg="yellowgreen",fg="red")
        label.pack(pady=20)

        return_button = Button(self, width=Cons.button_width, text="Перейти на головну", command=self.return_callback,bg="cyan")
        return_button.pack(pady=10)
        self.protocol("WM_DELETE_WINDOW", self.on_close) 
    def on_close(self):
        self.destroy()
        self.master.destroy()

class Tennis(Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master.title('Tennis Game')
        self.pause_menu = None
        self.board = None  # Будет инициализировано при запуске игры
        #self.pack()
        self.save_settings_check=0
        self.master.withdraw()
        # Показываем экран приветствия изначально
        self.show_welcome_screen()
        self.game_over_screen = None

    def show_welcome_screen(self):
        self.welcome_screen = WelcomeScreen(self)

    def start_game(self):
        # Скрыть текущее окно
        #self.master.withdraw()
        #self.pack_forget()
        self.master.deiconify()
        # Создать новое окно для игры
        self.board = Board(self,self.master)
    def destroy_game_window(self):
        
        if self.board:
            if self.board.game_over_screen:
                self.board.game_over_screen.destroy()
                self.board.game_over_screen = None
            if self.board.pause_menu:
                self.board.pause_menu.destroy()
                self.board.pause_menu = None
            self.board.destroy()
            self.board = None
        self.master.withdraw()


    def return_to_welcome_screen(self):
        self.destroy_game_window()
        self.show_welcome_screen()



class SettingsWindow(Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Налаштування")
        self.geometry("350x450")
        self.init_settings()


    def init_settings(self):
        # Размер мяча
        self.label_name_1 = Label(self, text="Ім'я гравця 1:")
        self.label_name_1.grid(row=0, column=0, padx=10, pady=10)

        self.entry_name_1 = Entry(self)
        self.entry_name_1.grid(row=0, column=1, padx=10, pady=10)
        self.entry_name_1.bind("<KeyRelease>", self.change_check)
        # Сложность игры
        self.label_name_2 = Label(self, text="Ім'я гравця 2:")
        self.label_name_2.grid(row=1, column=0, padx=10, pady=10)

        self.entry_name_2 = Entry(self)
        self.entry_name_2.grid(row=1, column=1, padx=10, pady=10)
        self.entry_name_2.bind("<KeyRelease>", self.change_check)

        # Шкала с ползунком
        self.label_ball_size = Label(self, text="Розмір м'яча:")
        self.label_ball_size.grid(row=2, column=0, padx=10, pady=10)

        self.ball_size = IntVar()
        self.scale = Scale(self, from_=50, to=200, orient="horizontal", variable=self.ball_size)
        self.scale.grid(row=2, column=1, padx=10, pady=10)
        self.scale.bind("<B1-Motion>", self.change_check)

        # Список
        self.label_difficulty = Label(self, text="Складність гри:")
        self.label_difficulty.grid(row=3, column=0, padx=10, pady=10)

        self.listbox = Listbox(self, selectmode="single")
        self.listbox.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

        # Применяем параметр rowspan
        self.listbox.grid(row=3, column=1, padx=10, pady=10, sticky="ew", rowspan=2)
        self.options = ["Легка", "Звичайна", "Склана"]
        for option in self.options:
            self.listbox.insert("end", option)

        # Флажок ВКЛ/ВЫКЛ
        label_enable_option = Label(self, text="Вімкнути налаштування\nза замовчанням :")
        label_enable_option.grid(row=5, column=0, padx=10, pady=10)
        self.listbox.bind("<<ListboxSelect>>", self.onSelect)

        self.var = StringVar()
        self.label = Label(self, text=0, textvariable=self.var)
        self.label.grid(row=4, column=0, padx=10, pady=10)
        self.checkbutton_var = IntVar()
        if self.master.master.save_settings_check ==0:
            self.checkbutton_var.set(1)
        self.var.set(self.listbox.get(Cons.BALL_SPEED_FACTOR))
        self.toggle_settings()
        checkbutton = Checkbutton(self, width=Cons.button_width, variable=self.checkbutton_var, command=lambda: self.toggle_settings())
        checkbutton.grid(row=5, column=1, padx=10, pady=10)
        # Кнопка сохранения настроек
        save_button = Button(self, width=Cons.button_width, text="Зберегти", command=self.save_settings)
        save_button.grid(row=6, column=0, columnspan=2, pady=20)

    def save_settings(self):
        self.master.master.save_settings_check = 1
        Cons.BALL_SPEED_FACTOR = self.options.index(self.var.get())
        Cons.BALL_SIZE = self.ball_size.get()
        Cons.BALL_SPEED = (Cons.BALL_SPEED_FACTOR+0.5)*0.03
        Cons.PLAYER1_NAME = self.entry_name_1.get()
        Cons.PLAYER2_NAME = self.entry_name_2.get()
        self.destroy()

    def onSelect(self, val):
        self.change_check(0)
        sender = val.widget
        idx = sender.curselection()
        if (idx):
            value = sender.get(idx)
            self.var.set(value)
    def toggle_settings(self):
        if self.checkbutton_var.get() == 1:  # Если флажок включен
            # Установите начальные значения полей ввода и других параметров
            self.entry_name_1.delete(0, "end")
            self.entry_name_1.insert("end", "Гравець 1")  # Начальное значение для размера мяча
            self.entry_name_2.delete(0, "end")
            self.entry_name_2.insert("end", "Гравець 2")  # Начальное значение для режима игры
            self.ball_size.set(100)  # Начальное значение для шкалы
            self.listbox.selection_clear(0, "end")  # Очистить текущий выбор
            self.listbox.selection_set(1)  # Выбрать "Звичайний"
            self.var.set(self.listbox.get(1))
        else:
            self.entry_name_1.delete(0, "end")
            self.entry_name_1.insert("end", Cons.PLAYER1_NAME)  # Начальное значение для размера мяча
            self.entry_name_2.delete(0, "end")
            self.entry_name_2.insert("end", Cons.PLAYER2_NAME) 
            self.ball_size.set(Cons.BALL_SIZE)
            self.listbox.selection_clear(0, "end")  # Очистить текущий выбор
            self.listbox.selection_set(Cons.BALL_SPEED_FACTOR)  # Выбрать "Звичайний"

    def change_check(self,event):
        self.checkbutton_var.set(0)

def main():
    root = Tk()
    root.withdraw()
    nib = Tennis(master=root)
    root.mainloop()

if __name__ == '__main__':
    main()
