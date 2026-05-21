from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parents[4]

PARSED_JSONS_PATH = ROOT_PATH / "assigment_2" / "step_2"/"outputs"/"parsed_xmls"

GROQ_KEY_PATH = Path(__file__).resolve().parents[2] / "ner_evaluation" / ".env"


DEFAULT_MODEL = "llama-3.3-70b-versatile"

# The prompt used to live here. It now lives in prompt_extraction.py, which
# implements the annotation rules validated in Phase 5c (ner_evaluation)
# while preserving the four-key output schema (author_mentions / new_people /
# organizations / projects) and the author-mention deduplication logic.
