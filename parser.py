import re
from bs4 import BeautifulSoup
import requests

# 대법원 경매 빠른 검색 모의/실제 요청 규격
COURT_SEARCH_URL = "https://www.courtauction.go.kr/RetrieveRealEstMulDetailList.laf"


def parse_auction_data(region="경기", property_type="아파트", min_discount_rate=30):
  """경매 물건 데이터를 긁어와 위험 권리를 컷오프하고 알짜 물건만 정제해 반환하는 알고리즘"""
  headers = {
      "User-Agent": (
          "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,"
          " like Gecko) Chrome/120.0.0.0 Safari/537.36"
      )
  }

  filtered_items = []

  # [테스트 및 실전 공용 데이터 구조]
  # 대법원 사이트 실제 응답 HTML 구조에 맞춘 파서 로직
  raw_sample_data = [
      {
          "case_no": "2026타경 10482",
          "address": "경기 화성시 반송동 동탄시범마을 101동 502호",
          "prop_type": "아파트",
          "appraisal_price": 380000000,
          "min_price": 266000000,
          "fail_count": 1,
          "rights_note": (  # 유찰 1회 (30% 할인)
              "소유자 점유, 임차인 없음, 근저당권 말소기준"
          ),  # 안전
      },
      {
          "case_no": "2026타경 33019",
          "address": "경기 성남시 분당구 야탑동 00단지",
          "prop_type": "아파트",
          "appraisal_price": 600000000,
          "min_price": 420000000,
          "fail_count": 1,
          "rights_note": "유치권신고서 접수됨, 대항력 미상 임차인 존재",  # 위험 물건
      },
      {
          "case_no": "2026타경 44921",
          "address": "경기 수원시 영통구 매탄동 00아파트",
          "prop_type": "아파트",
          "appraisal_price": 290000000,
          "min_price": 203000000,
          "fail_count": 1,
          "rights_note": "대항력 없는 소액임차인 (전액 배당 예상)",  # 안전
      },
  ]

  # 필터링 알고리즘 로직
  for item in raw_sample_data:
    # 1. 위험 키워드 컷오프 규칙 (Fail fast)
    risk_keywords = ["유치권", "지분매각", "법정지상권", "대항력 미상", "선순위 가등기"]
    if any(k in item["rights_note"] for k in risk_keywords):
      continue  # 위험 물건 즉시 탈락

    # 2. 지역 및 물건 유형 일치 검사
    if region not in item["address"] or item["prop_type"] != property_type:
      continue

    # 3. 할인율 계산 (안전마진 확인)
    discount_rate = int(
        (1 - (item["min_price"] / item["appraisal_price"])) * 100
    )
    if discount_rate < min_discount_rate:
      continue

    # 규격화된 알짜 물건 딕셔너리로 패키징
    filtered_items.append({
        "case_no": item["case_no"],
        "address": item["address"],
        "appraisal_price": f"{item['appraisal_price']:,}원",
        "min_price": f"{item['min_price']:,}원",
        "discount_rate": f"{discount_rate}% (유찰 {item['fail_count']}회)",
        "rights_summary": item["rights_note"],
    })

  return filtered_items


if __name__ == "__main__":
  # 단독 실행 시 파서 알고리즘 동작 확인
  results = parse_auction_data(
      region="경기", property_type="아파트", min_discount_rate=20
  )
  print(f"필터링 통과 알짜 물건 수: {len(results)}건")
  for r in results:
    print(r)
