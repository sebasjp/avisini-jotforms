from datetime import datetime
from src.refined.helper_process_scores import scoreInstrument, mergeProsocialScores


def scoreInstruments(participants: dict, overwrite: bool=False):

    for participant in participants.values():
        submissionsByForm = participant['submissionsByForm']
        for submissions in submissionsByForm.values():
            for submission in submissions:
                submission['instrumentsData'] = scoreSubmission(submission, overwrite)

    return participants


def scoreSubmission(submission: dict, overwrite: bool):

    writableInstrumentsData = submission['instrumentsData']
    ScoreInstrumentsData = []

    for writableInstrumentData in writableInstrumentsData:
        if writableInstrumentData.get('scores') is not None and not overwrite:
            ScoreInstrumentsData.append(writableInstrumentData)
        else:
            applicationDate = (
                datetime.strptime(submission['applicationData']['date'], '%Y-%m-%d')
                if 'date' in submission['applicationData']
                else datetime.strptime(submission['createdAt'], '%Y-%m-%d %H:%M:%S')
            )
            writableInstrumentData = scoreInstrument({
                'writableInstrumentData': writableInstrumentData, 
                'applicationDate': applicationDate
            })        
            ScoreInstrumentsData.append(writableInstrumentData)

    ScoreInstrumentsData = mergeProsocialScores(ScoreInstrumentsData)

    return ScoreInstrumentsData