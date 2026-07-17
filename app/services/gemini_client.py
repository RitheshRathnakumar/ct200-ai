"""
Gemini AI client using the new google-genai SDK.
"""

from __future__ import annotations

import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("GEMINI_API_KEY not found in environment variables.")

client = genai.Client(api_key=API_KEY)

MODEL_NAME = "gemini-flash-latest"


class GeminiGenerationError(Exception):
    """Raised when Gemini generation fails."""


def generate(
    prompt: str,
    retries: int = 3,
) -> str:
    """
    Generate text using Gemini.

    Parameters
    ----------
    prompt:
        Prompt sent to Gemini.

    retries:
        Maximum retry attempts.

    Returns
    -------
    str
        Raw response text from Gemini.

    Raises
    ------
    GeminiGenerationError
    """

    delay = 1
    last_exception = None

    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
            )

            if not response.text:
                raise GeminiGenerationError(
                    "Gemini returned an empty response."
                )

            return response.text.strip()

        except Exception as exc:
            last_exception = exc

            if attempt == retries - 1:
                break

            time.sleep(delay)
            delay *= 2

    raise GeminiGenerationError(
        f"Gemini generation failed: {last_exception}"
    )