import os
import resend

# GitHub Secrets에 등록한 API 키 자동 로드
resend.api_key = os.environ.get("ATfeed")

# 메일을 받을 본인 이메일 주소 (Resend 가입 메일)
TARGET_EMAIL = "jb591664@gmail.com"  # <--- 본인 이메일로 수정!

html_content = """
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 580px; margin: 0 auto; padding: 24px 16px; color: #1e293b;">
  
  <!-- 헤더 -->
  <div style="margin-bottom: 24px; text-align: center;">
    <span style="font-size: 11px; font-weight: 700; color: #4f46e5; background: #eef2ff; padding: 4px 12px; border-radius: 9999px;">AI AUCTION BRIEFING</span>
    <h2 style="font-size: 20px; font-weight: 800; color: #0f172a; margin: 10px 0 4px 0;">주간 맞춤 알짜 경매 브리핑</h2>
    <p style="font-size: 12px; color: #64748b; margin: 0;">선택 조건: [경기 남부 / 1~2억 대 / 아파트·오피스텔]</p>
  </div>

  <!-- [필독] 현장 임장 필수 권고 배너 -->
  <div style="background-color: #fffbeb; border: 1px solid #fde68a; border-left: 4px solid #d97706; border-radius: 8px; padding: 14px 16px; margin-bottom: 24px;">
    <div style="font-size: 13px; font-weight: 700; color: #b45309; margin-bottom: 4px;">
      ⚠️ [필독] 입찰 전 현장 임장(현장 확인) 필수 안내
    </div>
    <div style="font-size: 11px; line-height: 1.6; color: #78350f;">
      본 리포트는 공공데이터 및 법원 서류 기반의 1차 AI 요약 자료입니다. <strong>실제 현장 상황(점유 상태, 체납 관리비, 누수 및 시설 노후도 등)과 서류 데이터 간 차이가 존재할 수 있으므로,</strong> 입찰 전 반드시 현장 임장 및 최종 권리분석을 직접 수행하시기 바랍니다.
    </div>
  </div>

  <!-- 물건 1 카드 -->
  <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 20px; margin-bottom: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
      <span style="font-size: 11px; font-weight: 700; color: #0284c7; background: #e0f2fe; padding: 2px 8px; border-radius: 4px;">1회 유찰 (안전마진 확보)</span>
      <span style="font-size: 11px; color: #94a3b8; font-family: monospace;">2026타경 10482</span>
    </div>
    
    <h3 style="font-size: 15px; font-weight: 700; color: #0f172a; margin: 0 0 12px 0;">
      경기 화성시 반송동 동탄시범마을 00평형
    </h3>

    <table style="width: 100%; font-size: 12px; margin-bottom: 14px; border-collapse: collapse;">
      <tr>
        <td style="color: #64748b; padding: 4px 0; width: 80px;">감정가</td>
        <td style="color: #0f172a; font-weight: 600;">3억 8,000만 원</td>
      </tr>
      <tr>
        <td style="color: #64748b; padding: 4px 0;">최저입찰가</td>
        <td style="color: #4f46e5; font-weight: 700; font-size: 14px;">2억 6,600만 원 (70%)</td>
      </tr>
      <tr>
        <td style="color: #64748b; padding: 4px 0;">최근 실거래</td>
        <td style="color: #0f172a;">3억 5,000만 원 선</td>
      </tr>
    </table>

    <div style="background: #f8fafc; border-radius: 8px; padding: 12px; font-size: 11px; line-height: 1.6; color: #334155;">
      <div><strong>🔍 AI 권리분석:</strong> 말소기준등기 이후 모든 권리 소멸. 대항력 있는 임차인 없음 (소유자 점유 건, 일반 명도 대상).</div>
      <div style="margin-top: 6px;"><strong>📍 상권/입지:</strong> 초품아 단지, 중심상가 도보 7분. 인근 전세가율 75% 수준으로 실투자 방어 양호.</div>
      <div style="margin-top: 6px;"><strong>💰 예상 필요 현금:</strong> 경락잔금대출 감안 시 약 7,000만 원 내외.</div>
    </div>
  </div>

  <!-- 푸터 -->
  <div style="text-align: center; font-size: 10px; color: #94a3b8; margin-top: 24px;">
    본 메일은 개인 맞춤 경매 큐레이션 테스트용으로 자동 발송되었습니다.
  </div>

</div>
"""

params = {
    "from": "Auction Curation <onboarding@resend.dev>",
    "to": [TARGET_EMAIL],
    "subject": "[맞춤 경매 브리핑] 이번 주 선별 알짜 물건 리포트",
    "html": html_content,
}

response = resend.Emails.send(params)
print("발송 성공 ID:", response)
