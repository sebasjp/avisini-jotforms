from src.utils import readJson, saveJson
from src.config import path_raw, path_refined
from src.refined.process_submission import buildParticipantSumbmision, matchParticipant
from src.refined.process_scores import scoreInstruments, pivotInstruments
from src.refined.mark_duplicate import markDuplicateSubmissions


def main():

    submissions = readJson(path_raw)
    print(f"# de submissions a procesar: {len(submissions)}")

    # assignSubmissions
    participants = {}
    for submission in submissions:
        print("Procesando...", submission["answers"]["97"]["name"], submission["answers"]["97"]["answer"])
        participantSubmission = buildParticipantSumbmision(submission)
        documentNumber = participantSubmission['participantData'].get('documentNumber')
        participants[documentNumber] = matchParticipant(participants, participantSubmission)

    print(len(participants.keys()))

    print("ingresando a scoreInstruments")
    participants = scoreInstruments(participants)
    print(len(participants.keys()))

    print("ingresando a pivotInstruments")
    participants = pivotInstruments(participants)
    print(len(participants.keys()))

    print("ingresando a markDuplicateSubmissions")
    markDuplicateSubmissions(participants)

    # save json
    saveJson(participants, path_refined)

    return "Archivo guardado con exito"

main()
# list(participants.values())[0]