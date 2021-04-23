import dash
import dash_core_components as dcc
import dash_html_components as html
import geopandas as gpd
import plotly.express as px
import json
import pandas as pd
import dash_daq as daq

geo_df = gpd.read_file('hotel.geojson')
hotel_reviews_df = pd.read_csv("hotel_reviews.csv")

mapbox_access_token = "pk.eyJ1Ijoiam1jYXJyYXNjb3NhIiwiYSI6ImNrZGlvcmIzMzA3MW0zMG50dG90NWJ0aTEifQ.ZoobdVV5OqJUUVH-k2ZHDg"
external_stylesheets = ['https://codepen.io/chriddyp/pen/dZVMbK.css']
px.set_mapbox_access_token(mapbox_access_token)
country_areas = ["Madrid", "Costa del Sol", "Barcelona", "Costa Blanca"]
app = dash.Dash(external_stylesheets=external_stylesheets)



def update_reviews(reviews_toshow=None, average_score=None):
    
    if type(reviews_toshow) == type(None):
        return html.Div(
                children=[
                    html.H2(className="reviews-head", children="Reviews"),
                    html.Table(className="table", children=[
                            html.Tr(children=[
                                html.Td(children=[
                                    html.P(className="review", children="la review")])]
            )])])
    else:
        
        
        # grad = {"green":[6,10],"yellow":[2,6],"red":[0,2]}

        return html.Div(
                children=[html.Div(
                children=[
                    html.H2(className="reviews-head", children="Reviews"),
                    html.Table(className="table", children=[
                            html.Tr(children=[
                                html.Td(children=[
                                    html.P(className="review", children=reviews_toshow.iloc[i])])]
            ) for i in range(len(reviews_toshow))
            ]) ], style={"width": "100%", 'height': "70vh",
            'overflowY': 'scroll'}),
             daq.Gauge(id='score-gauge',
                        # color={"gradient":True, "ranges": grad},
                        label="Average user satisfaction",
                        showCurrentValue=True,
                        value=average_score
          )]
            
            )


layout=html.Div(children=[
    html.Div(className='row',  
            children=[
                html.Div(children=[
                    dcc.Dropdown(id="dropdown-menu", options=[{"label": i, "value": i} for i in country_areas], value="Madrid", multi=True, style={'backgroundColor': '#1E1E1E'}), 
                    # html.H2(id="click-data"), 
                    html.Div(className="div-reviews",
                    children=[html.Div(id="reviews", children=update_reviews())],)
                   ],
                    className="four columns div-user-controls"),
                        
                html.Div(className="eight columns div-for-charts bg-grey", 
                        children=[dcc.Graph(id='Graph1', config={'displayModeBar': False}, style={'width': '100vw', 'height': '100vh'})])
    
])])

app.layout = layout 


@app.callback(
    dash.dependencies.Output('Graph1', 'figure'),
    [dash.dependencies.Input('dropdown-menu', 'value')])
def update_figure(selected_region):
    if type(selected_region)==str:
        selected_region = [selected_region]
    filtered_geodf = geo_df[geo_df["country_area"].isin(selected_region)]
    
    fig = px.scatter_mapbox(filtered_geodf, lat=filtered_geodf.geometry.y,
                        lon=filtered_geodf.geometry.x, zoom=3,
                        hover_name="hotel_name", custom_data=["hotel_id"], template="plotly_dark")
    fig.update_layout(transition_duration=500, margin=dict(t=0, b=0, l=0, r=0), autosize=True)
    return fig


@app.callback(
    dash.dependencies.Output('reviews', 'children'),
    dash.dependencies.Input('Graph1', 'clickData'))
def select_clicked_data(clickData):
    id_selected = clickData["points"][0]["customdata"][0] #small start error cuz clickData is null at start
    reviews_toshow = hotel_reviews_df[hotel_reviews_df["hotel_id"]==id_selected][["review_title", "review_score"]]
    average_score = reviews_toshow["review_score"].mean()
    print(average_score)
    return update_reviews(reviews_toshow["review_title"], average_score)


if __name__ == '__main__':
    app.run_server()