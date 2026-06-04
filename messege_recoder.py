
import sqlite3

conn = sqlite3.connect('responza.db')

c =  conn.cursor()

c.execute('''create table if not exists users(
               email text primary key,
               passward text not null 
               )
        ''')

c.execute('''create table if not exists details(
               email text primary key,
               name text not null,
               profession text not null,
               reply integer,
               FOREIGN KEY (email) REFERENCES users(email)
               )
        ''')

# reply = 0

def inf(email):
    print("_____________welcome to responza_______________")
    print("your email: ", email)
    name = input("enter your name: ")
    profession = input("enter ur profession: ")
  
    c.execute('''insert into details (email,name,profession,reply)
    values (?, ?, ?, ?)''', (email, name, profession,0))
    conn.commit()
    print("Details updated successfully ✅")

def register():
    global email
    email = input("Enter email: ")
    passward = input("enter ur passward : ")
    c.execute("""
    SELECT EXISTS(
    SELECT 1 FROM users WHERE email = ?
    )
    """, (email,))

    result = c.fetchone()[0]

    if result == 0:
        c.execute('''insert into users (email, passward) values (?, ?)''', (email, passward))
        conn.commit()
        print("User registered successfully ✅")
        print("+"*50)
        inf(email)
    else:
        c.execute('''select passward from users where email = ?''',(email,))
        strong_p = c.fetchone()[0]
        if passward == strong_p:
            print("✔️✔️✔️✔️..login successfully..✔️✔️✔️✔️")
        else:
            print("invalid passward .. ")
            register()
    # return email

def all_details(email):
    c.execute('''select * from details where email = ?''',(email,))
    details = c.fetchone()
    if details is not None:
        print("name:",details[1])
        print("profession: ",details[2])
        print("reply:",details[3])
    else:
        print("no details")
    

def update_details(email):
    print("what do you want to update ?")
    print("1. name")
    print("2. profession")
    print("3.reply")
    ch = input("enter update choice: ")
    match ch:
        case '1':
            new_name = input("enter new name: ")
            c.execute('''update details set name = ? where email = ?''',(new_name,email))
            conn.commit()
        case '2':
            new_profession = input("enter new profession: ")
            c.execute('''update details set profession = ? where email = ?''',(new_profession,email))
            conn.commit()
        case '3':
            c.execute(
                    '''UPDATE details SET reply = COALESCE(reply, 0) + 1 WHERE email = ?''',
                    (email,))
            conn.commit()
    print("*"*50)

def delete_account(email):
    c.execute('''delete from users where email = ?''',(email,))
    c.execute('''delete from details where email = ?''',(email,))
    conn.commit()
    print("account deleted successfully...✅")
    print("-"*50)
    register()

        
def logined():
    while True:
        print("\n 1. all details")
        print("2. update details")
        print("3. delete account")
        print("4. exit ")
        print("-------")
        
        choice = input("enter your choice: ") 
        print("*"*50)
        match choice:
            case '1':
                
                all_details(email)
            case '2':
                update_details(email)
            case '3':
                delete_account(email)
            case '4':
                register()
            case _:
                print("invalied choice")
                register()
                     
    
def main():
    register()
    logined()    
    conn.close()
       
if __name__ == "__main__":
    main()
       
