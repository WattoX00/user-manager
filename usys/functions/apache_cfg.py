class ApacheFunctions:
    @staticmethod
    def apacheStart():
        cmd = ["sudo", "systemctl", "start", "apache2"]
        if Functions.executeCmd(cmd):
            print("Apache started.")

    @staticmethod
    def apacheStop():
        cmd = ["sudo", "systemctl", "stop", "apache2"]
        if Functions.executeCmd(cmd):
            print("Apache stopped.")

    @staticmethod
    def apacheRestart():
        cmd = ["sudo", "systemctl", "restart", "apache2"]
        if Functions.executeCmd(cmd):
            print("Apache restarted.")

    @staticmethod
    def apacheStatus():
        cmd = ["systemctl", "status", "apache2"]
        Functions.executeCmd(cmd, check=False)

    @staticmethod
    def apacheConfigTest():
        cmd = ["sudo", "apache2ctl", "configtest"]
        result = Functions.executeCmd(cmd, capture=True)

        if result:
            print(result.stdout)

    @staticmethod
    def apacheCreateTestSite():
        import os

        site_name = input("Site name: ").strip().lower()

        if not site_name:
            print("Invalid site name.")
            return

        site_path = f"/var/www/{site_name}"

        if os.path.exists(site_path):
            print("Site already exists.")
            return

        Functions.executeCmd(["sudo", "mkdir", "-p", site_path])

        html = f"<h1>{site_name} works!</h1>"

        Functions.executeCmd([
            "sudo", "bash", "-c",
            f"echo '{html}' > {site_path}/index.html"
        ])

        print(f"Test site created at {site_path}")

    @staticmethod
    def apacheCreateVHost():
        import os

        domain = input("Domain: ").strip().lower()

        if not domain:
            print("Invalid domain.")
            return

        docroot = f"/var/www/{domain}"

        config = f"""
    <VirtualHost *:80>
        ServerName {domain}

        DocumentRoot {docroot}

        <Directory {docroot}>
            AllowOverride All
            Require all granted
        </Directory>

        ErrorLog ${{APACHE_LOG_DIR}}/{domain}_error.log
        CustomLog ${{APACHE_LOG_DIR}}/{domain}_access.log combined
    </VirtualHost>
    """

        config_path = f"/etc/apache2/sites-available/{domain}.conf"

        Functions.executeCmd([
            "sudo", "bash", "-c",
            f"echo '{config}' > {config_path}"
        ])

        print(f"VirtualHost created: {config_path}")

    @staticmethod
    def apacheEnableSite():
        site = input("Site config name (example.conf): ").strip()

        cmd = ["sudo", "a2ensite", site]

        if Functions.executeCmd(cmd):
            print(f"Site '{site}' enabled.")

    @staticmethod
    def apacheDisableSite():
        site = input("Site config name: ").strip()

        cmd = ["sudo", "a2dissite", site]

        if Functions.executeCmd(cmd):
            print(f"Site '{site}' disabled.")
