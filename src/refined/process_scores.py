from datetime import datetime
from src.refined.helper_process_scores import scoreInstrument, mergeProsocialScores
from src.refined.helper_process_scores import getCleanAnswer


def scoreInstruments(participants: dict, overwrite: bool=False):

    for participant in participants.values():
        submissionsByForm = participant['submissionsByForm']
        for submissions in submissionsByForm.values():
            for submission in submissions:
                # esto va sobreescribiendo en participants, 
                # debido a que no se hace .copy() dentro de la funcion
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


def pivotInstruments(participants: dict):

    for participant in participants.values():

        submissionsByForm = participant['submissionsByForm']
        for submissions in submissionsByForm.values():
            for submission in submissions:
                # esto va sobreescribiendo en participants, 
                # debido a que no se hace .copy() dentro de la funcion
                submission = pivotSubmissionInstruments(submission)

    return participants


def pivotSubmissionInstruments(writableSubmission: dict):

    # writableSubmission = submission.copy()
    writableInstrumentsData = writableSubmission['instrumentsData']
    
    pivotedScores = {}
    pivotedAnswers = {}
    for writableInstrumentData in writableInstrumentsData:
        if "scores" in writableInstrumentData.keys():
          pivotedScores[writableInstrumentData['key']] = writableInstrumentData['scores']

          for answerObjectKey, answerObject in writableInstrumentData['answers'].items():
              clean_answer = getCleanAnswer(answerObject['answer'])
              pivotedAnswers[f"{writableInstrumentData['key']}.{answerObjectKey}"] = clean_answer

    writableSubmission['pivotedScores'] = pivotedScores
    writableSubmission['pivotedAnswers'] = pivotedAnswers

    return writableSubmission


