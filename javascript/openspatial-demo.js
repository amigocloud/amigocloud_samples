import fs from 'fs'

import axios from 'axios'
import FormData from 'form-data'
import {waitForJob} from './helpers.js'

// Required constant values
const API_TOKEN = 'A:CzjSMcgMZil54agXnwo2msoNqhQklNGZh6bUyt'
const ORGANIZATION_UUID = '9820f3db-7745-4c46-98ba-8824363e07db'
const PROJECT_UUID = 'acca4d97-7aef-4b0a-a6f5-e060c8e0aabc'
const USER_UUID = '6df02d58-8765-411f-bc82-5ca7e369ed7c'
const FILE_PATH = './Parks.zip'

const BASE_URL = 'http://localhost'
const TOOLS_URL = `${BASE_URL}/api/v2/tools/run?token=${API_TOKEN}`
const JOBS_BASE_URL = `${BASE_URL}/api/v1/me/jobs`
const UPLOAD_URL = `${BASE_URL}/api/v1/projects/${PROJECT_UUID}/datasets/upload?token=${API_TOKEN}`
const MAPS_URL = `${BASE_URL}/api/v1/projects/${PROJECT_UUID}/maps?token=${API_TOKEN}`

const TOOL_INPUT = {
  clone_maps: true,
  project_uuid: PROJECT_UUID,
  user_uuid: USER_UUID
}

const checkAOI = async () => {
  const mapsRaw = await axios.get(MAPS_URL)
  const initialMap = mapsRaw.data.results[0]

  if (!Boolean(initialMap)) throw 'No map found. Create one in the original dataset'

  console.log('Map AOI:', initialMap.boundingbox)
  console.log('Map view:', initialMap.view)
}

const demo = async () => {
  // 1. Clone Project "OpenSpatial Demo"

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

  const jobResult = await waitForJob(cloneJobId, JOBS_BASE_URL, API_TOKEN)

  if (!Boolean(jobResult) || jobResult.status === 'FAILURE') throw 'Error while polling clone job'
  
  // 2. Check initial Area of Interest (Bounding box)

  console.log('For initial map')
  await checkAOI()

  // 3. Upload new data, overwriting the old data

  const uploadFormData = new FormData()
  const newDatasetFile = await fs.promises.readFile(FILE_PATH, 'utf8')

  uploadFormData.append('datafile', newDatasetFile, 'Parks.zip')
  uploadFormData.append('dataset_write_action', 'overwrite')
  uploadFormData.append('csv_props.delimiter', ',')
  uploadFormData.append('csv_props.decimal_separator', '.')
  uploadFormData.append('process_now', 'true')

  console.log('uploadFormData', uploadFormData)

  let uploadResult
  try {
    uploadResult = await axios.post(UPLOAD_URL, uploadFormData)
  } catch (error) {
    console.log(error.response ? error.response.data : error.response)
  }

  if (!Boolean(uploadResult)) throw 'Error while uploading new dataset file'
  

  const uploadResultJobId = uploadResult.data.job_id
  const uploadJobResult = await waitForJob(uploadResultJobId, JOBS_BASE_URL, API_TOKEN)

  if (!Boolean(uploadJobResult) || jobResult.status === 'FAILURE') throw 'Error while polling upload job'

  // 4. Check new Area of Interest
  console.log('For overwritten map')
  await checkAOI()
}

demo()