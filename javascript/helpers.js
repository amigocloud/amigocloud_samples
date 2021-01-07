import axios from 'axios'

export const waitForJob = async (jobId, jobsBaseUrl, API_TOKEN) => {
  console.log('Waiting for job with id:', jobId)
  let result = {
    status: null
  }

  while (result.status !== 'SUCCESS' && result.status !== 'FAILURE') {
    try {
      const rawResult = await axios.get(`${jobsBaseUrl}/${jobId}?token=${API_TOKEN}`)
      result = rawResult.data
    }
    catch(error) {
      if (error.response) {
        return error.response.data
      }
      throw error
    }
    await new Promise(resolve => setTimeout(resolve, 1000)) // Wait for a second before checking again
  }

  return result
}

export const getFirstMap = async (BASE_URL, PROJECT_UUID, API_TOKEN) => {
  const MAPS_URL = `${BASE_URL}/api/v1/projects/${PROJECT_UUID}/maps?token=${API_TOKEN}`
  try {
    const mapsRaw = await axios.get(MAPS_URL)
    return mapsRaw.data.results[0]
  } catch(error) {
    if (error.response) {
      return error.response.data
    }

    throw error
  }
  
}