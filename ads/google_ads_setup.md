# 대흥정밀 - Google Ads 전환 추적 연동 보고서

본 문서는 대흥정밀 B2B 모바일 간편 견적 카탈로그 웹사이트에 Google Ads 광고 전환 추적(견적 문의 완료) 태그를 연동한 설정 보고서입니다.

---

## 1. 연동 개요

| 항목 | 내용 |
|---|---|
| **광고주 계정 ID** | `651-167-5293` (dhsteel) |
| **계정 이메일** | dnsteel7@gmail.com |
| **목표 카테고리** | `견적 요청` (Request Quote) |
| **측정 방식** | 코드를 사용한 수동 이벤트 측정 (JavaScript 성공 콜백 이벤트) |
| **전환 ID** | ※ 계정에서 발급 후 `app.js` 내 `AW-XXXXXXXX` 교체 필요 |
| **전환 라벨** | ※ 계정에서 발급 후 `app.js` 내 `CONVERSION_LABEL` 교체 필요 |
| **전환 값** | 전환당 1원 (KRW) 고정 |
| **전환 횟수** | 1회 (리드 중복 집계 방지) |

---

## 2. 전환 ID/라벨 발급 방법

Google Ads 계정(651-167-5293)에서 전환 태그를 발급하는 절차:

1. **전환 메뉴 진입:**
   좌측 메뉴 **`목표`** (🎯) → **`전환`** → **`요약`** → **`[+ 전환 액션 만들기]`** 클릭

2. **소스 선택:**
   **`웹사이트`** 유형 선택 → 대상 URL 입력 → `[검사]`

3. **수동 추가:**
   `[+ 전환 만들기]` → 수동 이벤트 방식 선택

4. **상세 설정:**
   - 카테고리: `견적 요청`
   - 전환 이름: `견적문의완료`
   - 값: `1 KRW` 고정
   - 횟수: `1회`

5. **코드 확인:**
   저장 후 `[이벤트 스니펫 보기]` → `AW-XXXXXXXXX/LABEL` 형태 복사

---

## 3. 코드 수정 위치

### ① `catalog/index.html` — 글로벌 태그 활성화
현재 주석 처리된 아래 블록에서 `AW-XXXXXXXX`를 실제 전환 ID로 교체:

```html
<!-- Google tag (gtag.js) - Google Ads: dhsteel 651-167-5293 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=AW-XXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'AW-XXXXXXXX');
</script>
```

### ② `catalog/app.js` — 전환 이벤트 수정
파일 상단 `GOOGLE_ADS_CONVERSION.sendTo` 값 교체:

```javascript
const GOOGLE_ADS_CONVERSION = {
  sendTo: 'AW-XXXXXXXX/CONVERSION_LABEL'  // ← 실제 값으로 교체
};
```

---

## 4. 전환 발동 시점

| 상황 | 발동 여부 |
|---|---|
| formsubmit.co AJAX 전송 **성공** 시 | ✅ 발동 |
| AJAX 실패 후 mailto: 폴백 시도 시 | ✅ 발동 |

---

## 5. 검증 방법

- **Google Tag Assistant** (크롬 확장) 설치 후 사이트에서 견적 폼 제출 테스트
- 개발자 도구(F12) → Network 탭 → `googleadservices.com/pagead/conversion/` 요청 확인
- Google Ads 대시보드 → 목표 → 전환 → 요약: 데이터 반영까지 **24~48시간** 소요
