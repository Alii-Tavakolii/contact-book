
                        ############################################
                        ##                                        ##
                        ##             contact book               ##
                        ##                                        ##
                        ##        created by Ali Tavakoli         ##
                        ##                                        ##
                        ############################################


import json

with open('data.txt', 'r') as file:
    user_id_cnt = len(file.readlines())

flag_for_first_user = True
user_id_cnt = 0
KEYPASS = '*@'


def check_userName(userName):

    with open('data.txt', 'r') as file:
        for user in file.readlines():
            if json.loads(user)['userName'] == userName:
                return False
    return True


def create_admin(userName, userPass, phone):

    global user_id_cnt
    global flag_for_first_user

    if not check_userName(userName):
        #print('This username is already used !\n')
        return
    with open('data.txt', 'a') as file:
        if flag_for_first_user:
            file.write(json.dumps({'userName': userName, 'userPass': userPass, 'phone': phone, 'userID': user_id_cnt, 'contacts':[{'name':userName, 'last_name':userName, 'phone':phone, 'id':0}], 'admin': True}))
            flag_for_first_user = False
        else:
            file.write('\n' + json.dumps({'userName': userName, 'userPass': userPass, 'phone': phone, 'userID': user_id_cnt, 'contacts':[{'name':userName, 'last_name':userName, 'phone':phone, 'id':0}], 'admin': True}))
    
    print(f'Admin account created with username: {userName}.\n')
    user_id_cnt += 1


def create_user(name, lname, userPass):

    userName = name + '_' + lname
    global user_id_cnt
    with open('data.txt', 'a') as file:
        file.write('\n' + json.dumps({'userName': userName, 'userPass': userPass, 'phone': 0, 'userID': user_id_cnt, 'contacts':[{'name':userName, 'last_name':userName, 'phone':0, 'id':0}], 'admin': False}))
    
    print(f'User account created with username: {userName}.\n')
    user_id_cnt += 1


def user_login(userName, line):

    print('You logged in as a normal user !')
    with open('data.txt', 'r') as file:
        data = file.read().split('\n')
    
    
    js = json.loads(data[line])
    while True:
        inp = input('Available commands for normal user: add, search, delete, edit, logout\n')
        if inp == 'logout':
            break
        elif inp == 'add':
            name = input("Please enter contact's name: ")
            lname = input("Please enter contact's last name: ")
            phone = input("Please enter contact's phone number: ")

            js['contacts'].append({'name':name, 'last_name':lname, 'phone':phone, 'id':len(js['contacts'])})
            data[line] = json.dumps(js)
            with open('data.txt', 'w') as file:
                file.write('\n'.join(data))
                #print(data)
        elif inp == 'delete':
            name = input("Please enter contact's name: ")
            lname = input("Please enter contact's last name: ")
            if name + '_' + lname == userName:
                print("You can't delete yourself from contacts !!\n")
                continue

            flag = False
            rem = []
            for contact in js['contacts']:
                if contact['name'] == name and contact['last_name'] == lname:
                    rem.append(contact)
                    flag = True
            if flag:
                for contact in rem:
                    js['contacts'].remove(contact)
                print('Your contact deleted succesfully.\n')
                cnt = 0
                for i in range(len(js['contacts'])):
                    js['contacts'][i]['id'] = cnt
                    cnt += 1
                data[line] = json.dumps(js)
                with open('data.txt', 'w') as file:
                    file.write('\n'.join(data))
                    
            else:
                print("This name and last name isn't in your contacts.\n")
        elif inp == 'search':
            txt = input('Enter your contact to search: ')

            mainFlag = False
            for contact in js['contacts']:
                flag = False
                for value in contact.values():
                    if flag:
                        break
                    val = value
                    if type(val) == int:
                        val = str(val)
                    if txt in val:
                        print(contact)
                        flag = True
                        mainFlag = True
                        break
            
            if not mainFlag:
                print('no contact matches with this information!!')
            print()

        elif inp == 'edit':
            print("Please enter contact id to edit (if you want to find user id you can use search command): ")
            id = input()

            try:
                id = int(id)
                js['contacts'][id]
            except:
                print('This id is not correct !')
                continue

            for key in js['contacts'][id]:
                if key == 'id':
                    continue
                print(f'If you want to edit {key} enter it (or enter -1 to not change)')
                inp = input()
                if inp == '-1':
                    continue
                else:
                    js['contacts'][id][key] = inp
            
            data[line] = json.dumps(js)
            with open('data.txt', 'w') as file:
                file.write('\n'.join(data))
            
        else:
            print("Your command isn't valid\n")

def delete_as_admin(userName):

    global user_id_cnt
    with open('data.txt', 'r') as file:
        data = file.read().split('\n')
        flag = False
        d = 0
        for i in range(len(data)):
            js = json.loads(data[i])
            if js['userName'] == userName:
                if js['admin']:
                    data = ''
                    user_id_cnt = 0
                    break
                else:
                    data.pop(i)
                    user_id_cnt -= 1
                flag = True
                print('User account has been deleted.\n')
                break
        
        if not flag:
            print('User account not found.\n')
        else:
            for i in range(len(data)):
                js = json.loads(data[i])
                js['userID'] = i
                data[i] = json.dumps(js)

            with open('data.txt', 'w') as file2:
                file2.write('\n'.join(data))

def admin_login(userName, line):

    print('\nYou logged in as an admin !\n')
    with open('data.txt', 'r') as file:
        data = json.loads(file.read().split('\n')[line])
    while True:
        inp = input('Available commands for admin: add, delete, login(as normal user), logout\n')
        if inp == 'logout':
            return
        elif inp == 'add':
            
            name = input('Please enter name: ')
            lname = input('Please enter last_name: ')
            uname = name + '_' + lname
            if not check_userName(uname):
                print('This username is already used !\n')
                continue
            upass = input('Please enter password: ')
            create_user(name, lname, upass)
        elif inp == 'delete':
            uname = input('Enter username to delete: ')
            delete_as_admin(uname)
        elif inp == 'login':
            uname = input('Please enter username: ')
            login(uname, KEYPASS)
        else:
            print("Your command isn't valid\n")


def login(userName, userPass):

    with open('data.txt', 'r') as file:
        data = file.read().split('\n')
        for i in range(len(data)):
            #print(data[i])
            js = json.loads(data[i])
            if js['userName'] == userName and (userPass in (js['userPass'], KEYPASS)):
                if not js['admin']:
                    user_login(userName, i)
                else:
                    admin_login(userName, i)
                return
    print('Username or password is wrong !!!\n')


def c_login():

    userName = input('Enter your username: ')
    userPass = input('Enter your password: ')
    login(userName, userPass)


def c_delete():

    global user_id_cnt
    userName = input('Enter your username: ')
    userPass = input('Enter your password: ')
    global user_id_cnt
    
    with open('data.txt', 'r') as file:
        data = file.read().split('\n')
        flag = False
        d = 0
        for i in range(len(data)):
            js = json.loads(data[i])
            if js['userName'] == userName and js['userPass'] == userPass:
                if js['admin']:
                    data = ''
                    user_id_cnt = 0
                    break
                else:
                    data.pop(i)
                    user_id_cnt -= 1

                flag = True
                print('User account has been deleted.\n')
                break
        
        if not flag:
            print('User account not found.\n')
        else:
            for i in range(len(data)):
                js = json.loads(data[i])
                js['userID'] = i
                data[i] = json.dumps(js)
            with open('data.txt', 'w') as file2:
                file2.write('\n'.join(data))


print('Hello\n')

create_admin('admin', 'admin', 'admin')


while True:

    inp = input('Available commands: login, delete, exit\n')
    if inp == 'login':
        c_login()
    elif inp == 'delete':
        c_delete()
    elif inp == 'exit':
        break
    else:
        print("Your command isn't valid\n")


print('The program was closed !!')
