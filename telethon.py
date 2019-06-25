from telethon.sync import TelegramClient
from telethon import functions,types
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser
from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
import sys
import csv
import traceback
import time

api_id = (insert your api id)
api_hash = 'insert your api hash'
phone = 'country code-mobile number'
client = TelegramClient(phone, api_id, api_hash)

client.connect()
if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter code: '))

input_file = sys.argv[1]
users2 = []
with open(input_file, encoding='UTF-8') as f:
    rows = csv.reader(f,delimiter=",",lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {}
        user['username'] = row[0]
        users2.append(user)
#print(users2)
dialogs = []
users = []
chats = []
last_date = None
chunk_size = 200
groups=[]

result = client(functions.messages.GetDialogsRequest(offset_date=last_date,offset_id=0,offset_peer=InputPeerEmpty(),limit=chunk_size,hash=0))
dialogs.extend(result.dialogs)
users.extend(result.users)
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup== True:
            groups.append(chat)
    except:
        continue

i=0
print('Choose a group:')

for group in groups:
    print(str(i) + '- ' + group.title)
    i+=1

g_index = input("Enter index: ")
target_group=groups[int(g_index)]

target_group_entity = InputPeerChannel(target_group.id,target_group.access_hash)

for user in users2:
	try:
		user_to_add = client.get_input_entity(user['username'])
		client(InviteToChannelRequest(target_group_entity,[user_to_add]))
	except PeerFloodError:
		print("Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
	except UserPrivacyRestrictedError:
		print("The user's privacy settings do not allow you to do this. Skipping.")
	except:
		traceback.print_exc()
		print("Unexpected Error")
		continue
