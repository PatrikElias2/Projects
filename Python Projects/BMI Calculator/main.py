from tkinter import *
import psycopg2

root = Tk()
root.title('BMI')
root.geometry('250x250')
root.resizable(False,False)


# functions
def calculate_bmi(weight, height):
    try:
        weight = float(weight)
        height = float(height)
    except ValueError:
        user_result_1_label['text'] = 'error'
        user_result_2_label['text'] = 'error'
        return None
    
    bmi = round(weight / height**2, 2)

    if bmi < 18.5:
        text_result = 'Underweight'
    elif bmi < 24.9:
        text_result = 'Normal'
    elif bmi < 29.9:
        text_result = 'Overweight'
    elif bmi < 34.9:
        text_result = 'Obese'
    elif bmi >= 34.9:
        text_result = 'Extreme obesity'
    
    user_result_1_label['text'] = bmi
    user_result_2_label['text'] = text_result

    insert_data(bmi, text_result)


def dot_checker(number):
    number_string = str(number)
    return number_string.replace(',', '.') if ',' in number_string else number_string

def insert_data(bmi_n, bmi_t):
    query = '''INSERT INTO bmi(bmi_number, bmi_text) VALUES (%s, %s)'''
    with psycopg2.connect(dbname='BMI', user='postgres', password='admin', host='localhost', port='5432') as conn:
        with conn.cursor() as cur:
            cur.execute(query, (bmi_n, bmi_t))


def count_data():
    query = '''SELECT COUNT(bmi_id) FROM bmi'''
    with psycopg2.connect(dbname='BMI', user='postgres', password='admin', host='localhost', port='5432') as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            return cur.fetchone()[0]


# general label
general_label = Label(root, text='Calculation of BMI')
general_label.grid(row=0,column=1)

# weight section
weight_label = Label(root, text='Set weight (kg): ')
weight_label.grid(row=1,column=0)

entry_weight = Entry(root)
entry_weight.grid(row=1,column=1)

# height section
height_label = Label(root, text='Set height (m): ')
height_label.grid(row=2,column=0)

entry_height = Entry(root)
entry_height.grid(row=2,column=1)

# button
button = Button(root, text='Calculate', command=lambda:calculate_bmi(dot_checker(entry_weight.get()), dot_checker(entry_height.get())))
button.grid(row=3, column=1)

# result section
result_1_label = Label(root,text='Number result: ')
result_1_label.grid(row=4,column=0)

user_result_1_label = Label(root)
user_result_1_label.grid(row=4,column=1)

result_2_label = Label(root,text='Result: ')
result_2_label.grid(row=5,column=0)

user_result_2_label = Label(root)
user_result_2_label.grid(row=5,column=1)

label_count_text = Label(root,text='Number of users: ')
label_count_text.grid(row=6, column=0)

label_count_number = Label(root,text=count_data())
label_count_number.grid(row=6, column=1)

root.mainloop()