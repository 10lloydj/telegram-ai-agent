import os
import datetime
from dataclasses import dataclass
from typing import Any, Dict

import yaml
from dotenv import load_dotenv


@dataclass
class RelevanceCfg:
    target_roles: list[str]
    preferred_locations: list[str]
    preferred_stack: list[str]
    exclude_seniority: list[str]
    min_confidence: float


@dataclass
class QuietHoursCfg:
    start: int
    end: int


@dataclass
class NotifyCfg:
    include_topic_title: bool
    include_jump_link: bool
    quiet_hours: QuietHoursCfg


@dataclass
class AppCfg:
    relevance: RelevanceCfg
    notify: NotifyCfg
    me: str


def _load_yaml(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_cfg() -> AppCfg:
    # Load .env first so env can override YAML defaults
    load_dotenv(override=False)

    cfg_path = os.environ.get("APP_CONFIG", os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "app.yaml"))
    raw = _load_yaml(cfg_path)

    # Fallbacks if YAML missing
    rel = raw.get("relevance", {})
    notify_raw = raw.get("notify", {})
    qh = notify_raw.get("quiet_hours", {})

    relevance = RelevanceCfg(
        target_roles=list(rel.get("target_roles", [])),
        preferred_locations=list(rel.get("preferred_locations", [])),
        preferred_stack=list(rel.get("preferred_stack", [])),
        exclude_seniority=list(rel.get("exclude_seniority", [])),
        min_confidence=float(os.environ.get("MIN_CONFIDENCE", rel.get("min_confidence", 0.70))),
    )

    notify = NotifyCfg(
        include_topic_title=bool(notify_raw.get("include_topic_title", True)),
        include_jump_link=bool(notify_raw.get("include_jump_link", True)),
        quiet_hours=QuietHoursCfg(
            start=int(os.environ.get("QUIET_HOURS_START", qh.get("start", 23))),
            end=int(os.environ.get("QUIET_HOURS_END", qh.get("end", 7))),
        ),
    )

    me = os.environ.get("SELF_USERNAME", "me")

    return AppCfg(relevance=relevance, notify=notify, me=me)


# A module-level singleton config
cfg = load_cfg()


def in_quiet_hours(now: datetime.datetime | None = None) -> bool:
    """Return True if current UK time is within quiet hours window.

    Assumes server time is UTC. Quiet hours can wrap across midnight.
    """
    if now is None:
        now = datetime.datetime.now(datetime.timezone.utc)

    # UK time handling: for simplicity, treat UTC as UK time; adjust as needed for DST.
    hour = now.hour
    start = cfg.notify.quiet_hours.start
    end = cfg.notify.quiet_hours.end

    if start == end:
        return False
    if start < end:
        return start <= hour < end
    # wrap over midnight
    return hour >= start or hour < end


