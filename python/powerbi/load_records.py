import sys
import os
import argparse
import logging
from amigocloud import AmigoCloud
import uuid
import json 
import time
import pandas as pd

amigocloud = AmigoCloud(token='<YOUR API TOKEN>')

def get_data_frame( amigocloud: AmigoCloud, project: str, dataset: str) -> pd.DataFrame:

    dataset_rows = amigocloud.get_cursor(
        'https://app.amigocloud.com/api/v1/projects/{project_id}/sql'.format(project_id=project),
        {
            'query': 'select * from dataset_{dataset_id}'.format(dataset_id=dataset)
        })

    columns = []
    data = []

    for column in dataset_rows.get('columns'):
        columns.append(column['name'])


    for row in dataset_rows:
        row_data = []
        for key, value in row.items(): 
            row_data.append(value)
        data.append(row_data)

    df = pd.DataFrame(data, columns=columns )

    return df

df = get_data_frame( amigocloud, "<YOUR PROJECT ID>", "<YOUR DATASET ID>" )


