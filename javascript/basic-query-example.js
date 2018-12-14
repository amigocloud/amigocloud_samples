DATASET_ID = 34109
PROJECT_ID = 208
OWNER_ID = 329

// get access token from https://www.amigocloud.com/accounts/tokens/
ACCESS_TOKEN = 'R:XXXXX...'

async function getContainedRows (lat, lng, radius) {
  const query = `
    SELECT
      tree_name,
      latitude,
      longitude
    FROM dataset_${DATASET_ID}
    WHERE
      ST_DWITHIN(
        ST_GEOMFROMTEXT('POINT(${lng} ${lat})', 4326),
        ST_GEOMFROMTEXT('POINT(dataset_${DATASET_ID}.longitude dataset_${DATASET_ID}.latitude)', 4326),
        ${radius}
      )`

  const endpoint = `https://www.amigocloud.com/api/v1/users/${OWNER_ID}/projects/${PROJECT_ID}/sql`

  fetch(endpoint, {
    method: 'GET',
    body: {
      query: query,
      token: ACCESS_TOKEN
    }
  })
    .then(res => res.json())
    .then(response => {
      // Here you receive the response from your query in JSON format
      console.log(response)
    })

}