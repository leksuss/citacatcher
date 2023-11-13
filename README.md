# Cita Catcher

Small script with tg bot to get cita for spanish TIE in Barcelona (Mallorca 213). 
Based on [Playwright](https://playwright.dev/) and [https://python-telegram-bot.org/](python-telegram-bot). 
It checks cita availability in [this page](https://icp.administracionelectronica.gob.es/icpplustieb/citar?p=8&locale=es) for every 10 minutes. And if it found any cita, sends alert via telegram bot.
Also, it makes a screenshot of the page if cita was found.

Note, this page don't allow you to use chromium headless mode. That means you should have some GUI interface to run this script. 

## How to run
Clone this repo:
```shell
git clone git@github.com:leksuss/citacatcher.git
```
Go inside folder
```shell
cd citacatcher
```
Install dependencies:
```shell
pip3 install -r requirements.txt
```

Playwright require some additional installation process (actually, it install cromium and some other utils):
```shell
playwright install
```

Next you need to [create your own telegram bot and receive token](https://core.telegram.org/bots#how-do-i-create-a-bot).
After this you need to get your user id in telegram. Just ask [this bot](https://t.me/raw_data_bot), and it gives you user id.
Now you ready to fill `.env` file with sensitive data. You can use `.env_example` as template.
 - `TG_TOKEN` - your tg bot token (ex. 15326866439:ABC-DEF1234ghIkl-zyx57W2v1u123ew11)
 - `TG_CHAT_ID` - your chat id (ex. 129391362)
 - `NIE` - your NIE (ex. X8846580K)
 - `NAME` - your name (ex. JOHN DOE)

And now you can run script:
```shell
python3 main.py
```