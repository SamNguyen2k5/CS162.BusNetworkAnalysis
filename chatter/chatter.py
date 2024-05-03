"""
module chatter.chatter
"""
import pandas as pd

from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI

from queries import StopQuery, VariantQuery, PathQuery
from network.bus import BusNetwork

from chatter.prompts import PROMPT
import chatter.tools

class Chatter:
    """
    Chatter class.
    """
    stops:          StopQuery
    variants:       VariantQuery
    paths:          PathQuery
    net:            BusNetwork

    stops_df:       pd.DataFrame
    variants_df:    pd.DataFrame = None
    paths_df:       pd.DataFrame = None

    stops_agent:    AgentType

    def reset_agents(self, is_smart: bool = True):
        """
        Reset pandas dataframe agent.
        """

        chatter.tools.load_net(self.net)

        extra_kwargs = {}
        if is_smart:
            extra_kwargs = {
                'prefix': PROMPT,
                'extra_tools': [
                    chatter.tools.distance_to_one
                    # chatter.tools.distance_to_all
                ]
            }

        print(extra_kwargs)

        self.stops_agent = create_pandas_dataframe_agent(
            ChatOpenAI(temperature = 0, model = 'gpt-4-turbo-preview'), 
            self.stops_df, 
            verbose = True,
            handle_parsing_errors=True,
            max_iterations=10,
            **extra_kwargs
        )
        
    def __init__(self, stops: StopQuery = None, variants: VariantQuery = None, paths: PathQuery = None, net: BusNetwork = None, is_smart: bool = True):
        # pylint: disable=too-many-arguments
        if stops is not None:
            self.stops = stops
            self.stops_df = stops.to_pandas(has_cartesian=True)
        if variants is not None:
            pass
        if paths is not None:
            pass
        if net is not None:
            self.net = net
        self.reset_agents(is_smart=is_smart)

    def ask(self, query: str, query_type: str = 'stop'):
        """
        Pass a query to the agent
        """
        if query_type == 'stop':
            return self.stops_agent.invoke(query)
        
        return None