import folium 

folium_layers = {
        'Google Satellite': folium.TileLayer(
                tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
                attr = 'Google',
                name = 'Google Satellite',
                overlay = True,
                control = True,
                show = False
                ),
        'whiteback': folium.TileLayer(
                tiles = 'https://api.mapbox.com/styles/v1/krktalilu/ckrdjkf0r2jt217qyoai4ndws/tiles/256/{z}/{x}/{y}@2x?access_token=pk.eyJ1Ijoia3JrdGFsaWx1IiwiYSI6ImNrcmRqMXdycTB3NG8yb3BlcGpiM2JkczUifQ.gEfOn5ttzfH5BQTjqXMs3w',
                name = 'Background: White',
                attr = 'Mapbox',
                control = True,
                overlay = True,
                show = False
                ),
        'Stamen TonerLite': folium.TileLayer(
                tiles = 'https://stamen-tiles-{s}.a.ssl.fastly.net/toner-lite/{z}/{x}/{y}{r}.png',
                attr = 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                name = 'Stamen TonerLite',
                control = True,
                overlay = True,
                show = False
        ), 
        'CyclOSM': folium.TileLayer(
                tiles = 'https://{s}.tile-cyclosm.openstreetmap.fr/cyclosm/{z}/{x}/{y}.png',
                attr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                name = 'CyclOSM',
                control = True,
                overlay = True,
                show = False
        ),     
        'OSM': folium.TileLayer(
                tiles = 'openstreetmap', 
                name = 'OpenStreetMap',
                attr = 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
                control = True, 
                overlay = True
                )
}