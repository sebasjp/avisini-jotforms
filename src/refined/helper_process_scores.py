from datetime import datetime
from dateutil.relativedelta import relativedelta
from html2text import html2text as convert
from unidecode import unidecode
import re


def getCleanAnswer(answer: str) -> str:
    return unidecode(convert(answer).replace('\n', ' ').strip().lower())


def getAnswerValue(payload: dict):
    caller = payload['caller']
    valueDictionary = payload['valueDictionary']
    answer = payload['answer']

    cleanAnswer = getCleanAnswer(answer)
    value = valueDictionary.get(cleanAnswer)

    if value is None:
        raise ValueError(f"{caller}: Unrecognized answer: {answer}")

    return value


def scoreDEMOGRAF(payload: dict):
    
    answers = payload['writableInstrumentData']['answers']
    applicationDate = payload['applicationDate']

    if answers=={}:
        # si no hay respuestas
        print("WARNING: scoreDEMOGRAF is empty")
        result = {
            'ageInYears': None,
            'ageOrdinal': None,
            'ageCategorical': None,
        }
    else:
        birthYear = str(answers['birthDate_3']['answer'])
        birthMonth = str(answers['birthDate_2']['answer'])
        birthDay = str(answers['birthDate_1']['answer'])

        birthMoment = datetime.strptime(f"{birthYear}-{birthMonth}-{birthDay}", "%Y-%m-%d")
        ageInYears = relativedelta(applicationDate, birthMoment).years

        if ageInYears < 0:
            raise ValueError(f"scoreDEMOGRAF: Negative age: {ageInYears}")

        ageCategories = {
            1: 'Primera Infancia',
            2: 'Infancia',
            3: 'Adolescencia',
            4: 'Juventud',
            5: 'Adultez',
            6: 'Persona Mayor',
        }

        ageOrdinal = 0

        if 0 <= ageInYears <= 5:
            ageOrdinal = 1
        elif 6 <= ageInYears <= 11:
            ageOrdinal = 2
        elif 12 <= ageInYears <= 18:
            ageOrdinal = 3
        elif 19 <= ageInYears <= 26:
            ageOrdinal = 4
        elif 27 <= ageInYears <= 59:
            ageOrdinal = 5
        elif ageInYears >= 60:
            ageOrdinal = 6

        result = {
            'ageInYears': ageInYears,
            'ageOrdinal': ageOrdinal,
            'ageCategorical': ageCategories[ageOrdinal],
        }

    return result


def scoreWhooley(payload: dict):

    answers = payload['writableInstrumentData']['answers']
    answerValues = {
        'no': 0,
        'si': 1,
    }
    numericScore = 0

    for answerObject in answers.values():
        numericScore += getAnswerValue({
            'caller': 'scoreWhooley',
            'valueDictionary': answerValues,
            'answer': answerObject['answer'],
        })
    categoricScore = 'positivo' if numericScore > 0 else 'negativo'

    return {
        'numericScore': numericScore,
        'categoricScore': categoricScore,
    }


def scorePTSD(payload: dict):

    answers = payload['writableInstrumentData']['answers']
    answerValues = {
        'para nada': 1,
        'un poco': 2,
        'mas o menos': 3,
        'bastante': 4,
        'extremadamente': 5,
    }
    numericScore = 0

    for answerObject in answers.values():
        numericScore += getAnswerValue({
            'caller': 'scorePTSD',
            'valueDictionary': answerValues,
            'answer': answerObject['answer'],
        })
    categoricScore = 'positivo' if numericScore >= 30 else 'negativo'

    return {
        'numericScore': numericScore,
        'categoricScore': categoricScore,
    }


def scoreHamilton(payload: dict):
    
    answers = payload['writableInstrumentData']['answers']
    answerValues = {
        'ausente': 0,
        'leve': 1,
        'moderado': 2,
        'grave': 3,
        'muy grave / incapacitante': 4,
    }
    questions = {
        'estado de ánimo ansioso. preocupaciones, anticipación de lo peor, aprensión (anticipación temerosa), irritabilidad.': 'ansiedad psíquica',
        'tensión. sensación de tensión, imposibilidad de relajarse, reacciones con sobresalto, llanto fácil, temblores, sensación de inquietud.': 'ansiedad psíquica',
        'temores. a la oscuridad, a los desconocidos, a quedarse solo, a los animales grandes, al tráfico, a las multitudes.': 'ansiedad psíquica',
        'insomnio. dificultad para dormirse, sueño interrumpido, sueño insatisfactorio y cansancio al despertar.': 'ansiedad psíquica',
        'intelectual (cognitivo). dificultad para concentrarse, mala memoria.': 'ansiedad psíquica',
        'estado de ánimo deprimido. pérdida de interés, insatisfacción en las diversiones, depresión, despertar prematuro, cambios de humor durante el día.': 'ansiedad psíquica',
        'comportamiento en la entrevista (general y fisiológico)tenso, no relajado, agitación nerviosa: manos, dedos cogidos, apretados, tics, enrollar un pañuelo; inquietud; pasearse de un lado a otro, temblor de manos, ceño fruncido, cara tirante, aumento del tono muscular, suspiros, palidez facial. tragar saliva, eructar, taquicardia de reposo, frecuencia respiratoria por encima de 20 res/min, sacudidas enérgicas de tendones, temblor, pupilas dilatadas, exoftalmos (proyección anormal del globo del ojo), sudor, tics en los párpados.': 'ansiedad psíquica',
        'síntomas somáticos generales (musculares). dolores y molestias musculares, rigidez muscular, contracciones musculares, sacudidas clónicas, crujir de dientes, voz temblorosa.': 'ansiedad somática',
        'síntomas somáticos generales (sensoriales) zumbidos de oídos, visión borrosa, sofocos y escalofríos, sensación de debilidad, sensación de hormigueo.': 'ansiedad somática',
        'síntomas cardiovasculares. taquicardia, palpitaciones, dolor en el pecho, latidos vasculares, sensación de desmayo, extrasístole.': 'ansiedad somática',
        'síntomas respiratorios. opresión o constricción en el pecho, sensación de ahogo, suspiros, disnea.': 'ansiedad somática',
        'síntomas gastrointestinales. dificultad para tragar, gases, dispepsia: dolor antes y después de comer, sensación de ardor, sensación de estómago lleno, vómitos acuosos, vómitos, sensación de estómago vacío, digestión lenta, borborigmos (ruido intestinal), diarrea, pérdida de peso, estreñimiento.': 'ansiedad somática',
        'síntomas genitourinarios. micción frecuente, micción urgente, amenorrea, menorragia, aparición de la frigidez, eyaculación precoz, ausencia de erección, impotencia.': 'ansiedad somática',
        'síntomas autónomos. boca seca, rubor, palidez, tendencia a sudar, vértigos, cefaleas de tensión, piloerección (pelos de punta).': 'ansiedad somática',
    }
    ansiedadPsiquicaScore = 0
    ansiedadSomaticaScore = 0
    totalNumericScore = 0

    for answerObject in answers.values():
        value = getAnswerValue({
            'caller': 'scoreHamilton',
            'valueDictionary': answerValues,
            'answer': answerObject['answer'],
        })

        questionStatement = answerObject['questionStatement']
        questionStatement = re.sub(' +',' ', questionStatement)
        if questionStatement not in questions:
            raise ValueError(f"scoreHamilton: Unrecognized question: {questionStatement}")

        subscale = questions[questionStatement]

        if subscale == 'ansiedad psíquica':
            ansiedadPsiquicaScore += value
        elif subscale == 'ansiedad somática':
            ansiedadSomaticaScore += value

        totalNumericScore += value

    scoreCategories = {
        1: 'leve',
        2: 'leve a moderada',
        3: 'moderada a severa',
        4: 'muy severa',
    }

    totalOrdinalScore = 0

    if 0 <= totalNumericScore <= 17:
        totalOrdinalScore = 1
    elif 18 <= totalNumericScore <= 24:
        totalOrdinalScore = 2
    elif 25 <= totalNumericScore <= 30:
        totalOrdinalScore = 3
    elif 31 <= totalNumericScore <= 56:
        totalOrdinalScore = 4

    return {
        'ansiedadPsiquicaScore': ansiedadPsiquicaScore,
        'ansiedadSomaticaScore': ansiedadSomaticaScore,
        'totalNumericScore': totalNumericScore,
        'totalOrdinalScore': totalOrdinalScore,
        'totalCategoricScore': scoreCategories[totalOrdinalScore],
    }


def scoreCDRISC(payload: dict):

    answers = payload['writableInstrumentData']['answers']
    answerValues = {
        'totalmente en desacuerdo': 0,
        'en desacuerdo': 1,
        'ni en acuerdo ni en desacuerdo': 2,
        'de acuerdo': 3,
        'totalmente de acuerdo': 4,
    }
    numericScore = 0

    for answerObject in answers.values():
        numericScore += getAnswerValue({
            'caller': 'scoreCDRISC',
            'valueDictionary': answerValues,
            'answer': answerObject['answer'],
        })

    return {
        'numericScore': numericScore,
    }


def scorePRO_A_B(payload: dict):

    answers = payload['writableInstrumentData']['answers']
    answerValues = {
        'f': {
            'totalmente en desacuerdo': 1,
            'en desacuerdo': 2,
            'ni en acuerdo ni en desacuerdo': 3,
            'de acuerdo': 4,
            'totalmente de acuerdo': 5,
        },
        'r': {
            'totalmente en desacuerdo': 5,
            'en desacuerdo': 4,
            'ni en acuerdo ni en desacuerdo': 3,
            'de acuerdo': 2,
            'totalmente de acuerdo': 1,
        },
    }
    questions = {
        'si una persona se porta de manera grosera conmigo, sentiría pocas ganas de tratarlo bien.': {'direction': 'r', 'subscale': 'responsabilidad social'},
        'me molestaría menos botar basura en un parque sucio que en uno limpio.': {'direction': 'r', 'subscale': 'responsabilidad social'},
        'no existe ninguna excusa para aprovecharnos de una persona sin importar lo que nos haya hecho.': {'direction': 'f', 'subscale': 'responsabilidad social'},
        'la persona que se copia en un examen no debería sentirse culpable porque muchas personas lo hacen.': {'direction': 'r', 'subscale': 'responsabilidad social'},
        'en caso de sentirme enfermo, no debo preocuparme por la forma en la que trato a las otras personas.': {'direction': 'r', 'subscale': 'responsabilidad social'},
        'en caso de dañar una máquina por darle un mal uso, me sentiría menos culpable si esta estuviera dañada antes de que yo la usara. (resulta que usted sabe que la licuadora está medio dañada, y usted necesita usarla. después de usarla termina de dañarla. teniendo en cuenta que ya estaba medio dañada, ¿considera que realmente no tiene de que sentirse culpable?).': {'direction': 'r', 'subscale': 'responsabilidad social'},
        'cuando tengo que realizar una actividad, es imposible que yo esté pendiente de que todas las personas que participan en esta estén bien.': {'direction': 'r', 'subscale': 'responsabilidad social'},

        'a veces me parece difícil ver las cosas desde el punto de vista las otras personas.': {'direction': 'r', 'subscale': 'toma de perspectiva'},
        'siento que debo proteger a una persona de quien se están aprovechando.': {'direction': 'f', 'subscale': 'preocupación empática'},
        'a veces intento entender mejor a mis amigos imaginando las cosas desde su punto de vista': {'direction': 'f', 'subscale': 'toma de perspectiva'},
        'las desgracias de las otras personas no me preocupan mucho.': {'direction': 'r', 'subscale': 'preocupación empática'},
        'si tengo la razón sobre algo, no pierdo mucho tiempo escuchando los argumentos de las otras personas.': {'direction': 'r', 'subscale': 'toma de perspectiva'},
        'a veces no siento mucha compasión hacia una persona que está siendo tratada de manera injusta.': {'direction': 'r', 'subscale': 'preocupación empática'},
        'usualmente sé manejar una situación de emergencia.': {'direction': 'r', 'subscale': 'angustia personal'},
        'por lo general me afectan mucho las cosas que pasan a mi alrededor.': {'direction': 'f', 'subscale': 'preocupación empática'},
        'creo que hay varios puntos de vista para cualquier situación e intento tener todos en cuenta.': {'direction': 'f', 'subscale': 'toma de perspectiva'},
        'tiendo a perder el control durante una emergencia.': {'direction': 'f', 'subscale': 'angustia personal'},
        'cuando estoy molesto con una persona, trato de "ponerme en sus zapatos" por un rato.': {'direction': 'f', 'subscale': 'toma de perspectiva'},
        'cuando veo que alguien necesita ayuda durante una emergencia, hago lo que esté a mi alcance para ayudarle.': {'direction': 'f', 'subscale': 'angustia personal'},
        'a la hora de tomar una decisión, me fijo en lo que necesitan las otras personas.': {'direction': 'f', 'subscale': 'razonamiento moral orientado al otro'},
        'por lo general tomo decisiones justas y equitativas.': {'direction': 'f', 'subscale': 'razonamiento moral de las preocupaciones mutuas'},
        'cuando tengo más de una alternativa (opción), selecciono la que más tiene en cuenta las necesidades de todas las personas.': {'direction': 'f', 'subscale': 'razonamiento moral de las preocupaciones mutuas'},
        'selecciono la opción que más beneficia a las otras personas, por encima de otras que podrían generar un mayor beneficio para mí.': {'direction': 'f', 'subscale': 'razonamiento moral orientado al otro'},
        'selecciono la opción que considera los derechos de todas las personas involucradas.': {'direction': 'f', 'subscale': 'razonamiento moral de las preocupaciones mutuas'},
        'por lo general, mis decisiones están basadas en mi preocupación por el bienestar de las otras personas, por encima de mi propio bienestar.': {'direction': 'f', 'subscale': 'razonamiento moral orientado al otro'},
    }
    preocupacionEmpaticaScore = 0
    responsabilidadSocialScore = 0
    razonamientoMoralOtroScore = 0
    tomaPerspectivaScore = 0
    razonamientoMoralPreocupacionesMutuasScore = 0
    angustiaPersonalScore = 0
    totalNumericScore = 0

    for answerObject in answers.values():
        questionStatement = answerObject['questionStatement']
        questionStatement = re.sub(' +',' ', questionStatement)
        if questionStatement not in questions:
            raise ValueError(f"scorePRO_A_B: Unrecognized question: {questionStatement}")

        questionMetadata = questions[questionStatement]

        value = getAnswerValue({
            'caller': 'scorePRO_A_B',
            'valueDictionary': answerValues[questionMetadata['direction']],
            'answer': answerObject['answer'],
        })

        totalNumericScore += value

        subscale = questionMetadata['subscale']

        if subscale == 'angustia personal':
            angustiaPersonalScore += value
        elif subscale == 'preocupación empática':
            preocupacionEmpaticaScore += value
        elif subscale == 'razonamiento moral de las preocupaciones mutuas':
            razonamientoMoralPreocupacionesMutuasScore += value
        elif subscale == 'razonamiento moral orientado al otro':
            razonamientoMoralOtroScore += value
        elif subscale == 'responsabilidad social':
            responsabilidadSocialScore += value
        elif subscale == 'toma de perspectiva':
            tomaPerspectivaScore += value

    return {
        'totalNumericScore': totalNumericScore,
        'preocupacionEmpaticaScore': preocupacionEmpaticaScore,
        'responsabilidadSocialScore': responsabilidadSocialScore,
        'razonamientoMoralOtroScore': razonamientoMoralOtroScore,
        'tomaPerspectivaScore': tomaPerspectivaScore,
        'razonamientoMoralPreocupacionesMutuasScore': razonamientoMoralPreocupacionesMutuasScore,
        'angustiaPersonalScore': angustiaPersonalScore,
    }


def scorePRO_C(payload: dict):

    answers = payload['writableInstrumentData']['answers']
    answerValues = {
        'nunca': 1,
        'una vez': 2,
        'mas de una vez': 3,
        'seguido': 4,
        'muy seguido': 5,
    }
    altruismoAutoreportadoScore = 0
    totalNumericScore = 0

    for answerObject in answers.values():
        answer = answerObject['answer']
        answer = answer.replace("<br>", " ")
        answer = re.sub(' +',' ', answer)
        value = getAnswerValue({
            'caller': 'scorePRO_C',
            'valueDictionary': answerValues,
            'answer': answer,
        })
        altruismoAutoreportadoScore += value
        totalNumericScore += value

    return {
        'totalNumericScore': totalNumericScore,
        'altruismoAutoreportadoScore': altruismoAutoreportadoScore,
    }


def scoreCOMP(payload: dict):
    
    answers = payload['writableInstrumentData']['answers']
    answerValues = {
        'nunca': 1,
        'casi nunca': 2,
        'a veces': 3,
        'casi siempre': 4,
        'siempre': 5,
    }
    questions = {
        'cuando veo que alguien está pasando un momento difícil le pregunto si puedo ayudarlo(a).': 'motivacion aliviar sufrimiento',
        'si veo a alguien pasando un momento difícil, trato de ayudar a esa persona.': 'motivacion aliviar sufrimiento',
        'cuando alguien está sufriendo suelo ser el primero en intervenir y ayudar.': 'motivacion aliviar sufrimiento',
        'cuando otros sienten tristeza, trato de confortarlos.': 'motivacion aliviar sufrimiento',
        'cuando veo que una persona se siente sola siento deseos de ofrecerle mi compañía.': 'motivacion aliviar sufrimiento',
        'procuro cuidar de las personas.': 'motivacion aliviar sufrimiento',
        'cuando me doy cuenta que alguien se siente mal le ofrezco mi ayuda sin dudarlo.': 'motivacion aliviar sufrimiento',
        'si veo que alguien necesita un consejo, trato de decirle algo que le ayude.': 'motivacion aliviar sufrimiento',
        'dedico parte de mi tiempo libre a ayudar a los demás.': 'motivacion aliviar sufrimiento',
        'si alguien necesita ayuda económica se la proporciono si tengo la posibilidad.': 'motivacion aliviar sufrimiento',

        'siento gran tristeza cuando veo a personas sin hogar.': 'reacción afectiva sufrimiento',
        'me duele la pobreza en el mundo.': 'reacción afectiva sufrimiento',
        'me entristece el sufrimiento de los seres humanos.': 'reacción afectiva sufrimiento',
        'siento gran pena por las personas que no tienen que comer.': 'reacción afectiva sufrimiento',

        'cuando veo a un animal sufriendo maltrato siento deseos de protegerlo.': 'compasion animales',
        'si veo a un animal en peligro trato de ayudarlo.': 'compasion animales',
        'procuro cuidar de los animales.': 'compasion animales',
    }
    totalNumericScore = 0
    motivacionAliviarSufrimiento = 0
    reaccionAfectivaSufrimiento = 0
    compasionAnimales = 0

    for answerObject in answers.values():
        answer = answerObject['answer']
        answer = answer.replace("<br>", " ")
        answer = re.sub(' +',' ', answer)
        value = getAnswerValue({
            'caller': 'scoreCOMP',
            'valueDictionary': answerValues,
            'answer': answer,
        })

        questionStatement = answerObject['questionStatement']
        questionStatement = re.sub(' +',' ', questionStatement)
        if questionStatement not in questions:
            raise ValueError(f"scoreCOMP: Unrecognized question: {questionStatement}")

        subscale = questions[questionStatement]

        if subscale == 'motivacion aliviar sufrimiento':
            motivacionAliviarSufrimiento += value
        elif subscale == 'reacción afectiva sufrimiento':
            reaccionAfectivaSufrimiento += value
        elif subscale == 'compasion animales':
            compasionAnimales += value

        totalNumericScore += value

    return {
        'totalNumericScore': totalNumericScore,
        'motivacionAliviarSufrimiento': motivacionAliviarSufrimiento,
        'reaccionAfectivaSufrimiento': reaccionAfectivaSufrimiento,
        'compasionAnimales': compasionAnimales,
    }


def scoreInstrument(payload: dict):

    writableInstrumentData = payload['writableInstrumentData'].copy()
    applicationDate = payload['applicationDate']
    instrumentKey = writableInstrumentData['key']
    
    scoringFunctions = {
        "DEMOGRAF": scoreDEMOGRAF,
        "WHOO": scoreWhooley,
        "PTSD": scorePTSD,
        "HAMI": scoreHamilton,
        "CDRI": scoreCDRISC,
        "PRO_A": scorePRO_A_B,
        "PRO_B": scorePRO_A_B,
        "PRO_C": scorePRO_C,
        "COMP": scoreCOMP,
    }
    if instrumentKey in scoringFunctions:
        scores = scoringFunctions[instrumentKey]({
            'writableInstrumentData': writableInstrumentData,
            'applicationDate': applicationDate,
        })

        writableInstrumentData['scores'] = scores

    return writableInstrumentData


def getInstrumentDataByKey(instrumentsData: dict, key: str):
    return next((item for item in instrumentsData if item['key'] == key), None)


def mergeProsocialScores(ScoreInstrumentsData: dict):

    writableInstrumentsData = ScoreInstrumentsData.copy()
    instrumentKeys = [instrumentData['key'] for instrumentData in writableInstrumentsData]
    wholeBattery = (
        'PRO_A' in instrumentKeys and 
        'PRO_B' in instrumentKeys and 
        'PRO_C' in instrumentKeys
    )
    if wholeBattery:
        proA = getInstrumentDataByKey(
            instrumentsData=writableInstrumentsData,
            key='PRO_A',
        )
        proB = getInstrumentDataByKey(
            instrumentsData=writableInstrumentsData,
            key='PRO_B',
        )
        proC = getInstrumentDataByKey(
            instrumentsData=writableInstrumentsData,
            key='PRO_C'
        )
        proAScores = proA['scores']
        proBScores = proB['scores']
        proCScores = proC['scores']

        # if proAScores is None or proBScores is None or proCScores is None:
        #     return

        mergedAScores = {
            'preocupacionEmpaticaScore': proAScores['preocupacionEmpaticaScore'],
            'responsabilidadSocialScore': proAScores['responsabilidadSocialScore'],
            'tomaPerspectivaScore': proAScores['tomaPerspectivaScore'],
            'angustiaPersonalScore': proAScores['angustiaPersonalScore'],
        }
        mergedBScores = {
            'razonamientoMoralOtroScore': proBScores['razonamientoMoralOtroScore'],
            'razonamientoMoralPreocupacionesMutuasScore': proBScores['razonamientoMoralPreocupacionesMutuasScore'],
        }
        mergedCScores = {
            'altruismoAutoreportadoScore': proCScores['altruismoAutoreportadoScore'],
        }
        empatiaOtros = (
            mergedAScores['preocupacionEmpaticaScore']
            + mergedAScores['responsabilidadSocialScore']
            + mergedAScores['tomaPerspectivaScore']
            + mergedBScores['razonamientoMoralOtroScore']
            + mergedBScores['razonamientoMoralPreocupacionesMutuasScore']
        )
        tendenciaAyudar = (
            18 - mergedAScores['angustiaPersonalScore'] + mergedCScores['altruismoAutoreportadoScore']
        )
        totalNumericScore = (
            proAScores['totalNumericScore']
            + proBScores['totalNumericScore']
            + proCScores['totalNumericScore']
        )
        mergedScores = {
            **mergedAScores,
            **mergedBScores,
            **mergedCScores,
            'empatiaOtros': empatiaOtros,
            'tendenciaAyudar': tendenciaAyudar,
            'totalNumericScore': totalNumericScore,
        }
        mergedAnswers = {
            **proA['answers'],
            **proB['answers'],
            **proC['answers'],
        }
        writableInstrumentsData.append({
            'name': 'Prosocial',
            'key': 'PRO',
            'answers': mergedAnswers,
            'scores': mergedScores,
        })
    
    return writableInstrumentsData
