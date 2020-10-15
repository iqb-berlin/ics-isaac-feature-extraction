from pydantic import BaseModel
from typing import List

class ShortAnswerInstance(BaseModel):
    taskId: str
    itemId: str
    itemPrompt: str
    itemTargets: List[str]
    learnerId: str
    answer: str
