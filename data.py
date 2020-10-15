from pydantic import BaseModel
from typing import List, Optional

class ShortAnswerInstance(BaseModel):
    taskId: str
    itemId: str
    itemPrompt: str
    itemTargets: List[str]
    learnerId: str
    answer: str
    label: Optional[str]
