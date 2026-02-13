from functions import Functions

while True:
    print("1. add user\n2. remove user\n3. List groups")
    inp = str(input('> '))
    if inp == '1':
        Functions.userAdd()
    elif inp == '2':
        Functions.deleteUser()
    elif inp == '3':
        Functions.listGroups()
    elif inp == '4':
        Functions.listUsers()
    else:
        print("nothing is selected")
        break
