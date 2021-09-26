import time
import logging
from Config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="❗ Non sei ancora iscritto al mio canale. Per favore, unisciti usando il bottone qui sotto e poi premi il pulsante 'FATTO'.", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❗ Sei mutato dagli amministratori per altri motivi.", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❗ **{cb.from_user.mention} Sta provando a smutare sé stesso ma non posso smutarlo perché non sono amministratore in questa chat, aggiungimi di nuovo come amministratore.**\n__#Leaving this chat...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❗ Attenzione: non premere il bottone se puoi parlare liberamente", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      if channel.startswith("-"):
          channel_url = client.export_chat_invite_link(int(channel))
      else:
          channel_url = f"https://t.me/{channel}"
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              " {}  Non sei ancora iscritto al mio canale. Per favore, unisciti usando il bottone qui sotto 'ISCRIVITI AL MIO CANALE' dopo premi il pulsante 'FATTO'".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
             reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("✍️ ISCRIVITI AL MIO CANALE", url=channel_url)
                ],
                [
                    InlineKeyboardButton("👉 FATTO 👈", callback_data="onUnMuteRequest")
                ]
            ]
        )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❗ **Non sono admin qui.**\n__Rendimi admin con i permessi per bannare e aggiungimi di nuovo.\n#Leaving this chat...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❗ **Non sono admin qui [channel]({channel_url})**\n__Rendimi admin con permessi per bannare e aggiungimi di nuovo.\n#Leaving this chat...__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub", "fsub@ForceSubscriber_UBot", "forcesubscribe@ForceSubscriber_UBot"]) & ~filters.private)
def config(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Force Subscribe è disabilitato qui.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Smuta tutti i membri mutati da me...**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **Smuta tutti i membri mutati da me.**')
        except ChatAdminRequired:
          sent_message.edit('❗ **Non soni admin qui.**\n__I can\'t smuta gli utenti perché non sono admin in questa chat rendimi admin con i permessi per bannare.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str) 
          if input_str.startswith("-"):
              channel_url = client.export_chat_invite_link(int(input_str))
          else:
              channel_url = f"https://t.me/{input_str}"
          message.reply_text(f"✅ **Force Subscribe is Enabled**\n__Force Subscribe is enabled, all the group members have to subscribe this [channel]({channel_url}) in order to send messages in this group.__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❗ **Nessun admin nel canale**\n__Non sono admin nel [channel]({channel_url}). Add me as a admin in order to enable ForceSubscribe.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❗ **Non Valido Username/ID.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        my_channel = sql.fs_settings(chat_id).channel
        if my_channel.startswith("-"):
            channel_url = client.export_chat_invite_link(int(input_str))
        else:
            channel_url = f"https://t.me/{my_channel}"
        message.reply_text(f"✅ **Force Subscribe è disabilitato in questa chat.**\n__For this [Channel]({channel_url})__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Force Subscribe is disabled in this chat.**")
  else:
      message.reply_text("❗ **Devi essere il proprietario del gruppo**\n__Devi essere il proprietario del gruppo per fare questo.__")
