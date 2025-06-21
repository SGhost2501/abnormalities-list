import json
import random
from datetime import datetime

TEMPLATES = [
    "What do you think of {Name}?",
    "How should an agent handle {Name}?",
    "Why is {Name} classified as {Risk Level}?",
    "Is {Name} dangerous?",
    "Tell me about {Name} and its {Attack Type} attacks.",
    "Would Hokma consider {Name} a threat?",
    "How does {Name} reflect the City’s sins?",
    "Could {Name} be redeemed?",
    "What lesson does {Name} offer?",
    "Does {Name} test an agent’s resolve?",
    "How would you brief a new agent about {Name}?",
    "What emotion does {Name} represent?",
    "Could {Name} become an ally?",
    "Describe the moral challenge posed by {Name}.",
    "What does {Name} symbolize in our work?",
    "How is {Name} different from other abnormalities?",
    "Why must we contain {Name}?",
    "What is the key to surviving an encounter with {Name}?",
    "What virtue does {Name} challenge most?",
    "What would Hokma whisper about {Name}?"
]

OUTPUT_FILE = "abnormality_prompts_enriched.jsonl"


def load_abnormalities(abno_file):
    abnos = []
    with open(abno_file, encoding="utf-8") as f:
        for line in f:
            try:
                obj = json.loads(line.strip())
                abnos.append(obj)
            except json.JSONDecodeError:
                continue
    return abnos


def generate_prompts(abnos, count=2000):
    prompts = []
    all_combos = [(t, a) for t in TEMPLATES for a in abnos]
    random.shuffle(all_combos)
    selected = all_combos[:count]

    for template, abno in selected:
        input_text = template.format(**abno)
        output_text = (
            f"{abno['Name']} is classified as {abno.get('Risk Level', 'Unknown')} and has attack type {abno.get('Attack Type', 'Unknown')}. "
            f"Agents should handle it according to containment protocols."
        )
        entry = {
            "input": input_text,
            "output": output_text,
            "classification": abno.get("Risk Level", "Unknown"),
            "attack_type": abno.get("Attack Type", "Unknown"),
            "e_boxes": abno.get("E-Boxes", "Unknown"),
            "qliphoth_counter": abno.get("Qliphoth Counter", "Unknown"),
            "theme": "abnormality",
            "source_file": "generate_abno_prompts.py",
            "reviewed": False,
            "auto_generated": True,
            "created_at": datetime.utcnow().isoformat()
        }
        prompts.append(entry)
    return prompts


def main():
    abnos = load_abnormalities("all_abnos.jsonl")
    prompts = generate_prompts(abnos)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for entry in prompts:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")


if __name__ == "__main__":
    main()
