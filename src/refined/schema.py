#INSTRUMNENTS
from typing import NamedTuple, Dict, Optional, Union, List


class InstrumentAnswer(Dict):
    questionStatement: str
    answer: str


class InstrumentMap(Dict):
    name: str
    key: str
    questions: Dict[str, int]


class InstrumentData(Dict):
    name: str
    key: str
    answers: Dict[str, InstrumentAnswer]
    scores: Optional[Dict[str, Union[int, str]]] = None


class ApplicationMap(Dict):
    type: int
    project: Optional[int] = None
    site: Optional[int] = None
    group: Optional[int] = None
    date: Optional[int] = None
    implementer: Optional[int] = None


class ParticipantMap(Dict):
    firstNameA: int
    lastNameA: int
    documentNumber: int
    firstNameB: Optional[int] = None
    lastNameB: Optional[int] = None
    documentType: Optional[int] = None
    type: Optional[int] = None
    ageCat: Optional[int] = None


class ConsentMap(Dict):
    aceptance: int


class FormMap(Dict):
    formId: str
    name: str
    applicationMap: ApplicationMap
    participantMap: ParticipantMap
    instrumentMaps: List[InstrumentMap]
    consentMap: Optional[ConsentMap] = None


class SimilarityMeasure(NamedTuple):
    firstNameSmilarity: float
    lastNameSmilarity: float
    idDocumentSmilarity: float
    avgSimilarity: float


identitySimilarityMeasure = SimilarityMeasure(
    firstNameSmilarity=1,
    lastNameSmilarity=1,
    idDocumentSmilarity=1,
    avgSimilarity=1
)

class JotformAnswer(Dict):
    name: str
    text: str
    type: str
    answer: Union[str, Dict[str, str]]

class JotformSubmission(Dict):
    id: str
    form_id: str
    created_at: str
    answers: Dict[int, JotformAnswer]

class ApplicationData(Dict):
    type: str
    projec: Optional[str] = None
    site: Optional[str] = None
    group: Optional[str] = None
    date: Optional[str] = None
    implementer: Optional[str] = None

class ParticipantData(Dict):
    firstNameA: str
    lastNameA: str
    documentType: str
    documentNumber: str
    firstNameB: Optional[str] = None
    lastNameB: Optional[str] = None
    type: Optional[str] = None
    ageCat: Optional[str] = None
    avgSimilarity: Optional[float] = None
    similarityMeasure: Optional[SimilarityMeasure] = None

class ParticipantSubmission(Dict):
    formId: str
    submisionId: str
    createdAt: str
    applicationData: ApplicationData
    participantData: ParticipantData
    instrumentsData: List[InstrumentData]
    jotformSubmission: JotformSubmission
    pivotedScores: Optional[Dict[str, Dict[str, Union[int, str]]]] = None
    pivotedAnswers: Optional[Dict[str, Dict[str, str]]] = None
    duplicate: Optional[bool] = None

class Participant(Dict):
    uuid: str
    firstNameA: str
    lastNameA: str
    documentNumber: str
    submissionsByForm: Dict[str, List[ParticipantSubmission]]

JotformMap = {
    '240436402972656': FormMap(
        formId='240436402972656',
        name='MEN',
        applicationMap=ApplicationMap(
            type=463,
        ),
        participantMap=ParticipantMap(
            firstNameA=82,
            firstNameB=83,
            lastNameA=84,
            lastNameB=85,
            documentType=96,
            documentNumber=97,
        ),
        instrumentMaps=[
            InstrumentMap(
                name='Consentimiento Informado',
                key='CONSENT',
                questions={
                    'aceptance': 400,
                }
            ),
            InstrumentMap(
                name='Datos sociodemográficos',
                key='DEMOGRAF',
                questions={
                    'birthDate': 62,
                    'sex': 238,
                    'ethnicity': 239,
                    'birthPlaceCountrySelect': 446,
                    'birthPlaceCountryText': 447,
                    'birthPlaceDivision': 241,
                    'birthPlaceCity': 242,
                    'residencePlaceCountrySelect': 455,
                    'residencePlaceCountryText': 456,
                    'residencePlaceDivision': 243,
                    'residencePlaceCity': 244,
                    'socioeconomicStata': 247,
                    'houseLocation': 248,
                    'phoneNumber': 448,
                    'maritalStatus': 249,
                    'naturalDisasterVictim': 252,
                    'warVictim': 253,
                    'registeredVictim': 254,
                    'personWDisability': 256,
                    'disbilityType': 257,
                    'registeredPersonWDisability': 258,
                    'socialSecurityCoverage': 264,
                    'socialSecurityType': 265,
                    'hmo': 266,
                }
            ),
            InstrumentMap(
                name='Whooley',
                key='WHOO',
                questions={
                    'WHOO_1': 269,
                    'WHOO_2': 270,
                }
            ),
            InstrumentMap(
                name='PTSD - PTSC',
                key='PTSD',
                questions={
                    'PTSD_1': 459,
                }
            ),
            InstrumentMap(
                name='Hamilton',
                key='HAMI',
                questions={
                    'HAMI_1': 386,
                }
            ),
            InstrumentMap(
                name='CDRISC',
                key='CDRI',
                questions={
                    'CDRI_1': 279,
                }
            ),
            InstrumentMap(
                name='Prosocial - I',
                key='PRO_A',
                questions={
                    'PRO_A_1': 284,
                }
            ),
            InstrumentMap(
                name='Prosocial - II',
                key='PRO_B',
                questions={
                    'PRO_B_1': 287,
                }
            ),
            InstrumentMap(
                name='Prosocial - III',
                key='PRO_C',
                questions={
                    'PRO_C_1': 289,
                }
            ),
            InstrumentMap(
                name='Compasión',
                key='COMP',
                questions={
                    'COMP_1': 291,
                }
            ),
        ]
    )
}
