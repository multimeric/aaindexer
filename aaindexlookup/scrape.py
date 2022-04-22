import requests
from pyaaisc import Aaindex
import json
from collections import defaultdict
from aaindexlookup.parser import aaindex_file

BASE_URL = "https://www.genome.jp/ftp/db/community/aaindex/"
FIELD_NAMES = {
    "H": "accession",
    "D": "description",
    "R": "pmid",
    "A": "authors",
    "T": "title",
    "J": "journal",
    "C": "correlation",
    "I": "index",
    "M": "matrix"
}

def main():
    databases = []
    for i in range(1, 4):
        db_name = f"aaindex{i}"
        res = requests.get(BASE_URL + db_name)
        parsed = aaindex_file.parse_string(res.text)
        databases += list(parsed)
    print(len(databases))
        # for entry in res.text.split("//"):
        #     entry_dict = defaultdict(str)
        #     current_field = None
        #     for line in entry.splitlines(keepends=False):
        #         if not line:
        #             continue
        #         field_name = line[0]
        #         # Continuation lines don't have a new field name
        #         if field_name.strip():
        #             # Provide a usable name for each field
        #             current_field = FIELD_NAMES[field_name]
        #         data = line[2:]
        #         entry_dict[current_field] += "\n" + data
        #     if "index" in entry_dict:
        #         entry_dict["index"] =
        #     databases[entry_dict['accession']] = entry_dict



if __name__ == '__main__':
    main()