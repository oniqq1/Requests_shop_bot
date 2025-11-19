# Shop Bot Requests 🤖🛍️

**Shop Bot Requests** is a demo project for clients, demonstrating how bots can be used for a store or business. Users can issue commands using the bot, and administrators can manage them through a separate interface.

---

## 🔹 Features

- For users:
-   Submitting requests
-   Viewing the results of your requests
- For administrators:
-   Managing requests
-   Viewing all active requests
- A simple and visual demonstration of the bot's operation

<img width="400" alt="image" src="https://github.com/user-attachments/assets/ab34eab6-431d-4fe5-acc6-133320397c89" />

---

## 💻 Installation

1. Clone the repositories:
``` bash
git clone https://github.com/oniqq1/Requests_shop_bot.git
```

2. Create requirements.txt
``` bash
  pip install -r requirements.txt
```

3. Create config.py in main directory and add two variables
``` bash
   BOT_TOKEN = 'YOUR BOT TOKEN'
    OWNER_ID = YOUR/OWNER token
```

4. Start project
``` bash
  python bot.py
```

My congratulations , You've launched the project.

---

## 📂 File structure

- bot.py — the main bot startup file
- commands.py — bot commands for users and administrators
- database/ — Files to works with db's tables
- keyboards.py — keyboards and interface elements
- handlers/ — event handlers
- models/ — data models
- states/ — states for the FSM

---

## ⚙️ Technologies

Python 3.13
aiogram 
SQLite
SQLAlchemy

---

If you have any questions or suggestions, please contact the author:
Github - [click](https://github.com/oniqq1)
Telegram - [here](https://t.me/codeniq)
Discord - [there](https://discord.com/users/944632344105586730)
