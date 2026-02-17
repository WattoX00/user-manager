class Functions():

    def userName():
        Functions.listUsers()
        username = str(input('User name: ')).lower().strip()
        return username

    def executeCmd(cmd, check=True, capture=False):
        import subprocess
        return subprocess.run(cmd, check=check, capture_output=capture, text=True)
