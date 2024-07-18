from src.utils import readJson, saveJson
from src.config import path_raw, path_refined
from src.refined.process_submission import buildParticipantSumbmision, matchParticipant
from src.refined.process_scores import scoreInstruments, pivotInstruments


def main():

    submissions = readJson(path_raw)
    print(len(submissions))
    
    participants = {}
    # assignSubmissions
    for submission in submissions:
        participantSubmission = buildParticipantSumbmision(submission)
        documentNumber = participantSubmission['participantData'].get('documentNumber')
        participants[documentNumber] = matchParticipant(participants, participantSubmission)

    print("ingresando a scoreInstruments")
    participants = scoreInstruments(participants=participants)

    print("ingresando a pivotInstruments")
    participants = pivotInstruments(participants)

    # save json
    saveJson(participants, path_refined)