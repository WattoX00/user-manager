import subprocess
import os

class SambaFunctions:

    SAMBA_CONF = "/etc/samba/smb.conf"
    SHARE_BASE = "/srv/samba"

    @staticmethod
    def executeCmd(cmd, check=True, capture=False):
        try:
            result = subprocess.run(
                cmd,
                check=check,
                capture_output=capture,
                text=True
            )
            if capture:
                return result.stdout.strip()
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def installSamba():
        print("Installing Samba server...")
        cmd = ["sudo", "apt", "install", "-y", "samba"]
        if SambaFunctions.executeCmd(cmd):
            print("Samba installed successfully.")

    @staticmethod
    def startSamba():
        cmd = ["sudo", "systemctl", "start", "smbd"]
        if SambaFunctions.executeCmd(cmd):
            print("Samba service started.")

    @staticmethod
    def stopSamba():
        cmd = ["sudo", "systemctl", "stop", "smbd"]
        if SambaFunctions.executeCmd(cmd):
            print("Samba service stopped.")

    @staticmethod
    def enableSamba():
        cmd = ["sudo", "systemctl", "enable", "smbd"]
        if SambaFunctions.executeCmd(cmd):
            print("Samba enabled at boot.")

    @staticmethod
    def disableSamba():
        cmd = ["sudo", "systemctl", "disable", "smbd"]
        if SambaFunctions.executeCmd(cmd):
            print("Samba disabled at boot.")

    @staticmethod
    def restartSamba():
        cmd = ["sudo", "systemctl", "restart", "smbd"]
        if SambaFunctions.executeCmd(cmd):
            print("Samba restarted.")

    @staticmethod
    def sambaStatus():
        cmd = ["systemctl", "status", "smbd"]
        output = SambaFunctions.executeCmd(cmd, capture=True)
        if output:
            print(output)

    @staticmethod
    def addSambaUser(username):
        print(f"Adding samba user: {username}")
        cmd = ["sudo", "smbpasswd", "-a", username]
        SambaFunctions.executeCmd(cmd, check=False)

    @staticmethod
    def removeSambaUser(username):
        cmd = ["sudo", "smbpasswd", "-x", username]
        if SambaFunctions.executeCmd(cmd):
            print(f"Samba user '{username}' removed.")

    @staticmethod
    def enableSambaUser(username):
        cmd = ["sudo", "smbpasswd", "-e", username]
        if SambaFunctions.executeCmd(cmd):
            print(f"Samba user '{username}' enabled.")

    @staticmethod
    def disableSambaUser(username):
        cmd = ["sudo", "smbpasswd", "-d", username]
        if SambaFunctions.executeCmd(cmd):
            print(f"Samba user '{username}' disabled.")

    @staticmethod
    def createShareFolder(folder):
        path = os.path.join(SambaFunctions.SHARE_BASE, folder)

        if not os.path.exists(path):
            SambaFunctions.executeCmd(["sudo", "mkdir", "-p", path])
            print(f"Folder created: {path}")
        else:
            print("Folder already exists.")

    @staticmethod
    def removeShareFolder(folder):
        path = os.path.join(SambaFunctions.SHARE_BASE, folder)

        if os.path.exists(path):
            SambaFunctions.executeCmd(["sudo", "rm", "-rf", path])
            print(f"Folder removed: {path}")

    @staticmethod
    def setFolderOwner(folder, username, group):
        path = os.path.join(SambaFunctions.SHARE_BASE, folder)
        cmd = ["sudo", "chown", "-R", f"{username}:{group}", path]
        if SambaFunctions.executeCmd(cmd):
            print(f"Ownership set to {username}:{group}")

    @staticmethod
    def setFolderPermissions(folder, perms):
        path = os.path.join(SambaFunctions.SHARE_BASE, folder)
        cmd = ["sudo", "chmod", "-R", perms, path]
        if SambaFunctions.executeCmd(cmd):
            print(f"Permissions set to {perms}")

    @staticmethod
    def addShareConfig(name, folder, valid_users="", valid_groups="", read_only="no"):
        path = os.path.join(SambaFunctions.SHARE_BASE, folder)

        config = f"""
[{name}]
   path = {path}
   browseable = yes
   read only = {read_only}
"""

        if valid_users:
            config += f"   valid users = {valid_users}\n"

        if valid_groups:
            config += f"   valid users = @{valid_groups}\n"

        try:
            with open("/tmp/samba_share.conf", "w") as f:
                f.write(config)

            SambaFunctions.executeCmd(
                ["sudo", "bash", "-c", f"cat /tmp/samba_share.conf >> {SambaFunctions.SAMBA_CONF}"]
            )

            print(f"Share '{name}' added.")
            SambaFunctions.restartSamba()

        except Exception:
            print("Failed to write samba configuration.")

    @staticmethod
    def listShares():
        try:
            with open(SambaFunctions.SAMBA_CONF, "r") as f:
                lines = f.readlines()

            for line in lines:
                if line.strip().startswith("[") and not line.strip().startswith("[global]"):
                    print(line.strip())

        except Exception:
            print("Unable to read smb.conf")

    @staticmethod
    def testConfig():
        cmd = ["testparm", "-s"]
        output = SambaFunctions.executeCmd(cmd, capture=True)
        if output:
            print(output)

    @staticmethod
    def listConnections():
        cmd = ["sudo", "smbstatus"]
        output = SambaFunctions.executeCmd(cmd, capture=True)
        if output:
            print(output)

    @staticmethod
    def folderPermissions(folder):
        path = os.path.join(SambaFunctions.SHARE_BASE, folder)
        cmd = ["ls", "-ld", path]
        output = SambaFunctions.executeCmd(cmd, capture=True)
        if output:
            print(output)

    @staticmethod
    def listSharedFiles(folder):
        path = os.path.join(SambaFunctions.SHARE_BASE, folder)
        cmd = ["ls", "-l", path]
        output = SambaFunctions.executeCmd(cmd, capture=True)
        if output:
            print(output)
