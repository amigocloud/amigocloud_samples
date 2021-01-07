import fs from 'fs'

import axios from 'axios'
import FormData from 'form-data'
import { waitForJob, getFirstMap } from './helpers.js'

// Required constant values from the user
const API_TOKEN = ''
const USER_UUID = ''
const ORGANIZATION_UUID = ''
const PROJECT_UUID = ''
const BASE_URL = ''


const FILE_PATH = './Parks.zip'
const TOOLS_URL = `${BASE_URL}/api/v2/tools/run?token=${API_TOKEN}`
const JOBS_BASE_URL = `${BASE_URL}/api/v1/me/jobs`


const TOOL_INPUT = {
  clone_maps: true,
  project_uuid: PROJECT_UUID,
  user_uuid: USER_UUID
}

const openspatial_demo = async () => {
  // 1. Check initial Area of Interest (Bounding box)

  console.log('For initial map')
  const initialMap = await getFirstMap(BASE_URL, PROJECT_UUID, API_TOKEN)

  if(!Boolean(initialMap)) {
    throw 'No map found. Create one in the initial dataset'
  }

  if (initialMap.error_code) {
    throw `Initial map response error: ${initialMap.detail}`
  }

  console.log('Area of Interest:', initialMap.boundingbox)
  console.log('View:', initialMap.view)

  // 2. Clone Project "OpenSpatial Demo"
  console.log('Cloning...')

  let cloneResult
  try {
    cloneResult = await axios.post(
      // Endpoint
      TOOLS_URL,
      // Request body
      {
        tool_name: 'clone_project',
        tool_input: TOOL_INPUT,
        organization_uuid: ORGANIZATION_UUID
      }
    )
  } catch (error) {
    if (error.response) {
      console.log(error.response)
      throw 'Error cloning project. See details above'
    }
    throw error
  } 

  const cloneJobId = cloneResult.data.job_id

  const jobResult = await waitForJob(cloneJobId, JOBS_BASE_URL, API_TOKEN)

  if (jobResult.error_code) {
    throw `Error polling clone job: ${jobResult.detail}`
  }

  if (jobResult.status === 'FAILURE') {
    throw `Cloning job resulted in FAILURE. Check details here: ${jobResult.url}`
  }

  const clonedProjectUUID = jobResult.extra.output.cloned_project_uuid
  const uploadToClonedProjectUrl = `${BASE_URL}/api/v1/projects/${clonedProjectUUID}/datasets/upload?token=${API_TOKEN}`

  // 3. Upload new data, overwriting the old data

  const uploadFormData = new FormData()
  const formHeaders = uploadFormData.getHeaders()
  const newDatasetFile = fs.createReadStream(FILE_PATH)

  uploadFormData.append('datafile', newDatasetFile, 'Parks.zip')
  uploadFormData.append('dataset_write_action', 'overwrite')
  uploadFormData.append('csv_props.delimiter', ',')
  uploadFormData.append('csv_props.decimal_separator', '.')

  console.log('Uploading overwrite file...')

  let uploadResult
  try {
    uploadResult = await axios.post(uploadToClonedProjectUrl, uploadFormData, { headers: formHeaders })
  } catch (error) {
    if (error.response) {
      console.log(error.response)
      throw 'Error uploading new dataset file. See details above'
    }
    throw error
  }

  const uploadResultJobId = uploadResult.data.job
  const uploadJobResult = await waitForJob(uploadResultJobId, JOBS_BASE_URL, API_TOKEN)

  if (uploadJobResult.error_code) {
    throw `Error polling upload job: ${uploadJobResult.detail}`
  }

  if (uploadJobResult.status === 'FAILURE') {
    throw `Upload job resulted in FAILURE. Check details here: ${uploadJobResult.url}`
  }
  
  // 4. Check new Area of Interest
  console.log('For overwritten map')
  let clonedMap = await getFirstMap(BASE_URL, clonedProjectUUID, API_TOKEN)

  if (clonedMap.error_code) {
    throw `Cloned map response error: ${clonedMap.detail}`
  }

  // Clear the map's cache so the AOI is correctly updated
  try {
    await axios.post(`${clonedMap.purge_cache}?token=${API_TOKEN}`, {})
  } catch (error) {
    if (error.response) {
      console.log(error.response.data)
      throw 'Error purging cache. See details above.'
    }
  }

  clonedMap = await getFirstMap(BASE_URL, clonedProjectUUID, API_TOKEN)

  if (clonedMap.error_code) {
    throw `Cloned map response error: ${clonedMap.detail}`
  }

  console.log('Area of Interest:', clonedMap.boundingbox)
  console.log('View:', clonedMap.view)
}

if ([API_TOKEN, ORGANIZATION_UUID, PROJECT_UUID, USER_UUID, BASE_URL].includes('')) {
  throw 'Some of the required user data is not present'
}

openspatial_demo()