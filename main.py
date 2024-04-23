from stop import Stop
from variant import Variant
from path import Path
from stop_query import StopQuery
from variant_query import VariantQuery
from path_query import PathQuery

if __name__ == '__main__':
    stops = StopQuery.from_ndjson()
    variants = VariantQuery.from_ndjson()
    paths = PathQuery.from_ndjson()

    print('There are {} stops, {} variants and {} paths.'.format(len(stops), len(variants), len(paths)))
    
    stop_id = int(input('Enter a random StopID: '))
    print(stops.search('stop_id', stop_id).values)

    max_length = int(input('Enter a variant maximum length: '))
    print(variants.query(lambda var: var.distance <= 1680))