# 1. Get species name

# 2. Ask iNat for observations

# 3. Read response

# 4. Print total observations found

import requests
import json

url = 'https://api.inaturalist.org/v1/observations'

species_name = 'Callicarpa americana'

params = {
    'taxon_name': species_name,
    'quality_grade': 'research',
    'per_page': 10,
    }

response = requests.get(url, params=params)
data = response.json()

observations = data['results']

print(f'Found {len(observations)} observations for {species_name}')

features = []

#Extract species, date, lattitude, longitude
for observation in observations:

    taxon = observation["taxon"]
    observation_id = observation["id"]
    taxon_id = taxon["id"]
    common_name = taxon["preferred_common_name"]
    scientific_name = taxon['name']
    observed_on = observation.get('observed_on')
    uri = observation['uri']
    rank = taxon['rank']
    iconic_taxon = taxon['iconic_taxon_name']

    #print(json.dumps(observation["geojson"], indent=2))

    properties = {
            "observation_id": observation_id,
            "taxon_id": taxon_id,
            "scientific_name": scientific_name,
            "common_name": common_name,
            "observed_on": observed_on,
            "uri": uri,
            "taxon_rank": rank,
        }


    feature = {
            "type": "Feature",
            "geometry": observation["geojson"],
            "properties" : properties
            }
    
    features.append(feature)
    

geojson = {
        "type": "FeatureCollection",
        "features": features
        }

print(json.dumps(geojson, indent=2))

with open("../observations/observations.geojson", "w", encoding="utf-8") as file:
    json.dump(geojson, file, indent=2)
