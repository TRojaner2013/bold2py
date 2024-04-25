# This module implements an interface to BOLDs Taxonomy API

from enum import Enum
from dataclasses import dataclass
from dataclasses import fields
from typing import List
import requests

API_TIMEOUT = 100

class BaseURL(Enum):
    ID_SERVICE = "http://www.boldsystems.org/index.php/API_Tax/TaxonData?"
    NAME_SERVICE = "http://www.boldsystems.org/index.php/API_Tax/TaxonSearch?"

class DataTypes(Enum):
    """ Data Fromats for taxonomy api requests """
    BASIC = "basic"
    STATS = "stats"
    GEO = "geo"
    IMG = "images"
    LABS = "sequencinglabs"
    DEPOT = "depository"
    THIRD_PARTY = "thirdparty"
    ALL = 'all'

@dataclass
class IdRequestData:
    """ Handles data for taxonomy id requests """
    taxId: List[str] = None
    data_types: List[DataTypes] = None
    include_Tree: bool = False

    def create_url(self) -> str:
        """ Returns parameter for url """
        params = []

        for field in fields(self):
            name = field.name
            value = getattr(self, name)

            if value is not None:
                if name == 'data_types':
                    params.append(f"dataTypes={'|'.join(map(str, (typ.value for typ in value)))}")
                elif isinstance(value, list):
                    params.append(f"{name}={'|'.join(map(str, value))}")
                elif isinstance(value, bool):
                    params.append(f"{name}={str(value).lower()}")

        return "&".join(params)

@dataclass
class NameRequestData:
    """ Handles data for taxon name service requests """
    taxName: List[str] = None
    fuzzy: bool = None

    def create_url(self) -> str:
        """ Returns parameter for url """
        params = []

        for field in fields(self):
            name = field.name
            value = getattr(self, name)

            if value is not None:
                if isinstance(value, list):
                    params.append(f"{name}={'|'.join(map(str, value))}")
                elif isinstance(value, bool):
                    params.append(f"{name}={str(value).lower()}")

        return "&".join(params)


def get_taxonomy_id(data: IdRequestData) -> dict:
    """ Queries data for provided taxonomy IDs

    Parameters:

    Returns:

    Raises:
        - ValueError
        -     

    """
    #ToDo: Check input query for obvious flaws
    query = BaseURL.ID_SERVICE.value + data.create_url()
    response = requests.get(query, timeout=API_TIMEOUT)

    if __debug__: print(f"[ID-SERVICE] QUERY URL: {query}")
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.json()

def get_taxon_name(data: NameRequestData) -> dict:
    """ Queries data for provided taxonomy names

    Parameters:

    Returns:

    Raises:
        - ValueError
        -     

    """
    #ToDo: Check input query for obvious flaws
    query = BaseURL.NAME_SERVICE.value + data.create_url()
    response = requests.get(query, timeout=API_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.json()