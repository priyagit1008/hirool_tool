
# third party imports
from hashids import Hashids


def generate_hash(min_length, salt, alphabet, _id):
    """
    """
    return Hashids(
        min_length=min_length,
        salt=salt,
        alphabet=alphabet
    ).encode(_id)
