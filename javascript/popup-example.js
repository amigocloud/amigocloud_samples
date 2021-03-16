L.amigo.auth.setToken('R:hlmpQ33KameDSQqiseMAlgLjdlpGMrStsmbnhH');

// This dataset layer will have default popup behavior and an additional callback
// to handle some custom behavior after showing the popup.
// Note that popup generation can be completely overridden by setting
// the overrideCallback option and passing it a callback similar to the one
// passed to additionalCallback.
map.addDatasetLayer({
    url: 'https://app.amigocloud.com/api/v1/users/23/projects/3386/datasets/26051',
    popup: {
        popupTitle: 'last_name',
        className: 'custom-popup-whatever',
        displayFields: ['first_name', 'last_name', 'age', 'gender', 'race'],
        additionalCallback: function (e, map) {
            if (e.data) {
                $('#redundancy').html('Looking at ' + e.data.amigo_id);
            } else {
                $('redundancy').html('Not looking at anything');
            }
        }
    }
});
