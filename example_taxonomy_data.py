from api.taxonomy import get_taxon_name
from api.taxonomy import get_taxonomy_id
from api.taxonomy import IdRequestData
from api.taxonomy import NameRequestData
from api.taxonomy import DataTypes

if __name__ == "__main__":

    # Let's send a taxonomy id request to bold.
    my_request = IdRequestData(taxId=['88898'],
                               data_types=[DataTypes.ALL],
                               include_Tree=True)

    result = get_taxonomy_id(my_request)
    print(f"Taxonomy ID request returned:\n{result}")

    # Now send a taxonomy name request to BOLD.
    my_request = NameRequestData(taxName=['Diplura'],
                                 fuzzy=True)

    result = get_taxon_name(my_request)
    print(f"Taxonomy Name request returned:\n{result}")