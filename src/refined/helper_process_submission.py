from src.refined.schema import JotformMap, SimilarityMeasure
from jaro import jaro_winkler_metric as similarity


def getSectionAnswers(submission: dict, map):

    return followMapAndGetAnswers(
        submission=submission, 
        map=map,
        plain=True
    )


def followMapAndGetAnswers(submission: dict, map, plain: bool=False):
    
    answers = {}

    for key, index in map.items():
        jotformAnswer = submission['answers'].get(str(index))

        if jotformAnswer:
            questionStatement = jotformAnswer['text']
            try:
              answer = jotformAnswer['answer']
            except Exception as e:
              answer = None

            if answer:
                if isinstance(answer, str):
                    answer = answer.lower().strip()

                    if plain:
                        answers[key] = answer
                    else:
                        answers[key] = {
                            'questionStatement': questionStatement,
                            'answer': answer,
                        }
                elif isinstance(answer, dict):
                    answer_index = 1

                    for statement, value in answer.items():
                        questionStatement = statement.lower().strip()
                        answer = value.lower().strip()

                        if plain:
                            answers[key] = answer
                        else:
                            answers[f"{key}_{answer_index}"] = {
                                'questionStatement': questionStatement,
                                'answer': answer,
                            }

                        answer_index += 1

    return answers


def getInstrumentsAnswers(submission: dict, map):

    instrument_data_array = []

    for instrument_map in map:
        answers = followMapAndGetAnswers(
            submission = submission,
            map = instrument_map['questions'],
        )
        instrument_data = {
            'name': instrument_map['name'],
            'key': instrument_map['key'],
            'answers': answers,
        }
        instrument_data_array.append(instrument_data)

    return instrument_data_array


def getFormMap(jotformSubmission: dict):

    formMap = JotformMap.get(jotformSubmission['form_id'], {})  # Retornar {} si no se encuentra
    if not formMap:
        raise ValueError(f"conformsToMap: Form-schema not found: {jotformSubmission['id']}")
    
    return formMap


def measureSimilarity(participant, submission):
    
    firstNameSmilarity = similarity(
        participant["firstNameA"],
        submission["participantData"]["firstNameA"]
    )
    lastNameSmilarity = similarity(
        participant["lastNameA"],
        submission["participantData"]["lastNameA"]
    )
    idDocumentSmilarity = similarity(
        participant["documentNumber"],
        submission["participantData"]["documentNumber"]
    )
    avgSimilarity = (
        firstNameSmilarity + lastNameSmilarity + idDocumentSmilarity
    ) / 3

    return SimilarityMeasure(
        firstNameSmilarity=firstNameSmilarity,
        lastNameSmilarity=lastNameSmilarity,
        idDocumentSmilarity=idDocumentSmilarity,
        avgSimilarity=avgSimilarity
    )


def assignParticipantSubmission(participant, participantSubmission):
    
    participant.submissionsByForm[participantSubmission.formId].append(participantSubmission)

    if len(participant.submissionsByForm[participantSubmission.formId]) > 1:
        participant.submissionsByForm[participantSubmission.formId].sort(
            key=lambda s: s.jotformSubmission.created_at
        )

    return participant