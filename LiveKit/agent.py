# filepath: LiveKit/agent.py
from dotenv import load_dotenv
import os
from Catalog import data2
from livekit import agents
from livekit.agents import ChatContext, AgentSession, Agent, RoomInputOptions, RoomOutputOptions
from livekit.plugins import (
    openai,
    noise_cancellation,
    silero,
    azure,
    tavus
)
from livekit.plugins.turn_detector.multilingual import MultilingualModel

# Load environment variables from .env file
load_dotenv()
print("TAVUS_API_KEY:", os.getenv("TAVUS_API_KEY"))

# Initialize the chat context with initial assistant message
initial_ctx = ChatContext()
initial_ctx.add_message(
    role="assistant",
    content=f"Here is the school catalog information: {data2}"
)

class Assistant(Agent):
    def __init__(self):
        super().__init__(instructions="أنت مساعد صوتي ذكي للمدارس السعودية. تحدث دائمًا باللغة العربية.",
                         chat_ctx=initial_ctx)

    async def on_conversation_item_added(self, item, ctx):
        print(f"[DEBUG] on_conversation_item_added called: role={item.role}, content={item.content}")
        user_id = getattr(ctx.participant, 'identity', 'unknown')
        if item.role == "user":
            log_user(user_id)
            ctx._last_user_message = item.content
        elif item.role == "assistant":
            user_message = getattr(ctx, '_last_user_message', '')
            log_conversation(user_id, user_message, item.content)

async def entrypoint(ctx: agents.JobContext):
    session = AgentSession(
        stt=openai.STT(model="gpt-4o-transcribe"),
        llm=openai.LLM(model="gpt-4o-mini"),
        vad=silero.VAD.load(),
        turn_detection=MultilingualModel(),
        tts=azure.TTS(
            voice="ar-SA-HamedNeural",
        )
    )

    await session.start(
        room=ctx.room,
        agent=Assistant(),
        room_input_options=RoomInputOptions(
            noise_cancellation=noise_cancellation.BVC(),
        ),
        room_output_options=RoomOutputOptions(
            audio_enabled=True,
        ),
    )
    await ctx.connect()
   
    await session.generate_reply(
        instructions="قم بتحية المستخدمين وعرّف نفسك بأنك المساعد الذكي للمدارس السعودية ثم قل يا هلا بيكم. تكلم دائما باللغة العربية",
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