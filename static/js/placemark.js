ymaps.ready(init);

function init() {
    var myMap = new ymaps.Map("map", {
            center: [51.459278, 58.446270],
            zoom: 16
        }, {
            searchControlProvider: 'yandex#search'
        });

    myMap.geoObjects
        .add(new ymaps.Placemark([51.458464, 58.443611], {
            balloonContent: 'Орская улица, 111В'
        }, {
            preset: 'islands#icon',
            iconColor: '#0095b6'
        }))
        .add(new ymaps.Placemark([51.460614, 58.450627], {
            balloonContent: 'Елшанская улица, 110А'
        }, {
            preset: 'islands#dotIcon',
            iconColor: '#735184'
        }));
}
