import requests
import sys
import json
from shapely.geometry import shape
import argparse

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
    output_path = "../observations/observations.geojson" 

    geojson = {
        "type": "FeatureCollection",
        "features": features,
        }

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(geojson, file, indent=2)

    print(f"Saved GeoJSON to {output_path}")

def load_boundary(boundary_file):

    with open(f"../vectors/{boundary_file}", "r", encoding="utf-8") as file:
        boundary = json.load(file)
        
        return boundary

def filter_observations_by_boundary(observations, boundary_geometry):
    filtered_observations = []

    for observation in observations:
        observation_geometry = shape(observation["geojson"])

        if boundary_geometry.covers(observation_geometry):
            filtered_observations.append(observation)

    return filtered_observations


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
            description="Download INaturalist observations and export them as GeoJSON."
            )

    parser.add_argument(
            "--species",
            required=True,
            help="Scientific name of the species"
            )

    parser.add_argument(
            "--boundary",
            default=None,
            help="Boundary GeoJSON file"
            )

    parser.add_argument(
            "--place-id",
            type=int,
            default=None,
            help="INaturalist place ID"
            )
        
    args = parser.parse_args()

    species_name = args.species
    place_id = args.place_id
    boundary_file = args.boundary


    if len(sys.argv) < 4:
        print("Usage: python update_observation.py \"Species Name\" \"place_id\" \"boundary_file.geojson\"" )
        sys.exit(1)

    max_pages = 12 
    
    boundary = load_boundary(boundary_file)

    boundary_geometry = shape(
            boundary['features'][0]["geometry"]
            )

   
    observations = fetch_all_observations(species_name, max_pages, place_id)

    filtered_observations = filter_observations_by_boundary(
            observations,
            boundary_geometry
        )

    features = create_features(filtered_observations)

    print(f"Inside boundary: {len(filtered_observations)}")

    save_geojson(features)




