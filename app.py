import pandas as pd
from dash import Dash, _dash_renderer
import dash_mantine_components as dmc
import dash_ag_grid as dag
import globals
import callbacks
from datetime import datetime
from dash_iconify import DashIconify
import gunicorn

globals.init()
df = pd.read_csv(f"assets/ewf_appearances.csv") 
df["date"] = df["date"].apply(lambda d: datetime.strptime(d, "%Y-%m-%d").date())

columndefs = [
    {"field":"team", "width":260},
    {"field":"played", "width":80},
    {"field":"won", "width":80},
    {"field":"drawn", "width":80},
    {"field":"lost", "width":80},
    {"field":"for", "width":80},
    {"field":"against", "width":90},
    {"field":"GD", "width":80},
    {"field":"points", "width":80},
]
gridwidth = sum([col["width"] for col in columndefs])

globals.gdata.update({
        "aprs": df,
        "columndefs":columndefs
})

_dash_renderer._set_react_version("18.2.0")
app = Dash(
    __name__,
    external_stylesheets=["https://unpkg.com/@mantine/dates@7/styles.css",]
)
server = app.server
# -------------------------------------------------------------------
def create_link(icon, href):
    return dmc.Anchor(
        dmc.ActionIcon(
            DashIconify(icon=icon, width=25), variant="transparent", size="lg"
        ),
        href=href,
        target="_blank",
    )
# ---------------
app.layout = dmc.MantineProvider(
    children=dmc.Container(
        children=[
            dmc.Group(
                children=[
                    dmc.Title("English Women's Football", order=1),
                    create_link(
                        "radix-icons:github-logo",
                        "https://github.com/dh3968mlq/figure-friday-week29",
                    )
                ],
                style={"width":"100%","height":"60px","background-color":"lightcyan"}
            ),
            dmc.Group(
                children=[
                    dmc.Text(children="Division:", style={"margin-bottom":"10px"}),
                    dmc.Select(
                        placeholder="Select division",
                        id="select-division",
                        value="Women's Super League (WSL)",
                        data=[{"value":div, "label":div} 
                                for div in sorted(list(set(df["division"])), reverse=True)],
                        w=400, mb=10,
                        persistence=True, persistence_type="session",
                        clearable=False,
                    ),
                ]
            ),
            dmc.Group(
                children=[
                    dmc.Text(children="Season:", style={"margin-bottom":"10px"}),
                    dmc.Select(
                        placeholder="Select season",
                        id="select-season",
                        w=400, mb=10, persistence=True,
                        persistence_type="session",
                        clearable=False,
                    ),
                ]
            ),
            dmc.Group(
                children=[
                    dmc.Text(children="Date:", style={"margin-bottom":"8px"}),
                    dmc.DatePicker(
                        id="date-picker-input",
                        w=250,
                    ),
                    dmc.Button(
                        children="Back one week",
                        leftSection=DashIconify(icon="icon-park:left"),
                        id="button-back"
                    ),
                    dmc.Button(
                        children="Forward one week",
                        rightSection=DashIconify(icon="icon-park:right"),
                        id="button-forward"
                    ),
                    dmc.Button(
                        children="End of season",
                        rightSection=DashIconify(icon="icon-park:right"),
                        id="button-end"
                    ),
                ]
            ),
            dmc.Space(h=24),
            dag.AgGrid(
                id="table",
                columnDefs=columndefs,
                rowData=[],
                dashGridOptions = {
                    "domLayout": "autoHeight",
                    "suppressColumnVirtualisation": True,
                },
                style = {"height": None, "width":gridwidth},
                defaultColDef={
                    "wrapHeaderText": True,
                    "autoHeaderHeight": True
                }
            ),
        ],
        size='lg',
    )
)
# -------------------------------------------------------------------
callbacks.cre_callbacks(app)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050)
