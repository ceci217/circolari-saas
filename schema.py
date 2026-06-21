from pydantic import BaseModel
from typing import List

class Circolare(BaseModel):
    titolo: str
    ente: str
    sintesi: str

    novita: List[str]
    soggetti: List[str]

    obblighi: List[str]
    scadenze: List[str]

    sanzioni: List[str]
    criticita: List[str]

    checklist: List[str]
    riferimenti: List[str]
