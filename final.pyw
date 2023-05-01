import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo
import TimeTable as TT
import AC3
from tkinter import messagebox
import pandas as pd
import os
import scriptCMUQ as script
def restart():
    root.destroy()
    os.startfile("final.pyw")
def scrap():
    script.start()
def is_safe(ac3, mapping, course, semester):
    aux = mapping[course]
    mapping[course] = semester
    for constraint in ac3.Constraints:
        if mapping[constraint[0]] != 0 and mapping[constraint[2]]!=0:
            if not ac3.op[constraint[1]](mapping[constraint[0]], mapping[constraint[2]]):
                mapping[course] = aux
                return False
    return True


def backtracking(ac3, solution, mapping):
    finish = True
    for course in mapping:
        if mapping[course] == 0:
            finish = False
    if finish:
        sol = {}
        for course in mapping:
            sol[course] = mapping[course]
        if sol not in solution:
            solution.append(sol)
    for course in mapping:
        if mapping[course] == 0:
            for semester in ac3.domains[course]:
                if is_safe(ac3, mapping, course, semester):
                    mapping[course] = semester
                    backtracking(ac3, solution, mapping)
                    mapping[course] = 0


def process_input():
    num_semesters = int(semesters_entry.get())
    starting_semester = starting_entry.get()

    # Call your function here and get the result
    tt = TT.TimeTable()
    ac3 = tt.solve(num_semesters, starting_semester)
    global solution
    solution = []
    mapping = {}
    for course in ac3.variables:
        mapping[course] = 0
    backtracking(ac3, solution, mapping)
    if(solution == []):
        messagebox.showerror("Check your course schedule","There is no solution!")
    else:
        # Open a new window to display the result
        global result_window
        result_window = tk.Toplevel(root)
        result_window.geometry("300x200")
        result_window.title("Solutions")

        # Create a label and a button to display and navigate the solutions
        global result_label, prev_button, next_button, result_index
        result_index = 0
        result_label = tk.Label(result_window, text=f"Option {result_index+1}/{len(solution)}", font=("Arial", 12))
        result_label.pack(pady=10)
        prev_button = tk.Button(result_window, text="< Previous", command=on_prev_click)
        prev_button.pack(side=tk.LEFT, padx=10)
        next_button = tk.Button(result_window, text="Next >", command=on_next_click)
        next_button.pack(side=tk.LEFT, padx=10)

        # Create a text widget to display the solution details
        global result_text
        result_text = tk.Text(result_window, width=30, height=10, font=("Arial", 12))
        result_text.pack(pady=10)

        # Initialize the text widget with the first solution details
        update_solution_text()


def update_solution_text():
    result_text.delete("1.0", tk.END)
    for key, value in solution[result_index].items():
        result_text.insert(tk.END, f"{key.name}: Semester {value}\n")


def on_prev_click():
    global result_index
    result_index -= 1
    if result_index < 0:
        result_index = len(solution) - 1
    result_label.config(text=f"Option {result_index+1}/{len(solution)}")
    update_solution_text()


def on_next_click():
    global result_index
    result_index += 1
    if result_index >= len(solution):
        result_index = 0
    result_label.config(text=f"Option {result_index+1}/{len(solution)}")
    update_solution_text()

def student():
    
    home = tk.Button(root, text="Home", command = restart)
    home.place(relx=0.5, rely=0.1, anchor="center")
    header_label = tk.Label(root, text="Course Timetable Solver", font=("Arial", 16))
    header_label.place(relx=0.5, rely=0.2, anchor="center")

    semesters_label = tk.Label(root, text="Number of semesters:")
    semesters_label.place(relx=0.5, rely=0.3, anchor="center")
    global semesters_entry
    semesters_entry = tk.Entry(root)
    semesters_entry.place(relx=0.5, rely=0.35, anchor="center")

    starting_label = tk.Label(root, text="Starting semester:")
    starting_label.place(relx=0.5, rely=0.45, anchor="center")
    global starting_entry
    starting_entry = tk.Entry(root)
    starting_entry.place(relx=0.5, rely=0.5, anchor="center")

    submit_button = tk.Button(root, text="Submit", command=process_input)
    submit_button.place(relx=0.5, rely=0.6, anchor="center")

    result_frame = tk.Frame(root, bd=2, relief="groove")
    result_frame.place(relx=0.5, rely=0.8, anchor="center")


def select_and_save_columns(df):
    # Create a new tkinter window
    root.title("Select and Save Courses")
    root.geometry("500x500")

    header_label = tk.Label(root, text="Select the courses you would like to take:", font=("Arial", 16))
    header_label.place(relx=0.5, rely=0.2, anchor="center")

    # Create a frame to hold the listbox
    listbox_frame = tk.Frame(root)
    listbox_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Create a scrollbar
    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a listbox and configure it with the scrollbar
    listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=listbox.yview)

    # Add each column in the dataframe as an item in the listbox
    for col in df.columns:
        listbox.insert(tk.END, col)

    # Create a function to retrieve the selected columns and delete the others
    def save_selected_columns():
        selected_cols = [listbox.get(idx) for idx in listbox.curselection()]
        df.drop([col for col in df.columns if col not in selected_cols], axis=1, inplace=True)
        listbox_frame.destroy()
        submit_button.destroy()
        header_label.destroy()
        TT.dataframe = df
        student()

    # Create a button to submit the selected columns and close the window
    submit_button = tk.Button(root, text="Submit", command=save_selected_columns)
    submit_button.place(relx=0.5, rely=0.8, anchor="center")

def addCourse(df, filename):
    # create new window
    window = tk.Toplevel()
    window.title("Add New Course")

    # create entry widgets for each parameter
    tk.Label(window, text="Name:").grid(row=0, column=0)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1)

    tk.Label(window, text="Semester:").grid(row=1, column=0)
    semester_entry = tk.Entry(window)
    semester_entry.grid(row=1, column=1)

    tk.Label(window, text="Days:").grid(row=2, column=0)
    days_entry = tk.Entry(window)
    days_entry.grid(row=2, column=1)

    tk.Label(window, text="Start Time:").grid(row=3, column=0)
    startTime_entry = tk.Entry(window)
    startTime_entry.grid(row=3, column=1)

    tk.Label(window, text="End Time:").grid(row=4, column=0)
    endTime_entry = tk.Entry(window)
    endTime_entry.grid(row=4, column=1)

    tk.Label(window, text="Credits:").grid(row=5, column=0)
    credits_entry = tk.Entry(window)
    credits_entry.grid(row=5, column=1)

    tk.Label(window, text="Professor:").grid(row=6, column=0)
    professor_entry = tk.Entry(window)
    professor_entry.grid(row=6, column=1)

    tk.Label(window, text="Classroom:").grid(row=7, column=0)
    classroom_entry = tk.Entry(window)
    classroom_entry.grid(row=7, column=1)

    tk.Label(window, text="Prereq:").grid(row=8, column=0)
    prereq_entry = tk.Entry(window)
    prereq_entry.grid(row=8, column=1)

    tk.Label(window, text="Coreq:").grid(row=9, column=0)
    coreq_entry = tk.Entry(window)
    coreq_entry.grid(row=9, column=1)

    # create submit button
    def add_new_column():
        # get input from entry widgets
        name = name_entry.get()
        semester = semester_entry.get()
        days = days_entry.get()
        startTime = startTime_entry.get()
        endTime = endTime_entry.get()
        credits = int(credits_entry.get())
        professor = professor_entry.get()
        classroom = classroom_entry.get()
        prereq = prereq_entry.get()
        coreq = coreq_entry.get()

        # create new column in dataframe with input values
        new_column = [semester, days, startTime, endTime, credits, professor, classroom, prereq, coreq]

        # add the new column to the dataframe
        df[name] = new_column
        df.to_excel(filename, index=False)
        window.destroy()

    submit_button = tk.Button(window, text="Submit", command=add_new_column)
    submit_button.grid(row=10, column=0, columnspan=2)
    
    # start the mainloop to wait for user input
    window.mainloop()


def dropCourse(df, filename):
    # Create a new tkinter window
    window = tk.Toplevel()
    window.title("Drop Course")
    header_label = tk.Label(window, text="Select the courses you would like to remove from the schedule:", font=("Arial", 16))
    header_label.pack(pady=10)

    # Create a frame to hold the listbox
    listbox_frame = tk.Frame(window)
    listbox_frame.pack(side=tk.TOP, padx=10, pady=10)

    # Create a scrollbar
    scrollbar = tk.Scrollbar(listbox_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Create a listbox and configure it with the scrollbar
    listbox = tk.Listbox(listbox_frame, selectmode=tk.MULTIPLE, yscrollcommand=scrollbar.set)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar.config(command=listbox.yview)

    # Add each column in the dataframe as an item in the listbox
    for col in df.columns:
        listbox.insert(tk.END, col)

    # Create a function to retrieve the selected columns and delete the others
    def save_selected_columns():
        selected_cols = [listbox.get(idx) for idx in listbox.curselection()]
        df.drop([col for col in df.columns if col in selected_cols], axis=1, inplace=True)
        listbox_frame.destroy()
        submit_button.destroy()
        header_label.destroy()
        TT.dataframe = df
        df.to_excel(filename, index=False)
        window.destroy()

    # Create a button to submit the selected columns and close the window
    submit_button = tk.Button(window, text="Submit", command=save_selected_columns)
    submit_button.pack(side=tk.BOTTOM, padx=10, pady=10)
def addDropCourse(dataframe, filename):
    root.title("Add/Remove Courses from Database (Professor)")
    header_label1 = tk.Label(root, text="Please select whether you want to add or remove a Course", font=("Arial",12))
    header_label1.place(relx=0.5, rely=0.25, anchor="center")
    add = tk.Button(root, text="Add a course", command= lambda: addCourse(dataframe, filename))
    add.place(relx=0.5, rely=0.4, anchor="center")
    remove = tk.Button(root, text="Remove a Course", command = lambda: dropCourse(dataframe, filename))
    remove.place(relx=0.5, rely=0.5, anchor="center")

def select_file():
    filetypes = (
        ('Excel Files', '*.xlsx'),
        ('All files', '*.*')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='C:/Mugur/Uni Assignments/15112/Project',
        filetypes=filetypes)
    TT.readFile(filename)
    open_button.destroy()
    root.title("Select Student/Professor")
    header_label1 = tk.Label(root, text="Please select whether you are a professor or a student:", font=("Arial",12))
    header_label1.place(relx=0.5, rely=0.25, anchor="center")
    prof = tk.Button(root, text="I'm a professor (Add/Drop Courses)", command = lambda: [prof.destroy(), st.destroy(), addDropCourse(TT.dataframe, filename), header_label1.destroy()])
    prof.place(relx=0.5, rely=0.45, anchor="center")
    st = tk.Button(root, text="I'm a student (Solve Timetable)", command = lambda: [prof.destroy(), st.destroy(), select_and_save_columns(TT.dataframe), header_label1.destroy()])
    st.place(relx=0.5, rely=0.6, anchor="center")

result_index = 0
root = tk.Tk()

root.geometry("500x500")

root.title("Select Database")
bgimg = tk.PhotoImage(file = "winner-2.ppm")
helper = tk.Label(root, i = bgimg, bg='grey',padx=0, pady=0)
helper.place(x=0,y=0,relwidth=1,relheight=1)

header_label = tk.Label(root, text="Welcome to the CMUQ Timetable Solver!", font=("Arial", 16))
header_label.place(relx=0.5, rely=0.2, anchor="center")
header_label1 = tk.Label(root, text="Please select the database of courses:", font=("Arial", 16))
header_label1.place(relx=0.5, rely=0.35, anchor="center")
# open button
open_button = ttk.Button(
    root,
    text='Open a File containing Courses',
    command= lambda: [select_file(), open_button.destroy(), header_label.destroy(), header_label1.destroy(), ret.destroy()]
)

open_button.place(relx=0.5, rely=0.5, anchor="center")
home = tk.Button(root, text="Home", command = restart)
home.place(relx=0.5, rely=0.1, anchor="center")
ret = tk.Button(root, text="Retrieve courses from CMUQ website", command = lambda: [scrap(), messagebox.showinfo("Complete!","Database retrieved successfuly!")])
ret.place(relx=0.5, rely=0.6, anchor="center")
root.configure(padx=20, pady=20)
root.mainloop()
