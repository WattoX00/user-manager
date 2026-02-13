import subprocess


def userAdd():
    newUserName = str(input('New User Name: '))
    # Home Directory
    homeQ = str(input(f'Do you want to add home directory [home/{newUserName}] (Y/n)')).lower()
    homeDir = ''
    if homeQ in ('y','yes',''):
        homeDir = '-m'
        
    groupQ = str(input(f'Do you want to add ({newUserName}) to a group (Y/n)')).lower()
    groupName = ''
    if groupQ in ('y','yes',''):
        listGroups()
        groupName = str(input('Type the primary group first then space them with space ( ) for secondary groups ')).lower()
    if len(groupName.split(' ')) > 1:
        list_of_groups = groupName.split(' ')
        first_group = '-g '+list_of_groups[0]
        list_of_groups.pop(0)
        secondary_groups = '-G '+",".join(list_of_groups)
    elif len(groupName.split(' ')) == 1:
        frist_group = '-g '+groupName
        secondary_groups = ''
    else:
        first_group = ''
        secondary_groups = ''
    subprocess.run(["bash", "-c", f"sudo useradd {homeDir} {first_group} {secondary_groups} {newUserName}"])

#subprocess.run(["bash", "-c", "echo hello world"])

def listGroups():
    subprocess.run(["bash", "-c", "getent group | awk -F: '$3 >= 1000 || $1 ~ /^(sudo|wheel|docker)$/ {print $1}'"])


userAdd()

