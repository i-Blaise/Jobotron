import time
from mongodbConnect import MongoDBManager

# Defaults mirror the behavior that was previously hardcoded across the app.
DEFAULT_CONFIG = {
    "schedule_hours": [9, 12, 15, 18],
    "keywords": [],  # empty = accept every Jobweb listing
    "jobberman_fallback_query": "remote software developer",
    "sources": {"jobwebghana": True, "jobberman": True},
    "max_post_count": 2,
    "min_queue_size": 4,
}

_CACHE_TTL_SECONDS = 15
_cache = {"config": None, "fetched_at": 0.0}


def _config_collection():
    db = MongoDBManager.get_database()
    if db is None:
        return None
    return db["config"]


def get_config(force_refresh=False):
    """Return the bot config, merged over defaults. Falls back to defaults
    if the database is unavailable so the bot never stalls on config."""
    now = time.time()
    if (
        not force_refresh
        and _cache["config"] is not None
        and now - _cache["fetched_at"] < _CACHE_TTL_SECONDS
    ):
        return _cache["config"]

    config = dict(DEFAULT_CONFIG)
    collection = _config_collection()
    if collection is not None:
        try:
            stored = collection.find_one({"_id": "settings"}) or {}
            for key in DEFAULT_CONFIG:
                if key in stored:
                    config[key] = stored[key]
        except Exception as e:
            print(f"Failed to read config, using defaults: {e}")

    _cache["config"] = config
    _cache["fetched_at"] = now
    return config


def update_config(changes):
    """Persist validated changes and return the merged config.
    Raises ValueError on bad input, RuntimeError if the DB is unavailable."""
    validated = validate_config(changes)
    collection = _config_collection()
    if collection is None:
        raise RuntimeError("Database unavailable")
    collection.update_one({"_id": "settings"}, {"$set": validated}, upsert=True)
    return get_config(force_refresh=True)


def validate_config(changes):
    if not isinstance(changes, dict):
        raise ValueError("Config must be an object")

    validated = {}
    for key, value in changes.items():
        if key == "schedule_hours":
            if (
                not isinstance(value, list)
                or not value
                or not all(isinstance(h, int) and 0 <= h <= 23 for h in value)
            ):
                raise ValueError("schedule_hours must be a non-empty list of hours 0-23")
            validated[key] = sorted(set(value))
        elif key == "keywords":
            if not isinstance(value, list) or not all(isinstance(k, str) for k in value):
                raise ValueError("keywords must be a list of strings")
            validated[key] = [k.strip() for k in value if k.strip()]
        elif key == "sources":
            if not isinstance(value, dict) or not all(
                source in DEFAULT_CONFIG["sources"] and isinstance(enabled, bool)
                for source, enabled in value.items()
            ):
                raise ValueError("sources must map jobwebghana/jobberman to booleans")
            validated[key] = {**DEFAULT_CONFIG["sources"], **value}
        elif key == "max_post_count":
            if not isinstance(value, int) or not 1 <= value <= 10:
                raise ValueError("max_post_count must be an integer between 1 and 10")
            validated[key] = value
        elif key == "min_queue_size":
            if not isinstance(value, int) or not 0 <= value <= 50:
                raise ValueError("min_queue_size must be an integer between 0 and 50")
            validated[key] = value
        elif key == "jobberman_fallback_query":
            if not isinstance(value, str):
                raise ValueError("jobberman_fallback_query must be a string")
            validated[key] = value.strip()
        else:
            raise ValueError(f"Unknown config key: {key}")

    if not validated:
        raise ValueError("No config changes provided")
    return validated
