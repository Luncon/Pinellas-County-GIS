import requests
import json

species_name = 'Callicarpa americana'

def fetch_all_observations(species_name, max_pages=10):
    all_observations = []

    for page in range(1, max_pages + 1):
        observations = fetch_observations(species_name, page=page)

        if not observations: #Stop loop if fetch_observations() returns empty page
            break

        all_observations.extend(observations)

        print(f"Fetched page {page}: {len(observations)} observations")

    return all_observations

def fetch_observations(species_name, page=1):
    url = 'https://api.inaturalist.org/v1/observations'

    params = {
        'taxon_name': species_name,
        'quality_grade': 'research',
        'per_page': 10,
        'page': page
        }

    response = requests.get(url, params=params)
    data = response.json()
    
    return data["results"]



#Extract species, date, lattitude, longitude
def create_feature(observation):
    taxon = observation["taxon"]

    properties = {
            "observation_id": observation["id"],
            "taxon_id": taxon["id"],
            "scientific_name": taxon["name"],
            "common_name": taxon.get("prefered_common_name"),
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

if __name__ == "__main__":

    observations = fetch_all_observations(species_name)

    features = create_features(observations)
            
    geojson = save_geojson(features)





