from dash_bootstrap_components._components.CardHeader import CardHeader
from dash_bootstrap_components._components.DropdownMenu import DropdownMenu
from dash_bootstrap_components._components.DropdownMenuItem import DropdownMenuItem
from dash_bootstrap_components._components.InputGroup import InputGroup
from dash_bootstrap_components._components.Label import Label
from dash_bootstrap_components._components.PopoverHeader import PopoverHeader
import dash_core_components as dcc
import dash_html_components as html
from dash_bootstrap_components._components.CardBody import CardBody
from dash_bootstrap_components._components.Row import Row
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
import numpy as np 
import bt 
from direct_redis import DirectRedis
import urllib.parse as urlparse
from datetime import timedelta
from .formatting import onramp_colors, externalgraph_rowstyling, externalgraph_colstyling, recapdiv
from .helpers import line_chart, scatter_plot

url = urlparse.urlparse('redis://default:mUtpOEwJc2F8tHYOGxF9JGvnIwHY3unu@redis-16351.c263.us-east-1-2.ec2.cloud.redislabs.com:16351')
r = DirectRedis(host=url.hostname, port=url.port, password=url.password)


####################################################################################################
# 000 - INDEX DATA 
####################################################################################################

# defi_list = ['uni3', 'link', 'wbtc', 'dai', 'aave', 'mkr', 'cake', 'luna', 'avax', 'rune', 'comp', 'yfi', 'sushi', 'snx', 'bat' ]
# currency_list = ['btc']
# smartc_list = ['eth', 'ada', 'xlm', 'vet', 'etc', 'eos', 'neo', 'algo', 'xtz', 'waves', 'xem', 'zil']
# all_index = defi_list + currency_list + smartc_list
# data = pd.DataFrame()

# for ticker in all_index:
#         data_x = r.get(ticker+'-usd')
#         if data_x is None:
#             try:
#                 print("Could not find", ticker, "in the cache.")
#                 data_x = bt.get(ticker+'-usd', start = '2017-12-01')
#                 r.set(ticker+'-usd', data_x)
#                 r.expire(ticker+'-usd', timedelta(seconds = 86400))
#                 data = data.join(data_x, how = 'outer')

#             except:
#                 print(ticker, "NO DATA")
#         else:
#             data = data.join(data_x, how = 'outer')

# data = data.dropna()
# print(data)

# defi_data = data[['uni3usd', 'linkusd', 'aaveusd', 'mkrusd', 'avaxusd', 'runeusd', 'compusd', 'yfiusd', 'sushiusd', 'snxusd', 'batusd' ]]
# currency_data = data[['btcusd']]
# smartc_data = data[['ethusd', 'adausd', 'xlmusd', 'vetusd', 'etcusd', 'eosusd', 'neousd', 'algousd', 'xtzusd', 'wavesusd', 'xemusd', 'zilusd']]

# strategy_defi = bt.Strategy('Defi Index', 
#                                     [bt.algos.RunQuarterly(), 
#                                     bt.algos.SelectAll(), 
#                                     bt.algos.WeighEqually(),
#                                     bt.algos.Rebalance()]) #Creating strategy
# strategy_currency = bt.Strategy('Currency Index', 
#                                     [bt.algos.RunQuarterly(), 
#                                     bt.algos.SelectAll(), 
#                                     bt.algos.WeighEqually(),
#                                     bt.algos.Rebalance()]) #Creating strategy
# strategy_smartc = bt.Strategy('Smart Contract Index', 
#                                     [bt.algos.RunQuarterly(), 
#                                     bt.algos.SelectAll(), 
#                                     bt.algos.WeighEqually(),
#                                     bt.algos.Rebalance()]) #Creating strategy

# test_defi = bt.Backtest(strategy_defi, defi_data)
# results_defi = bt.run(test_defi)

# test_currency = bt.Backtest(strategy_currency, currency_data)
# results_currency = bt.run(test_currency)

# test_smartc = bt.Backtest(strategy_smartc, smartc_data)
# results_smartc = bt.run(test_smartc)

# results_list = [results_defi, results_currency, results_smartc]

# index_line = line_chart(results_list)

#index_scat = scatter_plot(results_list)


####################################################################################################
# 000 - LAYOUTS
####################################################################################################

#####################
# Nav bar
def get_navbar(p="dashboard"):

    navbar_dashboard = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard", active=True, href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top")

    navbar_custom = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard",active=True, href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top", className = "m-n4", style = {"width": "10000px"})

    navbar_optimizer = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", active=True, href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top", className = "m-n4", style = {"width": "10000px"})

    navbar_index = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", active=True, href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top", className = "m-n4", style = {"width": "10000px"})

    navbar_vol = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart", active=True, href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top")

    navbar_btc_vol = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart",  href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", active=True, href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix", href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top")

    navbar_heatmap = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix", active=True, href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top")

    navbar_timeline = dbc.Navbar([
            dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Dashboard",  href="/apps/dashboard", style = {"color": "black", "outline-color": 'black'})),
                dbc.NavItem(dbc.NavLink("Custom Strategy Dashboard", href="/apps/custom-dashboard", style = {"color": "black"})),
                dbc.NavItem(dbc.NavLink("Portfolio Optimizer", href="/apps/portfolio-optimizer", style = {"color": "black"})),
                #dbc.NavItem(dbc.NavLink("Crypto Indexes", href="/apps/crypto-index", style = {"color": "black"})),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Volatility Chart", href="/apps/volatility-chart", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Annualized Volatility ", href="/apps/annualized-volatility", style = {"color": "black"})),
                    ],
                    label = "Volatility Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                ),
                dbc.DropdownMenu(
                    [
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Matrix",  href="/apps/correlation-matrix", style = {"color": "black"})),
                    dbc.DropdownMenuItem(dbc.NavLink("Correlation Over Time", active=True, href="/apps/correlation-timeline", style = {"color": "black"})),
                    ],
                    label = "Correlation Charts",
                    toggle_style={"color": "black"},
                    nav = True,
                    
                    
                ),
            ],
            pills=True, 
            ), 
        ], color = "#f5f5f5", sticky = "top")


    if p == "dashboard":
        return navbar_dashboard
    elif p == "volatility":
        return navbar_vol
    elif p == "heatmap":
        return navbar_heatmap
    elif p == "timeline":
        return navbar_timeline
    elif p == "btc_vol":
        return navbar_btc_vol
    elif p == "custom":
        return navbar_custom
    elif p == "optimize":
        return navbar_optimizer
    elif p == "index":
        return navbar_index
    else:
        return navbar_dashboard

#####################
# Empty row
def get_emptyrow(h="45px"):
    """This returns an empty row of a defined height"""

    emptyrow = html.Div(
        [html.Div([html.Br()], className="col-12")],
        className="row",
        style={"height": h},
    )

    return emptyrow


####################################################################################################
# 001 - Portfilio Modeling
####################################################################################################
dashboard_page = html.Div(
    [
        # ##################### commented out for Nutech to place in iframe ########################
        # # Row 1 : Header
        # get_header(),
        #####################
        # Row 2 : Nav bar
        get_navbar("dashboard"),
        
        
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Impact of Adding BTC to a 60/40 Portfolio",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Cryptoassets such as Bitcoin (BTC) and Ether (ETH) have emerged as an asset class that clients are interested in holding long term. Cryptoassets are usually held away from advisors. As a trusted confidante and risk manager, Advisors should have access to tools and insights that help them manage portfolios holistically. Use the slider to show the performance change of adding 1-5% BTC to a typical 60/40 portfolio. ",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        # $html.Br(),
                                        html.H3(
                                            children="100% 60/40",
                                            style={"color": onramp_colors["white"]},
                                        ),
                                    ],
                                    className="col-2 slider-text",
                                ),
                                html.Div(
                                    [
                                        html.Br(),
                                        dcc.Slider(
                                            id="slider_num",
                                            min=0,
                                            max=10,
                                            value=0,
                                            step=0.5,
                                            marks={
                                                0: {
                                                    "label": "0% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                2.5: {
                                                    "label": "2.5% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                5: {
                                                    "label": "5% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                7.5: {
                                                    "label": "7.5% BTC",
                                                    "style": {"color": "white"},
                                                },
                                                10: {
                                                    "label": "10% BTC",
                                                    "style": {"color": "white"},
                                                },
                                            },
                                        ),
                                        html.Br()
                                    ],
                                    className="col-8",
                                ),
                                html.Div(
                                    [
                                        # html.Br(),
                                        html.H3(
                                            children="10% Bitcoin",
                                            style={"color": onramp_colors["white"]},
                                        ),
                                        
                                    ],
                                    className="col-2 slider-text",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAPS
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                dbc.Col(
                                    [   
                                        html.Br(),
                                        #dcc.Graph(id="pie_chart"),
                                        dcc.Loading(id = "loading-icon1", 
                                                children=[html.Div(dcc.Graph(id='pie_chart', style = {"height": 500}))], type="default")
                                        
                                        ], className="col-3", xs = 12, sm = 12, md = 12, lg = 3, xl = 3),
                                html.Div(

                                ),
                                # Chart Column
                                dbc.Col(
                                    [
                                        # dcc.Graph(
                                        #     id="line_chart", style={"responsive": True}
                                        # )
                                        html.Br(),
                                        dcc.Loading(id = "loading-icon2", 
                                                children=[html.Div(dcc.Graph(id='line_chart'))], type="default")

                                    ],
                                    style={"margin": "auto"},
                                    className="col-5", xs = 12, sm = 12, md = 12, lg = 5, xl = 5
                                ),
                                # Chart Column
                                dbc.Col(
                                    [
                                        #dcc.Graph(id="scatter_plot")
                                        html.Br(),
                                        dcc.Loading(id = "loading-icon3", 
                                                children=[html.Div(dcc.Graph(id='scatter_plot'))], type="default")
                                        
                                    
                                    ], className="col-4", xs = 12, sm = 12, md = 12, lg = 4, xl = 4

                                ),
                            ],
                            className="row",
                        ),  # Internal row
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                dbc.Col(
                                    [   #html.Br(),
                                        #dcc.Graph(id="bar_chart_rr")
                                        dcc.Loading(id = "loading-icon4", 
                                                children=[html.Div(dcc.Graph(id='bar_chart_rr'))], type="default")
                                    
                                    
                                    ], className="col-6", xs = 12, sm = 12, md = 6, lg = 6, xl = 6
                                ),
                                # Chart Column
                                dbc.Col(
                                    [   
                                        #html.Br(),
                                        #dcc.Graph(id="bar_chart_ss")
                                        dcc.Loading(id = "loading-icon5", 
                                                children=[html.Div(dcc.Graph(id='bar_chart_ss'))], type="default")
                                    ], className="col-6", xs = 12, sm = 12, md = 6, lg = 6, xl = 6),
                                html.Div(

                                ),
                                # Chart Column
                                html.Div([], className="col-4"),
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 002 - Volatility over Time Page
####################################################################################################
vol_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
        # Row 2 : Nav bar
        get_navbar("volatility"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Rolling Volatility Charts",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors will now have remote access to held-away client cryptoasset accounts via Read-Only or direct access to allocate on clients’ behalf via the Onramp platform, allowing Advisors to comprehensively manage clients’ assets and risk. Here we show how dynamic volatility can be in the cryptoasset ecosystem creating multiple opportunities to reach out to clients and discuss their risk tolerance and ability to withstand this volatility. ",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {"label": "Crypto", "value": "CC",},
                                                {
                                                    "label": "Mixed Asset Classes",  # TODO @cyrus let's use these names going forward.
                                                    "value": "AC",
                                                },
                                            ],
                                            value="AC",
                                        ),
                                    ],
                                    className="col-3",
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : onramp_colors['white']}),
                                    ],
                                    className="col-2",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAP
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-3'),
                                # Chart Column
                                html.Div(
                                    [
                                        # dcc.Graph(
                                        #     id="vol_chart", style={"responsive": True},
                                        # )
                                        dcc.Loading(
                                            id="loading-icon_vol",
                                            children=[
                                                
                                                    dcc.Graph(
                                                        id="vol_chart",
                                                        style={"responsive": True},
                                                    )
                                                
                                            ],
                                            type="default",
                                            
                                        )
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-4",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 003 - Annualized Volatility  Page
####################################################################################################
btc_vol_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
        # Row 2 : Nav bar
        get_navbar("btc_vol"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Annualized Volatility",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors will now have remote access to held-away client cryptoasset accounts via Read-Only or direct access to allocate on clients’ behalf via the Onramp platform, allowing Advisors to comprehensively manage clients’ assets and risk. Here we show how dynamic volatility can be in the cryptoasset ecosystem creating multiple opportunities to reach out to clients and discuss their risk tolerance and ability to withstand this volatility. ",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown_btc_vol",
                                            options=[
                                                {"label": "Bitcoin", "value": "BTC",},
                                                {"label": "Bitcoin Cash ABC", "value": "BCHABC",},
                                                {"label": "Tron", "value": "TRX",},
                                                {"label": "Chainlink", "value": "LINK",},
                                                {"label": "Stellar Lumen", "value": "XLM",},
                                                {"label": "Eos", "value": "EOS",},
                                                {"label": "Cardano", "value": "ADA",},
                                                {"label": "Litecoin", "value": "LTC",},
                                                {"label": "Neo", "value": "NEO",},
                                                {"label": "Binance Coin", "value": "BNB",},
                                                {"label": "Ethereum", "value": "ETH",},
                                            ],
                                            value="BTC",
                                        ),
                                    ],
                                    className="col-3",
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : onramp_colors['white']}),
                                    ],
                                    className="col-2",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAP
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-3'),
                                # Chart Column
                                html.Div(
                                    [
                                        # dcc.Graph(
                                        #     id="vol_chart", style={"responsive": True},
                                        # )
                                        dcc.Loading(id = "loading-icon_btc_vol", 
                                                children=[html.Div(dcc.Graph(id='btc_vol_chart', style = {"responsive": True, "width": "100%", "height": "70vh"}))], type="default"),
                                        
                                        dcc.Loading(id = "loading-icon_btc_vol_table", 
                                                children=[html.Div(dcc.Graph(id='btc_vol_chart_t', style = {"responsive": True, "width": "95%", "height": "70vh"}))], type="default")
                                        
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-8",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 004 - Correlation Matrix Heatmap Page
####################################################################################################
heatmap_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
        # Row 2 : Nav bar
        get_navbar("heatmap"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Correlation Matrix",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors can now manage the overall expected return, risk, Sharpe ratio, et cetera, of clients’ total mix of financial assets, including cryptocurrencies and decentralized finance. This heatmap, updated daily, shows current intra-asset correlations for: BTC, ETH, S&P500, All World Equities, High Yield, Global Hedge Funds, Gold, Emerging Market Indices, Russell 2000, Oil, Frontier Markets, and Biotech. Historical correlations are presented in the next tab.",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {"label": "Crypto", "value": "CC",},
                                                {
                                                    "label": "Mixed Asset Classes",
                                                    "value": "AC",
                                                },
                                            ],
                                            value="AC",
                                        ),
                                    ],
                                    className="col-3",
                                    # TODO: #1 style the dropdown to accommodate the text
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : onramp_colors['white']}),
                                    ],
                                    className="col-2",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAP
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4'),
                                # Chart Column
                                html.Div(
                                    [
                                        # dcc.Graph(
                                        #     id="heatmap",
                                        #     # figure = heatmap_fig_new,
                                        #     style={"responsive": True},
                                        # )
                                        dcc.Loading(
                                            id="loading-icon_heat",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="heatmap",
                                                        style={"responsive": True},
                                                    )
                                                )
                                            ],
                                            type="default",
                                        )
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-4",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 005 - Correlation over time (Heatmap over time) Page
####################################################################################################
heatmap_timeline_page = html.Div(
    [
        # #####################
        # # Row 1 : Header
        # get_header(),
        # #####################
        # Row 2 : Nav bar
        get_navbar("timeline"),
        #####################
        # Row 3 : Filters
        #####################
        # Row 4
        get_emptyrow(),
        #####################
        # Row 5 : Charts
        html.Div(
            [  # External row
                # html.Div([], className="col-1"),  # Blank 1 column
                html.Div(
                    [  # External 10-column
                        html.H2(
                            children="Correlation Over Time",
                            style={"color": onramp_colors["white"]},
                        ),
                        #html.Br(),
                        html.H6(
                            children="Advisors may have or receive questions about the value of adding cryptoassets, particularly BTC and ETH, to a traditional portfolio. Price returns speak for themselves but the history of their correlation to traditional assets is meaningful to holistic portfolio construction and client discussions. For example, the May 2021 drawdown in cryptoassets had very little correlation to the broader markets, illustrating its value as a minimally-correlated asset in a broader portfolio.",
                            style={"color": onramp_colors["white"]},
                        ),
                        html.Div(
                            [  # Internal row - RECAPS
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id="dropdown",
                                            options=[
                                                {"label": "Crypto", "value": "CC",},
                                                {
                                                    "label": "Mixed Asset Classes",
                                                    "value": "AC",
                                                },
                                            ],
                                            value="AC",
                                        ),
                                    ],
                                    className="col-3",
                                ),
                                html.Div([], className="col-8"),
                                html.Div(
                                    [
                                        # #html.Br(),
                                        # html.H3(children= "10% Bitcoin",
                                        # style = {'color' : onramp_colors['white']}),
                                    ],
                                    className="col-2",
                                ),  # Empty column
                            ],
                            className="row",
                            style=recapdiv,
                        ),  # Internal row - RECAP
                        html.Div(
                            [  # Internal row
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4'),
                                # Chart Column
                                html.Div(
                                    [
                                        # dcc.Graph(
                                        #     id="heatmap_timeline",
                                        #     # figure = heatmap_timeline_fig_new,
                                        #     style={"responsive": True},
                                        # )
                                        dcc.Loading(
                                            id="loading-icon_time",
                                            children=[
                                                html.Div(
                                                    dcc.Graph(
                                                        id="heatmap_timeline",
                                                        style={"responsive": True},
                                                    )
                                                )
                                            ],
                                            type="default",
                                        )
                                    ],
                                    style={"max-width": "100%", "margin": "auto"},
                                    className="col-4",
                                ),
                                # Chart Column
                                # html.Div([
                                # ],
                                # className = 'col-4')
                            ],
                            className="row",
                        ),  # Internal row
                    ],
                    className="col-12",
                    style=externalgraph_colstyling,
                ),  # External 10-column
                # html.Div([], className="col-1"),  # Blank 1 column
            ],
            className="row",
            style=externalgraph_rowstyling,
        ),  # External row
    ]
)
####################################################################################################
# 005 - Custom Strategy Page
####################################################################################################
stock_df = pd.read_csv('datafiles/tickerlist.csv')
stock_df = stock_df.dropna(how = "all")

ticker_list = list(stock_df["Ticker"])


for crypto in stock_df["Cryptos"]:
    if crypto is not np.nan:
        ticker_list.append(crypto)

def Inputs():

    inputs_ = dbc.Card([
            dbc.CardHeader(children= html.H3("Inputs"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
            dbc.CardBody([
                #Inputs 1

                dbc.Row([
                    dbc.Col([
                        html.Datalist(
                            id='list-suggested-inputs', 
                            children=[html.Option(value=word) for word in ticker_list]
                        ),
                        dbc.FormText("Enter Tickers"),
                        dbc.Input(
                            id = "Ticker1",
                            type= 'text',
                            value = "SPY",
                            placeholder= "Enter Ticker",
                            list = 'list-suggested-inputs',
                            debounce = True,
                            style = {"width" : "100%", "height": "60%"}

                        ),
                    ],width={'size':4}, className= " mb-4", 
                    ), 

                    dbc.Col([
                        dbc.FormText("Allocation %"),
                        dbc.InputGroup([
                            dbc.Input(
                                id = "Allocation1",
                                value = "50",
                                type= 'numeric',
                                placeholder= "Enter Allocation %",
                                style = {"width" : "100%"}

                            ), 
                            dbc.InputGroupAddon("%", addon_type = "append"),
                        ], size = 'sm' )
                        ],width={'size': 6, 'offset':1},
                    ),
                ]),

                #Inputs 2 
                dbc.Row([
                    dbc.Col(
                        dbc.Input(
                            id = "Ticker2",
                            type= 'text',
                            value = 'AGG',
                            placeholder= "Enter Ticker",
                            list = 'list-suggested-inputs',
                            style = {"width" : "100%", "height": "100%"}

                        ),
                    width={'size':4}, className= "mb-4"
                    ), 

                    dbc.Col([
                        dbc.InputGroup([
                            dbc.Input(
                                id = "Allocation2",
                                type= 'text',
                                value = "40",
                                placeholder= "Enter Allocation %",
                                style = {"width" : "100%"}

                            ), 
                            dbc.InputGroupAddon("%", addon_type = "append"),
                        ], size = 'sm')
                    ], width={'size':6, 'offset':1}),
                ]),

                #Inputs 3 
                dbc.Row([
                    dbc.Col(
                        dbc.Input(
                            id = "Ticker3",
                            type= 'text',
                            value = 'BTC-USD',
                            placeholder= "Enter Ticker",
                            list = 'list-suggested-inputs',
                            style = {"width" : "100%", "height": "100%"}

                        ),
                    width={'size':4}, className= "mb-4"
                    ), 

                    dbc.Col([
                        dbc.InputGroup([
                            dbc.Input(
                                id = "Allocation3",
                                type= 'text',
                                value = '7',
                                placeholder= "Enter Allocation %",
                                style = {"width" : "100%"}

                            ), 
                            dbc.InputGroupAddon("%", addon_type = "append"),
                        ], size = 'sm')
                        ], width={'size':6, 'offset':1},
                    ),
                ]),

                #Inputs 4 
                dbc.Row([
                    dbc.Col(
                        dbc.Input(
                            id = "Ticker4",
                            type= 'text',
                            value = 'ETH-USD',
                            placeholder= "Enter Ticker",
                            list = 'list-suggested-inputs',
                            style = {"width" : "100%", "height": "100%"}

                        ),
                    width={'size':4}, className= "mb-2"
                    ), 

                    dbc.Col([
                        dbc.InputGroup([
                        dbc.Input(
                            id = "Allocation4",
                            type= 'text',
                            value = "3",
                            placeholder= "Enter Allocation %",
                            style = {"width" : "100%"}
                        ), 
                        dbc.InputGroupAddon("%", addon_type = "append"),
                        ], size = 'sm')
                        ],width={'size':6, 'offset':1},
                    ),
                ]),

                #Inputs 5 
                dbc.Row([
                    dbc.Col(
                    width={'size':4}, className= "mb-4" #Empty Col for Rebalance 
                    ), 

                    dbc.Col([
                        dbc.FormText("Rebalance Threshold %"),
                        dbc.InputGroup([
                            dbc.Input(
                                id = "Rebalance",
                                type= 'text',
                                placeholder= "Optional",
                                style = {"width" : "100%", "height": "100%"}

                            ), 
                            dbc.InputGroupAddon("%", addon_type = "append"),
                        ], size = "sm", style = {"height": "60%"}),
                        dbc.Popover(
                            children = [
                            dbc.PopoverHeader("Rebalance Threshold", style = {"color": "black"}),
                            dbc.PopoverBody("This sets a constraint on the total allocation allowed to any one ticker. If the % an asset makes up within the broader portfolio increases or decreases by more than the designated rebalance threshold amount (X%), the portfolio will automatically rebalance to reach its target allocation for the asset."),
                            dbc.PopoverBody("Ex: BTC has a 5% allocation within your portfolio, with a 5% rebalance threshold. If BTC becomes 10% or more of the overall portfolio, it will trigger a rebalance."),
                            ],
                            id = "pop_rebal",
                            target = "Rebalance",
                            trigger = "hover"
                        )
                        ],width={'size':6, 'offset':1}, className= "mb-4"
                    ),
                ]),

                #Submit Button
                dbc.Row([
                    
                    dbc.Col(
                        dbc.Button(
                            id = "submit_button",
                            children= "Create Strategy",
                            n_clicks=0,
                            style= {"width": "100%", "height": "100%"}

                        ), width={'size':11, 'offset':0},
                    ),
                ]),
                
            ]), 
    ], className= "text-center mb-2 mr-2", style= {"height": "28rem"}, color= onramp_colors["dark_blue"], inverse= True,)

    return inputs_

def DisplayPie():
    pie = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Allocation"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            
            dcc.Loading( id = "loading_pie", children=
            dcc.Graph(
                id = "pie_chart_c",
                style = {"responsive": True,  "width": "100%", "height": 350}
            )
            )
        ]),
    ],  className= "text-center mb-2 mr-2", style= {"height": "28rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return pie
           
def DisplayLineChart():
    line = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Performance"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_line", children=
            dcc.Graph(
                id = "line_chart_c",
                style= {"responsive": True, "height": 350}
            ))
        ]), 
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "28rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return line        

def DisplayScatter():
    scat = dbc.Card([
        dbc.CardHeader(children= html.H3("Risk vs. Return"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading-scatter", children=
            dcc.Graph(
                id = "scatter_plot_c",
                style= {"responsive": True, "height": 370}
            )
            )
        ]),  
    ], className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "30rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return scat        

def DisplayStats():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Performance Statistics"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_stats", children=
            dcc.Graph(
                id = "stats_table",
                style= {"responsive": True}
            )
            )
        ]),  
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "30rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

def DisplayReturnStats():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Returns Recap"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_return1", children= 
                dcc.Graph(
                id = "balance_table",
                style= {"responsive": True}
                )
            ),
            dcc.Loading(id = "loading_returns2", children=
                dcc.Graph(
                id = "return_stats",
                style= {"responsive": True}
                )
            )
            
                            
        ])
    ],  className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "30rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats      

def DisplayMonthTable():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Returns Breakdown"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading( id = "loading_month", children=
            dcc.Graph(
                id = "month_table",
                style= {"responsive": True}
            )
            )
        ])
    ],  className= "text-center", style= {"max-width" : "100%", "margin": "auto", "height": "59rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

custom_page = dbc.Container([
    
    get_navbar('custom'),

    get_emptyrow(),
    #get_emptyrow(),
    #Title 
    dbc.Row(
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    html.H1(children="Custom Strategy Dashboard", style = {"color": onramp_colors["white"]}), 
                    
                    html.P(children= "Use the following tool to build hypothetical portfolios of equities, ETFs, and various Cryptoassets.  Analyze the impact of cryptoassets modeled in a traditional portfolio allocation. Over time we will enable advisors to create custom reports for clients based on the output.", 
                            style = {"fontSize": "vmin", "color": onramp_colors["white"]}),
                ]),
            className="text-center mb-2", color= onramp_colors["dark_blue"], inverse= True,), 
        width = 12)
    ),

    
    # Inputs | Pie Chart | Line Chart
    dbc.Row([
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    Inputs()
                ],  ),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 3),

        dbc.Col([
            
            dbc.Row([
                dbc.Col([
                    DisplayPie()
                ],  ),
            ]),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 3),
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayLineChart()
                ]),
            )
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 6 )
    ],no_gutters = True),

    # Stats | Scatter Plot | Return Recap
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayScatter()
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 4),


        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayReturnStats()
                    
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 4),
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayStats()
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 4)
    ], no_gutters = True),

    
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayMonthTable(),
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 12),
    ]),
], fluid=True)

####################################################################################################
# 005 - Portfolio Optimizer Page
####################################################################################################

def Inputs():

    inputs_ = dbc.Card([
            dbc.CardHeader(children= html.H3("Inputs"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
            dbc.CardBody([
                #Stock Ticker 
                dbc.Row([
                    dbc.Col([
                        dbc.FormText("Stock Tickers"),
                        dbc.Input(
                            id = "Ticker_o",
                            type= 'text',
                            value = "spy,agg,tsla,msft",
                            placeholder= "Enter Tickers",
                            debounce = True,
                            style = {"width" : "100%", "height": "62%"}

                        ),
                    ],width={'size':6}, className= "text-left mb-3", 
                    ),
                    dbc.Col([
                        dbc.FormText("Crypto Tickers"),
                        dbc.Input(
                            id = "cTicker_o",
                            type= 'text',
                            value = "btc-usd,eth-usd",
                            placeholder= "Enter Cryptos",
                            debounce = True,
                            style = {"width" : "100%", "height": "62%"}

                        ),
                    ],width={'size':6}, className= "text-left mb-3", 
                    ), 

                ]),

                #Inputs 1 
                # dbc.Row([
                #     dbc.Col([
                #         dbc.FormText("Enter Crypto Tickers Comma Seperated"),
                #         dbc.Input(
                #             id = "cTicker_o",
                #             type= 'text',
                #             value = "btc-usd,eth-usd,bnb-usd",
                #             placeholder= "Enter Cryptos",
                #             debounce = True,
                #             style = {"width" : "100%", "height": "50%"}

                #         ),
                #     ],width={'size':12}, className= "text-left mb-3", 
                #     ), 
                # ]),
                
                #Inputs 2
                dbc.Row([
                    dbc.Col([
                        dbc.FormText("Select Optimization Type"),
                        dbc.Select(
                            id = "opti_sel",
                            options=[
                                {"label": "Mean Variance Optimization", "value": "ef"},
                                {"label": "Equal Risk Contribution", "value": "er"},
                                {"label": "Inverse Volitility", "value": "iv"},
                            ],
                            value = "ef",
                            style = {"width" : "100%", "height": "62%"}

                        ),
                        dbc.Popover(
                            children = [
                            dbc.PopoverHeader("Optimization Types", style = {"color": "black"}),
                            dbc.PopoverBody("Mean Variance: Using the Efficient Frontier theory, MVM allows for the neutralization of asset specific (unsystematic) risk by optimizing for maximum return given existing correlation values and sharpe ratios of individual assets"),
                            dbc.PopoverBody("Equal Risk Contribution: Optimizes for maximum return by assigning equal risk to each asset "),
                            dbc.PopoverBody("Inverse Volatility: Gives the inverse of the volatility for each asset"),
                            ],
                            id = "pop_opti",
                            target = "opti_sel",
                            trigger = "hover"
                        )
                    ],width={'size':12}, className= "text-left mb-3"), 
                ]),

                #Inputs 3
                dbc.Row([
                    dbc.Col([
                        dbc.FormText("Rebalance Freq"),
                        dbc.Select(
                            id = "Frequency_sel",
                            options=[
                                {"label": "Daily Rebalance", "value": "Daily"},
                                {"label": "Monthly Rebalance", "value": "Month"},
                                {"label": "Quarterly Rebalance", "value": "Quart"},
                                {"label": "Yearly Rebalance", "value": "Year"},
                                {"label": "Compare All", "value": "Compare"},
                            ],
                            value = "Quart",
                            style = {"width" : "100%", "height": "62%"}
                        ),
                        dbc.Popover(
                            children = [
                            dbc.PopoverHeader("Rebalance Frequency", style = {"color": "black"}),
                            dbc.PopoverBody("Desired interval at which a rebalance to optimal portfolio allocation occurs."),
                            ],
                            id = "pop_freq",
                            target = "Frequency_sel",
                            trigger = "hover"
                        )
                        
                    ], width={'size':6}, className= "mb-5 text-left"
                    ), 

                    dbc.Col([
                        dbc.FormText("Max Crypto Alloc"),
                        dbc.InputGroup([
                        dbc.Input(
                            id = "crypto_alloc",
                            type= 'text',
                            placeholder= "Optional",
                            style = {"width" : "100%"}
                        ),
                        dbc.Popover(
                            children = [
                            dbc.PopoverHeader("Maximum Crypto Allocation", style = {"color": "black"}),
                            dbc.PopoverBody("Allows the advisor to place a Maximum on the percentage of crypto allocated in the portfolio. Determined allocation could be lower than this number, but will not exceed it"),
                            ],
                            id = "pop_max",
                            target = "crypto_alloc",
                            trigger = "hover"
                        ),
                        dbc.InputGroupAddon("%", addon_type = "append")
                        ], )
                    ], width={'size':6, 'offset':0}, className = "text-left"),
                ]),

                

                #Submit Button
                dbc.Row([
                    
                    dbc.Col(
                        dbc.Button(
                            id = "submit_button_o",
                            children= "Create Strategy",
                            n_clicks=0,
                            style= {"width": "100%"}

                        ), width={'size':12, 'offset':0},
                    ),
                ]),
                
            ]), 
    ], className= "text-center mb-2 mr-2", style= {"height": "25rem"}, color= onramp_colors["dark_blue"], inverse= True,)

    return inputs_

def DisplayPie():
    pie = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Allocation"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            
            dcc.Loading( id = "loading_pie_o", children=
            dcc.Graph(
                id = "pie_chart_o",
                style = {"responsive": True, "height": 300}
            )
            )
        ]),
    ],  className= "text-center mb-2 mr-2", style= {"height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return pie
           
def DisplayLineChart():
    line = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Performance"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_line", children=
            dcc.Graph(
                id = "line_chart_o",
                style= {"height": 300}
            ))
        ]), 
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)
    
    return line            

def DisplayScatter():
    scat = dbc.Card([
        dbc.CardHeader(children= html.H3("Risk vs. Return"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading-scatter", children=
            dcc.Graph(
                id = "scatter_plot_o",
                style= {"responsive": True, "height": 300}
            )
            )
        ]),  
    ], className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return scat        

def DisplayStats():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Performance Statistics"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_stats", children=
            dcc.Graph(
                id = "stats_table_o",
                style= {"responsive": True}
            )
            )
        ]),  
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

def DisplayOptomizeTable():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Allocation"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_return1", children= 
                dcc.Graph(
                id = "opto_table",
                style= {"responsive": True}
                )
            ),                
        ])
    ],  className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats      

def DisplayMonthTable():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Returns Breakdown"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading( id = "loading_month", children=
            dcc.Graph(
                id = "month_table_o",
                style= {"responsive": True}
            )
            )
        ])
    ],  className= "text-center", style= {"max-width" : "100%", "margin": "auto", "height": "65rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

optimizer_page = dbc.Container([
    
    get_navbar('optimize'),

    get_emptyrow(),
    #get_emptyrow(),
    #Title 
    dbc.Row(
        dbc.Col(
            dbc.Card([
                #dbc.CardHeader(children = html.H1("Portfolio Optimizer Dashboard")),
                dbc.CardBody([
                    html.H1(children="Portfolio Optimizer Dashboard", style = {"color": onramp_colors["white"]}), 
                    
                    html.P(children= "Determines favorable asset allocation of a portfolio based on preferred optimization method, rebalancing frequency, and (if desired) crypto allocation constraints. ", 
                            style = {"fontSize": "vmin", "color": onramp_colors["white"]}),
                    html.P(children= "Provides strategic portfolio insights via: backtested performance visualization, risk and return chart, performance statistics, and historical breakdown of monthly returns.", 
                            style = {"fontSize": "vmin", "color": onramp_colors["white"]}),
                ]),
            ],className="text-center mb-2", color= onramp_colors["dark_blue"], inverse= True,), 
        width = 12)
    ),

    
    # Inputs | Pie Chart | Line Chart
    dbc.Row([
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    Inputs()
                ],  ),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 3),

        dbc.Col([
            
            dbc.Row([
                dbc.Col([
                    DisplayPie()
                ],  ),
            ]),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 4),
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayLineChart()
                ]),
            )
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 5 )
    ],no_gutters = True),

    # Stats | Scatter Plot | Return Recap
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayOptomizeTable()
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 2, xl = 2),


        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayScatter()
                    
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 5, xl = 5),
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayStats()
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 5, xl = 5)
    ], no_gutters = True),

    
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayMonthTable(),
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 12),
    ]),
], fluid=True)

####################################################################################################
# 005 - Crypto Indexes Page
####################################################################################################

def Inputs():

    inputs_ = dbc.Card([
            dbc.CardHeader(children= html.H3("Inputs"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
            dbc.CardBody([
                #Stock Ticker 
                dbc.Row([
                    dbc.Col([
                        dbc.FormText("Stock Tickers"),
                        dbc.Input(
                            id = "Ticker_o",
                            type= 'text',
                            value = "spy,agg,tsla,msft",
                            placeholder= "Enter Tickers",
                            debounce = True,
                            style = {"width" : "100%", "height": "62%"}

                        ),
                    ],width={'size':6}, className= "text-left mb-3", 
                    ),
                    dbc.Col([
                        dbc.FormText("Crypto Tickers"),
                        dbc.Input(
                            id = "cTicker_o",
                            type= 'text',
                            value = "btc-usd,eth-usd",
                            placeholder= "Enter Cryptos",
                            debounce = True,
                            style = {"width" : "100%", "height": "62%"}

                        ),
                    ],width={'size':6}, className= "text-left mb-3", 
                    ), 

                ]),

                #Inputs 1 
                # dbc.Row([
                #     dbc.Col([
                #         dbc.FormText("Enter Crypto Tickers Comma Seperated"),
                #         dbc.Input(
                #             id = "cTicker_o",
                #             type= 'text',
                #             value = "btc-usd,eth-usd,bnb-usd",
                #             placeholder= "Enter Cryptos",
                #             debounce = True,
                #             style = {"width" : "100%", "height": "50%"}

                #         ),
                #     ],width={'size':12}, className= "text-left mb-3", 
                #     ), 
                # ]),
                
                #Inputs 2
                dbc.Row([
                    dbc.Col([
                        dbc.FormText("Select Optimization Type"),
                        dbc.Select(
                            id = "opti_sel",
                            options=[
                                {"label": "Mean Variance Optimization", "value": "ef"},
                                {"label": "Equal Risk Contribution", "value": "er"},
                                {"label": "Inverse Volitility", "value": "iv"},
                            ],
                            value = "ef",
                            style = {"width" : "100%", "height": "62%"}

                        ),
                        dbc.Popover(
                            children = [
                            dbc.PopoverHeader("Optimization Types", style = {"color": "black"}),
                            dbc.PopoverBody("Mean Variance: Using the Efficient Frontier theory, MVM allows for the neutralization of asset specific (unsystematic) risk by optimizing for maximum return given existing correlation values and sharpe ratios of individual assets"),
                            dbc.PopoverBody("Equal Risk Contribution: Optimizes for maximum return by assigning equal risk to each asset "),
                            dbc.PopoverBody("Inverse Volatility: Gives the inverse of the volatility for each asset"),
                            ],
                            id = "pop_opti",
                            target = "opti_sel",
                            trigger = "hover"
                        )
                    ],width={'size':12}, className= "text-left mb-3"), 
                ]),

                #Inputs 3
                dbc.Row([
                    dbc.Col([
                        dbc.FormText("Rebalance Freq"),
                        dbc.Select(
                            id = "Frequency_sel",
                            options=[
                                {"label": "Daily Rebalance", "value": "Daily"},
                                {"label": "Monthly Rebalance", "value": "Month"},
                                {"label": "Quarterly Rebalance", "value": "Quart"},
                                {"label": "Yearly Rebalance", "value": "Year"},
                                {"label": "Compare All", "value": "Compare"},
                            ],
                            value = "Quart",
                            style = {"width" : "100%", "height": "62%"}
                        ),
                        dbc.Popover(
                            children = [
                            dbc.PopoverHeader("Rebalance Frequency", style = {"color": "black"}),
                            dbc.PopoverBody("Desired interval at which a rebalance to optimal portfolio allocation occurs."),
                            ],
                            id = "pop_freq",
                            target = "Frequency_sel",
                            trigger = "hover"
                        )
                        
                    ], width={'size':6}, className= "mb-5 text-left"
                    ), 

                    dbc.Col([
                        dbc.FormText("Max Crypto Alloc"),
                        dbc.InputGroup([
                        dbc.Input(
                            id = "crypto_alloc",
                            type= 'text',
                            placeholder= "Optional",
                            style = {"width" : "100%"}
                        ),
                        dbc.Popover(
                            children = [
                            dbc.PopoverHeader("Maximum Crypto Allocation", style = {"color": "black"}),
                            dbc.PopoverBody("Allows the advisor to place a Maximum on the percentage of crypto allocated in the portfolio. Determined allocation could be lower than this number, but will not exceed it"),
                            ],
                            id = "pop_max",
                            target = "crypto_alloc",
                            trigger = "hover"
                        ),
                        dbc.InputGroupAddon("%", addon_type = "append")
                        ], )
                    ], width={'size':6, 'offset':0}, className = "text-left"),
                ]),

                

                #Submit Button
                dbc.Row([
                    
                    dbc.Col(
                        dbc.Button(
                            id = "submit_button_o",
                            children= "Create Strategy",
                            n_clicks=0,
                            style= {"width": "100%"}

                        ), width={'size':12, 'offset':0},
                    ),
                ]),
                
            ]), 
    ], className= "text-center mb-2 mr-2", style= {"height": "25rem"}, color= onramp_colors["dark_blue"], inverse= True,)

    return inputs_

def DisplayPie():
    pie = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Allocation"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            
            dcc.Loading( id = "loading_pie_o", children=
            dcc.Graph(
                id = "pie_chart_o",
                style = {"responsive": True, "height": 300}
            )
            )
        ]),
    ],  className= "text-center mb-2 mr-2", style= {"height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return pie
           
def DisplayLineChart():
    line = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Performance"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_line", children=
            dcc.Graph(
                id = "line_chart_i",
                style= {"height": 300}
            ))
        ]), 
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)
    
    return line            

def DisplayScatter():
    scat = dbc.Card([
        dbc.CardHeader(children= html.H3("Risk vs. Return"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading-scatter", children=
            dcc.Graph(
                id = "scatter_plot_o",
                style= {"responsive": True, "height": 300}
            )
            )
        ]),  
    ], className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return scat        

def DisplayStats():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Performance Statistics"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_stats", children=
            dcc.Graph(
                id = "stats_table_o",
                style= {"responsive": True}
            )
            )
        ]),  
    ], className= "text-center mb-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

def DisplayOptomizeTable():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Portfolio Allocation"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading(id = "loading_return1", children= 
                dcc.Graph(
                id = "opto_table",
                style= {"responsive": True}
                )
            ),                
        ])
    ],  className= "text-center mb-2 mr-2", style= {"max-width" : "100%", "margin": "auto", "height": "25rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats      

def DisplayMonthTable():
    stats = dbc.Card([
        dbc.CardHeader(children= html.H3("Returns Breakdown"), style = {"font": "Roboto", "color": onramp_colors["gray"]}),
        dbc.CardBody([
            dcc.Loading( id = "loading_month", children=
            dcc.Graph(
                id = "month_table_o",
                style= {"responsive": True}
            )
            )
        ])
    ],  className= "text-center", style= {"max-width" : "100%", "margin": "auto", "height": "65rem"}, color= onramp_colors["dark_blue"], inverse = True)

    return stats        

index_page = dbc.Container([
    
    get_navbar('index'),

    get_emptyrow(),
    #get_emptyrow(),
    #Title 
    dbc.Row(
        dbc.Col(
            dbc.Card([
                #dbc.CardHeader(children = html.H1("Portfolio Optimizer Dashboard")),
                dbc.CardBody([
                    html.H1(children="Crypto Indexes", style = {"color": onramp_colors["white"]}), 
                    
                    html.P(children= "Determines favorable asset allocation of a portfolio based on preferred optimization method, rebalancing frequency, and (if desired) crypto allocation constraints. ", 
                            style = {"fontSize": "vmin", "color": onramp_colors["white"]}),
                    html.P(children= "Provides strategic portfolio insights via: backtested performance visualization, risk and return chart, performance statistics, and historical breakdown of monthly returns.", 
                            style = {"fontSize": "vmin", "color": onramp_colors["white"]}),
                ]),
            ],className="text-center mb-2", color= onramp_colors["dark_blue"], inverse= True,), 
        width = 12)
    ),

    
    # Inputs | Pie Chart | Line Chart
    dbc.Row([
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayLineChart()
                ],  ),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 5),

        dbc.Col([
            
            dbc.Row([
                dbc.Col([
                    DisplayScatter()
                ],  ),
            ]),
        ], xs = 12, sm = 12, md = 12, lg = 6, xl = 4),
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayPie()
                ]),
            )
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 3 )
    ],no_gutters = True),

    # Stats | Scatter Plot | Return Recap
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayOptomizeTable()
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 2, xl = 2),


        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayScatter()
                    
                ],),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 5, xl = 5),
        
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayStats()
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 5, xl = 5)
    ], no_gutters = True),

    
    dbc.Row([
        dbc.Col([
            dbc.Row(
                dbc.Col([
                    DisplayMonthTable(),
                ]),
            ),
        ], xs = 12, sm = 12, md = 12, lg = 12, xl = 12),
    ]),
], fluid=True)
