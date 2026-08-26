from pydantic import BaseModel, Field


class ResearchFinding(BaseModel):
    source: str
    query: str
    title: str
    summary: str
    url: str
    relevance_score: float = 0.5
    has_conflict: bool = False
    conflict_notes: str = ""


class ResearchConflict(BaseModel):
    finding_a_title: str
    finding_b_title: str
    conflict_description: str


class KnowledgeSynthesisOutput(BaseModel):
    topic_summary: str
    key_insights: list[str]
    important_statistics: list[str]
    examples: list[str]
    advantages: list[str]
    limitations: list[str]
    future_trends: list[str]
    controversies: list[str]
    missing_information: list[str]
    linkedin_angles: list[str] = Field(default_factory=list)
    hook_ideas: list[str] = Field(default_factory=list)
