# 대흥정밀 B2B 아웃바운드 메일 발송 현황 대시보드 연동 계획서

## 💡 대시보드 연동 제안
현재 [dashboard.html](file:///D:/Antigravity/builder-dhsteel-sales/dashboard.html)은 **'모바일 카탈로그'**와 **'공식 홈페이지'**의 유입 및 견적 현황을 실시간(구글 시트 연동) 또는 시뮬레이션으로 모니터링할 수 있는 뛰어난 구조를 가지고 있습니다.

여기에 **"✉️ B2B 이메일 발송 현황"** 모니터링 뷰를 추가하여, 영업 메일이 계획대로 발송되고 피드백이 오는지 한눈에 확인할 수 있는 통합 모니터링 대시보드 구축 계획을 제안합니다.

---

## 🎨 1. 대시보드 UI/UX 통합 설계안

대시보드 상단의 사이트 선택 드롭다운(`site-selector`)에 **"✉️ B2B 이메일 발송 현황"** 옵션을 신규로 추가하여, 화면의 테마와 배치를 유지하면서 데이터 소스만 부드럽게 스위칭되도록 구현합니다.

### 1) 사이트 선택 드롭다운 확장
```html
<select id="site-selector" class="site-select" onchange="switchSite(this.value)">
    <option value="catalog">📱 모바일 카탈로그</option>
    <option value="main_site">🌐 공식 홈페이지 (daeheungsteel.co.kr)</option>
    <option value="mailling">✉️ B2B 이메일 발송 현황</option> <!-- 신규 추가 -->
</select>
```

### 2) 이메일 발송 뷰 선택 시 화면 레이아웃 변화
이메일 발송 뷰가 활성화되면 기존 KPI 영역, 차트 영역, 로그 테이블 영역의 항목이 아래와 같이 자동 변환됩니다.

#### 📊 KPI 대시보드 카드 영역
- **총 발송 완료 메일수**: 누적 이메일 발송 성공 건수 (`mail_log` G열 기준)
- **발송 성공률 (cvr 카드 대체)**: 성공 대비 실패율 계산하여 백분율 표기
- **최근 24시간 발송수**: 당일 발송된 메일 건수

#### 📈 차트 영역 (Chart.js)
- **차트 1 (Doughnut)**: **발송 결과 비율** (성공 vs 실패 비율 시각화)
- **차트 2 (Bar)**: **회차별 메일 발송 분포** (1일차, 9일차, 10일차 등 F열 기준)

#### 📋 데이터 피드 테이블 영역 (기존 견적 리스트 대체)
- 이메일 발송 로그 피드로 컬럼 변경:
  - **연번(B)** / **발송 일시(C)** / **회사명(D)** / **이메일 주소(E)** / **발송 회차(F)** / **발송 상태(G)** / **비고(I)**

#### ⚡ 시뮬레이터 기능 연동
- 시뮬레이터 모드일 때 "가상 견적 접수" 버튼이 **"⚡ 시뮬레이션: 가상 메일 발송 로그 생성"**으로 전환되어 발송 실패 및 성공 시나리오를 테스트할 수 있게 설계합니다.

---

## 🛠️ 2. 실시간 데이터 통신 설계 (구글 스프레드시트 GAS 연동)

현재 대시보드는 `GAS_WEB_APP_URL`을 통해 JSONP 방식으로 실시간 데이터를 연동하도록 설계되어 있습니다. 이메일 발송 현황도 동일한 API를 활용해 가져오도록 확장합니다.

### 1) Google Apps Script Web App (`doGet`) — 확정 코드

> [!IMPORTANT]
> **mail_log 시트 컬럼 인덱스 (0-based)**
> - `row[0]` = A열: 체크 (스킵)
> - `row[1]` = B열: 연번
> - `row[2]` = C열: 발송일자
> - `row[3]` = D열: 회사명
> - `row[4]` = E열: 이메일 주소
> - `row[5]` = F열: 발송회차
> - `row[6]` = G열: 발송상태 (`성공`/`실패`)
> - `row[7]` = H열: 세부결과
> - `row[8]` = I열: 비고

```javascript
function doGet(e) {
  var site = e.parameter.site;
  var callback = e.parameter.callback;
  var responseData = {};

  if (site === 'mailling') {
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var logSheet = ss.getSheetByName("mail_log");
    var logs = [];
    var visits = { success: 0, fail: 0 };

    if (logSheet) {
      var data = logSheet.getDataRange().getValues();

      // 역순 정렬 (최신 로그 우선), 헤더(0행) 제외
      for (var i = data.length - 1; i >= 1; i--) {
        var row = data[i];
        var status = row[6]; // G열: 발송상태

        if (status === "성공") visits.success++;
        else if (status === "실패") visits.fail++;

        logs.push({
          id: row[1],          // B열: 연번
          date: row[2],        // C열: 발송일자
          company: row[3],     // D열: 회사명
          email: row[4],       // E열: 이메일 주소
          round: row[5],       // F열: 발송회차
          status: status,      // G열: 발송상태
          detail: row[7],      // H열: 세부결과
          note: row[8] || ""   // I열: 비고
        });
      }
    }

    responseData = {
      visits: visits,
      logs: logs
    };
  } else {
    // 기존 catalog, main_site 처리 로직 (필요 시 확장)
  }

  // JSONP 규격으로 래핑하여 리턴 (CORS 회피)
  var result = callback + "(" + JSON.stringify(responseData) + ")";
  return ContentService.createTextOutput(result).setMimeType(ContentService.MimeType.JAVASCRIPT);
}
```

---

## 📅 3. 다음 작업 시 구축 계획
1. **Apps Script API 배포**: 수정된 `google_apps_script_outbound.js`(doGet 포함)를 구글 앱스 스크립트 편집기에 반영 후 웹 앱으로 재배포.
2. **`dashboard.html` 프론트엔드 연동**:
   - `site-selector`에 이메일 발송 현황 옵션 추가.
   - `mailling` 선택 시 테이블 헤더, KPI 명칭, 차트 포맷 동적 변경 로직 추가.
   - 로컬 시뮬레이터 더미 데이터에 가상 메일 로그 데이터 세트 반영.
   - 대시보드 내 `loadData()` → `loadLocalData()` 분기 처리 확인.
