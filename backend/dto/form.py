from pydantic import BaseModel
from typing import List, Optional

class TaskConfigForm(BaseModel):
    TASK_MODEL: Optional[str]
    TASK_MODEL_EXTERNAL: Optional[str]
    TITLE_GENERATION_PROMPT_TEMPLATE: str
    SEARCH_QUERY_GENERATION_PROMPT_TEMPLATE: str
    SEARCH_QUERY_PROMPT_LENGTH_THRESHOLD: int
    TOOLS_FUNCTION_CALLING_PROMPT_TEMPLATE: str

class AddPipelineForm(BaseModel):
    url: str
    urlIdx: int
    
class DeletePipelineForm(BaseModel):
    id: str
    urlIdx: int

class ModelFilterConfigForm(BaseModel):
    enabled: bool
    models: List[str]

class UrlForm(BaseModel):
    url: str
    
class ModelFilterConfigForm(BaseModel):
    enabled: bool
    models: List[str]