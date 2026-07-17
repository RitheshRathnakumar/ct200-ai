"""
Validation utilities for LLM-generated QA test cases.

This module validates that Gemini returns the exact JSON structure
expected by the application. Any malformed output raises a validation
error so the generation service can retry or fail gracefully.
"""

from __future__ import annotations

import json
import re
from typing import Any


class LLMValidationError(Exception):
    """Raised when the LLM response cannot be validated."""


CODE_FENCE_PATTERN = re.compile(
    r"^```(?:json)?\s*|\s*```$",
    re.IGNORECASE | re.MULTILINE,
)


def strip_code_fences(text: str) -> str:
    """
    Remove markdown code fences.

    Gemini occasionally returns:

    ```json
    { ... }
    ```

    instead of raw JSON.
    """

    return CODE_FENCE_PATTERN.sub("", text).strip()


def parse_json(raw_response: str) -> dict[str, Any]:
    """
    Parse raw JSON returned by the LLM.

    Raises
    ------
    LLMValidationError
    """

    cleaned = strip_code_fences(raw_response)

    try:
        return json.loads(cleaned)

    except json.JSONDecodeError as exc:
        raise LLMValidationError(
            f"Invalid JSON returned by LLM: {exc}"
        ) from exc


def validate_test_case(test_case: dict[str, Any]) -> None:
    """
    Validate one QA test case.
    """

    required_fields = (
        "title",
        "objective",
        "steps",
        "expected_result",
        "traceability",
    )

    for field in required_fields:
        if field not in test_case:
            raise LLMValidationError(
                f"Missing field '{field}'"
            )

    if not isinstance(test_case["title"], str):
        raise LLMValidationError("title must be string")

    if not isinstance(test_case["objective"], str):
        raise LLMValidationError("objective must be string")

    if not isinstance(test_case["expected_result"], str):
        raise LLMValidationError(
            "expected_result must be string"
        )

    if not isinstance(test_case["steps"], list):
        raise LLMValidationError(
            "steps must be list"
        )

    if len(test_case["steps"]) == 0:
        raise LLMValidationError(
            "steps cannot be empty"
        )

    for step in test_case["steps"]:
        if not isinstance(step, str):
            raise LLMValidationError(
                "every step must be string"
            )

    if not isinstance(test_case["traceability"], list):
        raise LLMValidationError(
            "traceability must be list"
        )

    if len(test_case["traceability"]) == 0:
        raise LLMValidationError(
            "traceability cannot be empty"
        )

    for item in test_case["traceability"]:
        if not isinstance(item, str):
            raise LLMValidationError(
                "traceability entries must be string"
            )


def validate_generation(data: dict[str, Any]) -> dict[str, Any]:
    """
    Validate the complete generation payload.

    Expected schema:

    {
        "test_cases": [
            ...
        ]
    }

    Returns
    -------
    dict
        The validated payload.
    """

    if not isinstance(data, dict):
        raise LLMValidationError(
            "LLM output must be a JSON object"
        )

    if "test_cases" not in data:
        raise LLMValidationError(
            "Missing 'test_cases'"
        )

    test_cases = data["test_cases"]

    if not isinstance(test_cases, list):
        raise LLMValidationError(
            "'test_cases' must be a list"
        )

    if not (3 <= len(test_cases) <= 5):
        raise LLMValidationError(
            "LLM must generate between 3 and 5 test cases"
        )

    for case in test_cases:
        if not isinstance(case, dict):
            raise LLMValidationError(
                "Every test case must be an object"
            )

        validate_test_case(case)

    return data


def validate_llm_response(raw_response: str) -> dict[str, Any]:
    """
    Complete validation pipeline.

    Raw Text
          ↓
    Remove markdown
          ↓
    Parse JSON
          ↓
    Validate schema
          ↓
    Return dictionary
    """

    parsed = parse_json(raw_response)

    return validate_generation(parsed)