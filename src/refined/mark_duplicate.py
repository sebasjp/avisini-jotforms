from datetime import datetime
from src.config import formId


def markDuplicateSubmissions(participants: dict):

    lowerLimitDate = datetime.strptime('01-01-2024 00:00:00', '%m-%d-%Y %H:%M:%S')
    upperLimitDate = datetime.strptime('12-31-2024 00:00:00', '%m-%d-%Y %H:%M:%S')
    
    formSubmissionsByType = {}

    for participant in participants.values():
        formSubmissions = participant["submissionsByForm"].get(formId, [])

        for submission in formSubmissions:
            # print(submission.keys())
            # print("antes del if", submission["applicationData"]["type"])        
            if submission["applicationData"]["type"] not in formSubmissionsByType:
                formSubmissionsByType[submission["applicationData"]["type"]] = []            
            formSubmissionsByType[submission["applicationData"]["type"]].append(submission)

        for submissions in formSubmissionsByType.values():
            if len(submissions) >= 2:
                submissionsInDateInterval = [
                    s for s in submissions
                    if lowerLimitDate <= datetime.strptime(s["createdAt"], "%Y-%m-%d %H:%M:%S") <= upperLimitDate
                ]
                submissionsInDateInterval.sort(key=lambda s: s["createdAt"])
                for i in range(len(submissionsInDateInterval)-1):
                    submissionsInDateInterval[i]["duplicate"] = True
