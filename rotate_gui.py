from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
from coordinate_rotate import ex_rotate
import time

root = Tk()
root.geometry('300x400')
root.title('Coordinate Rotate')

path = StringVar()
limit = IntVar()
angles = [90, 180, 270]
angle = IntVar()
angle.set(angles[0])


def do_browse():
    folder_selected = filedialog.askdirectory()
    print(folder_selected)
    path.set(folder_selected)


def do_rotate():
    input_path = path.get()
    input_limit = limit.get()
    try :
        int(input_limit)
    except ValueError:
        messagebox.showerror(title='Error', message='Only digits are allowed')
    print(input_limit)
    if input_path == '':
        messagebox.showerror(title='Error', message='Input folder not found')
    elif input_limit == 0:
        messagebox.showerror(title='Error', message='Please input limit')
    else:
        input_angle = angle.get()
        if ex_rotate(input_path, input_angle, input_limit):
            messagebox.showinfo(title='Success', message='Done')


frame1 = Frame()
frame1.pack(fill=X)

browse_btn = Button(frame1, text='Browse folder', command=do_browse)
browse_btn.place(relx=0.0, rely=0.0)

lbl1 = Label(frame1, textvariable=path)
lbl1.pack(fill=Y, pady=5, expand=True)

frame2 = Frame()
frame2.pack(fill=X)

lbl2 = Label(frame2, text="Choose angle")
lbl2.pack(side=LEFT, padx=5, pady=5)

angle_drop = OptionMenu(frame2, angle, *angles)
angle_drop.pack(fill=X, padx=5, expand=True)

frame3 = Frame()
frame3.pack(fill=X)

lbl3 = Label(frame3, text="Limit")
lbl3.pack(side=LEFT, padx=5, pady=5)

txt = Entry(frame3, textvariable=limit)
txt.pack(fill=X, padx=3, expand=True)

frame4 = Frame()
frame4.pack(fill=X)

browse_btn = Button(frame4, text='Execute', command=do_rotate)
browse_btn.pack()

frame5 = Frame()
frame5.pack(fill=X)
#
# lbl4 = Label(frame4, text="Limit")
# lbl4.pack(side=LEFT, padx=5, pady=5)

# progress_bar = Progressbar(frame5, orient=HORIZONTAL, length=300, mode='determinate')
# progress_bar.pack(pady=5)

root.mainloop()
