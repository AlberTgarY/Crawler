predict = {
    "体育": ["体育", "足球", "运动员", "赛跑", "NBA", "比赛", "胜利", "领先", "赛季", "球队", "开局", "巨星", "球星", "退役", "连胜", "失败", "输"],
    "体": ["体育", "足球", "运动员", "赛跑", "NBA", "比赛", "胜利", "领先", "赛季", "球队", "开局", "巨星", "球星", "退役", "连胜", "失败", "输"]
}
for key, list in zip(predict.keys(), predict.values()):
    print(key)
    print(list)
frequency_dict = {"体育": 0, "时政": 0, "军事": 0}
type = max(frequency_dict, key=frequency_dict.get)
print(type)

