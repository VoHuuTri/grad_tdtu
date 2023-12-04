import json


# # use to delete the long text in the sample_data.jsonl

# with open("sample_data.jsonl", "r") as f:
#     lines = f.readlines()
# for line in lines:
#     if len(line) < 20000:
#         with open("to_long.jsonl", "a", encoding="utf-8") as f:
#             f.write(line)

# # find none tag in the sample_data.jsonl
# with open("to_long.jsonl", "r") as f:
#     lines = f.readlines()

# with open("none_tag.jsonl", "a", encoding="utf-8") as f:
#     for line in lines:
#         json_data = json.loads(line)
#         if json_data["meta_data"]["tag"] == None or json_data["meta_data"]["tag"] == '':
#             json.dump(json_data, f, ensure_ascii=False)
#             f.write("\n")

with open("sample_data.jsonl", "r") as f:
    lines = f.readlines()

# for line in lines:
#     json_data = json.loads(line)
#     if json_data["meta_data"]["tag"] == None or json_data["meta_data"]["tag"] == '' or "tháng" in json_data["meta_data"]["time"] or "năm" in json_data["meta_data"]["time"]:
#         with open("wrong_time.jsonl", "a", encoding="utf-8") as f:
#             json.dump(json_data, f, ensure_ascii=False)
#             f.write("\n")

for line in lines:
    json_data = json.loads(line)
    if "Thông tư" in json_data["meta_data"]["tag"] :
        # print(json_data["data"])

        with open("thong_tu.jsonl", "a", encoding="utf-8") as f:
            json.dump(json_data, f, ensure_ascii=False)
            f.write("\n")