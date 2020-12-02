import plotly.express as px
import json
import pandas as pd
import plotly.io as pio
import plotly.graph_objects as go
from datetime import date
from datetime import timedelta


def map_create(df, s, color):
    india_states = json.load(open("./data/states_india.geojson", "r"))
    state_id_map = {}
    for feature in india_states["features"]:
        feature["id"] = feature["properties"]["state_code"]
        state_id_map[feature["properties"]["st_nm"]] = feature["id"]

    fig = go.Figure(data=go.Choropleth(
        locations=df["id"],
        z=df['total'],
        text=df['states'],
        geojson=india_states,
        colorscale=color,

        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgrey',
        marker_line_width=0.5,
        # colorbar_title="Total {}".format(s),
        colorbar=dict(
            title={'text': "Total {}".format(s)},

            thickness=15,
            len=0.5,
            bgcolor='rgba(255,255,255,0.6)',

            # tick0=0,
            # dtick=20000,

            # xanchor='left',
            # x=0.01,
            # yanchor='bottom',
            # y=0.05
        )

    ))
    fig.update_geos(
        visible=False,
        fitbounds="locations",
        projection=dict(
            type='miller',
            # parallels=[12.472944444, 35.172805555556],
            parallels=[86.472944444, 98.172805555556],
            rotation={'lat': 24, 'lon': 80}
        ),
        # lonaxis={'range': [68, 98]},
        # lataxis={'range': [6, 38]}
    )

    fig.update_layout(
        title=dict(
            text="{} COVID-19 Cases in India till {}".format(
                s, (date.today()-timedelta(days=1)).strftime("%B %d,%Y")),
            xanchor='center',
            x=0.5,
            yref='paper',
            yanchor='bottom',
            y=1,
            pad={'b': 10}
        ),
        margin={'r': 0, 't': 50, 'l': 0, 'b': 0},

    )

    # fig.update_geos(fitbounds="locations", visible=False)

    pio.write_image(fig, './images/{}.png'.format(s), width=800, height=700)
    # fig.show()


# confirmed = pd.read_csv("./data/confirmed_t.csv")
# map_create(confirmed, "Confirmed", "Blues")

# deceased = pd.read_csv("./data/deceased_t.csv")
# map_create(deceased, "Deceased", "Reds")

# recovered = pd.read_csv("./data/recovered_t.csv")
# map_create(recovered, "Recovered", "Greens")
