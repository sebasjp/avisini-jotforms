from src.refined.helper_process_submission import (
    getFormMap, 
    getSectionAnswers, 
    getInstrumentsAnswers,
    measureSimilarity,
    assignParticipantSubmission
)
from src.refined.schema import identitySimilarityMeasure, Participant
from src.config import SIMILARITY_THRESHOLD
import hashlib


def buildParticipantSumbmision(submission: dict):

    # get schema
    formMap = getFormMap(submission)
    
    if 'applicationMap' not in formMap or 'participantMap' not in formMap:
        raise KeyError("Required map keys missing in formMap")    

    applicationData = getSectionAnswers(
        submission = submission,
        map = formMap['applicationMap'],
    )
    if applicationData.get('type') is None:
        applicationData['type'] = 'entrada'
    
    participantData = {
        **getSectionAnswers(
            submission = submission,
            map = formMap['participantMap']
        ),
        'similarityMeasure': identitySimilarityMeasure,
    }
    instrumentsData = getInstrumentsAnswers(
        submission=submission,
        map=formMap['instrumentMaps'],
    )
    participantSubmission = {
        'formId': submission['form_id'],
        'submisionId': submission['id'],
        'createdAt': submission['created_at'],
        'applicationData': applicationData,
        'participantData': participantData,
        'instrumentsData': instrumentsData,
        'jotformSubmission': submission,
    }
    # print("Built participant submission:", participantSubmission)  # Debugging statement

    return participantSubmission


def matchParticipant(participants: dict, participantSubmission: dict):

    matched = False
    if participantSubmission.get('documentNumber') in participants:  # Use get() for safer access
        participant = participants[participantSubmission['documentNumber']]
        similarityMeasure = measureSimilarity(participant, participantSubmission)
        print("participant:", participant, "similarityMeasure:", similarityMeasure)

        if similarityMeasure.avgSimilarity >= float(SIMILARITY_THRESHOLD):
            matched = True
            participant = assignParticipantSubmission(participant, participantSubmission)
    
    if not matched:
        for participant in participants.values():

            similarityMeasure = measureSimilarity(participant, participantSubmission)
            if similarityMeasure.avgSimilarity >= float(SIMILARITY_THRESHOLD):
                matched = True
                participant = assignParticipantSubmission(participant, participantSubmission)

    if not matched:
        newParticipant = Participant(
            uuid=hashlib.md5(participantSubmission["participantData"].get('documentNumber', '').encode()).hexdigest(),  # Safer document number access
            firstNameA=participantSubmission["participantData"].get('firstNameA', ''),  # Handle potential missing keys
            lastNameA=participantSubmission["participantData"].get('lastNameA', ''),  # Handle potential missing keys
            submissionsByForm=participantSubmission.get('submissionsByForm', {}),
            documentNumber=participantSubmission["participantData"].get('documentNumber', ''),  # Handle potential missing keys
        )
        print("Creating new participant:", newParticipant)  # Debugging statement

        if not newParticipant["documentNumber"] or newParticipant["documentNumber"] == 'N/A':
            print("Invalid document number. Skipping participant creation.")  # Debugging statement

        newParticipant["submissionsByForm"] = {participantSubmission['formId']: [participantSubmission]}
        resultParticipant = newParticipant.copy()
    else:
        resultParticipant = participant.copy()
        print(
            "Participant already exists:", 
            {var: val for var, val in resultParticipant.items() if var in ["uuid","firstNameA", "lastNameA", "documentNumber"]}
        )  # Debugging statement
        
    return resultParticipant

