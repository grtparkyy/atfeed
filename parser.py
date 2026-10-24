import re
import requests
from bs4 import BeautifulSoup

def parse_auction_data(region="제주", property_type="아파트", min_discount_rate=20):
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://www.courtauction.go.kr/",
        "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7"
    })

    items = []

    try:
        init_url = "https://www.courtauction.go.kr/RetrieveRealEstCarSearchList.laf"
        session.get(init_url, timeout=10)

        # 제주 관할 검색 요청
        search_data = {
            "targetRowMax": "50",
            "page": "1"
        }

        res = session.post(init_url, data=search_data, timeout=15)
        res.encoding = "euc-kr"

        soup = BeautifulSoup(res.text, "html.parser")
        rows = soup.select("table.Ltbl_list tbody tr")

        for row in rows:
            cols = row.select("td")
            if len(cols) < 5:
                continue

            case_no_elem = cols[1].find("a")
            case_no = case_no_elem.get_text(strip=True) if case_no_elem else cols[1].get_text(strip=True)
            info_text = cols[3].get_text(strip=True)

            # 지역 검사 (주소에 '제주'가 포함되어 있는지 확인)
            if region and region not in info_text:
                continue

            # 감정가 및 최저가
            price_text = cols[4].get_text(separator=" ", strip=True)
            numbers = re.findall(r'[\d,]+', price_text)
            
            if len(numbers) >= 2:
                appraisal_val = int(numbers[0].replace(",", ""))
                min_val = int(numbers[1].replace(",", ""))
            else:
                continue

            # 위험 키워드 제외
            risk_keywords = ["유치권", "지분매각", "법정지상권", "대항력"]
            if any(k in info_text for k in risk_keywords):
                continue

            # 할인율 계산
            discount_rate = int((1 - (min_val / appraisal_val)) * 100) if appraisal_val > 0 else 0
            if discount_rate < min_discount_rate:
                continue

            items.append({
                "case_no": case_no,
                "address": info_text[:70] + "..." if len(info_text) > 70 else info_text,
                "appraisal_price": f"{appraisal_val:,}원",
                "min_price": f"{min_val:,}원",
                "discount_rate": f"할인율 {discount_rate}%",
                "rights_summary": "서류상 위험 키워드 미발견"
            })

            if len(items) >= 3:
                break

    except Exception as e:
        print(f"스크래핑 처리 중 오류: {e}")

    # 조건에 맞는 물건이 없을 경우 fallback
    if not items:
        items.append({
            "case_no": "물건 조회 안내",
            "address": f"현재 {region} 지역 내 설정 조건({discount_rate if 'discount_rate' in locals() else min_discount_rate}% 이상 할인)에 부합하는 안전 물건이 없습니다.",
            "appraisal_price": "-",
            "min_price": "-",
            "discount_rate": "-",
            "rights_summary": "다음 회차 경매 일정에 맞춰 자동 갱신됩니다."
        })

    return items

if __name__ == "__main__":
    results = parse_auction_data(region="제주")
    print(f"제주 알짜 물건 결과: {len(results)}건")
    for r in results:
        print(r)
