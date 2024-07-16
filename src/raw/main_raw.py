from src.raw.fetchSubmissions import fetchSubmissions
from src.utils import saveJson
from src.config import JOTFORM_BASEURL, JOTFORM_KEY, formId, path_raw

# inputs
payload = {
  "JOTFORM_BASEURL": JOTFORM_BASEURL,
  "JOTFORM_KEY": JOTFORM_KEY,
  "formId": formId,
}
submissions = fetchSubmissions(payload)
print(len(submissions))

submissions = submissions[:2]
print(len(submissions))

# save list of json
saveJson(submissions, path_raw)