# https://camillovisini.medium.com/create-a-macos-menu-bar-app-with-python-pomodoro-timer-f941f75602d1
# https://readthedocs.org/projects/rumps/downloads/pdf/latest/
import rumps
import shlex
import subprocess


class ReChargeApp(object):
    def __init__(self):
        self.config = {
            "app_name": "ReCharge",
            "pause": "Charge to 100%",
            "start": "Charge to 80%",
            "enable_alerts": "Enable alerts",
            "disable_alerts": "Disable alerts",
            "quit": "Quit",
        }
        self.app = rumps.App(self.config["app_name"])
        self.alerts_enabled = True
        self.set_up_menu(False)
        self.start_pause_button = rumps.MenuItem(title=self.config["start"], callback=self.start_recharge, key='r')
        self.alerts_button = rumps.MenuItem(title=self.config["disable_alerts"], callback=self.set_alerts)
        self.app.quit_button = rumps.MenuItem(title=self.config["quit"], callback=None, key='q')
        self.app.menu = [self.start_pause_button, self.alerts_button]

    def set_up_menu(self, is_recharge_on):
        # icons by https://www.flaticon.com/authors/pixel-perfect
        if is_recharge_on:
            self.app.icon = "renew.png"
        else:
            self.app.icon = "stop-renew.png"

    def set_alerts(self, sender):
        if sender.title == "Disable alerts":
            sender.title = self.config["enable_alerts"]
            self.alerts_enabled = False
        else:
            sender.title = self.config["disable_alerts"]
            self.alerts_enabled = True

    def set_max_charge(self, max_charge, sender):
        process = subprocess.Popen(shlex.split("chmod +x smcutil"))
        process.communicate()
        max_charge_hex = hex(max_charge - 3)  # subtract 3 as smcutil is weird

        try:
            process = subprocess.Popen(
                shlex.split("/usr/bin/osascript -e \'do shell script \"./set_max_charge.sh {} 2>&1 etc\" with "
                            "administrator privileges\'".format(str(max_charge_hex)[2:])),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True)
            out, error = process.communicate()
        except Exception as e:
            rumps.alert(title="There was a problem setting the charge limit.",
                        message="Please make sure you have administrator privileges.")
            return
        if error:
            rumps.alert(title="There was a problem setting the charge limit.",
                        message="Please make sure you have administrator privileges. Error: {}".format(error))
            return
        else:
            if max_charge == 100:
                self.set_up_menu(is_recharge_on=False)
                sender.title = self.config["start"]
                if self.alerts_enabled:
                    rumps.alert(message="Success! The battery will now fully charge.", title="ReCharge")
                return
            elif max_charge == 80:
                self.set_up_menu(is_recharge_on=True)
                sender.title = self.config["pause"]
                if self.alerts_enabled:
                    rumps.alert(
                        message="Success! If your MacBook currently has more than 80% charge, leave the charger "
                                "unplugged until the battery level is a little less than that. Afterwards, "
                                "you can leave the MacBook connected to the charger and the battery will not charge "
                                "over 80%.", title="ReCharge")
                return

    def start_recharge(self, sender):
        if sender.title == "Charge to 80%":
            self.set_max_charge(80, sender)
            # start recharge -- 80%
        else:
            self.set_max_charge(100, sender)
            # pause recharge -- 100%

    def run(self):
        self.app.run()


if __name__ == '__main__':
    app = ReChargeApp()
    app.run()
