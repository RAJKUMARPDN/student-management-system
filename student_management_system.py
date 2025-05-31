import sqlite3
from tkinter import *
from tkinter import messagebox

# Database setup
def connect_db():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY, name TEXT, roll TEXT, branch TEXT)"
    )
    conn.commit()
    conn.close()

def insert(name, roll, branch):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO student VALUES (NULL, ?, ?, ?)", (name, roll, branch))
    conn.commit()
    conn.close()
    view()

def view():
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student")
    rows = cur.fetchall()
    conn.close()
    return rows

def search(name="", roll="", branch=""):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM student WHERE name=? OR roll=? OR branch=?", (name, roll, branch))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete(id):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM student WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update(id, name, roll, branch):
    conn = sqlite3.connect("students.db")
    cur = conn.cursor()
    cur.execute("UPDATE student SET name=?, roll=?, branch=? WHERE id=?", (name, roll, branch, id))
    conn.commit()
    conn.close()

# GUI
def get_selected_row(event):
    try:
        global selected_tuple
        index = list1.curselection()[0]
        selected_tuple = list1.get(index)
        e1.delete(0, END)
        e1.insert(END, selected_tuple[1])
        e2.delete(0, END)
        e2.insert(END, selected_tuple[2])
        e3.delete(0, END)
        e3.insert(END, selected_tuple[3])
    except IndexError:
        pass

def view_command():
    list1.delete(0, END)
    for row in view():
        list1.insert(END, row)

def search_command():
    list1.delete(0, END)
    for row in search(name_text.get(), roll_text.get(), branch_text.get()):
        list1.insert(END, row)

def add_command():
    insert(name_text.get(), roll_text.get(), branch_text.get())
    view_command()

def delete_command():
    delete(selected_tuple[0])
    view_command()

def update_command():
    update(selected_tuple[0], name_text.get(), roll_text.get(), branch_text.get())
    view_command()

connect_db()

window = Tk()
window.title("Student Management System")

Label(window, text="Name").grid(row=0, column=0)
Label(window, text="Roll No").grid(row=0, column=2)
Label(window, text="Branch").grid(row=1, column=0)

name_text = StringVar()
e1 = Entry(window, textvariable=name_text)
e1.grid(row=0, column=1)

roll_text = StringVar()
e2 = Entry(window, textvariable=roll_text)
e2.grid(row=0, column=3)

branch_text = StringVar()
e3 = Entry(window, textvariable=branch_text)
e3.grid(row=1, column=1)

list1 = Listbox(window, height=10, width=40)
list1.grid(row=2, column=0, rowspan=6, columnspan=2)

sb1 = Scrollbar(window)
sb1.grid(row=2, column=2, rowspan=6)
list1.configure(yscrollcommand=sb1.set)
sb1.configure(command=list1.yview)

list1.bind("<<ListboxSelect>>", get_selected_row)

Button(window, text="View All", width=12, command=view_command).grid(row=2, column=3)
Button(window, text="Search", width=12, command=search_command).grid(row=3, column=3)
Button(window, text="Add", width=12, command=add_command).grid(row=4, column=3)
Button(window, text="Update", width=12, command=update_command).grid(row=5, column=3)
Button(window, text="Delete", width=12, command=delete_command).grid(row=6, column=3)
Button(window, text="Close", width=12, command=window.destroy).grid(row=7, column=3)

window.mainloop()
