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

const blueIcon = L.icon({
    iconUrl: 'icons\\circle_blue.png',

    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, -15]
});

const redIcon = L.icon({
    iconUrl: 'icons\\circle_red.png',

    iconSize: [20, 20],
    iconAnchor: [10, 10],
    popupAnchor: [0, -15]
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
        this.path_list = [];
        this.trackers = L.polygon([], trackersStyle).addTo(this.map);
        this.trackers_list = [];
        this.target = L.marker([0, 0], { icon: greenIcon, zIndexOffset: 10 }).addTo(this.map);
        this.target_guess = L.marker([0, 0], { icon: purpleIcon, zIndexOffset:11 }).addTo(this.map);
    }

    update_path(update) {
        this.path.setLatLngs(update['latlon']);
        update['latlon'].forEach(e => {
            const marker = L.marker(e, {icon: blueIcon}).addTo(this.map);
            marker.bindPopup(`Path<br>${marker.getLatLng()}`);
            this.path_list.push(marker);
        });
        this.map.fitBounds(this.path.getBounds());
    }

    update_trackers(update) {
        this.trackers.setLatLngs(update['latlon']);
        update['latlon'].forEach(e => {
            const marker = L.marker(e, {icon: redIcon}).addTo(this.map);
            marker.bindPopup(`Tracker<br>${marker.getLatLng()}`);
            this.trackers_list.push(marker);
        });
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