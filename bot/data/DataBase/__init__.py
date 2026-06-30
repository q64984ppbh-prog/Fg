from .base import DatabaseCore
from .users import UsersDB
from .channels import ChannelsDB
from .referals import ReferalDB
from .admin import AdminDB
from .game_channel import GameChannelsDB
from .Game.game_mines import GameUserDB
from .WithdrawSystem.send import SendDB

class DB:
    def __init__(self, db_core: DatabaseCore):
        self.core = db_core
        self.users = UsersDB(db_core)
        self.channels = ChannelsDB(db_core)
        self.referals = ReferalDB(db_core)
        self.admin = AdminDB(db_core)
        self.game_channel = GameChannelsDB(db_core)
        self.send = SendDB(db_core)
        self.game_mines = GameUserDB(db_core)