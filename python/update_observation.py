# 1. Get species name

# 2. Ask iNat for observations

# 3. Read response

# 4. Print total observations found

import requests

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
