import json

existing_json_data = []

# 새로운 JSON 파일을 불러와서 파싱
with open('./festival2023/contents/fixtures/boothinfos.json', 'r', encoding='utf-8') as file:
    new_json_data = json.load(file)

# 새로운 JSON 데이터의 형식을 기존 데이터와 통합
for item in new_json_data:
    # 필요한 필드를 추출하고 "model" 및 "fields"를 추가
    booth_data = {
        "model": "contents.booth",
        "fields": {
            "booth_id": item["booth_id"],
            "name": item["name"],
            "category": item["category"],
            "date": item["date"],
            "place": item["place"],
            "introduce": item["introduce"],
            "image": item["image"] + ".png"  # 이미지 파일 이름에 ".png" 추가
        }
    }
    # 통합된 데이터를 기존 JSON 데이터에 추가
    existing_json_data.append(booth_data)

# 새로운 JSON 파일로 저장
with open('./festival2023/contents/fixtures/booth-data.json', 'w', encoding='utf-8') as output_file:
    json.dump(existing_json_data, output_file, ensure_ascii=False, indent=2)

print("새로운 JSON 파일로 저장되었습니다: merged_booth_data.json")
