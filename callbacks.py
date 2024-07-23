from dash import Input, Output, State
from dash.exceptions import PreventUpdate
from datetime import datetime, timedelta
import globals
import utils

def cre_callbacks(app):
    # -- Populate seasons Select
    @app.callback(
        Output("select-season","data"),
        Output("select-season","value"),
        Input("select-division", "value")
    )
    def populate_seasons(division):
        df = globals.gdata["aprs"]
        seasons = sorted(list(set(df[df["division"]==division]["season"])))
        sdata = [{"value":season, "label":season} for season in seasons]
        return sdata, seasons[-1]
    
    # -- Populate Datepicker
    @app.callback(
        Output("date-picker-input","minDate"),
        Output("date-picker-input","maxDate"),
        Output("date-picker-input","value", allow_duplicate=True),
        Input("select-season", "value"),
        Input("select-division", "value"),
        prevent_initial_call=True
    )
    def populate_datepicker(season, division):
        df = globals.gdata["aprs"]
        df = df[(df["division"] == division) & (df["season"] == season)]
        dates = df["date"]
        return min(dates), max(dates), max(dates)

    # -- Populate table
    @app.callback(
        Output("table","rowData"),
        Input("select-division", "value"),
        Input("select-season", "value"),
        Input("date-picker-input","value"),
        prevent_initial_call=True
    )
    def populate_table(division, season, date):
        if date is None:
            raise PreventUpdate
        df = utils.calc_table(division, season, date)
        return df.to_dict("records")

    # -- Back one week
    @app.callback(
        Output("date-picker-input","value", allow_duplicate=True),
        Input("button-back", "n_clicks"),
        State("date-picker-input","minDate"),
        State("date-picker-input","value"),
        prevent_initial_call=True
    )
    def back_oneweek(_, mindate, valdate):
        mindate = datetime.strptime(mindate, "%Y-%m-%d").date()
        valdate = datetime.strptime(valdate, "%Y-%m-%d").date()
        newdate=max(valdate-timedelta(days=7), mindate)
        return newdate

    # -- Forward one week
    @app.callback(
        Output("date-picker-input","value", allow_duplicate=True),
        Input("button-forward", "n_clicks"),
        State("date-picker-input","maxDate"),
        State("date-picker-input","value"),
        prevent_initial_call=True
    )
    def forward_oneweek(_, maxdate, valdate):
        maxdate = datetime.strptime(maxdate, "%Y-%m-%d").date()
        valdate = datetime.strptime(valdate, "%Y-%m-%d").date()
        newdate=min(valdate+timedelta(days=7), maxdate)
        return newdate

    # -- End of season
    @app.callback(
        Output("date-picker-input","value", allow_duplicate=True),
        Input("button-end", "n_clicks"),
        State("date-picker-input","maxDate"),
        prevent_initial_call=True
    )
    def forward_to_end(_, maxdate):
        return maxdate
