# 📋 B2B 리드 수집·주소 보강 작업 지침서
### 적용 대상: `E:\Antigravity\builder-dhsteel-sales`
### 기반 작업: `E:\Antigravity\builder-samhyup-sales` (완료 참조)

---

## ✅ 오늘 완료된 작업 요약 (삼협스틸 기준)

| 단계 | 내용 | 결과 |
|---|---|---|
| **A안** | 기존 시트 정제 (비산업 업종 제거) | 비타겟 1,327행 정리 |
| **B안** | 전국 확대 수집 (Playwright 헤드리스 브라우저) | 신규 157개 이메일 타겟 추가 |
| **C단계** | I2~I501 주소 보강 (번지·도로명 추가) | 498개 중 467개 성공 (93.8%) |
| **PPT** | 보강 결과 보고서 생성 | `address_enrichment_report.pptx` |

---

## 🛠️ 사전 준비 사항

### 1. 필수 패키지 확인
```powershell
& "C:\Program Files\Python310\python.exe" -m pip install gspread google-auth playwright requests beautifulsoup4 python-pptx
& "C:\Program Files\Python310\python.exe" -m playwright install chromium
```

### 2. 대흥정밀 Google Sheet 정보 확인
- **스프레드시트 ID**: 대흥정밀 시트 URL에서 `/d/` 와 `/edit` 사이의 값
  - 예: `https://docs.google.com/spreadsheets/d/[여기가 ID]/edit`
- **워크시트 이름**: 삼협은 `company` → 대흥도 동일 워크시트명 확인 필요
- **인증 파일**: `E:\Antigravity\credentials\ghkim\ghkim_credentials_crawler-hifus_20260221.json`

### 3. 스크립트 폴더 생성
```powershell
New-Item -ItemType Directory -Path "E:\Antigravity\builder-dhsteel-sales\search" -Force
```

---

## 📁 작업 파일 목록 (복사 대상)

아래 파일들을 삼협 프로젝트에서 복사한 뒤, **SPREADSHEET_ID만 변경**하면 됩니다.

| 원본 파일 경로 | 복사 경로 | 변경 항목 |
|---|---|---|
| `E:\Antigravity\builder-samhyup-sales\search\plan_a_clean_enrich.py` | `E:\Antigravity\builder-dhsteel-sales\search\plan_a_clean_enrich.py` | `SPREADSHEET_ID` |
| `E:\Antigravity\builder-samhyup-sales\search\plan_b_nationwide.py` | `E:\Antigravity\builder-dhsteel-sales\search\plan_b_nationwide.py` | `SPREADSHEET_ID` |
| `E:\Antigravity\builder-samhyup-sales\search\enhance_addresses_robust.py` | `E:\Antigravity\builder-dhsteel-sales\search\enhance_addresses_robust.py` | `SPREADSHEET_ID` |

---

## 🚀 단계별 실행 순서

### STEP 1 — A안: 기존 시트 정제
**목적**: 비산업 업종(낚시/동물/반려동물 등) 제거, 주소/이메일 데이터 초기 정제

```powershell
cd E:\Antigravity\builder-dhsteel-sales
& "C:\Program Files\Python310\python.exe" search\plan_a_clean_enrich.py
```

**확인 사항**:
- 실행 후 Google Sheet에서 비타겟 업종 행이 삭제되었는지 확인
- 콘솔에 `정제 완료: X행 삭제` 출력 확인

---

### STEP 2 — B안: 전국 확대 수집 (Playwright)
**목적**: 전국 20개 주요 산업 지역 × 9개 키워드 조합으로 신규 B2B 업체 수집
**소요 시간**: 약 30~50분 (180개 쿼리)

```powershell
cd E:\Antigravity\builder-dhsteel-sales
& "C:\Program Files\Python310\python.exe" search\plan_b_nationwide.py
```

**수집 키워드** (스크립트 내 `KEYWORDS` 변수):
- 1순위: `철망`, `용접철망`, `메쉬`, `휀스`, `메쉬휀스`
- 2순위: `건재상`, `철물`, `금속`, `금속인테리어`

**수집 지역** (스크립트 내 `REGIONS` 변수):
```
부산, 대구, 광주, 대전, 울산, 창원, 전주, 청주,
천안, 아산, 진주, 포항, 구미, 원주, 춘천,
익산, 순천, 여수, 충주, 당진
```

**확인 사항**:
- 완료 후 `✅ B안 완료! 신규 X개 메일 마케팅 타겟 추가 완료!` 출력 확인
- Google Sheet `company` 워크시트에 신규 행 추가 확인

---

### STEP 3 — C단계: 주소 보강 (번지·도로명 추가)
**목적**: 시트 I열(주소)에서 `동/읍/면` 단위로만 기록된 짧은 주소를 상세 도로명+번지수로 교체
**소요 시간**: 약 15~20분 (약 500행 기준)

```powershell
cd E:\Antigravity\builder-dhsteel-sales
& "C:\Program Files\Python310\python.exe" search\enhance_addresses_robust.py
```

**처리 범위**: I2 ~ I501 (스크립트 내 `end_idx = 501` 확인)
- 대상 행 수에 따라 `end_idx` 조정 가능

**결과 파일**:
- `address_enrichment_log.txt` — 성공·실패 전체 로그
- (로그에서 `⚠️ 주소 못 찾음` 항목이 수동 검증 대상)

---

### STEP 4 — PPT 보고서 생성 (선택)
**목적**: 전체 작업 결과를 6슬라이드 보고서로 자동 생성

```powershell
& "C:\Program Files\Python310\python.exe" "C:\Users\Administrator\.gemini\antigravity\brain\1ed84be1-709e-4d5f-b7c8-a035954e1437\artifacts\generate_report_ppt.py"
```

> ⚠️ 이 스크립트는 SPREADSHEET_ID가 삼협 기준으로 설정되어 있으므로,  
> 대흥 적용 시 파일을 복사한 뒤 ID를 변경해야 합니다.

---

## 🔧 스크립트 수정 방법 (핵심: SPREADSHEET_ID 교체)

각 스크립트 상단의 아래 줄을 찾아 대흥정밀 시트 ID로 교체:

```python
# 변경 전 (삼협)
SPREADSHEET_ID = "161bSIprv3S0P8-UyPHnC9fWk4q_KcuANSPL-aZEJo04"

# 변경 후 (대흥 — 실제 ID로 교체)
SPREADSHEET_ID = "여기에_대흥정밀_스프레드시트_ID_입력"
```

---

## ⚠️ 주의사항 및 트러블슈팅

### Naver 차단 감지 시
- 콘솔에 `Naver 차단 감지, 5초 대기...` 출력되면 정상 (자동 재시도)
- 반복 차단 시 → `time.sleep(0.6)` 값을 `1.5` 로 늘려 재실행

### 인코딩 오류 시
- 스크립트 상단에 `sys.stdout.reconfigure(encoding='utf-8')` 포함되어 있는지 확인
- `response.encoding = 'utf-8'` 설정 확인 (`safe_get` 함수 내)

### Google Sheet API 할당량 초과 시
- 오류: `APIError: Quota exceeded`
- 해결: `time.sleep(0.6)` → `time.sleep(1.5)` 로 변경 후 재실행
- 스크립트는 이미 업데이트된 행은 건너뜀 (중복 방지)

### Playwright 실행 오류 시
```powershell
# Playwright 브라우저 재설치
& "C:\Program Files\Python310\python.exe" -m playwright install chromium
```

---

## 📊 예상 성과 (삼협 기준 참고)

| 항목 | 삼협스틸 실적 | 대흥정밀 예상 |
|---|---|---|
| B안 신규 수집 업체 | 157개 | 100~200개 (지역·업종에 따라 상이) |
| 주소 보강 성공률 | 93.8% | 90%+ 예상 |
| 전체 소요 시간 | 약 60~80분 | 동일 |

---

## 📁 최종 산출물

작업 완료 후 아래 파일/데이터가 생성됩니다:

| 산출물 | 위치 | 내용 |
|---|---|---|
| Google Sheet 업데이트 | 대흥정밀 시트 `company` 탭 | 신규 업체 + 상세 주소 반영 |
| `address_enrichment_log.txt` | `search\` 폴더 | 주소 보강 전체 로그 |
| `address_enrichment_report.pptx` | `search\` 폴더 (선택) | KPI 요약 보고서 |

---

## 🔗 참고: 삼협스틸 작업 완료 기록

- **작업일**: 2026-07-17
- **대화 ID**: `1ed84be1-709e-4d5f-b7c8-a035954e1437`
- **최종 시트**: `161bSIprv3S0P8-UyPHnC9fWk4q_KcuANSPL-aZEJo04` (워크시트: company)
- **신규 수집**: 157개
- **주소 보강**: 498개 대상 / 467개 성공
