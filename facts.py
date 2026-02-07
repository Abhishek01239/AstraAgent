import json
import os

FACTS_FILE = "facts.json"

def load_facts():
    if not os.path.exists(FACTS_FILE):
        return {}
    
    try:
        with open(FACTS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_facts(facts):
    with open(FACTS_FILE,"w") as f:
        json.dump(facts, f, indent=2)

def remember_fact(key, value):
    facts = load_facts()
    facts[key] = value
    save_facts(facts)

def get_fact(key):
    facts = load_facts()
    return facts.get(key)
