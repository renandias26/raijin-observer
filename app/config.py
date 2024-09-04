from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

def get_settingConfig(prefix: str = ''):
    return SettingsConfigDict(
        env_prefix= prefix,
        env_file='.env', 
        env_file_encoding='utf-8', 
        extra='ignore'
    )

class WhapiSettings(BaseSettings):
    model_config = get_settingConfig('whapi_')

    Token: str
    Url: str
    Phone: str

@lru_cache
def get_WhapiSetting():
    return WhapiSettings()