import requests
import sys
import json
from shapely.geometry import shape

def fetch_all_observations(species_name, max_pages=10, place_id=None):
    all_observations = []

    for page in range(1, max_pages + 1):
        observations = fetch_observations(species_name, page=page, place_id=place_id) 

        if not observations: #Stop loop if fetch_observations() returns empty page
            break

        all_observations.extend(observations)

        print(f"Fetched page {page}: {len(observations)} observations")

    return all_observations

def fetch_observations(species_name, page=1, place_id=None):
    url = 'https://api.inaturalist.org/v1/observations'

    params = {
        'taxon_name': species_name,
        'quality_grade': 'research',
        'per_page': 10,
        'page': page,
        }

    if place_id is not None:
        params['place_id'] = place_id

    response = requests.get(url, params=params)
    data = response.json()
    
    return data["results"]

#Convert one INat observaation into GeoJSON feature
def create_feature(observation):
    taxon = observation["taxon"]

    properties = {
            "observation_id": observation["id"],
            "taxon_id": taxon["id"],
            "scientific_name": taxon["name"],
            "common_name": taxon.get("preferred_common_name"),
            "observed_on": observation.get("observed_on"),
            "uri": observation["uri"],
            "taxon_rank": taxon["rank"],
            "iconic_taxon": taxon["iconic_taxon_name"]
            }

    feature = {
            "type": "Feature",
            "geometry": observation["geojson"],
            "properties" : properties
            }
    
    return feature


def create_features(observations):
    features = []

    for observation in observations:
        feature = create_feature(observation)
        features.append(feature)
    
    return features

def save_geojson(features):
    geojson = {
        "type": "FeatureCollection",
        "features": features,
        }

    with open("../observations/observations.geojson", "w", encoding="utf-8") as file:
        json.dump(geojson, file, indent=2)

def load_boundary():

    with open("../vectors/pinellas_boundary.geojson", "r", encoding="utf-8") as file:
        boundary = json.load(file)
        
        return boundary



if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python update_observation.py \"Species Name\"")
        sys.exit(1)

    species_name = sys.argv[1]
    max_pages = 12 #sys.argv[2]

    place_id = None


    boundary = load_boundary()

    boundary_geometry = shape(boundary['features'][0]["geometry"])


    print(boundary["features"][0]["geometry"]["type"])   
    observations = fetch_all_observations(species_name, max_pages, place_id)

    features = create_features(observations)
            
    geojson = save_geojson(features)




