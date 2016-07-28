# bot-army

```
  _________________________________
 |.--------_--_------------_--__--.|
 ||    /\ |_)|_)|   /\ | |(_ |_   ||
 ;;`,_/``\|__|__|__/``\|_| _)|__ ,:|
((_(-,-----------.-.----------.-.)`)
 \__ )        ,'     `.        \ _/
 :  :        |_________|       :  :
 |-'|       ,'-.-.--.-.`.      |`-|
 |_.|      (( (*  )(*  )))     |._|
 |  |       `.-`-'--`-'.'      |  |
 |-'|        | ,-.-.-. |       |._|
 |  |        |(|-|-|-|)|       |  |
 :,':        |_`-'-'-'_|       ;`.;
  \  \     ,'           `.    /._/
   \/ `._ /_______________\_,'  /
    \  / :   ___________   : \,'
     `.| |  |           |  |,'
       `.|  |           |  |
```


# The Bot Army
Described [here](https://square-root.atlassian.net/wiki/display/TPI/Put+a+Bot+on+It%3A+SR+Bot+Army).

# Creating bots.

## The easy way.

Extend legion-bot.

TBD: How one actually does this.

## The hard way.

Clone one of the templates and go to town.

### Clone a template bot in your favorite language
If it doesn't exist, add it. We need a haskell-bot, for example...

### update the env folder
Python supports the concept of "versioning" the distribution--this is stored in the requirements.txt file. If you want to work in a different language or a different version of python, you should add the relevant environment artifacts in the env folder.

**Note!** Store all unversioned environment artifacts in a folder called src--these are ignored by version control.

### Build-a-bot
Code.

### Add a startup script
You need to have a startup script in your bots bin directory. That script will be run when the master "init.sh" script is called, so anything your bot needs to have running needs to be spawned in that script.

### Register your bot
Add the relevant configuration entries to bot_config.json.

### Add your bot to the army
Run init.sh?
