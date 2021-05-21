const greenIcon = L.icon({
    iconUrl: 'icons\\circle_green.png',

    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -20]
});

const purpleIcon = L.icon({
    iconUrl: 'icons\\circle_purple.png',

    iconSize: [30, 30],
    iconAnchor: [15, 15],
    popupAnchor: [0, -20]
});

const trackersStyle = {
    color: 'red',
    fillColor: 'rgba(0,0,0,0)',
}

const pathStyle = {
    color: 'rgb(51, 136, 255)',
}

const hideStyle = {
    color: 'rgba(0,0,0,0)',
}

class Plot {
    constructor(id) {
        this.map = L.map(id);
        L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token=pk.eyJ1IjoiamFja3Jvc3MiLCJhIjoiY2tvdTdla2xzMDQwZjJub2IweXJhajc2MCJ9.BBNjH9bJ0U32S-r777oCLQ', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 18,
            id: 'mapbox/streets-v11',
            tileSize: 512,
            zoomOffset: -1,
            accessToken: 'your.mapbox.access.token'
        }).addTo(this.map);

        this.path = L.polyline([], pathStyle).addTo(this.map);
        this.trackers = L.polygon([], trackersStyle).addTo(this.map);
        this.target = L.marker([0, 0], { icon: greenIcon }).addTo(this.map);
        this.target_guess = L.marker([0, 0], { icon: purpleIcon }).addTo(this.map);
    }

    update_path(update) {
        this.path.setLatLngs(update['latlon']);
        this.map.fitBounds(this.path.getBounds());
    }

    update_trackers(update) {
        this.trackers.setLatLngs(update['latlon']);
    }

    update_target(update) {
        this.target.setLatLng(update['latlon']);
        this.target.bindPopup(`Target<br>${this.target.getLatLng()}`);
    }

    update_target_guess(update) {
        this.target_guess.setLatLng(update['latlon']);
        this.target_guess.bindPopup(`Guess Target<br>${this.target_guess.getLatLng()}`);
    }

    hide_path(state = true) {
        if (state) {
            this.path.setStyle(hideStyle);
        }
        else {
            this.path.setStyle(pathStyle);
        }
    }
}