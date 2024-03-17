global _print 

import sys
from textual.app import App, ComposeResult
from textual.containers import Container, VerticalScroll, Horizontal, Vertical
from textual.widgets import Header, Footer, Switch, Static, Button, LoadingIndicator,Checkbox,  Tabs, Markdown, Input, Log

import threading, time, ctypes, pwinput, ctypes, os, time, traceback, json, threading, requests, discord


# modules 

from core import untils, installer, auth, sec, config, rp, css, ui, docs as docs_file, logger, xd
from twitch import gen, integrity, follow, view, chat, advertise, react, report, unfollow






docs = docs_file.docs


logo = """   _  __              ___         
  / |/ /__ _  _____  / (_)__  ___ 
 /    / _ \ |/ / _ \/ / / _ \/ -_)
/_/|_/\___/___/\___/_/_/_//_/\__/ 
                                  
"""


user_key = ""
config_file = json.loads(open("data/config.json","r").read())








config_key = config_file['key']
if config_key != "":
    user_key = config_key
else:
    os.system("cls")
    user_key = pwinput.pwinput(prompt = "\n [?] KEY  >> ", mask='•')





    






def login(self):
    self.key = user_key
    self.ip = ipp
    self.computer_name = computer_name
    self.computer_username = usernamee
    self.auth = auth.Authentication(
        key=self.key,
        fingerprint= untils.get_fingerprint(),
        kill = self.force_kill
        )
    res = self.auth.auth()
    if res == 200:
        self.auth.start_check()
        return True # ok
    elif res == 400:
        ctypes.windll.user32.MessageBoxW(0, "Invalid password", "Auth", 1)
        time.sleep(3)
        self.force_kill() # time expired / invalid
    elif res == 404:
        self.force_kill() # error
    elif res == 500:
        self.force_kill() # connection error



print = logger.log








class NovoUi(App):

    ACTIVE_EFFECT_DURATION = 0.3
    CSS = css.CSS
    ACTIVE = ""

    def _print(self, message):
        self.log_object.write(str(message) + "\n")
        

    def run_installer(self):
        installer.Installer()

    def compose(self) -> ComposeResult:

        self.force_kill = sec.start_protection()
        self.data = {
            "proxies": open("data/proxies.txt","r").read().splitlines(),
            "usernames": open("data/usernames.txt","r").read().splitlines(),
            "token": open("data/token.txt","r").read().splitlines(),
            "integrity": open("integrity.txt","r").read().splitlines(),
            "config":  json.loads(open("data/config.json","r").read()),
        }
        os.system("cls")
        if self.data['config']['presence'] == True:
            threading.Thread(target=rp.set_presence).start()
        ctypes.windll.kernel32.SetConsoleTitleW(f"Novoline AIO > " + config.version)
        self.key = None
        login(self)
        self.data["auth"] = self.auth
        self.run_installer()
        self.input_list = []

        self.logo_box = Static(logo, classes="logo")
        self.is_rgb = Switch(value=True)
        self.load = LoadingIndicator()
        self.md_box = VerticalScroll( Markdown(docs), classes="docs", )

        args = []

        for i in range(4):
            _input = Input(id="input_"+str(i))
            self.input_list.append(_input)
            args.append(_input)

        self.run_button = Button.success("RUN")
        self.log_box = Log(classes="log-box", auto_scroll=True)
        args.append(self.run_button)
        args.append(self.log_box)
        
        self.main_box =  Vertical(*args, classes="main-box")



        yield Container(
            Container(self.logo_box,classes="logo",),
            Container(Tabs("Generator","Integrity","Followers","Messages","Viewers","Advertise","React","Report","Unfollower","Docs", active="tab-10"), classes="top-bar",),
            self.md_box,
            self.main_box,
            Container(self.is_rgb, classes="rgb-box")
        )

        yield self.load
        yield Header(show_clock=True)
        yield Footer()
        

    def show_inputs(self, inputs: list):
        

        saved_inputs = json.loads(open("data/data.json","r").read())


        self.log_box.styles.display = "none"
        self.run_button.styles.display = "block"

        for inp, ele in zip(inputs, self.input_list):
            ele.styles.display = "block"
            ele.placeholder = inp['text']
            if inp.get("validation"):
                ele.validators = [inp["validation"]]
            try:
                ele.value = saved_inputs[self.ACTIVE][inp['text']]
            except:
                if inp.get("default"):
                    ele.value = str(inp["default"])
                else:
                    ele.value = ""

    def hide_and_run(self):

        saved_inputs = json.loads(open("data/data.json","r").read())

        self.active_inputs = []
        for i in self.input_list:
            if i.styles.display == "block":
                self.active_inputs.append(i)

        inputs_value = {}
        for i in self.active_inputs:
            inputs_value[i.placeholder] = i.value
        
        for i in self.input_list:
            i.styles.display = "none"

        self.run_button.styles.display = "none"

        self.log_box.styles.display = "block"

        for i in inputs_value:
            saved_inputs[self.ACTIVE][i] = inputs_value[i]

        open("data/data.json","w").write(json.dumps(saved_inputs, indent=4))
        

        return inputs_value
    

    def wait_for_run(self, tab):
        while True:
            time.sleep(0.1)
            if self.ACTIVE != tab:
                return False
            if self.started == True:
                return self.hide_and_run()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.started = True

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:

        self.data = {
            "proxies": open("data/proxies.txt","r").read().splitlines(),
            "usernames": open("data/usernames.txt","r").read().splitlines(),
            "token": open("data/token.txt","r").read().splitlines(),
            "integrity": open("integrity.txt","r").read().splitlines(),
            "config":  json.loads(open("data/config.json","r").read()),
        }
        self.data["auth"] = self.auth

        TABS_LIST = ("Generator","Integrity","Followers","Messages","Viewers","Advertise","React","Report","Unfollower","Docs")
        log = self.query_one(Log)
        selected = int(str(event.tab).split("id='tab-")[1].split("'")[0]) - 1

        self.started = False
        self.ACTIVE = str(TABS_LIST[selected])

        for i in self.input_list:
            i.styles.display = "none"

        if str(TABS_LIST[selected]) == "Docs":
            self.main_box.styles.display = "none"
            self.md_box.styles.display = "block"
        else:
            self.main_box.styles.display = "block"
            self.md_box.styles.display = "none"

        UNTILS_LIST = ("Generator","Integrity","Followers","Messages","Viewers","Advertise","React","Report", "Unfollower")
        if str(TABS_LIST[selected]) in UNTILS_LIST:
            run_list = [gen.Generator, integrity.Generator, follow.Follow, chat.ChatBot, view.View, advertise.AdvertiseBot, react.React, report.Report, unfollow.Unfollow]
            threading.Thread(target=run_list[selected], args=(self.data, self)).start()
            

    def on_ready(self):
        self.log_object = self.query_one(Log)

    def on_mount(self):
        self.hue = 0.0
        threading.Thread(target=ui.animation, args=(self, ),daemon=True).start()
        self.title = config.version

if __name__ == "__main__":
    app = NovoUi()
    app.run()
