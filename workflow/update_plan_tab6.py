# -*- coding: utf-8 -*-
"""
update_plan_tab6.py
plan/dhsteel_plan_2026.html에 6번째 독립 탭 추가:
[📘 6. B2B 주간 발송 실무 매뉴얼 (메일·반송스캔·팩스)]
"""

import os, sys

sys.stdout.reconfigure(encoding='utf-8')

plan_path = r'E:\Antigravity\builder-dhsteel-sales\plan\dhsteel_plan_2026.html'

with open(plan_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. 탭 버튼 추가 (tab-sop 뒤에 tab-manual 추가)
target_btn = """    <button type="button" class="plan-tab-btn" onclick="switchPlanTab('tab-sop')">
      📖 5. B2B 정기 발송 표준운영절차 (SOP)
    </button>"""

replacement_btn = """    <button type="button" class="plan-tab-btn" onclick="switchPlanTab('tab-sop')">
      📖 5. B2B 정기 발송 표준운영절차 (SOP)
    </button>
    <button type="button" class="plan-tab-btn" onclick="switchPlanTab('tab-manual')">
      📘 6. B2B 주간 발송 실무 매뉴얼 (메일·스캔·팩스)
    </button>"""

if 'switchPlanTab(\'tab-manual\')' not in html:
    if target_btn in html:
        html = html.replace(target_btn, replacement_btn)
        print('[성공] 탭 네비게이션 버튼 6 추가 완료.')
    else:
        print('[경고] target_btn 문자열을 찾지 못했습니다.')

# 2. 탭 컨텐츠 추가
tab_manual_content = """
  <!-- ============================================================== -->
  <!-- TAB 6: B2B 주간 발송 실무 매뉴얼 (메일·반송스캔·팩스) -->
  <!-- ============================================================== -->
  <div id="tab-manual" class="plan-tab-pane">

    <!-- 개요 & 타임라인 카드 -->
    <div class="card" style="border-left: 5px solid #2563EB;">
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:10px;">
        <h3 class="card-title" style="margin-bottom:0; border-bottom:none; padding-bottom:0;">
          📘 대흥정밀 B2B 주간 아웃바운드 통합 실무 매뉴얼
        </h3>
        <span class="badge badge-primary">실무 표준 SOP (2026-11-23 최신 개정)</span>
      </div>
      <p style="font-size:14px; color:#475569; margin-bottom:16px;">
        본 매뉴얼은 매주 월요일과 목요일 집행되는 <strong>이메일 발송</strong>, <strong>반송 메일 자동 감지</strong>, <strong>팩스 발송 및 실패 전환</strong>의 전 과정을 실무자 관점에서 체계화한 통합 표준 가이드입니다.
        더 이상 <strong>보낸메일함을 수동으로 캡처하실 필요 없이</strong>, 시스템이 100% 무인 자동 감지 및 처리합니다.
      </p>

      <!-- 주간 타임라인 표 -->
      <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:10px; padding:16px; margin-top:10px;">
        <h4 style="font-size:14px; font-weight:800; color:#1E293B; margin-bottom:10px;">🗓️ 주간 업무 타임라인 (Weekly Schedule at a Glance)</h4>
        <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap:12px;">
          <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:12px;">
            <div style="font-size:12px; font-weight:800; color:#2563EB; margin-bottom:4px;">1단계 | 월요일 10:00</div>
            <div style="font-size:13.5px; font-weight:700; color:#0F172A; margin-bottom:4px;">📬 정기 이메일 발송 (70건)</div>
            <div style="font-size:12px; color:#64748B;">시트 A열 체크박스 확인 후 [선택 제안서 발송] 클릭 (Gmail API)</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:12px;">
            <div style="font-size:12px; font-weight:800; color:#10B981; margin-bottom:4px;">2단계 | 월~화요일 (상시)</div>
            <div style="font-size:13.5px; font-weight:700; color:#0F172A; margin-bottom:4px;">📧 반송 자동 감지 &amp; 팩스 전환</div>
            <div style="font-size:12px; color:#64748B;">트리거 매 1시간 무인 감지 / 반송 업체 팩스 발송군 자동 분류</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:12px;">
            <div style="font-size:12px; font-weight:800; color:#8B5CF6; margin-bottom:4px;">3단계 | 목요일 14:00</div>
            <div style="font-size:13.5px; font-weight:700; color:#0F172A; margin-bottom:4px;">📠 센드랩스 팩스 발송 (30건)</div>
            <div style="font-size:12px; color:#64748B;">팩스 전용 제조사 + 메일 실패사 흡수 단축 제안서 일괄 전송</div>
          </div>
          <div style="background:#FFFFFF; border:1px solid #CBD5E1; border-radius:8px; padding:12px;">
            <div style="font-size:12px; font-weight:800; color:#F59E0B; margin-bottom:4px;">4단계 | 마감 &amp; 보고서</div>
            <div style="font-size:13.5px; font-weight:700; color:#0F172A; margin-bottom:4px;">🤝 에이전트 자동 리포팅</div>
            <div style="font-size:12px; color:#64748B;">채팅창 "발송 완료" 알림 시 주간 성과 워드(.docx) 자동 발행</div>
          </div>
        </div>
      </div>
    </div>

    <!-- 파트 1: 이메일 발송 실무 프로세스 -->
    <div class="card">
      <h3 class="card-title">📬 파트 1: 주간 이메일 발송 실무 프로세스 (매주 월요일 오전 10:00)</h3>
      
      <div style="display:flex; flex-direction:column; gap:14px; margin-top:14px;">
        <!-- STEP 1 -->
        <div style="border:1px solid #E2E8F0; border-radius:8px; padding:14px; background:#FFFFFF;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
            <span class="badge badge-primary">STEP 1</span>
            <strong style="font-size:14px; color:#1E293B;">구글 스프레드시트 대상 및 체크박스 확인</strong>
          </div>
          <ul style="font-size:13px; color:#475569; margin-left:20px; line-height:1.7;">
            <li>구글 스프레드시트(<code>builder-dhsteel_data</code>) 접속</li>
            <li><strong>A열 체크박스 타입 확인</strong>: 반드시 파란색 네모 체크박스(☑ True) 형태여야 합니다. (문자열 <code>"TRUE"</code>로 들어가면 Apps Script의 <code>values[r][0] !== true</code> 조건에 걸려 <strong>발송이 스킵</strong>됩니다.)</li>
            <li><strong>발송 대상 확인</strong>: 금주 발송 대상 업체 68~70개사에 체크박스(☑) 및 M열(발송회차: 예 '3차 정기(11/23)') 확인</li>
          </ul>
        </div>

        <!-- STEP 2 -->
        <div style="border:1px solid #E2E8F0; border-radius:8px; padding:14px; background:#FFFFFF;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
            <span class="badge badge-primary">STEP 2</span>
            <strong style="font-size:14px; color:#1E293B;">발송 전용 계정 로그인 확인</strong>
          </div>
          <ul style="font-size:13px; color:#475569; margin-left:20px; line-height:1.7;">
            <li>발송 프로그램(Gmail API)은 <strong>현재 스프레드시트를 열고 있는 구글 계정</strong>의 권한으로 메일을 발송합니다.</li>
            <li>브라우저 상단 프로필이 <strong>발송 전용 계정 (<code>dhsteel7@gmail.com</code>)</strong>으로 로그인되어 있는지 반드시 확인합니다.</li>
          </ul>
        </div>

        <!-- STEP 3 -->
        <div style="border:1px solid #E2E8F0; border-radius:8px; padding:14px; background:#FFFFFF;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
            <span class="badge badge-primary">STEP 3</span>
            <strong style="font-size:14px; color:#1E293B;">원클릭 발송 실행</strong>
          </div>
          <ul style="font-size:13px; color:#475569; margin-left:20px; line-height:1.7;">
            <li>스프레드시트 상단 메뉴바에서 <strong>[대흥 아웃바운드]</strong> 클릭</li>
            <li><strong>[선택 제안서 발송 (v1/v2 자동분기)]</strong> 클릭</li>
            <li>프로그램이 이전 발송 성공 이력을 자동 판별하여 <code>v1(신규 협력제안)</code> 또는 <code>v2(정기 리마인드)</code> 맞춤 HTML 제안서를 자동 분기 발송합니다.</li>
            <li>발송 완료 팝업창(<strong>"발송 완료: 성공 N건 / 실패 0건"</strong>) 확인 후 확인 버튼 클릭</li>
          </ul>
        </div>

        <!-- STEP 4 -->
        <div style="border:1px solid #E2E8F0; border-radius:8px; padding:14px; background:#FFFFFF;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
            <span class="badge badge-primary">STEP 4</span>
            <strong style="font-size:14px; color:#1E293B;">시트 자동 기록 상태 확인</strong>
          </div>
          <ul style="font-size:13px; color:#475569; margin-left:20px; line-height:1.7;">
            <li>발송된 행은 A열 체크박스가 자동으로 해제(☐)됩니다.</li>
            <li>N열(발송상태: '성공'), O열(발송일시), P열(결과: 'Gmail API 발송 완료')이 자동 갱신됩니다.</li>
            <li><code>mail_log</code> 워크시트 맨 하단에 신규 발송 이력 N건이 자동으로 누적 기록됩니다.</li>
          </ul>
        </div>
      </div>
    </div>

    <!-- 파트 2: 반송 메일 감지 및 스캔 프로세스 -->
    <div class="card">
      <h3 class="card-title">📧 파트 2: 반송 메일 감지 &amp; 스캔 프로세스 (더 이상 수동 캡처 불필요!)</h3>

      <div class="tip-box green" style="margin-bottom:16px;">
        💡 <strong>핵심 안내</strong>: 과거처럼 보낸메일함이나 받은편지함을 일일이 확인하고 실패 화면을 캡처해서 전달하실 필요가 전혀 없습니다!
        스프레드시트에 내장된 <strong>[Gmail 반송 메일 자동 파싱 엔진]</strong>이 백그라운드에서 모든 반송을 100% 자동 감지하고 분류합니다.
      </div>

      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap:16px; margin-bottom:16px;">
        <!-- 방법 1 -->
        <div style="border:1px solid #CBD5E1; border-radius:10px; padding:16px; background:#F8FAFC;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span class="badge badge-success">기본 방식 (권장)</span>
            <strong style="font-size:14.5px; color:#166534;">⏰ 1회 설치 무인 자동 감지</strong>
          </div>
          <p style="font-size:13px; color:#334155; margin-bottom:10px;">
            메뉴에서 <strong>[대흥 아웃바운드] → [⏰ 자동 스캔 트리거 설치 (1회)]</strong>를 딱 한 번만 눌러두면 세팅 완료!
          </p>
          <ul style="font-size:12.5px; color:#475569; margin-left:18px; line-height:1.6;">
            <li>구글 클라우드 서버가 <strong>매 1시간마다 Gmail 수신함을 자동 조회</strong></li>
            <li>반송 메일(Mailer-Daemon, Delivery Status Notification) 발견 시 시트 자동 실패 처리</li>
            <li>신규 반송 발생 시 대표님 이메일(<code>daeheungsteel@naver.com</code>)로 요약 리포트 자동 발송</li>
            <li>발송 후 시트를 닫아도 알아서 작동합니다.</li>
          </ul>
        </div>

        <!-- 방법 2 -->
        <div style="border:1px solid #CBD5E1; border-radius:10px; padding:16px; background:#F8FAFC;">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:8px;">
            <span class="badge badge-info">즉시 확인용</span>
            <strong style="font-size:14.5px; color:#075985;">📧 원클릭 수동 즉시 스캔</strong>
          </div>
          <p style="font-size:13px; color:#334155; margin-bottom:10px;">
            발송 직후 바로 반송 여부를 확인하고 싶을 때 사용하는 원클릭 메뉴입니다.
          </p>
          <ul style="font-size:12.5px; color:#475569; margin-left:18px; line-height:1.6;">
            <li>스프레드시트 메뉴 <strong>[대흥 아웃바운드] → [📧 반송 메일 지금 스캔]</strong> 클릭</li>
            <li>즉시 최근 30일 이내의 모든 반송 알림 메일을 실시간 정밀 스캔</li>
            <li>발견된 실패 업체를 <code>mail_log</code>와 <code>company</code> 시트에 즉시 반영</li>
            <li>캡처를 찍거나 메일함을 열람할 필요가 전혀 없습니다.</li>
          </ul>
        </div>
      </div>

      <!-- 5대 에러 분류 표 -->
      <h4 style="font-size:14px; font-weight:800; color:#1E293B; margin-bottom:8px;">🔍 반송 에러 5대 유형 및 자동 분류 기준</h4>
      <table class="data-table">
        <thead>
          <tr>
            <th style="width:22%;">자동 분류 에러명</th>
            <th style="width:25%;">감지 키워드 / 프로토콜 코드</th>
            <th style="width:25%;">발생 원인</th>
            <th style="width:28%;">시스템 후속 처리</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="badge badge-danger">수신자 없음 (주소 오류)</span></td>
            <td><code>550 No such user</code>, <code>invalid address</code></td>
            <td>퇴사 담당자 메일 삭제, 계정 오탈자</td>
            <td><strong>즉시 팩스 발송 대상군으로 자동 전환</strong></td>
          </tr>
          <tr>
            <td><span class="badge badge-warning">도메인 없음</span></td>
            <td><code>No MX</code>, <code>Domain not found</code></td>
            <td>기업 폐업, 도메인 만료/오타</td>
            <td>영구 제외 처리 또는 사업자 팩스 조회</td>
          </tr>
          <tr>
            <td><span class="badge badge-info">메일함 용량 초과</span></td>
            <td><code>Mailbox full</code>, <code>Over quota</code></td>
            <td>상대방 웹메일 서버 용량 부족</td>
            <td>1회 재시도 후 미수신 시 팩스 전환</td>
          </tr>
          <tr>
            <td><span class="badge badge-danger">스팸/차단 거부</span></td>
            <td><code>554 Blocked</code>, <code>Rejected</code>, <code>Spam</code></td>
            <td>상대 사내 메일 보안 게이트웨이 차단</td>
            <td><strong>즉시 팩스 발송군으로 우선 전환</strong></td>
          </tr>
          <tr>
            <td><span class="badge badge-primary">일시적 오류</span></td>
            <td><code>Connection refused</code>, <code>Timeout</code></td>
            <td>상대방 메일 서버 일시 다운/점검</td>
            <td>차주 월요일 자동 재발송 대상 유지</td>
          </tr>
        </tbody>
      </table>

      <!-- 계정 바인딩 주의사항 -->
      <div style="background:#FFFBEB; border:1px solid #FCD34D; border-radius:8px; padding:14px; margin-top:14px;">
        <strong style="color:#92400E; font-size:13.5px;">⚠️ 계정 바인딩 주의사항 (반드시 숙지)</strong>
        <p style="font-size:12.5px; color:#78350F; margin-top:6px; line-height:1.6;">
          구글 보안 규정상, 자동 스캔 프로그램은 <strong>"트리거를 설치한 바로 그 계정의 Gmail 편지함"만 읽을 수 있습니다.</strong><br>
          • 반드시 메일 발송과 스프레드시트 관리는 <strong>공식 계정(<code>dhsteel7@gmail.com</code>) 하나로만 로그인</strong>하여 사용해야 합니다.<br>
          • 만약 다른 개인 계정으로 로그인하여 메일을 보내면, 프로그램이 다른 계정의 메일함을 들여다볼 수 없어 반송 감지가 되지 않습니다.<br>
          • 향후 발송 계정을 변경할 때는, 새 계정으로 로그인 후 <code>[⏰ 자동 스캔 트리거 설치 (1회)]</code>를 다시 눌러주시면 새 계정으로 자동 연동됩니다.
        </p>
      </div>
    </div>

    <!-- 파트 3: 팩스 발송 & 메일 실패 전환 프로세스 -->
    <div class="card">
      <h3 class="card-title">📠 파트 3: 주간 팩스 발송 &amp; 메일 실패 전환 프로세스 (매주 목요일 오후 14:00)</h3>
      <p style="font-size:14px; color:#475569; margin-bottom:14px;">
        이메일 확인율이 낮거나 현장 공장 중심인 제조기업, 그리고 <strong>월요일 이메일 발송에서 반송·차단된 업체</strong>를 대상으로 
        <strong>센드랩스(SendLabs) 대량 팩스 엔진</strong>을 통해 직관적인 1장 규격의 단축 제안서를 발송합니다.
      </p>

      <div style="display:grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap:14px; margin-bottom:16px;">
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:14px;">
          <h4 style="font-size:13.5px; font-weight:800; color:#1E293B; margin-bottom:6px;">1. 타겟 대상 선정 기준</h4>
          <ul style="font-size:12.5px; color:#475569; margin-left:16px; line-height:1.6;">
            <li><strong>핵심 군 (우량 팩스사)</strong>: 파이프 클램프, 조인트, 밴딩 가공 실수요처 20~22개사</li>
            <li><strong>전환 군 (메일 실패사)</strong>: 월요일 메일 반송/차단 업체(예: 아이디오, 대명기업 등) 자동 흡수 8~10개사</li>
            <li><strong>주간 총 발송 규모</strong>: 30개사 일괄 로테이션</li>
          </ul>
        </div>
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:14px;">
          <h4 style="font-size:13.5px; font-weight:800; color:#1E293B; margin-bottom:6px;">2. 발송 규격 및 플랫폼</h4>
          <ul style="font-size:12.5px; color:#475569; margin-left:16px; line-height:1.6;">
            <li><strong>발송 플랫폼</strong>: 센드랩스 (https://www.sendlabs.co.kr)</li>
            <li><strong>발송 문서</strong>: <code>sales/대흥정밀_파이프임가공_팩스전용_단축제안서.pdf</code></li>
            <li><strong>문서 특징</strong>: A4 1장 흑백 인쇄 가독성 극대화, 파이프 확관/벤딩/절단 가공 사례 요약</li>
          </ul>
        </div>
      </div>

      <!-- 팩스 실무 4단계 -->
      <div style="border:1px solid #E2E8F0; border-radius:8px; padding:14px; background:#FFFFFF;">
        <h4 style="font-size:13.5px; font-weight:800; color:#1E293B; margin-bottom:10px;">📋 목요일 팩스 발송 실무 순서</h4>
        <ol style="font-size:13px; color:#475569; margin-left:20px; line-height:1.7;">
          <li><strong>타겟 명단 추출</strong>: 구글 시트 <code>company</code>에서 팩스 대상사 30개사 팩스번호(D열) 검증</li>
          <li><strong>센드랩스 로그인</strong>: 대흥정밀 계정 접속 및 전송 캐시(약 30건 분량) 확인</li>
          <li><strong>문서 첨부 및 전송</strong>: 단축 제안서 PDF 업로드 후 30개사 일괄 전송 예약 또는 즉시 발송</li>
          <li><strong>결과 시트 반영</strong>: 발송 완료 후 <code>fax_log</code> 시트에 기록 추가 및 <code>company</code> 시트 N열을 '팩스 성공'으로 갱신</li>
        </ol>
      </div>
    </div>

    <!-- 파트 4: 에이전트 연계 후속 마감 -->
    <div class="card">
      <h3 class="card-title">🤝 파트 4: 에이전트 연계 후속 마감 및 통합 대시보드 SOP</h3>
      <p style="font-size:14px; color:#475569; margin-bottom:12px;">
        발송 작업을 마치신 후에는 복잡한 수기 작업 없이, Antigravity 에이전트와 아래와 같이 대화 한마디로 마감하시면 됩니다.
      </p>

      <div style="display:flex; flex-direction:column; gap:10px;">
        <div style="display:flex; gap:12px; align-items:flex-start; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px;">
          <span style="font-weight:800; color:#2563EB; font-size:13px; min-width:80px;">사용자 알림</span>
          <div style="font-size:13px; color:#1E293B;">
            채팅창에 <strong>"오늘 68개사 발송 완료했어. 로그 정리하고 보고서 만들어줘."</strong> 라고 전달
          </div>
        </div>
        <div style="display:flex; gap:12px; align-items:flex-start; background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:12px;">
          <span style="font-weight:800; color:#10B981; font-size:13px; min-width:80px;">에이전트 처리</span>
          <div style="font-size:13px; color:#475569; line-height:1.6;">
            1. 스프레드시트 <code>mail_log</code> 및 <code>fax_log</code> 실시간 검증<br>
            2. <code>schedule</code> 시트에 금주 집행 데이터 자동 동기화<br>
            3. 사용자 표준 서식(맑은 고딕 10pt)에 맞춘 <strong>주간 결과 보고서(.docx) 자동 생성 및 링크 제공</strong><br>
            4. 마스터 플랜(<code>dhsteel_plan_2026.html</code>) 이력 Phase 업데이트 및 <code>dist_deploy</code> 패키지 자동 동기화
          </div>
        </div>
      </div>
    </div>

  </div>
"""

# tab-sop 뒤에 tab-manual 삽입
if 'id="tab-manual"' not in html:
    # Find end of tab-sop div
    # tab-sop begins with <div id="tab-sop"
    idx_sop = html.find('id="tab-sop"')
    if idx_sop != -1:
        # Find the closing </div> of tab-sop
        # Let's find <!-- ============================================================== --> after tab-sop or </div>\n</div>\n</body>
        # Actually let's find the closing of tab-sop
        idx_end_container = html.rfind('</div>\n\n<script>')
        if idx_end_container == -1:
            idx_end_container = html.rfind('</div>\n<script>')
        if idx_end_container == -1:
            idx_end_container = html.rfind('<script>')
            
        html = html[:idx_end_container] + tab_manual_content + '\n' + html[idx_end_container:]
        print('[성공] tab-manual 컨텐츠 삽입 완료.')
    else:
        print('[경고] tab-sop를 찾을 수 없습니다.')

with open(plan_path, 'w', encoding='utf-8') as f:
    f.write(html)

print('[완료] plan/dhsteel_plan_2026.html 업데이트 완료.')

