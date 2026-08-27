/**
 * 대흥정밀 B2B 아웃바운드 이메일 자동 발송 Google Apps Script (GAS)
 * 
 * [설치 및 사용 방법]
 * 1. 구글 스프레드시트에서 [확장 프로그램] > [Apps Script]를 클릭합니다.
 * 2. 기존 코드가 있다면 하단에 붙여넣거나 새 스크립트 파일을 만들어 본 코드를 입력합니다.
 * 3. 저장 후 스프레드시트를 새로고침하면 상단에 "대흥 아웃바운드" 메뉴가 나타납니다.
 * 4. "company" 시트의 A열 체크박스를 선택한 후, "대흥 아웃바운드" > "선택 제안서 발송"을 누릅니다.
 * 
 * [company 시트 컬럼 구조]
 * A열: 체크 (체크박스) | B열: 연번 | C열: 회사명 | D열: 주요품목 | E열: 대표번호
 * F열: 이메일 | G열: 사이트 주소 | H열: 지역 | I열: 주소 | J열: 사이트 상태
 * K열: 전화번호 상태 | L열: 품질 | M열: 발송대기(회차) | N열: 발송상태
 * O열: 최종발송일 (수식: =IFERROR(MAXIFS(mail_log!C:C,mail_log!D:D,C2),""))
 * P열: 발송경과 (수식: =IF(ISBLANK(O2),"",TODAY()-O2))
 * Q열: 누적발송횟수 (수식: =COUNTIF(mail_log!D:D,C2))
 *
 * [mail_log 시트 컬럼 구조]
 * A열: 체크 (사용자 관리) | B열: 연번 (자동) | C열: 발송일자 | D열: 회사명
 * E열: 이메일 주소 | F열: 발송회차 | G열: 발송상태 | H열: 세부결과 | I열: 비고
 */

// Vercel 배포 주소에 맞춰 설정 (catalog 디렉토리 반영)
var BASE_URL = "https://dhsteel.vercel.app/";

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('대흥 아웃바운드')
    .addItem('선택 제안서 발송', 'sendOutboundEmails')
    .addToUi();
}

/**
 * mail_log 시트에 발송 이력 기록
 * @param {string} companyName - 회사명
 * @param {string} email - 이메일 주소
 * @param {string} round - 발송회차 (예: '1일차', '9일차')
 * @param {string} status - 발송상태 ('성공' 또는 '실패')
 * @param {string} detail - 세부결과 (API 로그 또는 에러 메시지)
 */
function writeMailLog(companyName, email, round, status, detail) {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var logSheet = ss.getSheetByName("mail_log");

  // mail_log 시트가 없으면 신규 생성
  if (!logSheet) {
    logSheet = ss.insertSheet("mail_log");
    logSheet.appendRow(["체크", "연번", "발송일자", "회사명", "이메일 주소", "발송회차", "발송상태", "세부결과", "비고"]);
    logSheet.getRange("A1:I1").setFontWeight("bold").setBackground("#f1f5f9");
  }

  // 연번: 현재 마지막 행 번호 - 1 (헤더 제외)
  var lastRow = logSheet.getLastRow();
  var seqNum = lastRow; // 헤더(1행) 제외한 데이터 행 수 = 연번

  var today = new Date();
  // A열(체크)은 빈칸, B열(연번)은 자동 부여, C열부터 데이터
  logSheet.appendRow(["", seqNum, today, companyName, email, round, status, detail, ""]);
}

function sendOutboundEmails() {
  var sheet = SpreadsheetApp.getActiveSheet();

  var lastRow = sheet.getLastRow();
  if (lastRow < 2) {
    SpreadsheetApp.getUi().alert('발송할 데이터가 없습니다.');
    return;
  }

  // 헤더 파싱하여 회사명, 이메일, 발송회차 열 찾기
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var emailColIdx = -1;
  var companyColIdx = -1;
  var roundColIdx = -1;

  for (var i = 0; i < headers.length; i++) {
    var header = headers[i].toString().trim();
    if (header.indexOf('이메일') !== -1 || header === '메일' || header.toLowerCase().indexOf('email') !== -1) {
      emailColIdx = i + 1;
    }
    if (header === '회사명' || header === '업체명' || header === '상호' || header === '회사' || header === '수신처') {
      companyColIdx = i + 1;
    }
    if (header.indexOf('발송대기') !== -1 || header.indexOf('발송회차') !== -1 || header.indexOf('회차') !== -1) {
      roundColIdx = i + 1;
    }
  }

  // 감지 실패 시 기본값 설정
  // company 시트: A=체크, B=연번, C=회사명, F=이메일, M=발송대기(회차)
  if (companyColIdx === -1) companyColIdx = 3; // 기본 C열 (회사명)
  if (emailColIdx === -1) emailColIdx = 6;     // 기본 F열 (이메일)
  if (roundColIdx === -1) roundColIdx = 13;    // 기본 M열 (발송대기/회차)

  var dataRange = sheet.getRange(2, 1, lastRow - 1, sheet.getLastColumn());
  var values = dataRange.getValues();

  var targets = [];
  for (var r = 0; r < values.length; r++) {
    var rowNum = r + 2;
    var isChecked = values[r][0]; // A열 (체크박스)

    if (isChecked === true || isChecked === 'TRUE') {
      var companyName = values[r][companyColIdx - 1].toString().trim();
      var emailAddress = values[r][emailColIdx - 1].toString().trim();
      var round = values[r][roundColIdx - 1].toString().trim() || '1일차';

      if (emailAddress) {
        targets.push({
          rowNum: rowNum,
          companyName: companyName || '대표님',
          emailAddress: emailAddress,
          round: round
        });
      }
    }
  }

  if (targets.length === 0) {
    SpreadsheetApp.getUi().alert('알림: A열 체크박스에 체크된 대상이 없습니다.');
    return;
  }

  // 확인 창 표시
  var confirmUi = SpreadsheetApp.getUi().alert(
    '이메일 발송 확인',
    '총 ' + targets.length + '개 업체에 B2B 제안서를 발송하시겠습니까?',
    SpreadsheetApp.getUi().ButtonSet.YES_NO
  );

  if (confirmUi !== SpreadsheetApp.getUi().Button.YES) {
    return;
  }

  // 1. 템플릿 파일 로드
  var htmlTemplate = "";
  try {
    var response = UrlFetchApp.fetch(BASE_URL + "templates/dhsteel_proposal.html");
    htmlTemplate = response.getContentText("UTF-8");
  } catch (err) {
    SpreadsheetApp.getUi().alert('템플릿 로드 실패: ' + BASE_URL + 'templates/dhsteel_proposal.html 주소를 확인해주세요. (에러: ' + err.toString() + ')');
    return;
  }

  // 2. 인라인 이미지 목록 정의 및 Blob 미리 가져오기
  var imageCids = [
    'logo',
    'pipe_swaging', 'pipe_bending', 'pipe_custom',
    'swaging_02', 'swaging_03', 'swaging_04', 'swaging_05',
    'swaging_06', 'swaging_07', 'swaging_08', 'processing_13',
    'bending_02', 'bending_03', 'bending_04', 'bending_05',
    'bending_06', 'bending_07', 'bending_08', 'bending_09',
    'forming_02', 'forming_03', 'forming_04', 'forming_05',
    'forming_06', 'forming_07', 'forming_08', 'forming_01'
  ];

  var inlineImages = {};
  for (var i = 0; i < imageCids.length; i++) {
    var cid = imageCids[i];
    var url = "";
    if (cid === 'logo') {
      url = BASE_URL + "images/logo_dhsteel.png";
    } else if (cid === 'pipe_swaging') {
      url = BASE_URL + "gallery/swaging_01.jpg";
    } else if (cid === 'pipe_bending') {
      url = BASE_URL + "gallery/bending_01.jpg";
    } else if (cid === 'pipe_custom') {
      url = BASE_URL + "gallery/custom_01.jpg";
    } else {
      url = BASE_URL + "gallery/" + cid + ".jpg";
    }

    try {
      var imgBlob = UrlFetchApp.fetch(url).getBlob();
      imgBlob.setName(cid);
      inlineImages[cid] = imgBlob;
    } catch (err) {
      Logger.log("이미지 로드 실패 (CID: " + cid + "): " + url + " - " + err.toString());
    }
  }

  // 3. 순차 발송 진행
  var successCount = 0;
  var failCount = 0;

  for (var t = 0; t < targets.length; t++) {
    var target = targets[t];

    // 회사명 개인화 치환
    var personalizedHtml = htmlTemplate.replace(/{회사명}/g, target.companyName);

    try {
      GmailApp.sendEmail(
        target.emailAddress,
        "[대흥정밀] " + target.companyName + " 귀사 파이프 임가공 협력 제안",
        "본 메일은 B2B 협력 제안서 메일입니다. HTML 형식을 지원하는 메일 클라이언트에서 확인해주세요.",
        {
          htmlBody: personalizedHtml,
          inlineImages: inlineImages
        }
      );

      // 발송 완료 후 체크 해제
      sheet.getRange(target.rowNum, 1).setValue(false);

      // mail_log 시트에 성공 이력 기록
      writeMailLog(target.companyName, target.emailAddress, target.round, '성공', 'Gmail API 발송 완료');

      successCount++;
    } catch (err) {
      Logger.log("메일 발송 에러 (" + target.emailAddress + "): " + err.toString());

      // mail_log 시트에 실패 이력 기록
      writeMailLog(target.companyName, target.emailAddress, target.round, '실패', err.toString());

      failCount++;
    }
  }

  SpreadsheetApp.getUi().alert(
    '이메일 발송 완료\n\n' +
    '- 성공: ' + successCount + '건\n' +
    '- 실패: ' + failCount + '건'
  );
}

/**
 * 대시보드 실시간 연동 Web App API (doGet)
 * 배포 후 대시보드에서 ?site=mailling&callback=xxx 형태로 호출
 *
 * [mail_log 시트 row 인덱스 기준 (0-based)]
 * row[0]=체크, row[1]=연번, row[2]=발송일자, row[3]=회사명
 * row[4]=이메일, row[5]=발송회차, row[6]=발송상태, row[7]=세부결과, row[8]=비고
 */
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
