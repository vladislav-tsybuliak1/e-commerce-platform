import re
import unicodedata


def slugify(string: str) -> str:
    """
    Convert a string to a URL-friendly slug.

    Example:
        >>> slugify(' Hello World--!  Кирилиця ')
        "hello-world"
    """

    normalized_text = (
        unicodedata.normalize("NFKD", string)
        .encode("ascii", "ignore")
        .decode("ascii")
    )

    # Replace non-alphanumeric characters with hyphens
    text = re.sub(r"[^\w\s-]", "", normalized_text.lower())

    # Replace spaces or repeated hyphens with a single hyphen
    text = re.sub(r"[-\s]+", "-", text).strip("-")

    return text
