# 대흥정밀 B2B 메일 발송 스케줄 및 이력 관리 구축 계획서

## 💡 제안 배경 및 의견
- **별도의 이력 관리(로그) 시트를 만드는 방안을 적극 권장합니다.**
- 메인 `company` 시트의 발송 관련 열 하나에 날짜를 계속 누적시키면, 나중에 특정 업체가 메일을 **총 몇 번 발송받았는지**, **마지막 발송이 언제였는지** 통계를 내거나 분석하기가 어렵습니다.
- 이에 따라, 메일 발송 시마다 별도의 `mail_log` 시트에 한 행(Row)씩 발송 이력을 생성(로그 적재)하고, 메인 `company` 시트에서는 구글시트 수식(`MAXIFS`, `COUNTIF`, `TODAY()`)을 활용해 최종 발송일과 누적 횟수, 경과일수를 자동으로 실시간 표시하도록 구현하는 설계가 가장 효율적이고 직관적입니다.

---

## 📊 1. 구글 스프레드시트 컬럼 구조 (확정)

### [메인 시트: company] 컬럼 구조
| 열 | 컬럼명 | 입력 형식 및 수식 | 역할 및 설명 |
|:---|:---|:---|:---|
| **A열** | 체크 | 체크박스 | 발송 대상 선택 (GAS 트리거) |
| **B열** | 연번 | 숫자 | 업체 일련번호 (사용자 관리) |
| **C열** | 회사명 | 텍스트 | 업체명 |
| **F열** | 이메일 | 텍스트 | 수신 이메일 주소 |
| **M열** | 발송대기 (회차) | 텍스트 (예: `1일차`, `9일차`) | 현재 보낼 타겟 회차 기재 |
| **N열** | 발송상태 | 텍스트 | 발송 성공 여부 상태 표기 |
| **O열** | 최종 발송일 | `=IFERROR(MAXIFS(mail_log!C:C, mail_log!D:D, C2), "")` | mail_log의 C열(발송일자)에서 D열(회사명)이 일치하는 가장 최신 날짜 자동 조회 |
| **P열** | 발송경과 | `=IF(ISBLANK(O2), "", TODAY() - O2)` | 마지막 발송일로부터 오늘까지 경과 일수 |
| **Q열** | 누적 발송 횟수 | `=COUNTIF(mail_log!D:D, C2)` | mail_log D열(회사명)에서 해당 업체 로그 건수 카운트 |

> [!TIP]
> **P열 10일 도래 시 조건부 서식 강조 설정**
> - **적용 범위**: `P2:P`
> - **조건**: `보다 크거나 같음` → `10`
> - **서식**: 셀 배경색을 연한 빨간색 또는 주황색으로 설정하여 재발송 대상 시각적 모니터링

### [로그 시트: mail_log] 컬럼 구조 (확정)
발송할 때마다 기록이 누적되는 데이터베이스 테이블 역할의 시트입니다.

| 열 | 컬럼명 | 입력 방식 | 비고 |
|:---|:---|:---|:---|
| **A열** | 체크 | 사용자 직접 관리 | 체크박스 |
| **B열** | 연번 | GAS 자동 부여 | 헤더 제외 행 수 기준 |
| **C열** | 발송일자 | GAS 자동 기록 | `yyyy-MM-dd HH:mm:ss` |
| **D열** | 회사명 | GAS 자동 기록 | company 시트 C열 값 |
| **E열** | 이메일 주소 | GAS 자동 기록 | company 시트 F열 값 |
| **F열** | 발송회차 | GAS 자동 기록 | company 시트 M열 값 (`1일차` 등) |
| **G열** | 발송상태 | GAS 자동 기록 | `성공` / `실패` |
| **H열** | 세부결과 | GAS 자동 기록 | API 성공 메시지 또는 에러 로그 |
| **I열** | 비고 | 사용자 직접 관리 | 수동 메모 |

---

## ⚙️ 2. Google Apps Script (GAS) 수정 완료 내용

`google_apps_script_outbound.js` 파일에 다음 내용이 반영되었습니다.

### writeMailLog() 함수 (신규 추가)
```javascript
function writeMailLog(companyName, email, round, status, detail) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = ss.getSheetByName("mail_log");

  if (!logSheet) {
    logSheet = ss.insertSheet("mail_log");
    logSheet.appendRow(["체크", "연번", "발송일자", "회사명", "이메일 주소", "발송회차", "발송상태", "세부결과", "비고"]);
    logSheet.getRange("A1:I1").setFontWeight("bold").setBackground("#f1f5f9");
  }

  var lastRow = logSheet.getLastRow();
  var seqNum = lastRow; // 헤더 제외 연번 자동 부여
  var today = new Date();
  // A열(체크)은 빈칸, B열(연번)은 자동, C열부터 데이터
  logSheet.appendRow(["", seqNum, today, companyName, email, round, status, detail, ""]);
}
```

### sendOutboundEmails() 변경 사항
- 기본 컬럼 인덱스 수정: `companyColIdx` 기본값 → **C열(3)**, `emailColIdx` 기본값 → **F열(6)**, `roundColIdx` 기본값 → **M열(13)**
- 발송 성공/실패 양쪽 분기에 `writeMailLog()` 호출 추가
- M열(발송대기/회차) 값을 읽어 mail_log에 기록

---

## 📅 3. company 시트 수식 적용 방법

O, P, Q열 수식을 아래와 같이 적용합니다.

```
O2: =IFERROR(MAXIFS(mail_log!C:C, mail_log!D:D, C2), "")
P2: =IF(ISBLANK(O2), "", TODAY() - O2)
Q2: =COUNTIF(mail_log!D:D, C2)
```

> [!IMPORTANT]
> O열은 날짜 형식 서식으로 지정해야 합니다. (`서식 > 숫자 > 날짜`)
> O2:O, P2:P, Q2:Q 범위에 수식 적용 후 아래 행으로 복사

---

## 📅 4. 다음 작업 진행 예정 사항
1. **스프레드시트 수식 적용**: `company` 시트 O/P/Q열에 위 수식 및 조건부 서식 적용.
2. **GAS 코드 스프레드시트 반영**: 수정된 `google_apps_script_outbound.js` 내용을 구글 앱스 스크립트 편집기에 붙여넣고 저장.
3. **테스트 발송 확인**: 199·200행(대흥정밀1·2, 0일차)으로 테스트 발송 후 `mail_log` C~I열 정상 기록 여부 확인.
4. **대시보드 연동**: `doGet` 함수 배포 후 `dashboard.html` 프론트엔드 연동.
