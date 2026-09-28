"""학교알리미 OpenAPI 수집 스크립트.

사용법:
  export SCHOOLINFO_API_KEY=...        # 학교알리미 OpenAPI 키
  python scripts/schoolinfo.py probe --region 강남구
      -> apiType 0~99를 훑어 응답이 오는 코드와 필드명을 출력한다.
         (교과별 학업성취사항, 졸업생 진로 현황 코드를 확인하는 용도)
  python scripts/schoolinfo.py fetch --region 강남구 --region 아산시 --types 0 <성취코드> <진로코드>
      -> data/raw/{지역}_{apiType}_{연도}.json 으로 저장한다.
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

ENDPOINT = "https://www.schoolinfo.go.kr/openApi.do"
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"

# 행정표준코드 (시도 2자리, 시군구 5자리)
REGIONS = {
    "강남구": {"sidoCode": "11", "sggCode": "11680"},
    "아산시": {"sidoCode": "44", "sggCode": "44200"},
}

# 공개된 예제 코드에서 확인된 apiType. 성취·진로 코드는 probe로 확인한다.
KNOWN_TYPES = {
    "0": "학교기본정보",
    "09": "학년별·학급별 학생수",
    "10": "전·출입 및 학업중단",
    "51": "입학생 현황",
    "63": "성별 학생수",
}

HIGH_SCHOOL = "04"


def call(api_key, api_type, year, region):
    params = {
        "apiKey": api_key,
        "apiType": api_type,
        "pbanYr": str(year),
        "schulKndCode": HIGH_SCHOOL,
        **REGIONS[region],
    }
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        body = resp.read().decode("utf-8")
    return json.loads(body)


def rows_of(payload):
    """응답 JSON에서 학교별 레코드 목록을 꺼낸다 (최상위 키 이름에 의존하지 않음)."""
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        for value in payload.values():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                return value
    return []


def get_key():
    key = os.environ.get("SCHOOLINFO_API_KEY")
    if not key:
        sys.exit("SCHOOLINFO_API_KEY 환경 변수가 없습니다.")
    return key


def probe(args):
    key = get_key()
    region = args.region[0]
    for n in range(100):
        for api_type in {str(n), f"{n:02d}"}:
            try:
                rows = rows_of(call(key, api_type, args.year, region))
            except Exception:  # 잘못된 코드는 오류/빈 응답
                rows = []
            if rows:
                fields = ", ".join(list(rows[0].keys())[:25])
                print(f"[{api_type}] {len(rows)}행  {KNOWN_TYPES.get(api_type, '')}\n    {fields}")
            time.sleep(0.2)


def fetch(args):
    key = get_key()
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for region in args.region:
        for api_type in args.types:
            rows = rows_of(call(key, api_type, args.year, region))
            out = RAW_DIR / f"{region}_{api_type}_{args.year}.json"
            out.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
            print(f"{out.name}: {len(rows)}행")
            time.sleep(0.2)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name, func in (("probe", probe), ("fetch", fetch)):
        p = sub.add_parser(name)
        p.add_argument("--region", action="append", required=True, choices=sorted(REGIONS))
        p.add_argument("--year", type=int, default=2026, help="공시연도 (기본 2026)")
        if name == "fetch":
            p.add_argument("--types", nargs="+", required=True, help="apiType 코드들")
        p.set_defaults(func=func)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
