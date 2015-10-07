import time

from amigocloud import AmigoCloud

# Use amigocloud version 1.0.5 or higher to login with tokens
# This will raise an AmigoCloudError if the token is invalid or has expired
ac = AmigoCloud(token='<your_token>')

# For examples of how to get these values, see simple_example2.py
PROJECT_OWNER = 1
PROJECT_ID = 2
DATASET_ID = 3

# From which state to which state do you wanna revert? (the changesets will be
# reverted in reversed order)
FROM_STATE = '...'
TO_STATE = '...'

# Get dataset information
dataset_url = (
    '/users/{user_id}/projects/{project_id}/datasets/{dataset_id}'.format(
        user_id=PROJECT_OWNER, project_id=PROJECT_ID, dataset_id=DATASET_ID
    )
)
dataset = ac.get(dataset_url)

# Get list of all the states between FROM_STATE and TO_STATE
result = ac.get(dataset['states'], {'from': FROM_STATE, 'to': TO_STATE})
states = result['states']

# Revert the states in reverted order
for state in reversed(states):
    revert_state_url = dataset_url + '/revert/{state}'.format(state=state)
    result = ac.post(revert_state_url)  # Send revert
    job = result['job']
    # Request AmigoCloud every second to check if the async job finished
    while True:
        result = ac.get('me/jobs/{job}'.format(job=job))
        if result['status'] not in ('PENDING', 'STARTED'):
            break
        time.sleep(1)  # Sleep 1s
    print 'Reverting state "{state}" finished with status: {status}'.format(
        state=state, status=result.get('status', None)
    )
