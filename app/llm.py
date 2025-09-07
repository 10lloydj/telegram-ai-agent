import os
import json
from typing import Any, Dict

from dotenv import load_dotenv
from tenacity import wait_exponential_jitter, stop_after_attempt, retry
from openai import AsyncOpenAI

# Ensure environment is loaded
load_dotenv()

from .schemas import Verdict


MODEL = os.getenv("OPENAI_MODEL", "o4-mini")

_client_kwargs: Dict[str, Any] = {}
_base_url = os.getenv("OPENAI_BASE_URL")
if _base_url:
    _client_kwargs["base_url"] = _base_url

client = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"), **_client_kwargs)


SYSTEM = (
    "You are an expert recruiting analyst.\n"
    "Return only valid JSON conforming to this schema:\n"
    "{ \"is_job_post\": boolean,\n"
    "  \"is_relevant\": boolean,\n"
    "  \"confidence\": number,\n"
    "  \"reasons\": string[],\n"
    "  \"job\": {\n"
    "    \"role\": string|null,\n"
    "    \"seniority\": string|null,\n"
    "    \"is_founding\": boolean,\n"
    "    \"company\": string|null,\n"
    "    \"location\": string|null,\n"
    "    \"remote\": boolean|null,\n"
    "    \"visa_sponsorship\": boolean|null,\n"
    "    \"stack\": string[],\n"
    "    \"compensation_hint\": string|null\n"
    "  },\n"
    "  \"contact\": {\n"
    "    \"method\": string|null,\n"
    "    \"value\": string|null\n"
    "  }\n"
    "}\n"
    "Decide relevance for a UK-based engineer/developer (Python/TypeScript/AI, etc). Prefer London/UK/Remote/EU. "
    "Exclude roles beyond IC scope (CTO/VP/Director). If uncertain, set is_relevant=false and lower confidence."
)

USER_TMPL = (
    "You will receive a single Telegram message's plain text.\n\n"
    "TEXT:\n---\n{{message_text}}\n---\n\n"
    "Output only the JSON object. No prose."
)


@retry(wait=wait_exponential_jitter(initial=1, max=20), stop=stop_after_attempt(6))
async def classify_text(message_text: str) -> Verdict:
    user = USER_TMPL.replace("{{message_text}}", (message_text or "")[:6000])
    resp = await client.responses.create(
        model=MODEL,
        input=[
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": user},
        ],
        response_format={"type": "json_object"},
    )
    raw = resp.output_text
    data: Dict[str, Any] = json.loads(raw)
    return Verdict.model_validate(data)


