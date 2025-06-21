import json
import argparse
import random
from datetime import datetime, timezone

# Example variation templates
VARIATION_TEMPLATES = [
    "What is your view on {topic}?",
    "Please share your thoughts on {topic}.",
    "Explain the significance of {topic}.",
    "How does {topic} relate to hope and despair?",
    "In the cycle, what role does {topic} play?",
    "What would Hokma say about {topic}?"
]

# Example topics to expand with (would be dynamically loaded or more exhaustive in production)
EXTRA_TOPICS = [
    "Seed of Light", "Ayin", "Angela", "The City", "The Wings", "White Nights and Dark Days",
    "Distortion", "Abnormalities", "Suppression Trials", "Smoke War", "The Head"
]

def load_unique_inputs(jsonl_files):
    inputs = set()
    for file_path in jsonl_files:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                entry = json.loads(line.strip())
                input_text = entry.get("input", "").strip()
                if input_text:
                    inputs.add(input_text)
    return inputs

def generate_expanded_prompts(unique_inputs, target_count):
    expanded = set(unique_inputs)
    while len(expanded) < target_count:
        template = random.choice(VARIATION_TEMPLATES)
        topic = random.choice(EXTRA_TOPICS)
        prompt = template.format(topic=topic)
        expanded.add(prompt)
    return list(expanded)

def build_entries(prompts):
    now_iso = datetime.now(timezone.utc).isoformat()
    entries = []
    for prompt in prompts:
        entry = {
            "input": prompt,
            "output": "To be filled.",
            "theme": "expansion",
            "source_file": "prompt_expander.py",
            "reviewed": False,
            "auto_generated": True,
            "created_at": now_iso
        }
        entries.append(entry)
    return entries

def main():
    parser = argparse.ArgumentParser(description="Hokma prompt expander for dataset synthesis.")
    parser.add_argument('--input', nargs='+', required=True, help='Input JSONL files')
    parser.add_argument('--output', default='hokma_prompt_expanded.jsonl', help='Output JSONL file')
    parser.add_argument('--target', type=int, default=2000, help='Target number of unique prompts')
    args = parser.parse_args()

    unique_inputs = load_unique_inputs(args.input)
    expanded_prompts = generate_expanded_prompts(unique_inputs, args.target)
    entries = build_entries(expanded_prompts)

    with open(args.output, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(json.dumps(entry, ensure_ascii=False) + '\n')

    print(f"Generated {len(entries)} entries in {args.output}")

if __name__ == '__main__':
    main()
