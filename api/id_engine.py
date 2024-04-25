#
# Interface for BOLDs ID Engine API
#

from enum import Enum
import requests

API_TIMEOUT = 100

class BaseURL(Enum):
    ID_ENGINE = "http://boldsystems.org/index.php/Ids_xml?"

class Databases(Enum):
    """ Valid databeses for ID Engine """
    COX1 = "COX1"
    COX1_SPEC = "COX1_SPECIES"
    COX1_SEPC_PUB = "COX1_SPECIES_PUBLIC"
    COX1_L640 = "COX1_L640bp"

def query_id_engine(sequence: str, db: Databases) -> str:
    """ Queries data for provided taxonomy IDs

    Parameters:

    Returns:

    Raises:
        - ValueError
        -     

    """
    #ToDo: Check input query for obvious flaws
    query = BaseURL.ID_ENGINE.value + f"db={db.value}&sequence={sequence}"
    response = requests.get(query, timeout=API_TIMEOUT)

    if __debug__: print(f"[ID-ENGINE] QUERY URL: {query}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.content
