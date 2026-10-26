/**
 * 대흥정밀 아웃바운드 메일 발송 스크립트 v3
 * [company 시트 컬럼] A=체크, B=연번, C=회사명, F=이메일, M=발송대기(회차)
 * [mail_log 시트 컬럼] A=체크, B=연번, C=발송일자, D=회사명, E=이메일, F=발송회차, G=발송상태, H=세부결과, I=비고
 */

var BASE_URL = "https://dhsteel.vercel.app/";
var SS_ID = "1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic";

function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('대흥 아웃바운드')
    .addItem('선택 제안서 발송 (v1/v2 자동분기)', 'sendOutboundEmails')
    .addSeparator()
    .addItem('☑️ 2회차 리마인드 대상(122개사) 자동 체크', 'selectSecondRoundTargets')
    .addItem('⬜ 전체 체크박스 선택 해제', 'uncheckAllRows')
    .addSeparator()
    .addItem('🔄 mail_log → company 동기화', 'syncMailLogToCompany')
    .addSeparator()
    .addItem('📧 반송 메일 지금 스캔', 'scanBounceEmails')
    .addItem('⏰ 자동 스캔 트리거 설치 (1회)', 'installBounceScanner')
    .addToUi();
}

/**
 * 2회차 리마인드 대상(이전 발송 후 14일 이상 경과 또는 '메일 정기' 대상) 자동 체크
 */
function selectSecondRoundTargets() {
  var ss = SpreadsheetApp.openById(SS_ID);
  var sheet = ss.getSheetByName("company");
  if (!sheet) return;

  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;

  var range = sheet.getRange(2, 1, lastRow - 1, 16);
  var values = range.getValues();
  var checkCol = [];
  var selectedCount = 0;
  var today = new Date();

  for (var r = 0; r < values.length; r++) {
    var email = values[r][5].toString().trim(); // F열
    var round = values[r][12].toString().trim(); // M열 (발송회차)
    var status = values[r][13].toString().trim(); // N열 (발송상태)
    var sendDateStr = values[r][14].toString().trim(); // O열 (발송일)

    // 이메일이 있고, 발송 성공 이력이 있는 경우
    var isEligible = false;
    if (email && status === '성공') {
      if (sendDateStr) {
        var sDate = new Date(sendDateStr.replace(/-/g, '/'));
        var diffDays = (today - sDate) / (1000 * 60 * 60 * 24);
        // 오늘 발송된 것(1일 이내)은 제외하고, 과거 발송분(14일 이상 경과) 대상 선택
        if (diffDays >= 14 || round === '메일 정기') {
          isEligible = true;
        }
      } else {
        isEligible = true;
      }
    }

    if (isEligible) {
      checkCol.push([true]);
      selectedCount++;
    } else {
      checkCol.push([false]);
    }
  }

  sheet.getRange(2, 1, lastRow - 1, 1).setValues(checkCol);
  SpreadsheetApp.getUi().alert('2회차 리마인드 대상 선택 완료\n\n총 ' + selectedCount + '개 업체가 A열에 자동 체크되었습니다.\n\n[선택 제안서 발송]을 누르시면 v2 리마인드 제안서가 발송됩니다.');
}

/**
 * 체크박스 전체 해제
 */
function uncheckAllRows() {
  var ss = SpreadsheetApp.openById(SS_ID);
  var sheet = ss.getSheetByName("company");
  if (!sheet) return;
  var lastRow = sheet.getLastRow();
  if (lastRow < 2) return;
  
  sheet.getRange(2, 1, lastRow - 1, 1).setValue(false);
  SpreadsheetApp.getUi().alert('체크박스 전체 선택이 해제되었습니다.');
}

// 딱 한 번만 실행 (트리거 설치)
function installTrigger() {
  var ss = SpreadsheetApp.openById(SS_ID);
  ScriptApp.getProjectTriggers().forEach(function (t) { ScriptApp.deleteTrigger(t); });
  ScriptApp.newTrigger('onOpen').forSpreadsheet(ss).onOpen().create();
  Browser.msgBox('트리거 설치 완료!');
}

function writeMailLog(companyName, email, round, status, detail) {
  try {
    var ss = SpreadsheetApp.openById(SS_ID);
    var log = ss.getSheetByName("mail_log");
    if (!log) {
      log = ss.insertSheet("mail_log");
      log.appendRow(["체크", "연번", "발송일자", "회사명", "이메일 주소", "발송회차", "발송상태", "세부결과", "비고"]);
      log.getRange("A1:I1").setFontWeight("bold").setBackground("#f1f5f9");
    }
    var formattedDate = Utilities.formatDate(new Date(), "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");
    var lastRow = log.getLastRow();
    var seq = (lastRow <= 1) ? 1 : lastRow;
    log.appendRow(["", seq, formattedDate, companyName, email, round, status, detail, ""]);
  } catch (e) {
    try {
      SpreadsheetApp.getUi().alert("로그 작성 실패 에러: " + e.toString());
    } catch (err) {
      Logger.log("로그에러: " + e.toString());
    }
  }
}

function getSeasonGreeting() {
  var month = new Date().getMonth() + 1; // 1 ~ 12
  if (month >= 3 && month <= 5) {
    return "따스한 봄기운과 함께 귀사의 새로운 도약과 사업 번창을 기원합니다.";
  } else if (month >= 6 && month <= 8) {
    return "무더운 여름철 건강에 유의하시며, 귀사의 생산과 사업 번창을 기원합니다.";
  } else if (month >= 9 && month <= 11) {
    return "결실의 계절 가을, 귀사의 건승과 사업 번창을 기원합니다.";
  } else {
    return "추운 겨울철 건강에 유의하시며, 귀사의 한 해 마무리와 희망찬 사업 번창을 기원합니다.";
  }
}

function sendOutboundEmails() {
  var ss = SpreadsheetApp.openById(SS_ID);
  var sheet = ss.getSheetByName("company");
  if (!sheet) {
    SpreadsheetApp.getUi().alert("'company' 시트를 찾을 수 없습니다.");
    return;
  }

  var lastRow = sheet.getLastRow();
  if (lastRow < 2) {
    SpreadsheetApp.getUi().alert('발송할 데이터가 없습니다.');
    return;
  }

  var values = sheet.getRange(2, 1, lastRow - 1, sheet.getLastColumn()).getValues();
  var targets = [];

  for (var r = 0; r < values.length; r++) {
    if (values[r][0] !== true) continue;
    var company = values[r][2].toString().trim();   // C열 회사명
    var email = values[r][5].toString().trim();   // F열 이메일
    var round = values[r][12].toString().trim() || '대기'; // M열 발송회차
    var status = values[r][13].toString().trim(); // N열 발송상태
    
    // 이전에 발송 성공 이력이 있거나 '메일 정기'인 경우 v2 (정기 리마인드) 적용
    var isReminder = (round === '메일 정기' || status === '성공');
    
    if (email) {
      targets.push({
        row: r + 2,
        company: company || '대표님',
        email: email,
        round: round,
        isReminder: isReminder
      });
    }
  }

  if (targets.length === 0) {
    SpreadsheetApp.getUi().alert('A열 체크박스에 체크된 대상이 없습니다.');
    return;
  }

  var countV1 = targets.filter(function(t) { return !t.isReminder; }).length;
  var countV2 = targets.filter(function(t) { return t.isReminder; }).length;

  var ui = SpreadsheetApp.getUi();
  var confirmMsg = '총 ' + targets.length + '개 업체에 발송하시겠습니까?\n\n' +
                   '- 신규 소개 제안서(v1): ' + countV1 + '건\n' +
                   '- 정기 리마인드 제안서(v2): ' + countV2 + '건';
  var confirm = ui.alert('발송 확인 (자동 분기)', confirmMsg, ui.ButtonSet.YES_NO);
  if (confirm !== ui.Button.YES) return;

  // 1. 신규용 v1 템플릿 로드
  var htmlV1 = "";
  if (countV1 > 0) {
    var resp1 = UrlFetchApp.fetch(BASE_URL + "templates/dhsteel_proposal.html", { muteHttpExceptions: true });
    if (resp1.getResponseCode() === 200) {
      htmlV1 = resp1.getContentText("UTF-8");
    }
  }

  // 2. 리마인드용 v2 템플릿 로드
  var htmlV2 = "";
  if (countV2 > 0) {
    var resp2 = UrlFetchApp.fetch(BASE_URL + "templates/dhsteel_proposal_v2.html", { muteHttpExceptions: true });
    if (resp2.getResponseCode() === 200) {
      htmlV2 = resp2.getContentText("UTF-8");
    }
  }

  var seasonGreeting = getSeasonGreeting();
  var ok = 0, fail = 0;

  for (var t = 0; t < targets.length; t++) {
    var tgt = targets[t];
    var isRem = tgt.isReminder;
    var rawHtml = isRem ? (htmlV2 || htmlV1) : htmlV1;
    
    var title = isRem 
      ? "[대흥정밀] " + tgt.company + " 귀사 파이프 임가공 견적 및 납기 지원 안내 (정기 리마인드)"
      : "[대흥정밀] " + tgt.company + " 귀사 파이프 임가공 협력 제안";

    var body = rawHtml
      .replace(/{회사명}/g, tgt.company)
      .replace(/{계절인사}/g, seasonGreeting);

    try {
      GmailApp.sendEmail(
        tgt.email,
        title,
        "본 메일은 HTML 형식입니다.",
        { htmlBody: body }
      );
      sheet.getRange(tgt.row, 1).setValue(false);
      var nowStr = Utilities.formatDate(new Date(), "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");
      sheet.getRange(tgt.row, 13).setValue(isRem ? '2회차 완료' : '1회차 완료'); // M열 (발송회차)
      sheet.getRange(tgt.row, 14).setValue('성공'); // N열 (발송상태)
      sheet.getRange(tgt.row, 15).setValue(nowStr);  // O열 (발송일)
      sheet.getRange(tgt.row, 16).setValue(isRem ? 'Gmail API 리마인드(v2) 발송 완료' : 'Gmail API 제안서(v1) 발송 완료'); // P열 (발송결과)
      writeMailLog(tgt.company, tgt.email, isRem ? '2회차 정기' : '1회차 신규', '성공', 'Gmail API 발송 완료');
      ok++;
    } catch (e) {
      var nowStr = Utilities.formatDate(new Date(), "Asia/Seoul", "yyyy-MM-dd HH:mm:ss");
      sheet.getRange(tgt.row, 14).setValue('실패'); // N열 (발송상태)
      sheet.getRange(tgt.row, 15).setValue(nowStr);  // O열 (발송일)
      sheet.getRange(tgt.row, 16).setValue(e.toString()); // P열 (발송결과)
      writeMailLog(tgt.company, tgt.email, tgt.round, '실패', e.toString());
      fail++;
    }
  }

  ui.alert('발송 완료\n\n성공: ' + ok + '건\n실패: ' + fail + '건');
}

function doGet(e) {
  var site = e.parameter.site;
  var cb = e.parameter.callback;
  var data = {};

  if (site === 'mailling') {
    var ss = SpreadsheetApp.openById(SS_ID);
    var logSheet = ss.getSheetByName("mail_log");
    var companySheet = ss.getSheetByName("company");
    var logs = [];
    var visits = { success: 0, fail: 0 };

    // ── company 시트에서 회사명 → 상세정보 맵 생성 ──
    var companyMap = {};
    if (companySheet) {
      var cRows = companySheet.getDataRange().getValues();
      for (var c = 1; c < cRows.length; c++) {
        var cName = (cRows[c][2] || '').toString().trim();
        if (cName) {
          companyMap[cName] = {
            phone: (cRows[c][4] || '').toString().trim(),  // E열: 대표번호
            site: (cRows[c][6] || '').toString().trim(),  // G열: 사이트 주소
            region: (cRows[c][7] || '').toString().trim(),  // H열: 지역
            address: (cRows[c][8] || '').toString().trim()   // I열: 주소
          };
        }
      }
    }

    // ── company 시트에서 배정된 모든 회차 목록 수집 ──
    var allRoundsSet = {};
    if (companySheet) {
      var cRows = companySheet.getDataRange().getValues();
      for (var c = 1; c < cRows.length; c++) {
        var rVal = (cRows[c][12] || '').toString().trim(); // M열: 발송대기(회차)
        if (rVal) allRoundsSet[rVal] = true;
      }
    }

    if (logSheet) {
      var rows = logSheet.getDataRange().getValues();
      for (var i = rows.length - 1; i >= 1; i--) {
        var rVal = (rows[i][5] || '').toString().trim(); // F열: 발송회차
        if (rVal) allRoundsSet[rVal] = true;
        var s = rows[i][6];
        if (s === '성공') visits.success++;
        else if (s === '실패') visits.fail++;
        var companyName = rows[i][3];
        var info = companyMap[companyName] || { phone: '', site: '', region: '', address: '' };
        logs.push({
          id: rows[i][1],
          date: rows[i][2],
          company: companyName,
          email: rows[i][4],
          round: rVal,
          status: s,
          detail: rows[i][7],
          note: rows[i][8] || '',
          phone: info.phone,
          site: info.site,
          region: info.region,
          address: info.address
        });
      }
    }
    var allRounds = Object.keys(allRoundsSet);
    data = { visits: visits, logs: logs, allRounds: allRounds };
  } else if (site === 'fax') {
    var ss = SpreadsheetApp.openById(SS_ID);
    var faxSheet = ss.getSheetByName("fax_log");
    var logs = [];
    var visits = { success: 0, fail: 0 };

    if (faxSheet) {
      var rows = faxSheet.getDataRange().getValues();
      // B=연번, C=발송일자, D=회사명, E=팩스번호, F=발송회차, G=발송상태, H=세부결과, I=비고
      for (var i = rows.length - 1; i >= 1; i--) {
        var s = (rows[i][6] || '').toString().trim();
        if (s === '성공') visits.success++;
        else if (s === '실패') visits.fail++;
        logs.push({
          id: rows[i][1],
          date: rows[i][2],
          company: rows[i][3],
          fax: rows[i][4],
          round: rows[i][5],
          status: s,
          detail: rows[i][7],
          note: rows[i][8] || ''
        });
      }
    }
    data = { visits: visits, logs: logs };
  }

  return ContentService
    .createTextOutput(cb + "(" + JSON.stringify(data) + ")")
    .setMimeType(ContentService.MimeType.JAVASCRIPT);
}

// 홈페이지(https://dhsteel.vercel.app/) 견적 문의 데이터 수신 및 파일 업로드 처리 API
function doPost(e) {
  try {
    var params = e.parameter;

    // JSON body로 들어오는 경우 예외 처리
    if (e.postData && e.postData.contents) {
      try {
        var json = JSON.parse(e.postData.contents);
        params = json;
      } catch (err) { }
    }

    var company = params['회사명_현장명'] || params['companyName'] || '미기입';
    var name = params['담당자명'] || params['contactPerson'] || '미기입';
    var phone = params['연락처'] || params['contactPhone'] || '미기입';
    var email = params['이메일'] || params['contactEmail'] || '미기입';
    var service = params['가공_서비스'] || params['serviceSelect'] || '미선택';
    var specs = params['희망_규격_수량'] || params['specsInput'] || '미기입';

    var fileUrl = "첨부파일 없음";

    // 첨부파일 처리 (Base64 형식으로 올라올 경우 구글 드라이브에 저장)
    if (params.fileData && params.fileName) {
      try {
        var base64Data = params.fileData.split(",")[1] || params.fileData;
        var decoded = Utilities.base64Decode(base64Data);
        var blob = Utilities.newBlob(decoded, params.fileType || 'application/octet-stream', params.fileName);

        // 구글 드라이브 '대흥정밀_견적도면' 폴더에 저장
        var folder;
        var folders = DriveApp.getFoldersByName("대흥정밀_견적도면");
        if (folders.hasNext()) {
          folder = folders.next();
        } else {
          folder = DriveApp.createFolder("대흥정밀_견적도면");
        }

        var file = folder.createFile(blob);
        file.setSharing(DriveApp.Access.ANYONE_WITH_LINK, DriveApp.Permission.VIEW);
        fileUrl = file.getUrl();
      } catch (fileErr) {
        fileUrl = "파일 저장 실패: " + fileErr.toString();
      }
    }

    // 이메일 본문 생성
    var emailBody =
      "🏭 [대흥정밀 홈페이지 견적 문의 접수]\n\n" +
      "1. 회사/현장명: " + company + "\n" +
      "2. 담당자명: " + name + "\n" +
      "3. 연락처: " + phone + "\n" +
      "4. 이메일: " + email + "\n" +
      "5. 가공 서비스: " + service + "\n" +
      "6. 희망 규격 및 수량:\n" + specs + "\n\n" +
      "📁 도면 첨부파일 링크:\n" + fileUrl + "\n\n" +
      "---본 메일은 B2B 영업시스템 API에 의해 자동 발송되었습니다.---";

    // 대표님 네이버 이메일로 알림 전송
    MailApp.sendEmail({
      to: "daeheungsteel@naver.com",
      subject: "[대흥정밀 견적문의] " + service + " - " + company,
      body: emailBody
    });

    return ContentService
      .createTextOutput(JSON.stringify({ status: "success", fileUrl: fileUrl }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (error) {
    return ContentService
      .createTextOutput(JSON.stringify({ status: "error", message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

/**
 * 통합 동기화: mail_log 시트를 단일 소스로 company 시트에 반영
 *
 * 규칙:
 *  1. mail_log G열(발송상태) + H열(세부결과) 기준
 *  2. 동일 회사명 중복 로그 → 가장 최신(=낮은 행 번호) 우선
 *  3. company N열(발송상태), O열(발송일), P열(발송결과) 업데이트
 *  4. 발송대기(서울학교) 반송/에러 업체 쮘리 포함
 */
function syncMailLogToCompany() {
  var ss = SpreadsheetApp.openById(SS_ID);
  var logSheet     = ss.getSheetByName('mail_log');
  var companySheet = ss.getSheetByName('company');

  if (!logSheet || !companySheet) {
    SpreadsheetApp.getUi().alert('시트를 찾을 수 없습니다. (mail_log / company)');
    return;
  }

  // ── 1. mail_log 전체 읽기 ──
  var logRows = logSheet.getDataRange().getValues();
  // 로그맵: { 회사명: { status, detail, date, rowIdx } }
  // 동일 회사명이 여러 번 나오면 가장 마지막(=최신) 행을 영주
  var logMap = {};
  for (var i = 1; i < logRows.length; i++) {
    var cName  = (logRows[i][3] || '').toString().trim(); // D열: 회사명
    var status = (logRows[i][6] || '').toString().trim(); // G열: 발송상태
    var detail = (logRows[i][7] || '').toString().trim(); // H열: 세부결과
    var date   =  logRows[i][2];                          // C열: 발송일자

    if (!cName || !status) continue;

    // 실패인데 세부결과가 비어있으면 기본값
    if (status === '실패' && !detail) {
      detail = '발송 실패 (세부사유 미확인)';
    }

    // 파시: 반송(에러) 로그는 mail_log에 '반송' 또는 '실패'로 저장됨
    // 둘 다 '실패'로 통합 융합
    var normStatus = (status === '성공') ? '성공' : '실패';

    // 동일 회사: 여러 회차 기록이 있으면 가장 낙은 행이 최신
    if (!logMap[cName] || i > logMap[cName].rowIdx) {
      logMap[cName] = {
        status: normStatus,
        detail: detail,
        date  : date,
        rowIdx: i
      };
    }
  }

  // ── 2. company 시트를 순회하면서 동기화 ──
  var companyRows = companySheet.getDataRange().getValues();
  var updated = 0, skipped = 0;
  var nowStr  = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss');

  for (var r = 1; r < companyRows.length; r++) {
    var name = (companyRows[r][2] || '').toString().trim(); // C열: 회사명
    if (!name) continue;

    var entry = logMap[name];
    if (!entry) {
      skipped++;
      continue; // mail_log에 없는 업체는 건들지 않음
    }

    var displayDate = (entry.date instanceof Date)
      ? Utilities.formatDate(entry.date, 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss')
      : entry.date.toString();

    companySheet.getRange(r + 1, 14).setValue(entry.status);  // N열: 발송상태
    companySheet.getRange(r + 1, 15).setValue(displayDate);   // O열: 발송일
    companySheet.getRange(r + 1, 16).setValue(entry.detail);  // P열: 발송결과

    updated++;
  }

  SpreadsheetApp.getUi().alert(
    '🔄 동기화 완료\n\n' +
    '✅ 업데이트: ' + updated + '건\n' +
    '⏭️ 미해당(mail_log 미연동): ' + skipped + '건'
  );
}

// [deprecated] 통합 syncMailLogToCompany 사용 권장
function syncPastLogsToCompany() {
  syncMailLogToCompany();
}

// [deprecated] 통합 syncMailLogToCompany 사용 권장
function markBouncedEmails() {
  SpreadsheetApp.getUi().alert('⚠️ 이 함수는 사용 중단되었습니다.\n\n[대흥 아웃바운드] 메뉴 → [mail_log → company 동기화] 를 사용해주세요.');
}


// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
// 📧 Gmail 반송 메일 자동 파싱 시스템
// ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

/**
 * Gmail 반송/에러 메일을 자동으로 파싱하여 mail_log에 기록하고 company 시트를 동기화합니다.
 * - 매 1시간마다 자동 실행 (installBounceScanner 로 트리거 등록)
 * - 처리된 메일에는 '대흥_반송처리완료' 라벨을 붙여 중복 처리 방지
 * - 신규 반송이 감지되면 syncMailLogToCompany() 자동 호출
 */
function scanBounceEmails() {
  var ss = SpreadsheetApp.openById(SS_ID);
  var companySheet = ss.getSheetByName('company');
  var logSheet     = ss.getSheetByName('mail_log');
  if (!companySheet || !logSheet) {
    Logger.log('[반송스캔] 시트 없음');
    return 0;
  }

  // ── 1. company 시트 맵 구성 ──
  var companyNameMap = {}; // 회사명(소문자) → { email, round, displayName }
  var emailMap       = {}; // 이메일(소문자) → { company, round }
  var cRows = companySheet.getDataRange().getValues();
  for (var i = 1; i < cRows.length; i++) {
    var em  = (cRows[i][5]  || '').toString().trim().toLowerCase();
    var nm  = (cRows[i][2]  || '').toString().trim();
    var rnd = (cRows[i][12] || '').toString().trim() || '미상';
    if (nm) companyNameMap[nm.toLowerCase()] = { email: em, round: rnd, displayName: nm };
    if (em) emailMap[em] = { company: nm, round: rnd };
  }

  // ── 2. mail_log 맵 구성 ──
  var logRowMap     = {}; // 이메일 → 시트 행번호
  var alreadyFailed = {}; // 이미 실패 처리된 이메일
  var lRows = logSheet.getDataRange().getValues();
  for (var l = 1; l < lRows.length; l++) {
    var le = (lRows[l][4] || '').toString().trim().toLowerCase();
    var ls = (lRows[l][6] || '').toString().trim();
    if (!le) continue;
    logRowMap[le] = l + 1;
    if (ls === '실패') alreadyFailed[le] = true;
  }

  // ── 3. 라벨 확보 ──
  var LABEL = '대흥_반송처리완료';
  var doneLabel = GmailApp.getUserLabelByName(LABEL) || GmailApp.createLabel(LABEL);

  // ── 4. 반송 감지 패턴 ──
  var BOUNCE_RE = /주소를 찾을 수 없|메일이 전송되지 않|받을 수 없어|찾지 못하여|전송되지 않았|delivery.{0,30}fail|undeliverable|배달.*실패|no such user|user.*not found|does not exist|invalid.*address|도메인.*찾지|도메인.*없|no mx|mailbox.*full|over quota|spam|blocked|rejected|차단|temporarily|connection.*refused/i;

  var visited    = {};
  var newRecords = 0;
  var newDetails = [];

  // ── 5. 검색 쿼리 ──
  // 쿼리1: 우리 발송 스레드 전체 (라벨 제외 없음 - 이미 라벨된 것도 재검토)
  // → alreadyFailed 로 중복 방지
  var queries = [
    '"[대흥정밀]" "귀사" newer_than:30d',
    'from:(mailer-daemon@googlemail.com) newer_than:30d -label:' + LABEL,
    'from:(postmaster) newer_than:30d -label:' + LABEL,
    'subject:("Delivery Status Notification") newer_than:30d -label:' + LABEL,
    'subject:("배달 실패") newer_than:30d -label:' + LABEL,
    'subject:("배달 상태 알림") newer_than:30d -label:' + LABEL,
    'subject:(Undeliverable) newer_than:30d -label:' + LABEL
  ];

  for (var q = 0; q < queries.length; q++) {
    var threads;
    try {
      threads = GmailApp.search(queries[q], 0, 200);
    } catch (se) {
      Logger.log('[반송스캔] 검색실패: ' + queries[q] + ' / ' + se);
      continue;
    }

    for (var t = 0; t < threads.length; t++) {
      var thread = threads[t];
      var tid    = thread.getId();
      if (visited[tid]) continue;
      visited[tid] = true;

      var messages   = thread.getMessages();
      var threadSubj = thread.getFirstMessageSubject() || '';

      // 스레드 제목에서 회사명 추출 "[대흥정밀] 홀니스 귀사 파이프 임가공 협력 제안"
      var companyFromSubject = null;
      var sm = threadSubj.match(/\[대흥정밀\]\s+(.+?)\s+귀사/);
      if (sm) companyFromSubject = sm[1].trim();

      for (var m = 0; m < messages.length; m++) {
        var msg       = messages[m];
        var sender    = msg.getFrom()      || '';
        var plainBody = msg.getPlainBody() || '';
        var htmlBody  = msg.getRawContent() || msg.getBody() || '';
        // 텍스트 본문과 HTML/RAW 본문 모두 포함하여 검사
        var body      = plainBody + '\n' + htmlBody;
        var msubj     = msg.getSubject()   || '';
        var combined  = msubj + '\n' + body;

        // 발신자가 mailer-daemon / postmaster 거나 반송 키워드 포함 시 반송 처리
        var isSystemBounceSender = /mailer-daemon|postmaster/i.test(sender);
        if (!isSystemBounceSender && !BOUNCE_RE.test(combined)) continue;

        var errType = classifyBounceError(combined);

        // ── 방법 A: 스레드 제목의 회사명으로 매칭 (최우선) ──
        if (companyFromSubject) {
          var cinfo = companyNameMap[companyFromSubject.toLowerCase()];
          if (cinfo && cinfo.email && !alreadyFailed[cinfo.email]) {
            applyBounceLog(logSheet, logRowMap, emailMap, cinfo.email, errType);
            alreadyFailed[cinfo.email] = true;
            newRecords++;
            newDetails.push(cinfo.displayName + ' (' + cinfo.email + ') → ' + errType);
            Logger.log('[반송스캔] A(회사명): ' + cinfo.displayName + ' | ' + errType);
          }
        }

        // ── 방법 B: 본문의 이메일 주소로 매칭 (보완) ──
        var emailRe = /[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}/g;
        var found   = combined.match(emailRe) || [];
        var uniq    = {};
        for (var f = 0; f < found.length; f++) uniq[found[f].toLowerCase()] = true;
        for (var bounced in uniq) {
          if (!emailMap[bounced] || alreadyFailed[bounced]) continue;
          applyBounceLog(logSheet, logRowMap, emailMap, bounced, errType);
          alreadyFailed[bounced] = true;
          newRecords++;
          var ei = emailMap[bounced];
          newDetails.push(ei.company + ' (' + bounced + ') → ' + errType);
          Logger.log('[반송스캔] B(이메일): ' + ei.company + ' | ' + bounced + ' | ' + errType);
        }
      }

      try { thread.addLabel(doneLabel); } catch (le) {}
    }
  }

  // ── 6. 동기화 + 알림 ──
  if (newRecords > 0) {
    try { syncMailLogToCompany(); } catch (se) { Logger.log('[반송스캔] 동기화오류: ' + se); }
    try {
      var bodyLines = newDetails.map(function(d, idx) { return (idx + 1) + '. ' + d; }).join('\n');
      MailApp.sendEmail(
        'daeheungsteel@naver.com',
        '[대흥정밀] 반송 메일 자동처리 완료 (' + newRecords + '건)',
        '[대흥정밀 B2B 시스템] 반송 메일 자동 처리 결과\n\n처리 건수: ' + newRecords + '건\n처리 일시: ' +
        Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd HH:mm:ss') +
        '\n\n■ 처리 목록\n' + bodyLines + '\n\n* 구글 시트 mail_log 및 company 시트가 자동 업데이트되었습니다.'
      );
    } catch (me) { Logger.log('[반송스캔] 알림메일실패: ' + me); }
    Logger.log('[반송스캔] 완료 — ' + newRecords + '건 처리');
  } else {
    Logger.log('[반송스캔] 완료 — 신규 반송 없음');
  }

  return newRecords;
}

/** 에러 유형 분류 */
function classifyBounceError(text) {
  var t = text.toLowerCase();
  if (/주소를 찾을 수 없|찾지 못하여|받을 수 없어|전송되지 않았|no such user|user.*not found|does not exist|invalid.*address/.test(t)) return '수신자 없음 (주소 오류)';
  if (/도메인.*찾지|도메인.*없|no mx|domain.*not found/.test(t)) return '도메인 없음';
  if (/mailbox.*full|over quota|storage/.test(t)) return '메일함 용량 초과';
  if (/spam|blocked|rejected|차단/.test(t)) return '스팸/차단 거부';
  if (/temporarily|connection.*refused|timeout|일시적/.test(t)) return '일시적 오류 (재시도 필요)';
  return '반송 (이메일 오류)';
}

/** 기존 mail_log 행 업데이트 or 새 행 추가 */
function applyBounceLog(logSheet, logRowMap, emailMap, email, errType) {
  var existingRow = logRowMap[email];
  if (existingRow) {
    logSheet.getRange(existingRow, 7).setValue('실패');
    logSheet.getRange(existingRow, 8).setValue(errType);
    Logger.log('[반송스캔] 기존행 업데이트 행' + existingRow + ': ' + email);
  } else {
    var info = emailMap[email] || { company: email, round: '미상' };
    writeMailLog(info.company, email, info.round, '실패', errType);
    Logger.log('[반송스캔] 신규행 추가: ' + email);
  }
}


/**
 * 반송 자동 스캔 트리거 설치 (1회만 실행하면 됩니다)
 * 설치 후: 매 1시간마다 scanBounceEmails() 자동 실행
 */
function installBounceScanner() {
  // 기존 scanBounceEmails 트리거 제거
  ScriptApp.getProjectTriggers().forEach(function(tr) {
    if (tr.getHandlerFunction() === 'scanBounceEmails') {
      ScriptApp.deleteTrigger(tr);
    }
  });

  // 매 1시간 트리거 등록
  ScriptApp.newTrigger('scanBounceEmails')
    .timeBased()
    .everyHours(1)
    .create();

  SpreadsheetApp.getUi().alert(
    '✅ 자동 스캔 트리거 설치 완료!\n\n' +
    '📌 동작 방식:\n' +
    '  • 매 1시간마다 Gmail을 자동 확인\n' +
    '  • 반송 메일 감지 시 mail_log에 자동 기록\n' +
    '  • company 시트 N·O·P열 자동 동기화\n' +
    '  • 처리 완료 메일에 라벨 부착 (중복 방지)\n' +
    '  • 신규 반송 감지 시 대표 이메일로 요약 발송\n\n' +
    '💡 지금 즉시 실행: [📧 반송 메일 지금 스캔] 메뉴 사용'
  );
}


