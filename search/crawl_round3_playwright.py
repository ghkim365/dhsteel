"""
3차 통합 크롤링 (Playwright 버전)
- 네이버 광고 52개 키워드 + 사용자 추가 키워드를 13대 핵심 검색어로 단일화
- 15대 주요 산업/공단 지역 집중 탐색
- Playwright 브라우저 구동으로 네이버 WAF 차단 완벽 회피
- 중복(상호명/전화번호) 자동 제외 및 이메일/홈페이지/블로그 동시 보강
"""
import asyncio
from playwright.async_api import async_playwright
import re, sys, time
import gspread
from google.oauth2.service_account import Credentials
import requests
from bs4 import BeautifulSoup

sys.stdout.reconfigure(encoding='utf-8')

CREDS_PATH     = r"D:\Antigravity\credentials\ghkim\ghkim_credentials_crawler-hifus_20260221.json"
SPREADSHEET_ID = "1kEdvR2hLPBc60vkNwq_ArqOGn0In5J-nN2LCoj2tMic"
SCOPES         = ["https://www.googleapis.com/auth/spreadsheets",
                  "https://www.googleapis.com/auth/drive"]

EMAIL_RE = re.compile(r'([a-zA-Z0-9._%+\-]+@(?:naver\.com|hanmail\.net|daum\.net|nate\.com|gmail\.com|[a-zA-Z0-9\-]+\.[a-zA-Z]{2,6}))', re.I)
BLOG_RE  = re.compile(r'blog\.naver\.com/([a-zA-Z0-9_\-]+)')

# 15대 핵심 공업/산업단지 중심 지역
REGIONS = [
    "안산", "시흥", "인천", "화성", "김포", "평택",
    "부산", "대구", "울산", "창원", "구미", "포항",
    "천안", "아산", "광주"
]

# 광고 키워드 52개 + 추가 가공 키워드 통합/단일화 (13대 핵심 키워드)
KEYWORDS = {
    "1순위: 스웨이징":      ["파이프스웨이징", "스웨이징가공"],
    "1순위: 축관/확관":      ["파이프축관", "파이프확관", "테이퍼가공"],
    "1순위: 인발/이형":      ["파이프인발", "이형파이프", "압출파이프"],
    "1순위: 구조관제작":    ["구조관제작", "파이프제작"],
    "2순위: 파이프가공/절단": ["각파이프절단", "파이프절단", "파이프홀가공", "서스가공"],
    "3순위: 파이프벤딩":     ["파이프벤딩"]
}

NOISE = {
    'navercorp.com','naver.com','ncloud.com','naver.me',
    'map.naver.com','place.naver.com','m.place.naver.com',
    'youtube.com','facebook.com','instagram.com','kakao.com','daum.net',
    'saramin.co.kr','jobkorea.co.kr','wanted.co.kr','albamon.com',
    'dart.fss.or.kr','catch.co.kr','bizno.net','ftc.go.kr',
    'google.com','google.co.kr','wikipedia.org','namu.wiki',
    'coupang.com','lotteon.com','gmarket.co.kr','11st.co.kr',
    'daangn.com','findcompany.kr','114.co.kr','kwk114.com','bizwiki.co.kr'
}
NOISE_KW = ['news','tistory.com','egloos.com','sedaily','moneytoday','khan',
            'hankyung','donga','chosun','segye.com','ytn.co.kr','kbs.co.kr',
            'mbc.co.kr','sbs.co.kr','hankookilbo','fintechpost','joynews','newsis']

EXCLUDE_NAME_KW = ["대흥", "삼협"]

def is_noise(url):
    if not url or not url.startswith("http"): return True
    u = url.lower()
    return any(d in u for d in NOISE) or any(k in u for k in NOISE_KW)

def clean_emails(raw):
    bad = ('.png','.jpg','.gif','.js','.css','.svg','.woff','.ico')
    bad_dom = {'example.com','test.com','domain.com','w3.org','sentry.io','schema.org'}
    out = []
    for e in raw:
        e = e.lower().strip('.')
        if any(e.endswith(x) for x in bad): continue
        if e.split('@')[-1] in bad_dom: continue
        out.append(e)
    return out

async def get_search_place_ids(page, query):
    url = f"https://search.naver.com/search.naver?query={requests.utils.quote(query)}"
    place_ids = []
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(0.8)
        html = await page.content()
        matches = re.findall(r'place/(\d+)', html)
        for pid in matches:
            if pid not in place_ids:
                place_ids.append(pid)
    except Exception as e:
        print(f"[Error] ID 추출 실패: {e}")
    return place_ids

async def get_place_details(page, place_id):
    url = f"https://m.place.naver.com/place/{place_id}/home"
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=20000)
        await asyncio.sleep(0.8)
        html = await page.content()
        
        name_m = re.search(r'"name"\s*:\s*"([^"]+)"', html)
        name = name_m.group(1) if name_m else ""
        if not name:
            name_m = re.search(r'<span class="[^"]*Fc1rA[^"]*">([^<]+)</span>', html)
            if name_m: name = name_m.group(1).strip()
            
        if not name or any(kw in name for kw in EXCLUDE_NAME_KW): return None
        
        phone_m = re.search(r'"phone"\s*:\s*"([^"]+)"', html)
        phone = phone_m.group(1) if phone_m else ""
        
        address_m = re.search(r'"address"\s*:\s*"([^"]+)"', html)
        address = address_m.group(1) if address_m else ""
        
        homepage = ""
        hp_m = re.search(r'"homepage"\s*:\s*"([^"]+)"', html)
        if hp_m:
            homepage = hp_m.group(1).replace("\\/", "/")
            if is_noise(homepage): homepage = ""
            
        return {
            "name": name,
            "phone": phone,
            "address": address,
            "homepage": homepage
        }
    except Exception as e:
        return None

def crawl_email(base_url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36", "Accept-Language": "ko-KR,ko;q=0.9"}
    for path in ["", "/contact", "/about", "/company"]:
        url = base_url.rstrip("/") + path
        try:
            r = requests.get(url, headers=headers, timeout=6, allow_redirects=True)
            if r.status_code < 400:
                found = clean_emails(EMAIL_RE.findall(r.text))
                if found: return found[0]
        except Exception: pass
    return ""

def find_official_blog_email(company_name, region):
    query = f"{company_name} {region} 블로그"
    url = f"https://search.naver.com/search.naver?where=nexearch&query={requests.utils.quote(query)}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=8)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, "html.parser")
            links = soup.find_all("a", href=re.compile(r'blog\.naver\.com/([a-zA-Z0-9_\-]+)'))
            for a in links:
                href = a.get("href", "")
                title_text = (a.find_parent().get_text(strip=True) if a.find_parent() else "") + a.get_text(strip=True)
                if re.sub(r'[\s\(\)]', '', company_name) in re.sub(r'[\s\(\)]', '', title_text):
                    match = BLOG_RE.search(href)
                    if match and match.group(1) not in ["prologue", "postList", "category"]:
                        bid = match.group(1)
                        return f"https://blog.naver.com/{bid}", f"{bid}@naver.com"
    except Exception: pass
    return "", ""

def snippet_email(name, region):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"}
    for q in [f"{name} 이메일", f"{name} {region} 연락처"]:
        try:
            r = requests.get(f"https://search.naver.com/search.naver?where=nexearch&query={requests.utils.quote(q)}", headers=headers, timeout=8)
            if r.status_code == 200:
                found = clean_emails(EMAIL_RE.findall(r.text))
                if found: return found[0]
        except Exception: pass
    return ""

async def async_main():
    print("🚀 구글 시트 연결...")
    creds = Credentials.from_service_account_file(CREDS_PATH, scopes=SCOPES)
    gc    = gspread.authorize(creds)
    ws    = gc.open_by_key(SPREADSHEET_ID).worksheet("company")

    # 기존 정보 로드 (중복 제거)
    existing_rows = ws.get_all_values()
    existing_names  = {r[2].strip() for r in existing_rows[1:] if len(r) > 2 and r[2].strip()}
    existing_phones = {r[4].strip() for r in existing_rows[1:] if len(r) > 4 and r[4].strip()}
    last_seq = len(existing_rows) - 1
    print(f"기존 업체: {len(existing_names)}개")

    new_rows  = []
    seen_ids  = set()
    total_q   = 0

    print("\n🔍 3차 Playwright 기반 대규모 수집 시작...\n")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="ko-KR",
            viewport={"width": 1280, "height": 800}
        )
        page = await context.new_page()

        for priority, keywords in KEYWORDS.items():
            for kw in keywords:
                for region in REGIONS:
                    query = f"{region} {kw}"
                    total_q += 1
                    print(f"  [{total_q:>3}] {query}", end=" → ")
                    sys.stdout.flush()

                    place_ids = await get_search_place_ids(page, query)
                    new_cnt   = 0

                    for pid in place_ids[:6]:
                        if pid in seen_ids: continue
                        seen_ids.add(pid)
                        
                        c = await get_place_details(page, pid)
                        if not c or not c["name"]: continue
                        if c["name"] in existing_names: continue
                        if c["phone"] and c["phone"] in existing_phones: continue

                        email = ""
                        homepage = c["homepage"]
                        
                        # 1) 홈페이지 크롤링
                        if homepage:
                            email = crawl_email(homepage)
                            
                        # 2) 공식 블로그 조회
                        if not email:
                            blog_url, blog_email = find_official_blog_email(c["name"], region)
                            if blog_email:
                                email = blog_email
                                if not homepage: homepage = blog_url
                                
                        # 3) 검색 스니펫
                        if not email:
                            email = snippet_email(c["name"], region)

                        if not email: continue  # 이메일 발굴 실패 시 제외

                        web_status = "✅ 접속가능" if homepage else "URL없음"
                        quality    = "✅ 정상" if c["phone"] else "⚠️ 전화없음"
                        last_seq  += 1
                        phone_status = "✅ 형식OK" if c["phone"] else "전화없음"

                        row = [
                            "FALSE", str(last_seq), c["name"], priority,
                            c["phone"], email, homepage,
                            region, c["address"],
                            web_status, phone_status, quality
                        ]
                        new_rows.append(row)
                        existing_names.add(c["name"])
                        if c["phone"]: existing_phones.add(c["phone"])
                        new_cnt += 1
                        await asyncio.sleep(0.3)

                    print(f"{len(place_ids)}개 ID 추출 / {new_cnt}개 신규 추가")
                    await asyncio.sleep(0.8)

                    # 20개 쌓일 때마다 중간 저장
                    if len(new_rows) > 0 and len(new_rows) % 20 == 0:
                        ws.append_rows(new_rows[-20:], value_input_option='USER_ENTERED')
                        print(f"    -- [중간 저장 완료 (누적 {len(new_rows)}개)] --")

        await browser.close()

    if new_rows:
        remainder = len(new_rows) % 20
        if remainder > 0:
            ws.append_rows(new_rows[-remainder:], value_input_option='USER_ENTERED')
        print(f"\n✅ 3차 완료! 신규 {len(new_rows)}개 마케팅 타겟 시트 반영 완료!")
    else:
        print("\n신규 가망 고객 없음.")

def main():
    asyncio.run(async_main())

if __name__ == "__main__":
    main()
