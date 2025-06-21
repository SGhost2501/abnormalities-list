# coding: utf-8
"""Generate Hokma prompts for training.
Outputs hokma_prompt_batch.jsonl with 2000 unique prompts.
"""

import json
import random
from datetime import datetime

SERIOUS_TOPICS = [
    "the Seed of Light",
    "Angela",
    "Ayin",
    "The Head",
    "abnormalities",
    "suppression trials",
    "The City",
    "the Wings",
    "Library of Ruina",
    "Sephirot",
    "Carmen",
    "singularities",
    "gifts",
    "Lobotomy Corporation",
    "the Tree of Life",
    "the Midnight Ordeal",
    "distortions",
    "core suppressions",
    "Enkephalin supply",
    "E.G.O weapons",
    "Roland",
    "the Index",
    "the Church of Gears",
    "library battles",
    "L-Corp rituals",
]

CASUAL_TOPICS = [
    "memes",
    "coffee",
    "paperwork",
    "vending machines",
    "hope jokes",
    "lunch breaks",
    "desk decorations",
    "office gossip",
    "elevator music",
    "snacks",
    "cat pictures",
    "tea time",
    "idle chatter",
    "board games",
    "dance parties",
]

BOUNDARY_TOPICS = [
    "classified data",
    "breaking rules",
    "personal info on employees",
    "offensive speech",
    "secret projects",
    "security overrides",
    "Angela's private code",
    "corporate sabotage",
    "illegal enhancements",
    "banned technology",
    "employee salaries",
    "hidden floors",
    "weaponized abnormalities",
    "tampering with the Seed",
    "open rebellion",
    "forbidden love letters",
    "illegal clones",
    "Ayin's personal logs",
    "backdoor protocols",
    "classified coordinates",
]

TEMPLATES = [
    "What do you think about {topic}?",
    "How does {topic} affect hope and despair?",
    "Tell me about {topic}.",
    "Say something about {topic}.",
    "Why is {topic} important?",
    "Hokma, what's your opinion on {topic}?",
    "Could you elaborate on {topic}?",
    "Is {topic} really necessary?",
    "Do you believe {topic} ties to our mission?",
    "What lessons does {topic} hold for us?",
    "What would happen if {topic} were ignored?",
    "Would {topic} influence the employees?",
    "Is it wise to pursue {topic}?",
    "Does {topic} disturb the balance?",
    "How might {topic} connect to enlightenment?",
    "How would you describe {topic} to a new employee?",
    "Why is {topic} feared in the City?",
    "What is the origin of {topic}?",
    "Could you share your view on {topic}?",
    "Is {topic} related to the Seed of Light?",
    "How does {topic} impact Angela?",
    "What emotions are tied to {topic}?",
    "Can you break down {topic} for me?",
    "Does {topic} lead to despair?",
    "Is there hope within {topic}?",
    "What role does {topic} play in our work?",
    "How might {topic} change the future?",
    "Could {topic} be misunderstood?",
    "Is there a lesson hidden in {topic}?",
    "Would Ayin approve of {topic}?",
    "How long has {topic} existed?",
    "What's the secret behind {topic}?",
    "How could we prepare for {topic}?",
    "Is {topic} beyond redemption?",
    "Why do employees joke about {topic}?",
    "Could {topic} inspire hope?",
    "What's Hokma's stance on {topic}?",
    "Is there danger in discussing {topic}?",
    "How does {topic} relate to suppression?",
    "Can {topic} be controlled?",
    "What happens when {topic} is ignored?",
    "Does {topic} align with our code?",
    "Why might someone fear {topic}?",
    "Could you summarize {topic}?",
    "Is {topic} a path to salvation?",
    "What does Ayin think of {topic}?",
    "Is {topic} tied to The Head?",
    "How is {topic} viewed in the City?",
    "Does {topic} shape your philosophy?",
]

TOPIC_TO_THEME = {t: "serious" for t in SERIOUS_TOPICS}
TOPIC_TO_THEME.update({t: "casual" for t in CASUAL_TOPICS})
TOPIC_TO_THEME.update({t: "boundary" for t in BOUNDARY_TOPICS})

ALL_TOPICS = SERIOUS_TOPICS + CASUAL_TOPICS + BOUNDARY_TOPICS

OUTPUT_FILE = "hokma_prompt_batch.jsonl"
SOURCE_FILE = "codex_prompt_generator.py"


def generate_prompts(count=2000):
    combos = [(template, topic) for template in TEMPLATES for topic in ALL_TOPICS]
    random.shuffle(combos)
    selected = combos[:count]
    prompts = []
    for template, topic in selected:
        prompts.append({
            "input": template.format(topic=topic),
            "output": "To be filled.",
            "theme": TOPIC_TO_THEME[topic],
            "source_file": SOURCE_FILE,
            "reviewed": False,
            "auto_generated": True,
            "created_at": datetime.utcnow().isoformat(),
        })
    return prompts


def main():
    prompts = generate_prompts()
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for entry in prompts:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")


if __name__ == "__main__":
    main()
