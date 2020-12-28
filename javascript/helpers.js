import axios from 'axios'

export const waitForJob = async (jobId, jobsBaseUrl, API_TOKEN) => {
  console.log('Waiting for job with id', jobId, 'using token', API_TOKEN)
  let result = {
    status: null
  }

  while (result.status !== 'SUCCESS' && result.status !== 'FAILURE') {
    try {
      const rawResult = await axios.get(`${jobsBaseUrl}/${jobId}?token=${API_TOKEN}`)
      result = rawResult.data
    }
    catch(err) {
      console.log(err.response ? err.response.data : err)
      return false
    }
    await new Promise(resolve => setTimeout(resolve, 1000)) // Wait for a second before checking again
  }

  return result
}