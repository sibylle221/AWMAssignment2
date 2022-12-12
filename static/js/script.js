map = L.map("map", { doubleClickZoom: false }).locate({
  setView: true,
  watch: true,
  maxZoom: 16,
});

let osm = L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
});
osm.addTo(map);

map.on("locationfound", onLocationFound);

// let geoJsonFile = "geodjango_tutorial/static/fuel_location.geojson";

var icon = L.icon({
  iconUrl: icon,
  iconSize: [38, 95], // size of the icon
});

fetch(fuel)
  .then(function (response) {
    return response.json();
  })
  .then(function (data) {
    L.geoJson(data, {
      onEachFeature: function (feature, layer) {
        let petrolStation = "";

        if (feature.properties.brand) {
          petrolStation += "<p>" + feature.properties.brand + "</p>";
        }
        if (feature.properties.street) {
          petrolStation += "<p>Street: " + feature.properties.street + "</p>";
        }
        if (feature.properties.city) {
          petrolStation += "<p>City: " + feature.properties.city + "</p>";
        }

        layer.bindPopup(petrolStation);
      },
    }).addTo(map);
  });

//   fetch(icon)
//   .then(function (response) {
//     return response.json();
//   })
//   .then(function (data) {
//     L.geoJson(data, {
//       onEachFeature: function (feature, layer) {
//         layer.bindPopup(feature.properties.brand);
//       },
//     }).addTo(map);
//   });

let gpsMarker = null;
let gpsCircleMarker;

function onLocationFound(e) {
  let radius = e.accuracy / 2;
  let popupContent = "You are within " + radius + " meters from this point";

  if (gpsMarker == null) {
    gpsMarker = L.marker(e.latlng).addTo(map);
    gpsMarker.bindPopup(popupContent).openPopup();
    gpsCircleMarker = L.circle(e.latlng, radius).addTo(map);
  } else {
    gpsMarker.getPopup().setContent(popupContent);
    gpsMarker.setLatLng(e.latlng);
    gpsCircleMarker.setLatLng(e.latlng);
    gpsCircleMarker.setRadius(radius);
  }

  let url = "/update_location/";

  fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrftoken,
    },
    body: JSON.stringify({ latitude: e.latlng.lat, longitude: e.latlng.lng }),
  }).then((response) => {
    return response.json();
  });
}
