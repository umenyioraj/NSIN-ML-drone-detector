# import tkinter 
from tkinter import * 

# create a root window 
root = Tk() 

# create a title at the top of the windor 
root.title("Drone Detection") 
# geometry is width x height 
root.geometry('350x200')

# add a menu bar in the root window 
menu = Menu(root)
# create an item in the menu bar 
item = Menu(menu)
# add more items in the menu bar 
item.add_command(label='New')
menu.add_cascade(label='File', menu=item)
root.config(menu=menu)

# create text in the root window
lbl = Label(root, text = "Enter the ID")
lbl.grid()

# create an entry field 
txt = Entry(root, width=10)
txt.grid(column=1, row=0)

# what happens when the button gets clicked 
def clicked(): 
    # allows for user entry to be shown 
    res = "The ID you are looking for is " + txt.get()
    lbl.configure(text = res)

    # changes the text when you click to be "surprise!"
    # lbl.configure(text = "surprise!")


# create the button 
btn = Button(root, text = "Enter", fg = "black", command = clicked)

# put the button in the root window but you can change where it is 
# tkinter uses row and columnns for placements 
btn.grid(column = 2, row = 0)


root.mainloop()