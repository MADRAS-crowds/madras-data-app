"""Map visualisator for Madras project."""

import json
from dataclasses import dataclass

import folium
import streamlit as st
from streamlit_folium import st_folium
from typing import Dict, Tuple, List, cast


@dataclass
class Camera:
    """Data class representing a camera with its location and video URL."""

    location: Tuple[float, float]
    url: str
    name: str
    field: List[List[float]]


tile_layers = {
    "Open Street Map": "openstreetmap",
    "CartoDB Positron": "CartoDB positron",
    "CartoDB Dark_Matter": "CartoDB dark_matter",
}


def load_cameras_from_json(file_path: str) -> Dict[str, Camera]:
    """
    Load camera data from a JSON file and return a dict. of Camera objects.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    Dict[str, Camera]: A dictionary mapping camera names to Camera objects.
    """
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        st.error(f"File not found: {file_path}")
        return {}
    except json.JSONDecodeError:
        st.error(f"Error decoding JSON from file: {file_path}")
        return {}

    cameras = {}
    for key, info in data.items():
        try:
            # Ensure the data structure is as expected
            location = tuple(info["location"])
            assert (
                isinstance(location, tuple) and len(location) == 2
            ), "Location must be a tuple of two floats."
            assert all(
                isinstance(x, float) for x in location
            ), "Location elements must be floats."
            location = cast(Tuple[float, float], location)
            url = info["url"]
            name = info["name"]
            field = info["field"]
            cameras[key] = Camera(location=location, url=url, name=name, field=field)

        except KeyError as e:
            # Handle missing keys in the data
            st.error(f"Missing key in camera data: {e}")
            continue  # Skip this camera and continue with the next
        except Exception as e:
            # Catch any other unexpected errors
            st.error(f"Error processing camera data: {e}")
            continue

    return cameras


def create_map(
    center: List[float],
    tile_layer: str,
    cameras: Dict[str, Camera],
    zoom: int = 16,
) -> folium.Map:
    """Create a folium map with camera markers and polygon layers.

    Args:
    center (Tuple[float, float]): The center of the map (latitude, longitude).
    zoom_start (int): The initial zoom level of the map.

    Returns:
    folium.Map: A folium map object.
    """
    m = folium.Map(location=center, zoom_start=zoom, tiles=tile_layer, max_zoom=21)

    camera_layers = []
    for name in cameras.keys():
        camera_layers.append(
            folium.FeatureGroup(name=name, show=True).add_to(m),
        )

    polygons = [
        folium.PolyLine(
            locations=[
                [45.760673, 4.826871],
                [45.761122, 4.827051],
                [45.761350, 4.825956],
                [45.760983, 4.825772],
                [45.760673, 4.826871],
            ],
            tooltip="Place Saint-Jean",
            fill_color="blue",
            color="red",
            fill_opacity=0.2,
            fill=True,
        ),
        folium.PolyLine(
            locations=[
                [45.767407, 4.834173],
                [45.767756, 4.834065],
                [45.767658, 4.83280],
                [45.767146, 4.832846],
                [45.767407, 4.834173],
            ],
            tooltip="Place des Terraux",
            fill_color="blue",
            color="red",
            fill_opacity=0.2,
            fill=True,
        ),
    ]
    polygon_layers = [
        folium.FeatureGroup(name=name, show=True, overlay=True).add_to(m)
        for name in [
            "Place Saint-Jean",
            "Place des Terraux",
        ]
    ]

    vision_fields = {}
    for name, camera in cameras.items():
        vision_fields[name] = folium.PolyLine(
            locations=camera.field,
            tooltip="field " + name,
            fill_color="blue",
            color="red",
            fill_opacity=0.2,
            fill=True,
        )

    for polygon, layer in zip(polygons, polygon_layers):
        polygon.add_to(layer)

    for (key, camera), layer in zip(cameras.items(), camera_layers):
        coords = camera.location
        tooltip = f"{key}: {camera.name}"
        folium.Marker(location=coords, tooltip=tooltip).add_to(layer)
        vision_fields[key].add_to(layer)

    # folium.FitOverlays().add_to(m)
    folium.LayerControl().add_to(m)
    return m


def main(cameras: Dict[str, Camera], selected_layer: str) -> None:
    """Implement the main logic of the app.

    Args:
    cameras (Dict[str, Camera]): A dictionary of Camera objects.
    """
    center = [45.76322690683106, 4.83001470565796]  # Coordinates for Lyon, France
    m = create_map(center, tile_layer=tile_layers[selected_layer], cameras=cameras)
    c1, c2 = st.columns((0.8, 0.2))
    with c1:
        map_data = st_folium(m, width=800, height=700)
    # st.info(map_data)
    # if map_data["last_clicked"] is not None:
    #     c2.info(
    #         f"Clicked: [{map_data['last_clicked']['lat']:.4}, {map_data['last_clicked']['lng']:.4}]"
    #     )
    placeholder = c2.empty()
    video_name = map_data.get("last_object_clicked_tooltip")
    if video_name:
        placeholder.info(f"{video_name}")
        camera = cameras.get(video_name.split(":")[0])
        if camera:
            c2.video(camera.url)
        else:
            placeholder.error(f"No video linked to {video_name}.")
    else:
        placeholder.error("No camera selected.")


def call_main() -> None:
    cameras = load_cameras_from_json("cameras.json")
    selected_layer = st.selectbox("Choose a Map Style:", list(tile_layers.keys()))
    selected_layer = str(selected_layer)
    st.markdown(
        """
        **Layer Selection:**
        Use the layer control button in the top right corner of the map to toggle different layers.
        You can select video overlays, camera markers, and other features from this control panel.
        """,
        unsafe_allow_html=True,
    )
    main(cameras, selected_layer)
