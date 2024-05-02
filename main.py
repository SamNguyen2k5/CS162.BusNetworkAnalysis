import os

from chatter import Chatter
from queries import StopQuery

if __name__ == '__main__':
    stops = StopQuery.from_ndjson()
    # variants = VariantQuery.from_ndjson()
    # paths = PathQuery.from_ndjson()

    chatter = Chatter(_stops=stops)
    # print(os.environ['OPENAI_API_KEY'])