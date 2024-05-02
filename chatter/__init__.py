"""
module chatter
"""

import os
import pandas as pd

from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import OpenAI, ChatOpenAI

from queries import StopQuery, VariantQuery, PathQuery

class Chatter:
    """
    Chatter class.
    """
    stops:          StopQuery
    variants:       VariantQuery
    paths:          PathQuery

    stops_df:       pd.DataFrame
    variants_df:    pd.DataFrame = None
    paths_df:       pd.DataFrame = None

    stops_agent:    AgentType
    variants_agent: AgentType
    paths_agent:    AgentType

    def reset_agents(self):
        self.stops_agent = create_pandas_dataframe_agent(
            OpenAI(temperature = 0, model = 'text-davinci-003'), 
            self.stops_df, 
            verbose = True,
            max_iterations=5,
            prefix="""
                NOTES:

                Terminologies:
                * Phường/Xã = Ward
                * Quận/Huyện = Zone

                Locations and Distances:
                * The coordinates of a Stop is in meters.
                * To calculate the distance between two Stops, use the 'math.dist' function with coordinates in the columns 'coord_x' and 'coord_y'. 
            
                Searching Process:
                * A user may mistype a word, especially names. If there is any typo, find the most reasonable alternatives before applying the search.
                * A query may result in error due to lack of possible options, in which case, output all of the possible values found so far.
            """
        )

        self.variants_agent = None
        self.paths_agent = None

    def __init__(self, _stops: StopQuery = None, _variants: VariantQuery = None, _paths: PathQuery = None):
        if _stops is not None:
            self.stops = _stops
            self.stops_df = _stops.to_pandas(has_cartesian=True)
        if _variants is not None:
            pass
        if _paths is not None:
            pass
        self.reset_agents()

os.environ['OPENAI_API_KEY'] = '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'