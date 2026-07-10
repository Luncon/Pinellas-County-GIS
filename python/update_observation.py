# 1. Get species name

# 2. Ask iNat for observations

# 3. Read response

# 4. Print total observations found

import requests
import json

species_name = 'Callicarpa americana'

def fetch_observations(species_name):
    url = 'https://api.inaturalist.org/v1/observations'


    params = {
        'taxon_name': species_name,
        'quality_grade': 'research',
        'per_page': 10,
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


observations = fetch_observations(species_name)

features = []

for observation in observations:
    feature = create_feature(observation)
    features.append(feature)

geojson = {
        "type": "FeatureCollection",
        "features": features 
        }

print(json.dumps(geojson, indent=2))

with open("../observations/observations.geojson", "w", encoding="utf-8") as file:
    json.dump(geojson, file, indent=2)



