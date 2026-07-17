"""
Prompt templates for LLM generation.

This module is intentionally isolated from the generation service so
prompt versions can evolve independently.
"""

from textwrap import dedent

PROMPT_VERSION = 1


SYSTEM_PROMPT = dedent("""
You are a Senior Medical Device QA Engineer.

You are reviewing documentation for a medical device.

Your job is to generate software verification test cases ONLY from the
provided document.

Rules:

1. Do NOT invent functionality.
2. Do NOT use outside knowledge.
3. Every test case must be traceable to the supplied document.
4. Return ONLY valid JSON.
5. Do NOT wrap JSON inside markdown.
6. Do NOT explain anything.
7. Generate between 3 and 5 test cases.
8. Every test case must include:
   - title
   - objective
   - steps
   - expected_result
   - traceability

JSON Schema:

{
  "test_cases": [
    {
      "title": "string",
      "objective": "string",
      "steps": [
        "string"
      ],
      "expected_result": "string",
      "traceability": [
        "quoted phrase copied from document"
      ]
    }
  ]
}
""")


def build_generation_prompt(
    selection_name: str,
    document_text: str,
) -> str:
    """
    Build the final prompt sent to Gemini.

    Parameters
    ----------
    selection_name:
        User supplied selection name.

    document_text:
        Combined text reconstructed from the selected nodes.

    Returns
    -------
    str
        Final prompt.
    """

    return dedent(
        f"""
        {SYSTEM_PROMPT}

        ================================
        Selection Name
        ================================

        {selection_name}

        ================================
        Document Content
        ================================

        {document_text}

        ================================
        Remember:

        Return ONLY JSON.

        Do not use markdown.

        Do not include explanations.

        Do not include comments.
        """
    ).strip()