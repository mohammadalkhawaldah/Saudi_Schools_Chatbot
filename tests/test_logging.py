import os
import sys
import tempfile
import importlib.util
from pathlib import Path

# Load the logging utilities from LiveKit/agent.py without requiring it as a package
REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "LiveKit" / "agent.py"
sys.path.insert(0, str(REPO_ROOT))
spec = importlib.util.spec_from_file_location("agent", MODULE_PATH)
agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(agent)


def _setup_tmp_logging(tmpdir):
    agent.LOG_DIR = tmpdir
    agent.CONVERSATION_LOG = os.path.join(tmpdir, "conversations.log")
    agent.USER_LOG = os.path.join(tmpdir, "users.txt")


def test_log_user_records_unique_ids():
    with tempfile.TemporaryDirectory() as tmpdir:
        _setup_tmp_logging(tmpdir)

        agent.log_user("user1")
        agent.log_user("user1")
        agent.log_user("user2")

        with open(agent.USER_LOG, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]

        assert lines == ["user1", "user2"]


def test_log_conversation_writes_entries():
    with tempfile.TemporaryDirectory() as tmpdir:
        _setup_tmp_logging(tmpdir)

        agent.log_conversation("user1", "hello", "hi there")

        with open(agent.CONVERSATION_LOG, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]

        assert len(lines) == 2
        assert "USER: hello" in lines[0]
        assert "BOT: hi there" in lines[1]
