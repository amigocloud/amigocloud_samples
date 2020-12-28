import fs from 'fs'

import axios from 'axios'
import FormData from 'form-data'
import { waitForJob, getFirstMap } from './helpers.js'

// Required constant values from the user
const API_TOKEN = 'A:CzjSMcgMZil54agXnwo2msoNqhQklNGZh6bUyt'
const ORGANIZATION_UUID = '9820f3db-7745-4c46-98ba-8824363e07db'
const PROJECT_UUID = 'bd69dcb4-2d78-4c7b-9f7c-a5898cc95da7'
const USER_UUID = '6df02d58-8765-411f-bc82-5ca7e369ed7c'
const FILE_PATH = './Parks.zip'

const BASE_URL = 'http://localhost'
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

  console.log('Area of Interest:', initialMap.boundingbox)
  console.log('View:', initialMap.view)

  // 2. Clone Project "OpenSpatial Demo"

  const cloneResult = await axios.post(
    // Endpoint
    TOOLS_URL,
    // Request body
    {
      tool_name: 'clone_project',
      tool_input: TOOL_INPUT,
      organization_uuid: ORGANIZATION_UUID
    }
  )

  const cloneJobId = cloneResult.data.job_id

  console.log('Cloning...')
  const jobResult = await waitForJob(cloneJobId, JOBS_BASE_URL, API_TOKEN)

  if (!Boolean(jobResult) || jobResult.status === 'FAILURE') throw 'Error while polling clone job'

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

  let uploadResult
  try {
    uploadResult = await axios.post(uploadToClonedProjectUrl, uploadFormData, { headers: formHeaders })
  } catch (error) {
    console.log(error.response ? error.response.data : error)
  }

  if (!Boolean(uploadResult)) throw 'Error while uploading new dataset file'

  console.log('Uploading overwrite file...')
  const uploadResultJobId = uploadResult.data.job
  const uploadJobResult = await waitForJob(uploadResultJobId, JOBS_BASE_URL, API_TOKEN)

  if (!Boolean(uploadJobResult) || jobResult.status === 'FAILURE') throw 'Error while polling upload job'

  
  console.log('For overwritten map')
  let clonedMap = await getFirstMap(BASE_URL, clonedProjectUUID, API_TOKEN)

  // Clear the map's cache so the AOI is correctly updated
  await axios.post(`${clonedMap.purge_cache}?token=${API_TOKEN}`, {})

  // 4. Check new Area of Interest
  clonedMap = await getFirstMap(BASE_URL, clonedProjectUUID, API_TOKEN)
  console.log('Area of Interest:', clonedMap.boundingbox)
  console.log('View:', clonedMap.view)
}

openspatial_demo()