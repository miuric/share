from graia.broadcast import Broadcast
from graia.application import GraiaMiraiApplication, Session
from graia.application.message.chain import MessageChain
import asyncio

from graia.application.message.elements.internal import Plain
from graia.application.friend import Friend
from graia.application.entry import GroupMessage

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://188.131.148.7:8089", # 填入 httpapi 服务运行的地址
        authKey="1234567890", # 填入 authKey
        account=2300363951, # 你的机器人的 qq 号
        websocket=True # Graia 已经可以根据所配置的消息接收的方式来保证消息接收部分的正常运作.
    )
)

@bcc.receiver("FriendMessage")
async def friend_message_listener(app: GraiaMiraiApplication, friend: Friend):
    await app.sendFriendMessage(friend, MessageChain(__root__=[
        Plain("Hello, World!")
    ]))



@bcc.receiver(GroupMessage)
def im_listener():
    pass

app.launch_blocking()
