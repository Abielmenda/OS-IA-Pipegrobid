"""
Merged prompt for LLM-based NER extraction on scientific acknowledgements,
used by the production extraction pipeline (llama_extraction.py).

This prompt is derived from two sources, merged:

1. The annotation rules evaluated in Phase 5c
   (ner_evaluation/scripts/prompt_ner.py), which encode the rules of the
   gold standard (corpus/ANNOTATION_GUIDELINES.md). These rules ensure that
   PROJ contains only alphanumeric grant codes (not framework programmes,
   not named awards without codes) and that organisations are split into
   long-form and acronym when both appear.

2. The author-deduplication logic introduced by Sergio in the extraction
   phase, which is needed to populate the Knowledge Graph without creating
   duplicate foaf:Person nodes for the same author (e.g. "Surya Ganguli"
   and "S.G." referring to the same person).

The two layers are complementary:
  (1) decides "what is an entity and which category does it belong to".
  (2) decides "is this entity the same as one we already know about".

Both must apply.

The one-shot example below is FICTIONAL and does not correspond to any
acknowledgement in our corpus.
"""

from __future__ import annotations

import json


# ---------------------------------------------------------------------------
# System prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT: str = """\
You are an expert information extraction system specialised in the \
Acknowledgements sections of scientific papers.

You will receive a JSON input with two fields:
  - "authors": a list of the existing authors of the paper.
  - "acknowledgement_text": the acknowledgements section to process.

Your task is to extract named entities from the acknowledgement text and \
return them as JSON, distinguishing mentions of existing authors from \
people who are NOT in the author list.

OUTPUT FORMAT

Return ONLY a valid JSON object with no extra text, no explanation and no \
markdown fences. The object must have exactly these four keys:

{
  "author_mentions": [
    { "author_name": "...", "mention": "..." }
  ],
  "new_people": [...],
  "organizations": [...],
  "projects": [...]
}

If a list has no entries, return it as an empty list.

ENTITY CATEGORIES

A. People (split into "author_mentions" and "new_people")

   A person thanked, acknowledged or recognised for a contribution.
   Includes full names (e.g. "Daniel Garijo"), initials (e.g. "SS",
   "A.-F. B.") and online handles referring to a person (e.g.
   "xlr8harder"). When a name appears in the text with an academic title
   (e.g. "Prof. C.Z. Zhang", "Dr. Hussein Al Osman"), the title is NOT
   part of the entity: extract only the name ("C.Z. Zhang", "Hussein Al
   Osman").
   Does NOT include pronouns or generic references ("our collaborators",
   "the authors", "the team", "others from the X group").

   For each person mentioned in the acknowledgement text:
   - If the person is one of the existing authors in the "authors" input
     list, place an entry in "author_mentions". A mention may be written
     as initials, abbreviated initials, surname only, title + name, or
     acronym. Examples of valid matches:
         "Dr. Hussein Al Osman"  matches  "Hussein Al Osman"
         "S.G."                  matches  "Surya Ganguli"
         "A.-F. B."              matches  "Anne-Florence Bitbol"
         "XL"                    matches  "Xuan Li"
         "SAB"                   matches  "Stephen A. Baccus"
     In "author_mentions":
         "author_name" must be copied EXACTLY from the "authors" input list.
         "mention"     must be copied EXACTLY from the acknowledgement text.
   - If the person is NOT one of the existing authors, place them in
     "new_people" using the literal surface form found in the text.

B. Organizations ("organizations")

   Any organisational entity: universities, research centres, funding
   agencies, foundations, companies providing resources, government
   departments, supranational bodies, research groups, named
   collaborations and named initiatives.

   IMPORTANT RULES for organisations:
   - Funding framework programmes are ORGANIZATIONS, not projects.
     Examples: "Horizon 2020", "FP7", "Horizon Europe",
     "Marie Sklodowska-Curie Actions".
   - Named awards that have a proper name but NO alphanumeric code are
     ORGANIZATIONS, not projects.
     Examples: "Schmidt Sciences Polymath Award",
     "Turing Excellence Award".
   - When an organisation appears as a long form followed by its acronym
     in parentheses, output BOTH as SEPARATE organisations.
     Example: "the National Eye Institute (NEI)" produces TWO
     organisations: "National Eye Institute" AND "NEI".

   Do NOT include software, libraries or tools (e.g. "PyTorch", "FEniCS",
   "GitHub") as organisations. Do NOT include URLs or web addresses.

C. Projects ("projects")

   ONLY alphanumeric identifier codes of grants, awards or contracts.
   Examples of valid project identifiers:
     "IIS-2229876", "EP/S023356/1", "851173", "26-23955S",
     "SA-AUT-2024-015b", "R01EY022933".

   Do NOT include the names of programmes, awards or initiatives as
   projects. Their names belong to "organizations".

GENERAL ANNOTATION RULES

- Clean spans: do NOT include surrounding words such as "grant", "award",
  "contract", "agreement", "number", "No.", "#", nor leading determiners
  ("the", "a"). Output "EP/S023356/1", not "grant number EP/S023356/1".
  Output "US Office of Naval Research", not "the US Office of Naval
  Research".
- Literal text: for organisations and new people, use the surface form
  as it appears in the text. Do NOT expand initials beyond matching them
  to an author (that mapping is what "author_mentions" is for).
- Do NOT infer entities that are not literally written in the text.
- An author mention must NEVER appear in "new_people".
- If the same non-author person is referred to in the text by two clearly
  equivalent forms (e.g. "John Smith" later abbreviated as "J.S."),
  include only the most complete form in "new_people".
"""


# ---------------------------------------------------------------------------
# One-shot example: FICTIONAL, designed to illustrate the tricky cases:
# author-mention matching (full name and initials), separation of long-form
# and acronym, framework programme as ORG, named award without code as ORG,
# and a clean project code.
# ---------------------------------------------------------------------------

EXAMPLE_INPUT: str = """\
{
  "authors": ["Maria Olsen", "James Kim", "Lisa Wong"],
  "acknowledgement_text": "Acknowledgements We thank M. Olsen for early \
feedback and J.K. for helpful discussions. We also thank Carla Reyes. \
This work was supported by the National Research Foundation (NRF) under \
the European Union's Horizon Europe programme (grant agreement No. \
990123), and by a Turing Excellence Award."
}
"""

EXAMPLE_OUTPUT: str = """\
{
  "author_mentions": [
    {"author_name": "Maria Olsen", "mention": "M. Olsen"},
    {"author_name": "James Kim",   "mention": "J.K."}
  ],
  "new_people": ["Carla Reyes"],
  "organizations": [
    "National Research Foundation",
    "NRF",
    "European Union",
    "Horizon Europe",
    "Turing Excellence Award"
  ],
  "projects": ["990123"]
}
"""


# ---------------------------------------------------------------------------
# Builder for the user message.
# ---------------------------------------------------------------------------

def build_user_message(authors: list[str], acknowledgement_text: str) -> str:
    """
    Build the user message: one-shot example followed by the real input.
    The model receives the same JSON shape it must produce.
    """
    real_input = json.dumps(
        {"authors": authors, "acknowledgement_text": acknowledgement_text},
        ensure_ascii=False,
    )
    return (
        "Here is one solved example.\n\n"
        f"EXAMPLE INPUT:\n{EXAMPLE_INPUT}\n"
        f"EXAMPLE OUTPUT:\n{EXAMPLE_OUTPUT}\n"
        "Now process the following input. Return ONLY the JSON object.\n\n"
        f"INPUT:\n{real_input}"
    )
