import bcrypt
import psycopg2
from tkinter import *

def password_to_hash(plain_password):
    try:
        password_bytes = plain_password.encode('utf-8')
        hash = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
        return hash
    except Exception as e:
        print(f'Error hashing password: {e}')
        return None

# inserting data
def insert_bank_user(email, password):
    try:
        connection = psycopg2.connect(
            dbname='company',
            user='postgres',
            password='sennheiser25',
            host='localhost',
            port='5432'
        )


        cur = connection.cursor()
        query = '''INSERT INTO bank_user(email, password) VALUES(%s, %s)'''
        
        hash = password_to_hash(password)

        cur.execute(query, (email, hash))
        connection.commit()
        connection.close()
    except psycopg2.DatabaseError as e:
        print(f'Error database: {e}')
    except Exception as e:
        print(f'General error: {e}')


# Getting hashed password
def get_hash_from_database(email):
    try:
        connection = psycopg2.connect(
            dbname='bank',
            user='postgres',
            password='admin',
            host='localhost',
            port='5432'
        )

        cur = connection.cursor()
        query = '''SELECT password FROM bank_user WHERE email=(%s)'''


        cur.execute(query, (email,))
        user_hash_password = cur.fetchone()
        connection.close()
        if user_hash_password:
            return bytes.fromhex(user_hash_password[0][2:])
        else:
            return b''
    except psycopg2.DatabaseError as e:
        print(f'Error databáze: {e}')
        return b''
    except Exception as e:
        print(f'Obecná chyba: {e}')
        return b''

def login_authentication(password, email):
    try:
        hash = get_hash_from_database(email)
        password_bytes = bytes(password, encoding='utf-8')
        if hash == b'':
            result_label['text'] = 'Invalid'
        else:
            if bcrypt.checkpw(password_bytes, hash):
                result_label['text'] = 'Login successful'
            else:
                result_label['text'] = 'Invalid'
    except Exception as e:
        result_label['text'] = 'Došlo k chybě při ověřování'
        print(f'Cyhba při ověřování: {e}')


root = Tk()
root.title('Registration and log in')
root.geometry('300x300')
root.resizable(False, False)


# Registration section
registration_label = Label(text='Registration')
registration_label.grid(row=0, column=1)


email_label = Label(text='Email: ')
email_label.grid(row=1, column=0)


email_entry = Entry()
email_entry.grid(row=1, column=1)


password_label = Label(text='Password: ')
password_label.grid(row=2, column=0)


password_entry = Entry(show='*')
password_entry.grid(row=2, column=1)

registration_button = Button(text='Registrate', command=lambda: insert_bank_user(email_entry.get(), password_entry.get()))
registration_button.grid(row=3, column=1)



# Login section
login_label = Label(text='Log in')
login_label.grid(row=4, column=1)


email_login_label = Label(text='Email: ')
email_login_label.grid(row=5, column=0)


email_login_entry = Entry()
email_login_entry.grid(row=5, column=1)


password_login_label = Label(text='Password: ')
password_login_label.grid(row=6, column=0)


password_login_entry = Entry(show='*')
password_login_entry.grid(row=6, column=1)

login_button = Button(text='Log in',command=lambda: login_authentication(password_login_entry.get(), email_login_entry.get()))
login_button.grid(row=7, column=1)

# Result section
result_label = Label()
result_label.grid(row=8, column=1)

root.mainloop()

