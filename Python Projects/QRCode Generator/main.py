import pyqrcode
from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.title('QR Generator')
window.geometry('300x300')
window.resizable(False,False)

# Global variable
global_photo_image = None


# function
def generate_qr_code():
    global global_photo_image
    qr = pyqrcode.create(url_entry.get())
    qr.png('qr_code.png',scale=5)

    img = Image.open('qr_code.png')
    global_photo_image = ImageTk.PhotoImage(img)
    
    label = Label(window, image=global_photo_image)
    label.pack()


url_label = Label(window, text='Type url address')
url_label.pack(pady=(10,5))

url_entry = Entry(window, width=40)
url_entry.pack(pady=(0,20))

button = Button(text='Generate QR code', command=generate_qr_code)
button.pack()

window.mainloop()