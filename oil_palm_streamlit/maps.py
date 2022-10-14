import folium
from streamlit_folium import st_folium
import streamlit as st
from geopy.geocoders import Nominatim


# Add custom base maps to folium
BASEMAPS = {
    "ROADMAP": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Maps",
        overlay=True,
        control=True,
    ),
    "SATELLITE": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=True,
        control=True,
    ),
    "TERRAIN": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Terrain",
        overlay=True,
        control=True,
    ),
    "HYBRID": folium.TileLayer(
        tiles="https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}",
        attr="Google",
        name="Google Satellite",
        overlay=True,
        control=True,
    ),
    "ESRI": folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Satellite",
        overlay=True,
        control=True,
    ),
    "Esri Ocean": folium.TileLayer(
        tiles="https://services.arcgisonline.com/ArcGIS/rest/services/Ocean/World_Ocean_Base/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Ocean",
        overlay=True,
        control=True,
    ),
    "Esri Satellite": folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Satellite",
        overlay=True,
        control=True,
    ),
    "Esri Standard": folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Standard",
        overlay=True,
        control=True,
    ),
    "Esri Terrain": folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Terrain_Base/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Terrain",
        overlay=True,
        control=True,
    ),
    "Esri Transportation": folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Transportation",
        overlay=True,
        control=True,
    ),
    "Esri Topo World": folium.TileLayer(
        tiles="https://services.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Topo World",
        overlay=True,
        control=True,
    ),
    "Esri National Geographic": folium.TileLayer(
        tiles="http://services.arcgisonline.com/ArcGIS/rest/services/NatGeo_World_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri National Geographic",
        overlay=True,
        control=True,
    ),
    "Esri Shaded Relief": folium.TileLayer(
        tiles="https://services.arcgisonline.com/arcgis/rest/services/World_Shaded_Relief/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Shaded Relief",
        overlay=True,
        control=True,
    ),
    "Esri Physical Map": folium.TileLayer(
        tiles="https://services.arcgisonline.com/arcgis/rest/services/World_Physical_Map/MapServer/tile/{z}/{y}/{x}",
        attr="Esri",
        name="Esri Physical Map",
        overlay=True,
        control=True,
    ),
    "Bing VirtualEarth": folium.TileLayer(
        tiles="http://ecn.t3.tiles.virtualearth.net/tiles/a{q}.jpeg?g=1",
        attr="Microsoft",
        name="Bing VirtualEarth",
        overlay=True,
        control=True,
    ),
    "3DEP Elevation": folium.WmsTileLayer(
        url="https://elevation.nationalmap.gov/arcgis/services/3DEPElevation/ImageServer/WMSServer?",
        layers="3DEPElevation:None",
        attr="USGS",
        name="3DEP Elevation",
        overlay=True,
        control=True,
    ),
    "NAIP Imagery": folium.WmsTileLayer(
        url="https://services.nationalmap.gov/arcgis/services/USGSNAIPImagery/ImageServer/WMSServer?",
        layers="0",
        attr="USGS",
        name="NAIP Imagery",
        overlay=True,
        control=True,
    ),
}


def get_pos(lat, lng):
    return lat, lng


def search_bar():
    x, y = [41.00, 29.00]
    if "x" not in st.session_state:
        st.session_state["x"] = x
    if "y" not in st.session_state:
        st.session_state["y"] = y

    map_form = st.form("Map")

    # Default location
    # Search for another location
    location_input = map_form.text_input("Search in the map")
    submit_location = map_form.form_submit_button("Search")
    if submit_location:
        location = Nominatim(user_agent="GetLoc")
        getLocation = location.geocode(location_input)

        if getLocation is not None:
            x, y = getLocation.latitude, getLocation.longitude
            st.session_state["x"] = x
            st.session_state["y"] = y
        else:
            map_form.error("Location not found!")


def show_map():
    search_bar()
    m = folium.Map(
        location=[st.session_state["x"], st.session_state["y"]],
        zoom_start=13,
    )

    BASEMAPS["Esri Satellite"].add_to(m)
    folium.plugins.Draw(
        export=False,
        filename="my_data.geojson",
        position="topleft",
        draw_options={
            "rectangle": {
                "allowIntersection": False,
                "showRadius": True,
                "repeatMode": False,
            },
            "polyline": False,
            "polygon": False,
            "circle": False,
            "marker": False,
            "circlemarker": False,
        },
        edit_options={"poly": {"allowIntersection": False}},
    ).add_to(m)

    m.add_child(folium.LatLngPopup())

    map = st_folium(m, key="map", height=350, width=700)
    if map["last_clicked"] is not None:
        data = get_pos(map["last_clicked"]["lat"], map["last_clicked"]["lng"])
        st.write(map)

        if data is not None:
            st.write(data)
