from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

class Settings(BaseSettings):
    bot_token: SecretStr
    cryptobot_token: SecretStr
    xrocket_token: SecretStr
    admin_id: int
    logs_id: int
    topic_deposit: int
    topic_withdraw: int
    topic_ref_bonus: int

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

config = Settings()