import discord
from discord.ext import commands
import asyncio
import random
import time
import aiohttp
import tkinter as tk
from tkinter import messagebox
import os
import importlib.util
import sys
import threading
import json
from colorama import init, Fore
init(autoreset=True)
def load_config():
    with open('config.json', 'r') as file:
        return json.load(file)
config = load_config()
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents, self_bot=True)
SCRIPT_DIR = "scripts"
loaded_scripts = []
def load_script(script_name):
    global loaded_scripts
    script_path = os.path.join(SCRIPT_DIR, script_name)
    if script_name not in loaded_scripts:
        loaded_scripts.append(script_name)
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, 'setup'):
            module.setup(bot)
        print_to_console(f"[ + ] >> Script {script_name} loaded successfully.", Fore.GREEN)
    else:
        print_to_console(f"[ ? ] >> Script {script_name} is already loaded.", Fore.YELLOW)
def unload_script(script_name):
    global loaded_scripts
    if script_name in loaded_scripts:
        loaded_scripts.remove(script_name)
        if script_name in sys.modules:
            del sys.modules[script_name]
        print_to_console(f"[ - ] >> Script {script_name} unloaded successfully.", Fore.RED)
    else:
        print_to_console(f"[ ? ] >> Script {script_name} is not loaded.", Fore.YELLOW)
class ScriptLoaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("ZenFusion Bot Script Loader")
        self.root.geometry("600x500")
        self.root.configure(bg="#2E2E2E")
        self.font = ('Arial', 12)
        self.title_label = tk.Label(self.root, text="ZenFusion Bot Script Loader", font=('Arial', 18, 'bold'), fg="white", bg="#2E2E2E")
        self.title_label.pack(pady=10)
        self.script_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, height=10, width=50, font=self.font, bg="#3C3C3C", fg="white", selectbackground="#6A6A6A")
        self.script_listbox.pack(pady=20, padx=20)
        self.load_button = tk.Button(self.root, text="Load", command=self.load_scripts, font=self.font, bg="#4CAF50", fg="white", relief="flat")
        self.load_button.pack(pady=5, padx=20, fill=tk.X)
        self.unload_button = tk.Button(self.root, text="Unload", command=self.unload_scripts, font=self.font, bg="#F44336", fg="white", relief="flat")
        self.unload_button.pack(pady=5, padx=20, fill=tk.X)
        self.refresh_button = tk.Button(self.root, text="Refresh", command=self.refresh_script_list, font=self.font, bg="#2196F3", fg="white", relief="flat")
        self.refresh_button.pack(pady=5, padx=20, fill=tk.X)
        self.refresh_script_list()
    def refresh_script_list(self):
        self.script_listbox.delete(0, tk.END)
        for script_name in os.listdir(SCRIPT_DIR):
            if script_name.endswith(".py"):
                self.script_listbox.insert(tk.END, script_name)
    def load_scripts(self):
        selected_scripts = self.script_listbox.curselection()
        if not selected_scripts:
            messagebox.showinfo("Error", "No scripts selected to load.", icon='warning')
            return
        for script_index in selected_scripts:
            script_name = self.script_listbox.get(script_index)
            load_script(script_name)
        messagebox.showinfo("Success", "Selected scripts loaded successfully.", icon='info')
    def unload_scripts(self):
        selected_scripts = self.script_listbox.curselection()
        if not selected_scripts:
            messagebox.showinfo("Error", "No scripts selected to unload.", icon='warning')
            return
        for script_index in selected_scripts:
            script_name = self.script_listbox.get(script_index)
            unload_script(script_name)
        messagebox.showinfo("Success", "Selected scripts unloaded successfully.", icon='info')
@bot.before_invoke
async def before_command(ctx):
    if config["humanizer"]:
        delay = random.uniform(config["delay_range"]["thinking_delay_min"], config["delay_range"]["thinking_delay_max"])
        print(f"[ * ] >> Cooldown before command: {delay:.2f} seconds", Fore.CYAN)
        await asyncio.sleep(delay)
        await simulate_typing(ctx)
        typing_delay = random.uniform(config["delay_range"]["typing_delay_min"], config["delay_range"]["typing_delay_max"])
        await asyncio.sleep(typing_delay)
        print(f"[ * ] >> Cooldown for typing: {typing_delay:.2f} seconds", Fore.CYAN)
    else:
        await ctx.trigger_typing()

async def simulate_typing(ctx):
    typing_duration = random.uniform(2, 4) 
    typing_interval = random.uniform(0.1, 0.3)
    typing_start_time = time.time()

    while time.time() - typing_start_time < typing_duration:
        await ctx.trigger_typing()
        await asyncio.sleep(typing_interval)

@bot.event
async def on_ready():
    print_to_console(f"[ ? ] >> Logged in as {bot.user}", Fore.CYAN)
    bot.http.session = aiohttp.ClientSession()
bot.http.user_agent = f'DiscordBot ({random.randint(1000, 9999)}.{random.randint(1000, 9999)}.{random.randint(1000, 9999)}'
@bot.event
async def on_close():
    await bot.http.session.close()
def get_bot_token():
    if config["multi_tokens"]:
        token = random.choice(config["tokens"])
    else:
        token = config["token"]
    return token
def run_bot():
    bot.run(get_bot_token(), bot=False)
def print_to_console(message, color=Fore.WHITE):
    print(color + message)
def print_purple_fade():
    ascii_art = """

           ·▄▄▄▄•▄▄▄ . ▐ ▄  ▄▄▄· ▐▄• ▄ ▪  .▄▄ ·     
           ▪▀·.█▌▀▄.▀·•█▌▐█▐█ ▀█  █▌█▌▪██ ▐█ ▀.     
           ▄█▀▀▀•▐▀▀▪▄▐█▐▐▌▄█▀▀█  ·██· ▐█·▄▀▀▀█▄    
           █▌▪▄█▀▐█▄▄▌██▐█▌▐█ ▪▐▌▪▐█·█▌▐█▌▐█▄▪▐█    
           ·▀▀▀ • ▀▀▀ ▀▀ █▪ ▀  ▀ •▀▀ ▀▀▀▀▀ ▀▀▀▀     

     ZenFusin Bot || v1.0.0
    """
    
    fade_colors = [
        Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.MAGENTA, 
        Fore.LIGHTMAGENTA_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX, Fore.MAGENTA, Fore.LIGHTMAGENTA_EX
    ]
    
    lines = ascii_art.split("\n")
    for i, line in enumerate(lines):
        print(f"{fade_colors[i % len(fade_colors)]}{line.center(100)}")
def main():
    print_purple_fade()
    threading.Thread(target=run_bot).start()
    root = tk.Tk()
    app = ScriptLoaderApp(root)
    root.mainloop()
if __name__ == '__main__':
    main()
