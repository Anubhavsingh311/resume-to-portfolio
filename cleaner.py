import re


class ResponseCleaner:

    @staticmethod
    def remove_markdown(text: str) -> str:
        text = text.strip()

        # 1. Extract from a fenced code block if present
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # 2. Find the outermost JSON object (handles any preamble/postamble)
        start = text.find("{")
        end   = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            return text[start:end + 1].strip()

        return text

    @staticmethod
    def normalize_whitespace(text: str) -> str:
        return text.strip()
