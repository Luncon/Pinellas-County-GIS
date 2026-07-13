# Pinellas County GIS

A Python-based GIS utility that downloads species observations from the iNaturalist API and exports them as GeoJSON for use in GIS software such as QGIS.

The project supports filtering observations by species, location, date range, and custom geographic boundaries, making it useful for ecological mapping, biodiversity analysis, and conservation projects.

---

## Features

* Download research-grade observations from the iNaturalist API
* Search for one or multiple species in a single run
* Automatic pagination to retrieve large datasets
* Filter observations by:

  * iNaturalist Place ID
  * Observation date range
  * Custom GeoJSON boundary (point-in-polygon filtering)
* Export observations as GeoJSON
* Optional append mode for adding observations to an existing output file
* Command-line interface built with `argparse`

---

## Technologies

* Python 3
* Requests
* Shapely
* GeoJSON
* iNaturalist REST API
* QGIS

---

## Project Structure

```text
Pinellas-County-GIS/
│
├── python/
│   └── update_observation.py
│
├── vectors/
│   └── pinellas_boundary.geojson
│
├── observations/
│   └── observations.geojson
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Luncon/Pinellas-County-GIS.git
cd Pinellas-County-GIS
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Usage

### Basic example

```bash
python update_observation.py \
    --species "Anolis sagrei"
```

### Multiple species

```bash
python update_observation.py \
    --species "Anolis sagrei" "Anolis carolinensis"
```

### Filter by place

```bash
python update_observation.py \
    --species "Anolis sagrei" \
    --place-id 2864
```

### Filter by date

```bash
python update_observation.py \
    --species "Anolis sagrei" \
    --date-after 2026-01-01 \
    --date-before 2026-12-31
```

### Filter using a custom boundary

```bash
python update_observation.py \
    --species "Anolis sagrei" \
    --boundary pinellas_boundary.geojson
```

### Append observations to an existing output

```bash
python update_observation.py \
    --species "Anolis sagrei" \
    --append
```

---

## Output

The script exports a GeoJSON `FeatureCollection` containing one feature for each observation.

Each feature includes:

* Observation ID
* Taxon ID
* Scientific name
* Common name
* Observation date
* Observation URL
* Taxonomic rank
* Iconic taxon
* Geographic coordinates

The output GeoJSON can be loaded directly into QGIS or other GIS applications.

---

## Example Workflow

1. Download observations from iNaturalist.
2. Filter observations by date and place.
3. Apply a point-in-polygon filter using a custom boundary.
4. Export the filtered observations to GeoJSON.
5. Load the output into QGIS for visualization and analysis.

---

## Future Improvements

Planned features include:

* Improved API error handling
* Retry logic for failed requests
* Additional GeoJSON validation
* Configurable output filenames
* Duplicate observation detection
* Unit tests
* Logging
* Enhanced progress reporting

---

## Data Sources

* iNaturalist API
* User-provided GeoJSON boundary files

---

## License

This project is licensed under the MIT License.

---

## Author

Lucas Smith
