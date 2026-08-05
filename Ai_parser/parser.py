import json

from .cleaner import ResponseCleaner

from .validator import ResponseValidator

from .normalizer import ResponseNormalizer

from .exceptions import InvalidJSON

from .logger import logger


class AIResponseParser:

    @classmethod
    def parse(cls, raw_response):

        logger.info("Starting Parsing Pipeline")

        cleaned = ResponseCleaner.remove_markdown(raw_response)

        cleaned = ResponseCleaner.normalize_whitespace(cleaned)

        logger.info("Cleaning Completed")

        try:

            parsed = json.loads(cleaned)

        except json.JSONDecodeError as e:

            logger.error("JSON Parsing Failed")

            raise InvalidJSON(e)

        logger.info("JSON Loaded")

        ResponseValidator.validate(parsed)

        logger.info("Validation Successful")

        normalized = ResponseNormalizer.normalize(parsed)

        logger.info("Normalization Completed")

        return normalized