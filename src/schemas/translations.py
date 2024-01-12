from pydantic import BaseModel, Field
import enum

class Langs(str, enum.Enum):
    tr = 'tr'
    en = 'en'
    fr = 'fr'
    es = 'es'
    
class CreateTranslationRequestSchema(BaseModel):
    prefix: str = Field(...)
    lang: Langs = Field(...)
    text_content: str = Field(...)
