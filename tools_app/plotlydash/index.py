import dash
from .layouts import dashboard_page, vol_page, heatmap_page, heatmap_timeline_page, btc_vol_page, custom_page, optimizer_page, index_page
import dash_core_components as dcc
import dash_html_components as html
from .callbacks import init_callbacks


def init_dashboard(server):
    """Create a Plotly Dash dashboard."""
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/',
    )

    # Create Dash Layout
    dash_app.layout = html.Div(
        [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
    )

    dash_app.title = "Onramp Academy Tools"


    @dash_app.callback(
        dash.dependencies.Output("page-content", "children"),
        [dash.dependencies.Input("url", "pathname")],
    )
    def display_page(pathname):
        if pathname == "/apps/dashboard":
            return dashboard_page
        elif pathname == "/apps/volatility-chart":
            return vol_page
        elif pathname == "/apps/correlation-matrix":
            return heatmap_page
        elif pathname == "/apps/correlation-timeline":
            return heatmap_timeline_page
        elif pathname == "/apps/annualized-volatility":
            return btc_vol_page
        elif pathname == "/apps/custom-dashboard":
            return custom_page
        elif pathname == "/apps/portfolio-optimizer":
            return optimizer_page
        elif pathname == "/apps/crypto-index":
            return index_page
        else:
            return dashboard_page  # This is the "home page"

    init_callbacks(dash_app)
    return dash_app.server