import requests


def fetchSubmissions(payload: dict):
    
  JOTFORM_BASEURL = payload['JOTFORM_BASEURL']
  JOTFORM_KEY = payload['JOTFORM_KEY']
  formId = payload['formId']
  limit = payload.get('limit', 1000)

  url = f"{JOTFORM_BASEURL}/form/{formId}/submissions"

  try:
    response = requests.get(url, params={'apiKey': JOTFORM_KEY, 'limit': limit})
    response.raise_for_status()
  except requests.RequestException as e:
    print(f"Error fetching submission fetchSubmissions: {e}") #debug
    raise RuntimeError(f"Error fetching submissions: {e}")

  submissions = []

  for element in response.json()['content']:
    submissions.append({
        'id': element['id'],
        'form_id': element['form_id'],
        'created_at': element['created_at'],
        'answers': element['answers'],
    })

  return submissions
