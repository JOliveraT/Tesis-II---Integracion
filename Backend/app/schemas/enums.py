from enum import Enum


class EntrySource(str, Enum):
    chat_command = "chat_command"
    manual = "manual"
    channel_points_reward = "channel_points_reward"


class ConfirmationMode(str, Enum):
    instant = "instant"
    chat_confirmation = "chat_confirmation"
