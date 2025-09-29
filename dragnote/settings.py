from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    midi_synth_num: int = 2
