# import tkinter 
from tkinter import * 
from tkinter import filedialog

# create a root window 
root = Tk() 

# create a title at the top of the windor 
root.title("Drone Detection") 
# geometry is width x height 
root.geometry('350x200')

# enter in a file that we can run our algorithms on 
# create function to open your files and select 


def open_file_dialog():
    file_path = filedialog.askopenfilename(title="Select a File", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        selected_file_label.config(text=f"Selected File: {file_path}")
        process_file(file_path)

def process_file(file_path):
    # Implement your file processing logic here
    # For demonstration, let's just display the contents of the selected file
    try:
        with open(file_path, 'r') as file:
            file_contents = file.read()
            file_text.delete('1.0', END)
            file_text.insert(END, file_contents)
    except Exception as e:
        selected_file_label.config(text=f"Error: {str(e)}")

selected_file_label = Label(root, text="Selected File:", height = 50, width = 100)

file_text = Text(root, height=10, width=40)


# create upload button 
uploadBtn = Button(root, text = "Upload Your File", fg = "black", command = open_file_dialog)
uploadBtn.grid(column = 2, row = 0)

# add a menu bar in the root window 
menu = Menu(root)
# create an item in the menu bar 
item = Menu(menu)
# add more items in the menu bar 
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# create text in the root window
# lbl = Label(root, text = "Enter the ID")
# lbl.grid()

# create an entry field 
# txt = Entry(root, width=10)
# txt.grid(column=1, row=0)

###
# what happens when the button gets clicked 
# def clicked(): 
    # allows for user entry to be shown 
    # res = "The ID you are looking for is " + txt.get()
    # lbl.configure(text = res)

    # changes the text when you click to be "surprise!"
    # lbl.configure(text = "surprise!")


# create the button 
# btn = Button(root, text = "Enter", fg = "black", command = clicked)

# put the button in the root window but you can change where it is 
# tkinter uses row and columnns for placements 
# btn.grid(column = 2, row = 0)


root.mainloop()