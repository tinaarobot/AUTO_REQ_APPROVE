from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid
from pyrogram import Client, filters
from pyrogram.types import *
from motor.motor_asyncio import AsyncIOMotorClient  
from os import environ as env
import asyncio, datetime, time


ACCEPTED_TEXT = "❖ ʜᴇʏ ʙᴀʙʏ ➥ {user}\n\n❖ ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴛʜᴇ ➥ {chat}"
START_TEXT = "❖ ʜᴇʏ ʙᴀʙʏ {}\n\n● ɪ ᴀᴍ ᴀᴜᴛᴏ ʀᴇǫ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ.\n\n❖ ᴀᴅᴅ ᴍᴇ ɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ ᴛᴏ ᴜsᴇ."

API_ID = int(env.get('API_ID'))
API_HASH = env.get('API_HASH')
BOT_TOKEN = env.get('BOT_TOKEN')
MONGO_DB = env.get('MONGO_DB')
OWNER = int(env.get('OWNER'))

Dbclient = AsyncIOMotorClient(MONGO_DB)
Cluster = Dbclient['Cluster0']
Data = Cluster['users']
Bot = Client(name='AutoAcceptBot', api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
       
      
     
@Bot.on_message(filters.command("start") & filters.private)                    
async def start_handler(c, m):
    user_id = m.from_user.id
    if not await Data.find_one({'id': user_id}): await Data.insert_one({'id': user_id})
    button = [[        
        InlineKeyboardButton('ᴜᴘᴅᴀᴛᴇ', url='https://t.me/ROY_EDITX'),
        InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', url='https://t.me/THE_FRIENDZ')
    ]]
    return await m.reply_text(text=START_TEXT.format(m.from_user.mention), disable_web_page_preview=True, reply_markup=InlineKeyboardMarkup(button))
          

@Bot.on_message(filters.command(["broadcast", "users"]) & filters.user(OWNER))  
async def broadcast(c, m):
    if m.text == "/users":
        total_users = await Data.count_documents({})
        return await m.reply(f"ᴛᴏᴛᴀʟ ᴜsᴇʀs : {total_users}")
    b_msg = m.reply_to_message
    sts = await m.reply_text("⬤ ʙʀᴏᴀᴅᴄᴀsᴛɪɴɢ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ...")
    users = Data.find({})
    total_users = await Data.count_documents({})
    done = 0
    failed = 0
    success = 0
    start_time = time.time()
    async for user in users:
        user_id = int(user['id'])
        try:
            await b_msg.copy(chat_id=user_id)
            success += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await b_msg.copy(chat_id=user_id)
            success += 1
        except InputUserDeactivated:
            await Data.delete_many({'id': user_id})
            failed += 1
        except UserIsBlocked:
            failed += 1
        except PeerIdInvalid:
            await Data.delete_many({'id': user_id})
            failed += 1
        except Exception as e:
            failed += 1
        done += 1
        if not done % 20:
            await sts.edit(f"❖ ʙʀᴏᴀᴅᴄᴀsᴛ ɪɴ ᴘʀᴏɢʀᴇss ⏤͟͟͞͞★\n\n● ᴛᴏᴛᴀʟ ᴜsᴇʀs ➥ {total_users}\n● ᴄᴏᴍᴘʟᴇᴛᴇᴅ ➥ {done} / {total_users}\n● sᴜᴄᴄᴇss ➥ {success}\n● ғᴀɪʟᴇᴅ ➥ {failed}")    
    time_taken = datetime.timedelta(seconds=int(time.time()-start_time))
    await sts.delete()
    await message.reply_text(f"❖ ʙʀᴏᴀᴅᴄᴀsᴛᴇᴅ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ⏤͟͟͞͞★\n\n● ᴄᴏᴍᴘʟᴇᴛᴇᴅ ɪɴ {time_taken} sᴇᴄᴏɴᴅs.\n● ᴛᴏᴛᴀʟ ᴜsᴇʀs ➥ {total_users}\n● ᴄᴏᴍᴘʟᴇᴛᴇᴅ ➥ {done} / {total_users}\n● sᴜᴄᴄᴇss ➥ {success}\n● ғᴀɪʟᴇᴅ ➥ {failed}", quote=True)

  
 
@Bot.on_chat_join_request()
async def req_accept(c, m):
    user_id = m.from_user.id
    chat_id = m.chat.id
    if not await Data.find_one({'id': user_id}): await Data.insert_one({'id': user_id})
    await c.approve_chat_join_request(chat_id, user_id)
    try: await c.send_message(user_id, ACCEPTED_TEXT.format(user=m.from_user.mention, chat=m.chat.title))
    except Exception as e: print(e)
   
   

Bot.run()



