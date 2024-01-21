import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, Float, String, create_engine, ForeignKey
import os
from sqlalchemy.orm import relationship

# Connect to PostgreSQL database
database_name = 'python_car'
username = 'ahnaf'
password = '123'
port = '5432'
db_url = f'postgresql://{username}:{password}@localhost:{port}/{database_name}'
engine = create_engine(db_url)

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Create base model
Base = declarative_base()

class RidesData(Base):
    __tablename__ = 'rides_data'
    
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    timestamp = Column(sqlalchemy.ARRAY(sqlalchemy.DateTime), nullable=False)
    longitude = Column(sqlalchemy.ARRAY(Float), nullable=False)
    latitude = Column(sqlalchemy.ARRAY(Float), nullable=False)
    speed = Column(sqlalchemy.ARRAY(Integer))
    # Define the relationship to StatsTable

class StatsTable(Base):
    __tablename__ = 'stats_table'
    
    id = Column(Integer, primary_key=True)
    distance_travelled = Column(Float)
    hard_stops = Column(Integer)
    hard_accls = Column(Integer)
    start_loc = Column(String)
    end_loc = Column(String)
    duration = Column(Float)
    fuel_cost = Column(Float)

# Create app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div(
    children=[
        html.H1("Car Statistics", style={"textAlign": "center"}),
        html.Div(
            children=[
                html.Label("Select Date:"),
                dcc.Dropdown(
                    id="date-dropdown",
                    options=[
                        {"label": "All", "value": "All"}
                    ] + [
                        {"label": str(date[0]), "value": str(date[0])}
                        for date in session.query(RidesData.date).distinct().order_by(RidesData.date).all()
                    ],
                ),
            ],
            style={"width": "250px", "margin": "0 auto"},
        ),
        html.Div(
            children=[
                html.Label("Select Ride:"),
                dcc.Dropdown(
                    id="ride-dropdown",
                    options=[{"label": "All", "value": "All"}],
                ),
            ],
            style={"width": "250px", "margin": "0 auto"},
        ),
        dcc.Graph(id="ride-statistics"),
        html.Div(
            children=[
                html.H2("Ride Statistics", style={"textAlign": "center"}),
                html.Div(id="ride-stats-output")
            ],
            style={"width": "500px", "margin": "0 auto"},
        ),
    ]
)

@app.callback(
    Output('ride-stats-output', 'children'),
    Input('ride-dropdown', 'value')
)
def update_ride_stats(ride_id):
    if ride_id is not None and ride_id != "All":
        ride_data = session.query(RidesData).filter(RidesData.id == ride_id).first()
        if ride_data:
            date = ride_data.date
            timestamp = ride_data.timestamp[0]
            ride_stats = session.query(StatsTable).filter(StatsTable.id == ride_id).first()
            if ride_stats:
                stats_output = [
                    html.P(f"Distance Travelled: {round(ride_stats.distance_travelled, 3)}km"),
                    html.P(f"Hard Stops: {ride_stats.hard_stops}"),
                    html.P(f"Hard Accelerations: {ride_stats.hard_accls}"),
                    html.P(f"Start Location: {ride_stats.start_loc}"),
                    html.P(f"End Location: {ride_stats.end_loc}"),
                    html.P(f"Duration: {ride_stats.duration}"), 
                    html.P(f"Fuel Cost: {ride_stats.fuel_cost} AED")
                ]
                return stats_output
    return []

@app.callback(
    Output('ride-dropdown', 'options'),
    Output('ride-dropdown', 'value'),
    Input('date-dropdown', 'value')
)
def update_ride_dropdown(date):
    ride_options = [{"label": "All", "value": "All"}]
    
    if date != "All":
        rides = session.query(RidesData.id).filter(RidesData.date == date).all()
        for ride in rides:
            ride_options.append({"label": f"Ride {ride[0]}", "value": ride[0]})
    
    return ride_options, ride_options[0]["value"]

@app.callback(
    Output('ride-statistics', 'figure'),
    Input('date-dropdown', 'value'),
    Input('ride-dropdown', 'value')
)
def update_ride_statistics(date, ride):
    if date == "All" or ride == "All":
        if date == "All":
            ride_data = session.query(RidesData.timestamp, RidesData.longitude, RidesData.latitude, RidesData.speed).all()
        else:
            ride_data = session.query(RidesData.timestamp, RidesData.longitude, RidesData.latitude, RidesData.speed).filter(RidesData.date == date).all()
        if ride_data:
            ride_latitudes = []
            ride_longitudes = []
            ride_speeds = []
            ride_speedsText = []

            for ride in ride_data:
                ride_latitudes.extend(ride.latitude)
                ride_longitudes.extend(ride.longitude)
                ride_speedsText.extend(str(i) + "km/h" for i in ride.speed)
                ride_speeds.extend(ride.speed)
        else:
            return go.Figure()
    else:
        ride_data = session.query(RidesData.timestamp, RidesData.longitude, RidesData.latitude, RidesData.speed).filter(RidesData.date == date, RidesData.id == ride).first()
        
        if ride_data:
            ride_latitudes = [point for point in ride_data.latitude]
            ride_longitudes = [point for point in ride_data.longitude]
            ride_speeds = [point for point in ride_data.speed]
            ride_speedsText = [str(point) + "km/h" for point in ride_data.speed]             
        else:
            return go.Figure()

    trace = go.Scattermapbox(
        lat=ride_latitudes,
        lon=ride_longitudes,
        mode="markers+lines",
        marker=dict(
            size=8,
            color=ride_speeds,
            colorscale="Jet",
            opacity=0.7
        ),
        line=dict(
            color="rgb(0, 0, 0)",
            width=1
        ),
        hovertext=ride_speedsText
    )

    data = [trace]
    layout = go.Layout(
        autosize=True,
        hovermode="closest",
        mapbox=dict(
            accesstoken=os.getenv("mapKey"),
            bearing=0,
            center=dict(
                lat=sum(ride_latitudes) / len(ride_latitudes),
                lon=sum(ride_longitudes) / len(ride_longitudes)
            ),
            pitch=0,
            zoom=10
        ),
        height=500
    )

    fig = go.Figure(data=data, layout=layout)

    return fig

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)