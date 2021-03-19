L.amigo.auth.setToken('{replace with your API Token}');

// This dataset layer will have default popup behavior and an additional callback
// to handle some custom behavior after showing the popup.
// Note that popup generation can be completely overridden by setting
// the overrideCallback option and passing it a callback similar to the one
// passed to additionalCallback.
map.addDatasetLayer({
    url: 'https://app.amigocloud.com/api/v1/users/{user_id}/projects/{project_id}/datasets/{dataset_id}',
    popup: {
        popupTitle: '{field_in_dataset}',
        className: 'custom-popup-whatever',
        displayFields: ['{popup_title_field_in_dataset}', '{another_field_for_popup}'],
        additionalCallback: function (e, map) {
            if (e.data) {
                $('#redundancy').html('Looking at ' + e.data.amigo_id);
            } else {
                $('redundancy').html('Not looking at anything');
            }
        }
    }
});