from api.public_data import get_summary_stats
from api.public_data import get_full_data
from api.public_data import get_specimen_data
from api.public_data import get_sequence_data
from api.public_data import get_trace_file_data
from api.common import ReturnFormat


MY_PATH = "./my-data/"

a = get_summary_stats(taxon=['Bombus'], geo=['France'])
print(a)
b = get_specimen_data(MY_PATH+"my_specimen_data.tsv", taxon=['Bombus'])
c = get_sequence_data(MY_PATH+"my_sequence_data.fasta", taxon=['Bombus'])
d = get_full_data(MY_PATH+"my_full_data.tsv", taxon=['Bombus'],format=ReturnFormat.JSON)
e = get_trace_file_data(MY_PATH+"my_trace_files.tar", taxon=['Bombus'], geo=['France'])

print(a)