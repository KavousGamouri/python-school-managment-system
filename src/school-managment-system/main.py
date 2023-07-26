import sqlite3


# ADMIN LOGIN FOR FIRSST TIME
# ****************
# username = admin
# password = admin
# ****************

conn = sqlite3.connect('school.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          username text,
          password text,
          privilege text)''')

c.execute('''CREATE TABLE IF NOT EXISTS attendance (
          ID INTEGER PRIMARY KEY AUTOINCREMENT,
          username text,
          date text,
          status text)''')



def teacher_session():
    while True:
        print('')
        print('Teacher Login Successfull')
        print('')
        print('Teacher Menu')
        print('1. Mark Student Register')
        print('2. View Register')
        print('3. Logout')

        user_option = input('Option: ')
        if user_option == '1':
            print('')
            print('Mark Student Register')
            c.execute('SELECT username FROM users WHERE privilege = "student" ')
            records = c.fetchall()
            date = input(str('Date: DD/MM/YYYY: '))
            for record in records:
                record = str(record).replace("'", "")
                record = str(record).replace(",", "")
                record = str(record).replace("(", "")
                record = str(record).replace(")", "")
                # Present | Absent  | Late
                status = input(str('Status for ' + str(record) + 'P/A/L : '))
                query_vals = (str(record),date, status)
                c.execute('INSERT INTO attendance (username,date,status) VALUES (?,?,?)', query_vals)
                conn.commit()
                print(f"{record} Marked as {status}") 
        elif user_option == '2':
            print('')
            print('Viewing all students Register')
            c.execute('SELECT username, date, status FROM attendance')        
            records = c.fetchall()
            print('Display all students Register')
            for record in records:
                print(record)
        elif user_option == '3':
            break
        else:
            print('Invalid Option')

def student_session(username):
    while True:
        print('')
        print('Student Menu')
        print('')
        print('1. View Register')
        print('2. Download Register')
        print('3. Logout')

        user_option = input('Option: ')
        if user_option == '1':
            print('Displaying Register')
            username = (username,)
            c.execute('SELECT date, username, status FROM attendance WHERE username = ?', username)  
            records = c.fetchall()
            for record in records:
                print(record)

        elif user_option == '2':
            print('Downloading Register')
            username = (username,)
            c.execute('SELECT date, username, status FROM attendance WHERE username = ?', username)  
            records = c.fetchall()
            for record in records:
                with open('register.txt', 'w') as f:
                    f.write(str(records) + '\n')
                f.close()
            print('All records saved')       

        elif user_option == '3':
            break
        else:
            print('Invalid Option Selected')

def admin_session():
    while True:
        print('')
        print('Admin Menu')
        print('')
        print('1. Add New Student')
        print('2. Add New Teacher')
        print('3. Delete Student')
        print('4. Delete Teacher')
        print('5. Logout')

        user_option = input('Option: ')
        if user_option == '1':
            print('')
            print('Add New Student')
            username = input('Student Username: ')
            password = input('Student Password: ')
            query_vals = (username, password)
            c.execute('''INSERT INTO users (username, password, privilege) VALUES (?,?,'student')''', query_vals)
            conn.commit()
            print(f'{username} Added Successfully as Student') 

        elif user_option == '2':
            print('')
            print('Add New Teacher')
            username = input('Teacher Username: ')
            password = input('Teacher Password: ')
            query_vals = (username, password)
            c.execute('''INSERT INTO users (username, password, privilege) VALUES (?,?,'teacher')''', query_vals)
            conn.commit()
            print(f'{username} Added Successfully as Teacher')  

        elif user_option == '3':
            print('')
            print('Delete Student Account')
            username = input('Student Username: ')
            query_vals = (username, 'student')
            c.execute('''DELETE FROM users WHERE username =? AND privilege=?''', query_vals)  
            conn.commit()
            if c.rowcount == 0:
                print(f'{username} Account Not Found')
            else:
                print(f'{username} Account Deleted Successfully')    

        elif user_option == '4':
            print('')
            print('Delete Teacher Account')
            username = input('Teacher Username: ')
            query_vals = (username, 'teacher')
            c.execute('''DELETE FROM users WHERE username =? AND privilege=?''', query_vals)
            conn.commit()
            if c.rowcount == 0:
                print(f'{username} Account Not Found')
            else:
                print(f'{username} Account Deleted Successfully')    

        elif user_option == '5':
            break
        else:
            print('Invalid Option')

def auth_student():
    print('')
    print("Student's Login")
    print('')
    username = input('Student Username: ')
    password = input('Student Password: ')
    query_vals = (username,password)
    c.execute('SELECT username FROM users WHERE username = ? AND password = ? AND privilege = "student" ', query_vals)  
    if c.rowcount == 0:
        print('invalid login details')
    else:
        student_session(username)    

def auth_teacher():
    print('')
    print('Teacher Login')
    print('')
    username = input('Username: ')
    password = input('Password: ')
    query_vals = (username, password)
    c.execute('SELECT * FROM users WHERE username =? AND password =? AND privilege = "teacher" ', query_vals)
    conn.commit()
    if c.rowcount == 0:
        print('Login Failed')
    else:
        teacher_session()

def aut_admin():
    print('')
    print('Admin Login')
    print('')
    username = input('Username: ')
    password = input('Password: ')
    if username == 'admin':
        if password == 'admin':
            admin_session()
        else:
            print('Invalid Password')
    else:
        print('Login Failed')            
            
        

def main():
    while True:
        print('Welcome To School Managment System')
        print('')
        print('1. Login As Student')
        print('2. Login As Teacher')
        print('3. Login As Admin')

        user_option = input('Option: ')
        if user_option == '1':
            auth_student()
        elif user_option == '2':
            auth_teacher()
        elif user_option == '3':
            aut_admin()
        else:
            print('Invalid Option')

main()            