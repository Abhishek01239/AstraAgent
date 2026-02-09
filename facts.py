import json
import os
import time

FACTS_FILE = "facts.json"

def load_facts():
    if not os.path.exists(FACTS_FILE):
        return {}

    try:
        with open(FACTS_FILE, "r") as f:
            data = json.load(f)
    except:
        return {}

    clean = {}
    now = time.time()

    for key, fact in data.items():
        if not isinstance(fact, dict):
            continue

        created = fact.get("created_at", now)
        ttl = fact.get("ttl", 0)

        # ⏳ Expired
        if ttl > 0 and now - created > ttl:
            continue

        # 📉 Confidence decay (1% per day)
        days = (now - created) / 86400
        fact["confidence"] = max(0.0, fact["confidence"] - (0.01 * days))

        clean[key] = fact

    return clean


def save_facts(facts):
    with open(FACTS_FILE, "w") as f:
        json.dump(facts, f, indent=2)


def remember_fact(
    key,
    value,
    confidence=0.9,
    importance=0.5,
    ttl=None,
    source="explicit"
):
    facts = load_facts()
    now = time.time()

    if ttl is None:
        ttl = int(31536000 * importance)  # 1 year × importance

    if key in facts:
        if confidence <= facts[key]["confidence"]:
            return

    facts[key] = {
        "value": value,
        "confidence": confidence,
        "importance": importance,
        "created_at": now,
        "ttl": ttl,
        "source": source
    }

    save_facts(facts)


def get_fact(key):
    facts = load_facts()
    fact = facts.get(key)

    if not fact:
        return None

    if fact["confidence"] < 0.4:
        return None

    return fact["value"]
