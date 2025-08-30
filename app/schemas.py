from typing import List, Optional
from pydantic import BaseModel, Field


class ExtractedContact(BaseModel):
    method: Optional[str] = Field(None, examples=["email", "DM", "form", "apply_link"])
    value: Optional[str] = Field(None, examples=["jobs@startup.com", "https://..."])


class ExtractedJob(BaseModel):
    role: Optional[str] = None
    seniority: Optional[str] = None
    is_founding: bool = False
    company: Optional[str] = None
    location: Optional[str] = None
    remote: Optional[bool] = None
    visa_sponsorship: Optional[bool] = None
    stack: List[str] = []
    compensation_hint: Optional[str] = None


class Verdict(BaseModel):
    is_job_post: bool
    is_relevant: bool
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: List[str] = []
    job: ExtractedJob
    contact: ExtractedContact


