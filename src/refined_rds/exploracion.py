from src.utils import readJson
from src.config import path_refined

participants = readJson(path_refined)
len(participants)

id_ = list(participants.keys())[1]

# -
participant = participants[id_]
id_

participant.keys()
participant["uuid"]
participant["firstNameA"]
participant["lastNameA"]
participant["documentNumber"]
participant["submissionsByForm"].keys()
len(participant["submissionsByForm"]["240436402972656"])

# -
sub = participant["submissionsByForm"]["240436402972656"][0]
sub.keys()

sub["formId"]
sub["submisionId"]
sub["createdAt"]
sub["applicationData"]
sub["participantData"]
len(sub["instrumentsData"])

i = 1
sub["instrumentsData"][i].keys()
sub["instrumentsData"][i]["name"]
sub["instrumentsData"][i]["answers"].keys()


[x["name"] for x in sub["instrumentsData"]]

sub["jotformSubmission"].keys()
sub["jotformSubmission"]["answers"].keys()
for i in range(62, 100):
    _ = sub["jotformSubmission"]["answers"][str(i)]
    print(_)

sub["jotformSubmission"]["answers"]["109"]


sub["pivotedScores"]

sub["pivotedAnswers"]


# i = 11
# for key_, val in sub["instrumentsData"][i].items():
#     print(key_, "---->", val)

# df_i = pd.DataFrame(sub["instrumentsData"][i])
# df_i = df_i.reset_index()
# df_i = df_i.rename(columns={"index": "key_answerindex"})
# df_i["question_statement"] = [get_item(x, "questionStatement") for x in df_i["answers"]]
# df_i["answer"] = [get_item(x, "answer") for x in df_i["answers"]]

# df_i.head()
# df_i["answers"].iloc[1]

# df_i = df_i.drop(columns=["answers"])
