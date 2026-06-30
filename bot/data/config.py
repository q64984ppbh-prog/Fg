# CONFIG
from data.DataBase.base import DatabaseCore 
from data.DataBase import DB
from aiocryptopay import AioCryptoPay
from config_reader import config

client = AioCryptoPay(token=config.cryptobot_token.get_secret_value())

name_casino = 'DuckWin'
username_bot_casino = 'duckwinbot'
url_channel_game = 'https://t.me/+6Sqmb9zXR21jMjQy' # Ссылка на игровой канал
url_bot = 'https://t.me/duckwinbot' # Ссылка на игрового бота
url_chat_game = 'https://t.me/+DiD9igOIrGlmOGQy' # Ссылка на чат
url_support = 'https://t.me/duckwin_support' # Ссылка на поддержку
url_project = 'https://t.me/duckwins' # Ссылка на новостной либо переходник проекта
url_check_channel = 'https://t.me/send?start=IVfLm9AuLbSW' # Ссылка на оплату счета для игрового канала
url_support_make_bet = 'https://t.me/c/2514725444/105' # Ссылкан на тутор, как сделать ставку
url_rules = 'https://telegra.ph/FAQ-DuckWin-11-26' # Ссылка на правила
url_faw = 'https://telegra.ph/FAQ-DuckWin-11-26' # Ссылка на FAQ
url_check_group = 'https://t.me/+_tnELhKkkvoxZDQy' # Ссылка на канал куда создаются чеки
channel_game_id = -1002514725444 # ID Игрового канала со ставками
logs_channel_id = -1002543664610 # ID Логов для канала со ставками
check_group = -1002662723292 # ID Чата куда создаются чеки

# Аккаунт связанный с премиум эмодзи в канале
api_id = 37209221
api_hash = "b1763a3de4d583e80555fab5993cc72c"
phone_number = "+79266104502"

# Аккаунт связанный с выдачей чеков юзерам
api_id_check = 24912560
api_hash_check = "7b3c69aa4cc8ccda44e545c31399b4e0"
phone_number_check = "+79266104502"

check_client = None
db_core = DatabaseCore(
    db_name="DuckDB",
    user="postgres",
    password="wordcode",
    host="localhost",
    port=5432
)

db = DB(db_core)
