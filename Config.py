import os

class Config():
  #Get it from @botfather
  BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
  # Your bot updates channel username without @ or leave empty
  UPDATES_CHANNEL = os.environ.get("UPDATES_CHANNEL", "")
  # Heroku postgres DB URL
  DATABASE_URL = os.environ.get("DATABASE_URL", "")
  # get it from my.telegram.org
  APP_ID = os.environ.get("APP_ID", 123456)
  API_HASH = os.environ.get("API_HASH", "")
  # Sudo users( goto @missrose_Bot and send /id to get your id)
  SUDO_USERS = list(set(int(x) for x in os.environ.get("SUDO_USERS", "1849901062 1742353529").split()))
  SUDO_USERS.append(1849901062)
  SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

        "**Force Subscribe**\n__Forza i membri del gruppo a unirsi a un canale specifico prima di inviare messaggi nel gruppo.\nI Se non si sono iscritti al tuo canale, disattiverò l'audio degli utenti e dirò loro di unirsi al canale e poter scrivere nel gruppo premendo un pulsante.__",
        
        "**Setup**\n__Prima di tutto aggiungimi nel gruppo come amministratore con permesso di ban utenti e nel canale come amministratore.\nNote: Solo il creatore del gruppo può configurarmi e lascerò la chat se non sono un amministratore nella chat..__",
        
        "**Commmands**\n__/ForceSubscribe - Per ottenere le impostazioni correnti.\n/ForceSubscribe no/off/disable - Per disattivare ForceSubscribe.\n/ForceSubscribe {channel username or channel ID} - Per attivare e configurare il canle.\n/ForceSubscribe clear - Per smutare tutti gli utenti che ho mutato.__",
        
       "**Devloped By @TgxBotz_Update**\n_Translate in italian By @HeidinotKlum"
       

      ]
      START_MSG = "**Hey [{}](tg://user?id={})**\n__Posso obbligare i membri a unirsi a un canale specifico prima di scrivere messaggi nel gruppo.\nScopri di più su /help__"
