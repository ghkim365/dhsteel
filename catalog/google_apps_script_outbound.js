/**
 * 대흥정밀 B2B 아웃바운드 이메일 자동 발송 Google Apps Script (GAS)
 *
 * [사용 방법]
 *   1. company 시트에서 발송할 업체의 A열 체크박스 체크
 *   2. 상단 "대흥 아웃바운드" → "선택 제안서 발송" 클릭
 *
 * [컬럼 구조 - company 시트]
 *   A:체크 | B:연번 | C:회사명 | D:주요 품목/카테고리 | E:대표 번호
 *   F:이메일 | G:사이트 주소 | H:지역 | I:주소 | J:사이트 상태
 *   K:전화번호 상태 | L:품질 | M:발송대기 | N:발송상태 | O:발송일
 *
 * [중복 발송 방지]
 *   N열(발송상태)이 이미 "정상발송"인 행은 A열 체크되어 있어도 자동 스킵
 */

var BASE_URL = "https://dhsteel.pages.dev/";

// ─────────────────────────────────────────────────────────────────────────────
// 메뉴 생성
// ─────────────────────────────────────────────────────────────────────────────
function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('대흥 아웃바운드')
    .addItem('📧 선택 제안서 발송', 'sendOutboundEmails')
    .addSeparator()
    .addItem('📊 발송 현황 확인', 'checkSendStatus')
    .addToUi();
}

// ─────────────────────────────────────────────────────────────────────────────
// 컬럼 인덱스 찾기 (0-based)
// ─────────────────────────────────────────────────────────────────────────────
function getColIndex(headers, candidates) {
  for (var i = 0; i < headers.length; i++) {
    var h = headers[i].toString().trim().toLowerCase();
    for (var j = 0; j < candidates.length; j++) {
      if (h.indexOf(candidates[j].toLowerCase()) !== -1) return i;
    }
  }
  return -1;
}

// ─────────────────────────────────────────────────────────────────────────────
// 발송 현황 확인
// ─────────────────────────────────────────────────────────────────────────────
function checkSendStatus() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('company');
  if (!sheet) { SpreadsheetApp.getUi().alert('[오류] company 시트를 찾을 수 없습니다.'); return; }

  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var emailColIdx = getColIndex(headers, ['이메일', 'email', '메일']);
  var sendStatusIdx = getColIndex(headers, ['발송상태']);
  var lastRow = sheet.getLastRow();
  var values = sheet.getRange(2, 1, lastRow - 1, sheet.getLastColumn()).getValues();

  var sent = 0, errCount = 0, pending = 0, noEmail = 0;
  for (var r = 0; r < values.length; r++) {
    var email = values[r][emailColIdx].toString().trim();
    var status = sendStatusIdx >= 0 ? values[r][sendStatusIdx].toString().trim() : '';
    if (!email || email.indexOf('@') < 0) { noEmail++; }
    else if (status === '정상발송') { sent++; }
    else if (status.indexOf('발송오류') === 0) { errCount++; }
    else { pending++; }
  }

  SpreadsheetApp.getUi().alert(
    '📊 발송 현황\n\n' +
    '  ✅ 정상발송:    ' + sent + '개\n' +
    '  ❌ 발송오류:    ' + errCount + '개\n' +
    '  📋 미발송 대기: ' + pending + '개\n' +
    '  ⬜ 이메일 없음: ' + noEmail + '개\n' +
    '  ──────────────────\n' +
    '  전체 업체:      ' + values.length + '개'
  );
}

// ─────────────────────────────────────────────────────────────────────────────
// 메인: A열 체크된 업체에 발송
// ─────────────────────────────────────────────────────────────────────────────
function sendOutboundEmails() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var sheet = ss.getSheetByName('company');
  if (!sheet) { SpreadsheetApp.getUi().alert('[오류] company 시트를 찾을 수 없습니다.'); return; }

  var lastRow = sheet.getLastRow();
  if (lastRow < 2) { SpreadsheetApp.getUi().alert('발송할 데이터가 없습니다.'); return; }

  // 헤더 파싱
  var headers = sheet.getRange(1, 1, 1, sheet.getLastColumn()).getValues()[0];
  var companyColIdx = getColIndex(headers, ['회사명', '업체명', '상호', '수신처']);
  var emailColIdx = getColIndex(headers, ['이메일', 'email', '메일']);
  var sendStatusIdx = getColIndex(headers, ['발송상태']);  // N열
  var sendDateIdx = getColIndex(headers, ['발송일']);     // O열

  if (companyColIdx < 0) companyColIdx = 2;  // C열 기본값
  if (emailColIdx < 0) emailColIdx = 5;  // F열 기본값

  if (sendStatusIdx < 0 || sendDateIdx < 0) {
    SpreadsheetApp.getUi().alert('[오류] N열(발송상태) 또는 O열(발송일) 헤더를 찾을 수 없습니다.\n헤더를 확인해주세요.');
    return;
  }

  // 전체 데이터 읽기
  var values = sheet.getRange(2, 1, lastRow - 1, sheet.getLastColumn()).getValues();

  // A열 체크된 행 수집
  var targets = [];
  var skipped = [];

  for (var r = 0; r < values.length; r++) {
    var isChecked = values[r][0];
    if (isChecked !== true && isChecked !== 'TRUE') continue;

    var company = values[r][companyColIdx].toString().trim() || '대표님';
    var email = values[r][emailColIdx].toString().trim();
    var status = values[r][sendStatusIdx].toString().trim();

    // ★ 중복 발송 방지: 이미 정상발송된 행은 스킵
    if (status === '정상발송') {
      skipped.push(company + ' (이미 발송됨)');
      sheet.getRange(r + 2, 1).setValue(false);
      continue;
    }

    // 유효 이메일 없으면 스킵
    if (!email || email.indexOf('@') < 0) {
      skipped.push(company + ' (이메일 없음)');
      sheet.getRange(r + 2, 1).setValue(false);
      continue;
    }

    targets.push({ rowNum: r + 2, company: company, email: email });
  }

  if (targets.length === 0) {
    var msg = '발송 대상이 없습니다.';
    if (skipped.length > 0) msg += '\n\n스킵된 업체 (' + skipped.length + '개):\n' + skipped.join('\n');
    SpreadsheetApp.getUi().alert(msg);
    return;
  }

  // 발송 전 확인창
  var previewLines = targets.map(function (t, i) {
    return (i + 1) + '. ' + t.company + '  →  ' + t.email;
  }).join('\n');
  var skipMsg = skipped.length > 0 ? '\n\n⚠️ 이미 발송됨(스킵): ' + skipped.length + '개' : '';

  var confirm = SpreadsheetApp.getUi().alert(
    '📧 발송 대상 확인 (' + targets.length + '개)',
    previewLines + skipMsg + '\n\n위 ' + targets.length + '개 업체에 발송하시겠습니까?',
    SpreadsheetApp.getUi().ButtonSet.YES_NO
  );
  if (confirm !== SpreadsheetApp.getUi().Button.YES) return;

  // 템플릿 로드
  var htmlTemplate = '';
  try {
    htmlTemplate = UrlFetchApp.fetch(BASE_URL + 'templates/dhsteel_proposal.html').getContentText('UTF-8');
  } catch (err) {
    SpreadsheetApp.getUi().alert('[오류] 템플릿 로드 실패: ' + err.toString());
    return;
  }

  // 인라인 이미지 사전 로드
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
    var imgUrl = cid === 'logo' ? BASE_URL + 'images/logo_dhsteel.png'
      : cid === 'pipe_swaging' ? BASE_URL + 'gallery/swaging_01.jpg'
        : cid === 'pipe_bending' ? BASE_URL + 'gallery/bending_01.jpg'
          : cid === 'pipe_custom' ? BASE_URL + 'gallery/custom_01.jpg'
            : BASE_URL + 'gallery/' + cid + '.jpg';
    try {
      var blob = UrlFetchApp.fetch(imgUrl).getBlob();
      blob.setName(cid);
      inlineImages[cid] = blob;
    } catch (e) {
      Logger.log('이미지 로드 실패 (' + cid + '): ' + e.toString());
    }
  }

  // 순차 발송
  var successCount = 0, failCount = 0, failList = [];
  var todayStr = Utilities.formatDate(new Date(), 'Asia/Seoul', 'yyyy-MM-dd');

  for (var t = 0; t < targets.length; t++) {
    var target = targets[t];
    var personalizedHtml = htmlTemplate.replace(/{회사명}/g, target.company);

    try {
      GmailApp.sendEmail(
        target.email,
        '[대흥정밀] ' + target.company + ' 귀사 파이프 임가공 협력 제안',
        '본 메일은 B2B 협력 제안서 메일입니다. HTML 형식을 지원하는 메일 클라이언트에서 확인해주세요.',
        { htmlBody: personalizedHtml, inlineImages: inlineImages }
      );

      sheet.getRange(target.rowNum, sendStatusIdx + 1).setValue('정상발송');  // N열
      sheet.getRange(target.rowNum, sendDateIdx + 1).setValue(todayStr);    // O열
      sheet.getRange(target.rowNum, 1).setValue(false);                        // A열 체크 해제

      successCount++;
      Utilities.sleep(800); // 과부하 방지
    } catch (err) {
      Logger.log('발송 오류 (' + target.email + '): ' + err.toString());
      sheet.getRange(target.rowNum, sendStatusIdx + 1).setValue('발송오류: ' + err.message);
      failCount++;
      failList.push(target.company + ' (' + target.email + ')');
    }
  }

  // 완료 알림
  var resultMsg =
    '📧 발송 완료\n\n' +
    '  ✅ 정상발송: ' + successCount + '건\n' +
    '  ❌ 발송오류: ' + failCount + '건\n' +
    '  ⏭️ 중복스킵: ' + skipped.length + '건';
  if (failList.length > 0) resultMsg += '\n\n오류 업체:\n' + failList.join('\n');

  SpreadsheetApp.getUi().alert(resultMsg);
}
