from tkinter import HIDDEN, NORMAL, Tk, Canvas

def start_game():
    root = Tk()
    c = Canvas(root, width=400, height=400)
    c.configure(bg='light blue', highlightthickness=0)
    c.body_color = 'white'
    c.outline_color = 'black'
    root.config(cursor='spider')

    face = c.create_oval(35, 20, 365, 350, outline=c.outline_color, fill=c.body_color)
    ear_left = c.create_polygon(75, 80, 75, 10, 165, 70, outline=c.body_color, fill=c.body_color)
    ear_right = c.create_polygon(255, 45, 325, 10, 320, 70, outline=c.body_color, fill=c.body_color)
    nose1 = c.create_arc(220, 220, 180, 180, start=-330, extent=120, width=2, fill='pink')
    nose2 = c.create_line(201, 200, 201, 220, width=2, fill='black')

    def normal_face():
        c.itemconfigure(close_eye_left, state=NORMAL)
        c.itemconfigure(close_eye_right, state=NORMAL)
        c.itemconfigure(half_eye_left, state=HIDDEN)
        c.itemconfigure(half_eye_right, state=HIDDEN)
        c.itemconfigure(half_pupil_left, state=HIDDEN)
        c.itemconfigure(half_pupil_right, state=HIDDEN)
        c.itemconfigure(eye_left_angry, state=HIDDEN)
        c.itemconfigure(eye_right_angry, state=HIDDEN)
        c.itemconfigure(pupil_left_angry, state=HIDDEN)
        c.itemconfigure(pupil_right_angry, state=HIDDEN)
        c.itemconfigure(mouth_normal, state=NORMAL)
        c.itemconfigure(mouth_angry, state=HIDDEN)

    def show_angry(event):
        c.itemconfigure(eye_left_angry, state=NORMAL)
        c.itemconfigure(pupil_left_angry, state=NORMAL)
        c.itemconfigure(eye_right_angry, state=NORMAL)
        c.itemconfigure(pupil_right_angry, state=NORMAL)
        c.itemconfigure(close_eye_left, state=HIDDEN)
        c.itemconfigure(close_eye_right, state=HIDDEN)
        c.itemconfigure(mouth_angry, state=NORMAL)
        c.itemconfigure(mouth_normal, state=HIDDEN)
        root.after(2000, normal_face)

    def half_eyes_open(event):
        if (90 <= event.x and event.x <= 300) and (110 <= event.y and event.y <= 170):
            c.itemconfigure(half_eye_left, state=NORMAL)
            c.itemconfigure(half_eye_right, state=NORMAL)
            c.itemconfigure(half_pupil_left, state=NORMAL)
            c.itemconfigure(half_pupil_right, state=NORMAL)
        else:
            close_eyes(event)

        return

    def close_eyes(event):
        c.itemconfigure(half_eye_left, state=HIDDEN)
        c.itemconfigure(half_eye_right, state=HIDDEN)
        c.itemconfigure(half_pupil_left, state=HIDDEN)
        c.itemconfigure(half_pupil_right, state=HIDDEN)
        return

    # half eyes open
    half_eye_left = c.create_oval(90, 140, 160, 170, outline='black', fill='white', state=HIDDEN)
    half_pupil_left = c.create_oval(90, 150, 160, 155, outline='black', fill='black', state=HIDDEN)
    half_eye_right = c.create_oval(230, 140, 300, 170, outline='black', fill='white', state=HIDDEN)
    half_pupil_right = c.create_oval(230, 150, 300, 155, outline='black', fill='black', state=HIDDEN)

    # angry eyes
    eye_left_angry = c.create_oval(130, 110, 160, 170, outline='black', fill='white', state=HIDDEN)
    pupil_left_angry = c.create_oval(140, 145, 150, 155, outline='black', fill='black', state=HIDDEN)
    eye_right_angry = c.create_oval(230, 110, 260, 170, outline='black', fill='white', state=HIDDEN)
    pupil_right_angry = c.create_oval(240, 145, 250, 155, outline='black', fill='black', state=HIDDEN)

    # normal eyes:fully closed
    close_eye_left = c.create_arc(90, 140, 160, 170, start=0, extent=90, width=1, outline='black', style='arc',
                                  state=NORMAL)
    close_eye_right = c.create_arc(230, 140, 300, 170, start=90, extent=90, width=1, outline='black', style='arc',
                                   state=NORMAL)

    mouth_angry = c.create_line(170, 231, 200, 204, 230, 231, smooth=1, width=2, state=HIDDEN)
    mouth_happy = c.create_line(170, 211, 200, 232, 230, 211, smooth=1, width=2, state=HIDDEN)
    mouth_normal = c.create_line(170, 211, 200, 232, 230, 211, smooth=1, width=2, state=NORMAL)

    c.pack()
    c.bind('<Double-1>', show_angry)
    c.bind('<Motion>', half_eyes_open)
    c.bind('<Leave>', close_eyes)
    root.mainloop()



