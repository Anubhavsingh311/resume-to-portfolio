import re


class ResponseCleaner:

    @staticmethod
    def remove_markdown(text: str) -> str:

        text = text.strip()

        text = re.sub(r"^```json", "", text)

        text = re.sub(r"^```", "", text)

        text = re.sub(r"```$", "", text)

        return text.strip()

    @staticmethod
    def normalize_whitespace(text):

        return text.strip()