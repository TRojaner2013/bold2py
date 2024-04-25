# This module implements the BOLD PUBLIC DATA API
#
# API Documentation is provided online at
# https://www.boldsystems.org/index.php/resources/api?type=webservices

from typing import List
import requests
from enum import Enum
from dataclasses import dataclass
from dataclasses import fields

# Timeout for requests to api
# Some operations take more time thus a high timout
# is mandatory e.g. when downloading trace data.
API_TIMEOUT = 60
API_LONG_TIMEOUT = 5000

class BaseURL(Enum):
    """ Base urls from bold api """
    SUMMARY = "http://www.boldsystems.org/index.php/API_Public/stats?"
    SPECIMEN = "http://www.boldsystems.org/index.php/API_Public/specimen?"
    SEQUENCE = "http://www.boldsystems.org/index.php/API_Public/sequence?"
    COMBINED = "http://www.boldsystems.org/index.php/API_Public/combined?"
    TRACE = "http://www.boldsystems.org/index.php/API_Public/trace?"

class ReturnFormat(Enum):
    """ Return formats for api requests """
    JSON = "json"
    XML = "xml"
    TSV = "tsv"
    DWC = "dwc"
    FASTA = "fasta"

class DataFormats(Enum):
    """ Data Fromats for api requests """
    OVERVIEW = "overview"
    DRILL_DOWN = "drill_down"

@dataclass
class RequestData:
    """ Handles data for api request """
    taxon: List[str] = None
    ids: List[str] = None
    bin_: List[str] = None
    container: List[str] = None
    institutions: List[str] = None
    researchers: List[str] = None
    geo: List[str] = None

    def create_url(self) -> str:
        params = []

        for field in fields(self):
            name = field.name
            value = getattr(self, name)

            if name == "bin_":
                name = "bin"

            if value is not None:
                if isinstance(value, list):
                    params.append(f"{name}={'|'.join(map(str, value))}")

        return "&".join(params)

    def is_empty(self):
        """ Checks if request is empty """
        for field in self.__dataclass_fields__.values():

            if getattr(self, field.name) is not None:
                return False

        return True

def get_summary_stats(data:RequestData, format_: ReturnFormat = ReturnFormat.JSON, data_type: DataFormats = DataFormats.DRILL_DOWN):
    """ Queries summary stats and returns result

    Parameters:

    Returns:

    Raises:
        - ValueError
        -     

    """
    if not format_ in (ReturnFormat.JSON,
                       ReturnFormat.XML):
        raise ValueError(f"Format {format_} is invalid. Choose either JSON or XML.")

    if data_type not in (DataFormats.OVERVIEW, DataFormats.DRILL_DOWN):
        raise ValueError(f"Data type {data_type} is invalid.")

    # ToDo: check if unused arguments are None and warn user.
    query = BaseURL.SUMMARY.value + data.create_url() + f"&format={format_.value}&dataType={data_type.value}"
    if __debug__: print(f"[PUBLIC ID SUMMARY] QUERY URL: {query}")
    response = requests.get(query, timeout=API_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.json()

def get_specimen_data(data: RequestData, format_: ReturnFormat=ReturnFormat.TSV):
    """ Queries specimen data and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """
    if not format_ in (ReturnFormat.TSV, ReturnFormat.XML,
                       ReturnFormat.JSON, ReturnFormat.DWC):
        raise ValueError(f"Format {format_} is invalid. Choose either JSON or XML.")

    query = BaseURL.SPECIMEN.value + data.create_url() + f"&format={format_.value}"
    if __debug__: print(f"[PUBLIC ID SPECIMEN] QUERY URL: {query}")
    response = requests.get(query, timeout=API_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.content

def get_sequence_data(data: RequestData, marker:List[str] = []):
    """ Queries sequence data and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """
    query = BaseURL.SEQUENCE.value + data.create_url() + f"&marker={'|'.join(map(str, (value for value in marker)))}"
    if __debug__: print(f"[PUBLIC ID SEQUENCE] QUERY URL: {query}")
    response = requests.get(query, timeout=API_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    #with open(path, mode='wb') as datafile:
    #    datafile.write(response.content)

    return response.content

def get_full_data(data: RequestData, marker: List[str]=[]):
    """ Queries full data and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """
    query = BaseURL.COMBINED.value + data.create_url() + f"&marker={'|'.join(map(str, (value for value in marker)))}"
    if __debug__: print(f"[PUBLIC ID FULL DATA] QUERY URL: {query}")
    response = requests.get(query, timeout=API_LONG_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.content

def get_trace_file_data(data: RequestData, marker: List[str]=[]):
    """ Queries trace files and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """

    query = BaseURL.TRACE.value + data.create_url() + f"&marker={'|'.join(map(str, (value for value in marker)))}"
    if __debug__: print(f"[PUBLIC ID TRACE FILE] QUERY URL: {query}")
    response = requests.get(query, timeout=API_LONG_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.content
