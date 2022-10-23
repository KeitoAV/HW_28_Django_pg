import csv
import json

csv_file_ad = 'ad.csv'
json_file_ad = 'ad.json'
ad_model = 'ads.ad'

csv_file_category = 'category.csv'
json_file_category = 'category.json'
category_model = 'ads.category'

csv_file_location = 'location.csv'
json_file_location = 'location.json'
location_model = 'ads.location'

csv_file_user = 'user.csv'
json_file_user = 'user.json'
user_model = 'users.user'


def csv_to_json(csvFilePath: str, jsonFilePath: str, model_name: str):
    jsonArray = []

    with open(csvFilePath, encoding='utf-8') as csvf:
        csvReader = csv.DictReader(csvf)
        for row in csvReader:
            fixture_dict = {}
            fields_dict = {}
            for key, value in list(row.items())[1:]:
                if key == "is_published":
                    fields_dict[key] = bool(row[key])
                else:
                    fields_dict[key] = row[key]
            fixture_dict["model"] = model_name
            fixture_dict["pk"] = row[list(row.keys())[0]]
            fixture_dict["fields"] = fields_dict

            jsonArray.append(fixture_dict)

    with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
        jsonf.write(json.dumps(jsonArray, indent=4, ensure_ascii=False))


csv_to_json(csv_file_category, json_file_category, category_model)
csv_to_json(csv_file_ad, json_file_ad, ad_model)
csv_to_json(csv_file_location, json_file_location, location_model)
csv_to_json(csv_file_user, json_file_user, user_model)
