import tkinter as tk
import math

'''This function makes the window appear in the center of the screen'''

def center_window(window : tk, width : int, height : int) -> None:
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    pos_x = int((screen_width - width) / 2) 
    pos_y = int((screen_height - height) / 2)

    window.geometry(f"{width}x{height}+{pos_x}+{pos_y}")

window = tk.Tk()

window.title("Mi calculadora")

center_window(window, 350, 475)

window.update_idletasks()

window_width = window.winfo_width()
window_height = window.winfo_height()


'''UNICODE CHARACTERS:  \u00F7 -> division (/)
                        x\u00B2 -> squaring (x**2)
                        \u221A -> square root (math.sqrt())'''

division_char = '\u00F7'
square_char = 'x\u00B2'
sqroot_char = '\u221A'


'''The class MyNumber is used to represent the numbers we use in the calculator:
-self.actual represents the number the user is manipulating at the moment
-self.previous represents the previous number (either written by the user or the previous result)
(these two atributes initially are strings because the concatenation of the numbers the user is typing is easier to make with strings than
with numbers)

-self.operation represents the arithmetical operation the user wants to do
-self.result is a boolean variable useful to control if we want to show the number the user is typing or the result of an operation'''

class MyNumber:
    def __init__(self) -> None:
        self.actual = ''
        self.previous = ''
        self.operation = ''
        self.result = False

    def concatenate_number(self, num):
        #Function to concatenate the numbers that the user is typing 
        self.result = False
        
        if num == '.' and '.' in self.actual:
            ...
        elif isinstance(self.actual, str):
            self.actual += num
        else:
            self.actual = num
            self.operation = 's'

    def eliminate_number(self):
        #Function to pass self.actual to self.previous and eliminate self.actual to be manipulated again by the user
        if self.actual != '':
            num = float(self.actual)
            if num.is_integer():
                self.previous = int(num)
            else:
                self.previous = num

        self.actual = ''
        return self.previous
    
    
    
    def choose_operation(self, oper):
        #Function to change self.operation to the operation the user wants to do
        
        if not self.result and self.operation not in ['', square_char, sqroot_char]:
            self.do_operation(self.operation)
        
        self.operation = oper
        
        if self.previous == '':
            self.eliminate_number()
        else:
            self.actual = ''
        
        if self.operation in one_operations:
            self.do_operation(self.operation)
    
    def do_operation(self, oper : str):
        #Function to do the operation the user wants to do with self.previous and self.actual 
        self.result = True
        if self.actual != '':
            if isinstance(self.actual, str) and self.actual[-1] == '.':
                self.actual = self.actual[:-1]

            num = float(self.actual)
            if num.is_integer():
                self.actual = int(num)
            else:
                self.actual = num
        else: 
            self.actual = 0

        if oper == '+':
            res = self.previous + self.actual
        elif oper == '-':
            res = self.previous - self.actual
        elif oper == 'x':
            res = self.previous * self.actual
        elif oper == division_char:
            res = self.previous / self.actual
        elif oper == square_char:
            res = self.previous ** 2
        elif oper == sqroot_char:
            res = math.sqrt(self.previous)
        else:
            res = self.actual
        
        res = round(res, 12)
        
        if isinstance(res, float) and res.is_integer():
            res = int(res)
        
        self.previous = res
        
    
    def AC(self):
        #Function to delete all and come back to the initial state
        self.actual = ''
        self.previous = ''
        self.operation = ''
        self.result = False
    

principal = MyNumber()

'''The label is the part of the window that shows the numbers. It occupies a third of the window'''

label_width = window_width
label_height = window_height / 3


label_font = ('consolas', 26)

label = tk.Label(window, text = '', bg = 'black', fg = 'white', anchor = 'e', font = label_font)
label.place(x = 0, y = 0, width = label_width, height = label_height)

def update_label():
    '''Function to update the label with the numbers we want to appear. If principal.result is False, we want to show the number
    the user is manipulating (self.actual), and if it is True, we want to show the result (self.previous)'''
    if not principal.result and principal.actual != '':
            actual_value = principal.actual
    
    elif principal.result or (not principal.result and principal.actual == ''):
        actual_value = principal.previous

    label.config(text = f'{actual_value}')
    window.after(1, update_label)

update_label() 

'''The buttons have the width and height to create a 4x5 matrix of buttons (There is a bigger button but it occupies the size of two)'''

buttons_width = window_width / 4
buttons_height = window_height * (2 / 15)
buttons_font = ('consolas', 20)

number = 1
for i in range(1, 4):
    for j in range(1, 4):
        button = (tk.Button(window, text = str(number), command = lambda num = str(number) : principal.concatenate_number(num)))
        button.place(x = (j-1) * buttons_width , 
                     y = (window_height * (7/15)) + (i-1) * buttons_height, 
                     width = buttons_width, 
                     height = buttons_height)
        number += 1

button0 = (tk.Button(window, text = '0', command = lambda num = '0' : principal.concatenate_number(num)))
button0.place(x = 0, 
              y = window_height - buttons_height, 
              width = buttons_width * 2, 
              height = buttons_height)

comma = (tk.Button(window, text = '.', command = lambda num = '.' : principal.concatenate_number(num)))
comma.place(x = buttons_width * 2, 
            y = window_height - buttons_height, 
            width = buttons_width, 
            height = buttons_height)

operations = [division_char, 'x', '-', '+']

for i in range(len(operations)):
    button = (tk.Button(window, text = operations[i], command = lambda res = operations[i]: principal.choose_operation(res)))
    button.place(x = window_width - buttons_width, 
                 y = label_height + (i * buttons_height), 
                 width = buttons_width, 
                 height = buttons_height)
    

one_operations = [sqroot_char, square_char]

for i in range(len(one_operations)):
    button = (tk.Button(window, text = one_operations[i], command = lambda res = one_operations[i]: principal.choose_operation(res)))
    button.place(x = buttons_width * (i + 1),
                 y = label_height, 
                 width = buttons_width, 
                 height = buttons_height)
    

AC_button = tk.Button(window, text = 'AC', command = lambda : principal.AC())
AC_button.place(x = 0, 
                y = label_height, 
                width = buttons_width, 
                height = buttons_height)


equal_button = tk.Button(window, text = '=', command = lambda : principal.do_operation(principal.operation))
equal_button.place(x = window_width - buttons_width, 
                   y = window_height - buttons_height, 
                   width=buttons_width, 
                   height=buttons_height)



'''This is to control the colors of the buttons'''

for widget in window.winfo_children():
    if isinstance(widget, tk.Button):
        widget.config(font = buttons_font, bg = '#747474', fg = 'white')
        widget.bind('<Enter>', lambda event, button = widget : button.config(bg = '#606060'))
        widget.bind('<Leave>', lambda event, button = widget : button.config(bg = '#747474'))
        widget.bind('<Button-1>', lambda event, button = widget : button.config(bg = '#2C2C2C', activebackground='#2C2C2C', activeforeground='white'))
        widget.bind('<ButtonRelease-1>', lambda event, button = widget : button.config(bg = '#606060'))


        

window.mainloop()


    



