import os
import resend
from parser import parse_auction_data  # parser.py의 필터링 알고리즘 불러오기

# GitHub Secrets에서 API 키 로드
resend.api_key = os.environ.get("RESEND_API_KEY")

# 수신자 이메일 주소 (본인 작업용 이메일)
TARGET_EMAIL = "jb591664@gmail.com"  # <--- 본인 이메일로 유지

# 1. parser 모듈을 실행해 위험 권리가 배제된 알짜 물건만 수집
items = parse_auction_data(region="경기", property_type="아파트", min_discount_rate=20)

# 2. 물건 목록 HTML을 반복문(for)으로 동적 생성 (하드코딩 제거)
cards_html = ""
for item in items:
    cards_html += f"""
    <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="font-size: 11px; font-weight: 700; color: #0284c7; background: #e0f2fe; padding: 2px 8px; border-radius: 4px;">{item['discount_rate']}</span>
        <span style="font-size: 11px; color: #94a3b8; font-family: monospace;">{item['case_no']}</span>
      </div>
      
      <h3 style="font-size: 15px; font-weight: 700; color: #0f172a; margin: 0 0 12px 0;">
        {item['address']}
      </h3>

      <table style="width: 100%; font-size: 12px; margin-bottom: 14px; border-collapse: collapse;">
        <tr>
          <td style="color: #64748b; padding: 4px 0; width: 80px;">감정가</td>
          <td style="color: #0f172a; font-weight: 600;">{item['appraisal_price']}</td>
        </tr>
        <tr>
          <td style="color: #64748b; padding: 4px 0;">최저입찰가</td>
          <td style="color: #4f46e5; font-weight: 700; font-size: 14px;">{item['min_price']}</td>
        </tr>
      </table>

      <div style="background: #f8fafc; border-radius: 8px; padding: 12px; font-size: 11px; line-height: 1.6; color: #334155;">
        <div><strong>🔍 권리 현황:</strong> {item['rights_summary']}</div>
      </div>
    </div>
    """

# 3. 전체 이메일 템플릿 조립 (cards_html 자리에 동적 주입)
html_content = f"""
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 580px; margin: 0 auto; padding: 24px 16px; color: #1e293b;">
  
  <div style="margin-bottom: 24px; text-align: center;">
    <span style="font-size: 11px; font-weight: 700; color: #4f46e5; background: #eef2ff; padding: 4px 12px; border-radius: 9999px;">AI AUCTION BRIEFING</span>
    <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 10px 0 4px 0;">주간 맞춤 알짜 경매 브리핑</h2>
    <p style="font-size: 12px; color: #64748b; margin: 0;">선택 조건: [경기 / 아파트 / 할인율 20% 이상]</p>
  </div>

  <!-- [필독] 현장 임장 필수 권고 배너 유지 -->
  <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #d97706; border-radius: 8px; padding: 14px 16px; margin-bottom: 24px;">
    <div style="font-size: 13px; font-weight: 700; color: #b45309; margin-bottom: 4px;">
      ⚠️ [필독] 입찰 전 현장 임장(현장 확인) 필수 안내
    </div>
    <div style="font-size: 11px; line-height: 1.6; color: #78350f;">
      본 리포트는 서류 기반의 1차 AI 요약 자료입니다. <strong>실제 현장 상황(점유 상태, 체납 관리비, 시설 노후도 등)과 서류 데이터 간 차이가 존재할 수 있으므로,</strong> 입찰 전 반드시 현장 임장 및 최종 권리분석을 직접 수행하시기 바랍니다.
    </div>
  </div>

  <!-- 알고리즘이 뽑아낸 물건 카드가 들어가는 자리 -->
  {cards_html}

  <div style="text-align: center; font-size: 10px; color: #94a3b8; margin-top: 24px;">
    본 메일은 개인 맞춤 경매 큐레이션 테스트용으로 자동 발송되었습니다.
  </div>

</div>
"""

# 4. 발송
params = {
    "from": "Auction Curation <onboarding@resend.dev>",
    "to": [TARGET_EMAIL],
    "subject": f"[맞춤 경매 브리핑] 이번 주 선별 알짜 물건 ({len(items)}건)",
    "html": html_content,
}

response = resend.Emails.send(params)
print("발송 성공 ID:", response)
