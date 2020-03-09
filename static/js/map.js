mapboxgl.accessToken = 'pk.eyJ1IjoianNvbWEiLCJhIjoibFJmYl9JWSJ9.AUm8d76cbOvVEn2mMeG_ZA';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v9',
    center: [{{ center_long }}, {{ center_lat }}],
    zoom: {{ zoom }}
});
var features = []
{% for result in results %}
    features.push({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [
                    {{ result.coordinates.longitude }},
                    {{ result.coordinates.latitude }}
            ]
        }
    })
{% endfor %}
map.on('load', function() {
    var geojsonData = {
        "type": "FeatureCollection",
        "features": features
    };
    map.addLayer({
        "id": "points",
        "type": "circle",
        "source": {
        "type": "geojson",
        "data": geojsonData
        }
    })
})