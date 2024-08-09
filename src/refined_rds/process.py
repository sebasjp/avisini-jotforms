from src.utils import readJson
from src.config import path_refined, formId
import pandas as pd
from src.refined_rds.variables_tables import vars_dim_participants

pd.options.display.max_columns=None

participants = readJson(path_refined)
len(participants)

# para cada participant id
id_ = list(participants.keys())[-1]
participant = participants[id_]
id_

def get_item(x, nameitem: str):
    try:
        result = x[nameitem]
    except:
        result = None

    return result
    
sub = participant["submissionsByForm"][formId][0]
len(sub["instrumentsData"])

df_lst = []
for data_dict in sub["instrumentsData"]:

    test_dict = data_dict.copy()
    # print(test_dict.keys())
    if "scores" in test_dict.keys():
        test_dict.pop("scores")
    # print(test_dict.keys())
    # test_dict viene en diccionario lo pasamos a dataframe
    df_i = pd.DataFrame(test_dict)
    df_i = df_i.reset_index()
    df_i = df_i.rename(columns={"index": "key_answerindex"})

    # detalle de la pregunta y respuesta
    df_i["question_statement"] = [get_item(x, "questionStatement") for x in df_i["answers"]]
    df_i["answer"] = [get_item(x, "answer") for x in df_i["answers"]]
    df_i = df_i.drop(columns=["answers"])

    df_lst.append(df_i)

df = pd.concat(df_lst)
df["document_type"] = sub["participantData"]["documentType"]
df["document_number"] = sub["participantData"]["documentNumber"]

df.head(27)
df["key_answerindex"].unique()

# dimension participantes
dim_part = df[df["key_answerindex"].isin(vars_dim_participants)].copy()
dim_part.shape
dim_part.head()
n_ = list(
    dim_part["key_answerindex"]
    .value_counts()
    .value_counts()
    .index
)[0]
if n_!=1:
    print(f"Mas de un registro de una misma pregunta sociodemografica por participante; n = {n_}")

dim_part = dim_part.pivot_table(
    index=["document_type", "document_number"],
    columns=["key_answerindex"],
    values=["answer"],
    aggfunc=lambda x: x.unique()[0]
)
dim_part.columns = [x[1] for x in dim_part.columns]
dim_part = dim_part.reset_index()
dim_part.to_csv("data/ejemplo_dim_participants.csv", sep="|", index=False)
dim_part.T


dim_inst = df[["key_answerindex", "name", "key", "question_statement"]].copy()
dim_inst.shape
dim_inst.head()
dim_inst.to_csv("data/ejemplo_dim_instrumento.csv", sep="|", index=False)


df_hechos = df[["key_answerindex", "answer", "document_type", "document_number"]].copy()
df_hechos = df_hechos[~df_hechos["key_answerindex"].isin(vars_dim_participants)]
df_hechos["key_answerindex"].unique()
df_hechos.shape
df_hechos.to_csv("data/ejemplo_hechos.csv", sep="|", index=False)