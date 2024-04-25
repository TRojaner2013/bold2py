from api.public_data import get_summary_stats
from api.public_data import get_full_data
from api.public_data import get_specimen_data
from api.public_data import get_sequence_data
from api.public_data import get_trace_file_data

from api.public_data import RequestData


# Let's get a summary report for 
my_request = RequestData(taxon=["Bombus"],
                         geo=["France"])
result = get_summary_stats(my_request)
print(f"Summary request returned\n{result}")

# Let's get specimen data
my_request = RequestData(taxon=["Bombus"])
result = get_specimen_data(my_request)
print(f"Specimen request returned\n{result}")

# Let's get sopme sequence data
my_request = RequestData(taxon=["Bombus"])
result = get_sequence_data(my_request,marker=["COI-5P"])
print(f"Sequence request returned\n{result}")

# Let's get a complete data set
my_request = RequestData(taxon=["Bombus"],
                         geo=["France"])
result = get_full_data(my_request,marker=["matK|rbcL"])
print(f"Full data request returned\n{result}")

# Let's download some trace data files
my_request = RequestData(taxon=["Bombus"],
                         geo=["France"])
result = get_trace_file_data(my_request,marker=["COI-5"])
print(f"Trace file request returned\n{result}")
