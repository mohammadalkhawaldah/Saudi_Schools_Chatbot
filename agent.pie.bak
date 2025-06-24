from dotenv import load_dotenv
from Catalog import data2
from livekit import agents
from livekit.agents import ChatContext, AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import (
    openai,
    #cartesia,
    #deepgram,
    noise_cancellation,
    silero,
    azure,
    tavus
)

from livekit.plugins.turn_detector.multilingual import MultilingualModel
#from livekit.plugins.openai import OpenAIWhisperSTT
load_dotenv()
initial_ctx = ChatContext()
initial_ctx.add_message(
    role="assistant",
    content=f"Here is the school catalog information: {data2}"
)

class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions="You are a helpful voice AI assistant for school context.",
                         chat_ctx=initial_ctx)

    async def on_conversation_item_added(self, item, ctx):
        print(f"[DEBUG] on_conversation_item_added called: role={item.role}, content={item.content}")
        user_id = getattr(ctx.participant, 'identity', 'unknown')
        if item.role == "user":
            log_user(user_id)
            # Store the user message, response will be logged after agent replies
            ctx._last_user_message = item.content
        elif item.role == "assistant":
            # Log the conversation (user message and bot response)
            user_message = getattr(ctx, '_last_user_message', '')
            log_conversation(user_id, user_message, item.content)

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=openai.STT(
            model="gpt-4o-transcribe",
               
        ),
        
        #stt=openai.STT(model="whisper-1", language="ar"),
        #stt=deepgram.STT(model="nova-3", language="en"),
        llm=openai.LLM(model="gpt-4o-mini"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
        #turn_detection=VADTurnDetector(),
        #tts = openai.TTS(
    #model="gpt-4o-mini-tts"),

     tts=azure.TTS(
            #model="azure-tts",
            #voice="ar-OM-AbdullahNeural",  # Change to your preferred voice
            voice="ar-SA-HamedNeural",  # Change to your preferred voice
            
            #region="qatarcentral"  # Change to your Azure region
        )
    )
    # tts=azure.TTS(model="azure-tts", voice="ar-OM-AbdullahNeural", region="qatarcentral"),
    avatar = tavus.AvatarSession(
      replica_id="rf4703150052",  # ID of the Tavus replica to use
      persona_id="p48fdf065d6b",  # ID of the Tavus persona to use (see preceding section for configuration details)
   )
    await avatar.start(session, room=ctx.room)

    # --- Conversation logging event subscription ---
    # Removed manual event subscription; rely on Assistant.on_conversation_item_added
    # --- End event subscription ---

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            # LiveKit Cloud enhanced noise cancellation
            # - If self-hosting, omit this parameter
            # - For telephony applications, use `BVCTelephony` for best results
            noise_cancellation=noise_cancellation.BVC(), 
        ),
        room_output_options=RoomOutputOptions(
         # Disable audio output to the room. The avatar plugin publishes audio separately.
         audio_enabled=False,
         # text_enabled removed
         ),

    )
    await ctx.connect()
   
    await session.generate_reply(
        instructions="Greet the users and introduce yourself as a school assistant. answer in arabic if the question is in arabic, otherwise answer in english. ",
    )   

if __name__ == "__main__":
    agents.cli.run_app(agents.WorkerOptions(entrypoint_fnc=entrypoint))

import os
from datetime import datetime

LOG_DIR = "KMS/logs"
CONVERSATION_LOG = os.path.join(LOG_DIR, "conversations.log")
USER_LOG = os.path.join(LOG_DIR, "users.txt")

def log_conversation(user_id: str, user_message: str, bot_response: str):
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(CONVERSATION_LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {user_id} | USER: {user_message}\n")
        f.write(f"{datetime.now().isoformat()} | {user_id} | BOT: {bot_response}\n")

def log_user(user_id: str):
    os.makedirs(LOG_DIR, exist_ok=True)
    users = set()
    if os.path.exists(USER_LOG):
        with open(USER_LOG, "r", encoding="utf-8") as f:
            users = set(line.strip() for line in f)
    if user_id not in users:
        with open(USER_LOG, "a", encoding="utf-8") as f:
            f.write(f"{user_id}\n")

def get_total_users():
    if not os.path.exists(USER_LOG):
        return 0
    with open(USER_LOG, "r", encoding="utf-8") as f:
        return len(set(line.strip() for line in f))
