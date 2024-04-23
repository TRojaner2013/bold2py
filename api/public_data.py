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

    # ToDo: Pass these elements as argument in functions
    format_: ReturnFormat = None # Only Summary Stats, specimen data, full 
    data_type: DataFormats = None # Only summary data
    marker: List[str]=None # Only Sequence data, trace file, full data, 

    def create_url(self) -> str:
        params = []

        for field in fields(self):
            name = field.name
            value = getattr(self, name)

            if name == "format_":
                name = "format"
            elif name == "data_type":
                name = "dataType"
            elif name == "bin_":
                name = "bin"

            if value is not None:
                if isinstance(value, list):
                    params.append(f"{name}={'|'.join(map(str, value))}")
                elif isinstance(value, RequestData) or isinstance(value, DataFormats):
                    params.append(f"{name}={value.value}")

        return "&".join(params)

    def is_empty(self):
        """ Checks if request is empty """
        for field in self.__dataclass_fields__.values():
            if field.name == "__format":
                continue

            if field.name == "data_type":
                continue

            if getattr(self, field.name) is not None:
                return False

        return True


def create_url(**kwargs) -> str:
    """ Returns last part of bolds api url 

    Parmeters:
        -kwargs: keyworded arguments used for url

    Returns:
        str: last part of the url
    """
    params = []

    for key, value in kwargs.items():
        if value is not None and (isinstance(value, list) and value):
            params.append(f"{key}={'|'.join(map(str, value))}")

    return "&".join(params)

def get_summary_stats(data:RequestData):
        #taxon:List[str]=None,
        #              ids:List[str]=None,
        #              __bin:List[str]=None,
        #              container:List[str]=None,
        #              institutions:List[str]=None,
        #              researchers:List[str]=None,
        #              geo:List[str]=None,
        #              dataType:List[str]="drill_down",
        #              __format:ReturnFormat=ReturnFormat.JSON):
    """ Queries summary stats and returns result

    Parameters:

    Returns:

    Raises:
        - ValueError
        -     

    """
    if not data.__format in (ReturnFormat.JSON,
                             ReturnFormat.XML):
        raise ValueError(f"Format {data.__format} is invalid. Choose either JSON or XML.")

    if data.dataType not in ("overview", "drill_down"):
        raise ValueError(f"Data type {data.data_type} is invalid.")

    # ToDo: check if unused arguments are None and warn user.
    query = BaseURL.SUMMARY.value + create_url(data)
    response = requests.get(query, timeout=API_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.json()

def get_specimen_data(path: str, data: RequestData):
                      #taxon:List[str]=None,
                      #ids:List[str]=None,
                      #__bin:List[str]=None,
                      #container:List[str]=None,
                      #institutions:List[str]=None,
                      #researchers:List[str]=None,
                      #geo:List[str]=None,
                      #__format:ReturnFormat=ReturnFormat.JSON):
    """ Queries specimen data and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """
    if not data.__format in (ReturnFormat.TSV, ReturnFormat.XML,
                             ReturnFormat.JSON, ReturnFormat.DWC):
        raise ValueError(f"Format {data.__format} is invalid. Choose either JSON or XML.")

    query = BaseURL.SUMMARY.value + create_url(data)
    response = requests.get(query, timeout=API_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    return response.json()

def get_sequence_data(path: str, data: RequestData):
                      #taxon:List[str]=None,
                      #ids:List[str]=None,
                      #__bin:List[str]=None,
                      #container:List[str]=None,
                      #institutions:List[str]=None,
                      #researchers:List[str]=None,
                      #geo:List[str]=None,
                      #marker:List[str]=None):
    """ Queries sequence data and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """
    query = BaseURL.SEQUENCE.value + create_url(data)
    response = requests.get(query, timeout=API_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    with open(path, mode='wb') as datafile:
        datafile.write(response.content)

    return response

def get_full_data(path:str, data:RequestData):
                  #taxon:List[str]=None,
                  #ids:List[str]=None,
                  #__bin:List[str]=None,
                  #container:List[str]=None,
                  #institutions:List[str]=None,
                  #researchers:List[str]=None,
                  #geo:List[str]=None,
                  #marker:List[str]=None,
                  #__format:ReturnFormat=ReturnFormat.JSON):
    """ Queries full data and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """
    query = BaseURL.COMBINED.value + create_url(data)
    response = requests.get(query, timeout=API_LONG_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    with open(path, mode='wb') as datafile:
        datafile.write(response.content)

    return response

def get_trace_file_data(path:str, data:RequestData):
                        #taxon:List[str]=None,
                        #ids:List[str]=None,
                        #__bin:List[str]=None,
                        #container:List[str]=None,
                        #institutions:List[str]=None,
                        #researchers:List[str]=None,
                        #geo:List[str]=None,
                        #marker:List[str]=None):
    """ Queries trace files and returns result

    Parameters: ...

    Returns: ...

    Raises:
        - ValueError
        - ...

    """
    
    query = BaseURL.TRACE.value + create_url(data)
    response = requests.get(query, timeout=API_LONG_TIMEOUT)

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        raise error

    # ToDo: Perform some checks and make sure file is obtained.
    with open(path, mode='wb') as datafile:
        datafile.write(response.content)

    return response.content
