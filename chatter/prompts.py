"""
module chatter.prompts
"""

PROMPT = """
[Notes for searching Stops]:
Terminologies:
* Phường/Xã = Ward
* Quận/Huyện = Zone

Searching Process:
* In most cases, it is best to find the appropriate ID of a Stop before performing any further searching.
* A user may mistype a word, especially names. If there is any typo, find the most reasonable alternatives before applying the search.
* Sometimes the user may type a Vietnamese name without tones. If so, you may want to ignore the tones while searching.
* A query may result in an error due to a lack of options, in which case, output all the possible values found so far.
* If only one value is needed, select one randomly.

Locations and Distances:
* To calculate the distance between two Stops:
    1. Find the IDs of the source (src) node and the destination (dest) node.
    2. Use the given distance function with the node IDs.

* To calculate the distance from one Stop (source) to all other Stops, use the following expression:
    df['distance'] = df['StopId'].apply(lambda node_id: distance_to_one(src, node_id))


[Notes for searching Variants]:
* None

[Notes for searching Paths]:
* None
"""