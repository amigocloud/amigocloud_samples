# Script to query record_history across all AmigoCloud projects and export results to a CSV
#   Must have AmigoCloud Account
#   All projects must have a record_history dataset (no projects older than 2017)
from amigocloud import AmigoCloud
import csv

# AmigoCloud variables - change based on user
#   token found at www.amigocloud.com/accounts/tokens
#   project owner = user id found in /api/v1/me
amigocloud = AmigoCloud(token='<>')
projectOwner = <>
projectNum = [] * 200
recordNum = [] * 200

# Project variables used to parse through all projects the user has
projects = amigocloud.get('users/%s/projects/' % (projectOwner))
projectsNext = projects['next']

# Project list is offset by 20.  While loop is setup so if user has more than 20 projects it will grab the next set of 20.
while True:
    for project in projects['results']: #parse through projects
        projectNum.append(project['id'])
        projID = project['id']
        datasets = amigocloud.get('users/%s/projects/%s/datasets' % (projectOwner,projID))
        for rh in datasets['results']: #parse throgh datasets
            if rh['name'] == 'record_history': #if the dataset is called record_history append to recordNum list
                recordNum.append(rh['id'])
                projectsNext = projects['next']
    if projectsNext is None:
        break
    projects = amigocloud.get(projectsNext)

# temp list and final list
rows = []
export = []

# for each record_history dataset in each project, set variables, run query, add results to rows, extend export list
for p, d in zip(range(len(projectNum)),range(len(recordNum))):
    # query variables
    rows[:] = []
    offset = 0
    limit = 1000
    sqlURL = '/users/%s/projects/%s/sql' % (projectOwner, projectNum[p])
    datasetURL = '/users/%s/projects/%s/datasets/%s' % (projectOwner, projectNum[p], recordNum[d])
    dataset = amigocloud.get(datasetURL)
    tblName = dataset['table_name']
    query = "SELECT dataset_id, change_date, change_type, who_changed_custom_id, %s AS project_num, %s AS record_history FROM %s WHERE change_date > '2018-9-12' AND change_type ='inserted'" % (projectNum[p], recordNum[d], tblName)
    response = amigocloud.get(dataset['master'])
    master = response['master']

    # While loop count variables
    responseCt = amigocloud.get(sqlURL, {'query': query, 'offset': offset, 'limit': limit, 'state': master,'dataset_id': recordNum[d]})
    rowCt = len(responseCt['data'])
    print('Project: ' + str(projectNum[p]) + ' History: ' + str(recordNum[d]) + ' Row Count: ' + str(rowCt))

    # query data for each record_history dataset and extend to export list
    while len(rows) < rowCt:
            response = amigocloud.get(sqlURL, {'query': query, 'offset': offset, 'limit': limit, 'state': master,'dataset_id': recordNum[d]})
            dataRows = len(response['data'])
            offset += dataRows
            rows += response['data']
            export.extend(rows)

# write export list to CSV, use full path
with open('', 'w') as myFile:
    fieldnames = ['dataset_id', 'change_date', 'change_type', 'who_changed_custom_id', 'project_num', 'record_history']
    writer = csv.DictWriter(myFile, fieldnames=fieldnames, lineterminator = '\n')
    writer.writeheader()
    writer.writerows(export)
