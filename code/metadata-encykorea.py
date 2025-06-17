import json
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt


def fix_double_underscore(data):
    """metadata.id 내 __를 _로 치환"""
    def fix(item):
        if "metadata" in item and "id" in item["metadata"]:
            item["metadata"]["id"] = item["metadata"]["id"].replace("__", "_")
    if isinstance(data, list):
        for item in data:
            fix(item)
    else:
        fix(data)
    return data


def count_duplicate_contents(data):
    contents = [item.get("content", "").strip() for item in data]
    content_counts = Counter(contents)
    duplicate_contents = {k: v for k, v in content_counts.items() if v > 1}

    print(f"📦 전체 항목 수: {len(contents)}")
    print(f"📑 고유 content 수: {len(content_counts)}")
    print(f"🔁 중복된 content 수 (2개 이상 등장): {len(duplicate_contents)}")
    print(f"🧮 중복 항목의 총 건수: {sum(duplicate_contents.values())}")
    print(f"📊 중복 비율: {sum(duplicate_contents.values()) / len(contents) * 100:.2f}%")

    print("\n📌 가장 많이 중복된 content Top 10:")
    for content, count in content_counts.most_common(10):
        if count > 1:
            print(f"- {count}회: {content[:50]}{'...' if len(content) > 50 else ''}")


def merge_by_content(data):
    merged = {}
    for item in data:
        key = item['content']
        meta = item.get("metadata", {})

        if key not in merged:
            merged[key] = {
                "content": key,
                "url": item.get("url", ""),
                "metadata": {
                    "id": meta.get("id", ""),
                    "keyword": meta.get("keyword", ""),
                    "title": meta.get("title", ""),
                    "source": meta.get("source", ""),
                    "내용": meta.get("내용", {})
                }
            }
        else:
            existing_meta = merged[key]["metadata"]
            for field in ["id", "keyword"]:
                old_vals = existing_meta.get(field, "").split(",")
                new_vals = meta.get(field, "").split(",")
                merged_vals = set(v.strip() for v in old_vals + new_vals if v.strip())
                existing_meta[field] = ", ".join(sorted(merged_vals))

            if meta.get("title", "").strip() not in existing_meta["title"]:
                existing_meta["title"] += " | " + meta["title"].strip()

    return list(merged.values())


def remove_fields(data, fields_to_remove):
    for item in data:
        내용 = item.get("metadata", {}).get("내용", {})
        if isinstance(내용, dict):
            for key in fields_to_remove:
                내용.pop(key, None)
    return data


def merge_내용_into_content(data):
    for item in data:
        meta = item.get("metadata", {})
        original_content = item.get("content", "").strip()
        meta["title2"] = original_content
        내용 = meta.pop("내용", None)

        if 내용 and isinstance(내용, dict):
            merged_text = "\n\n" + "\n".join(f"■ {k}\n{v}" for k, v in 내용.items())
            item["content"] = original_content + merged_text
        else:
            item["content"] = original_content
    return data


def remove_url_fields(obj):
    """딕셔너리 또는 리스트 내부의 모든 url 키 제거 (재귀)"""
    if isinstance(obj, dict):
        obj.pop("url", None)
        for value in obj.values():
            remove_url_fields(value)
    elif isinstance(obj, list):
        for item in obj:
            remove_url_fields(item)


def analyze_content_lengths(data):
    lengths = [len(item.get("content", "")) for item in data]
    print("📊 content 길이 통계:")
    print(f"총 문서 수       : {len(lengths)}")
    print(f"최소 길이        : {np.min(lengths)}")
    print(f"최대 길이        : {np.max(lengths)}")
    print(f"평균 길이        : {np.mean(lengths):.2f}")
    print(f"중앙값 (median)  : {np.median(lengths)}")
    print(f"표준편차 (std)   : {np.std(lengths):.2f}")

    plt.hist(lengths, bins=50, color="skyblue", edgecolor="black")
    plt.title("Distribution of Content Lengths")
    plt.xlabel("Content Length (characters)")
    plt.ylabel("Number of Items")
    plt.grid(True)
    plt.show()

    # 80000자 이상 필터링
    long_contents = [item for item in data if len(item.get("content", "")) > 80000]
    print("\n📌 Length > 80000:")
    for item in long_contents:
        print(f"ID: {item.get('metadata', {}).get('title2', 'N/A')}")
    print(f"\n총 {len(long_contents)}개의 항목이 80000자 이상입니다.")


def transform_to_paragraph_units(data):
    transformed = []
    for i, item in enumerate(data, 1):
        meta = item.get("metadata", {})
        keyword = meta.get("keyword", "")
        main_title = item.get("content")
        내용 = meta.get("내용", {})

        for j, (section_title, section_text) in enumerate(내용.items(), 1):
            new_obj = {
                "content": f"{section_title}\n{section_text}\n",
                "metadata": {
                    "id": f"{i}-{j}",
                    "keyword": keyword,
                    "content_type": section_title,
                    "title": main_title
                }
            }
            transformed.append(new_obj)
    return transformed


def main():
    # 1. JSON 로드
    with open("민족대백과_JSON_최종본.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data = fix_double_underscore(data)

    # 2. 중복 content 분석
    count_duplicate_contents(data)

    # 3. content 기준 병합
    merged_data = merge_by_content(data)
    with open("merged_safe.json", "w", encoding="utf-8") as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=2)

    # 4. 필요 없는 필드 제거
    fields_to_remove = {"목차", "집필자", "관련 미디어", "주석", "참고문헌"}
    cleaned_data = remove_fields(merged_data, fields_to_remove)
    with open("cleaned_file.json", "w", encoding="utf-8") as f:
        json.dump(cleaned_data, f, ensure_ascii=False, indent=2)

    # 5. metadata["내용"] → content로 병합
    content_merged = merge_내용_into_content(cleaned_data)
    with open("merged_content.json", "w", encoding="utf-8") as f:
        json.dump(content_merged, f, ensure_ascii=False, indent=2)

    # 6. url 필드 제거
    remove_url_fields(content_merged)
    with open("no_url_file.json", "w", encoding="utf-8") as f:
        json.dump(content_merged, f, ensure_ascii=False, indent=2)

    # 7. 분석
    analyze_content_lengths(content_merged)

    # 8. 내용 단위 분해
    with open("cleaned_file.json", "r", encoding="utf-8") as f:
        original_data = json.load(f)
    transformed = transform_to_paragraph_units(original_data)
    with open("file.json", "w", encoding="utf-8") as f:
        json.dump(transformed, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()
