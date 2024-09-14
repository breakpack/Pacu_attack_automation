import re
from datetime import datetime, timedelta
import subprocess
import json
import os

def aws_cli_login(access_key_id, secret_access_key):
    # AWS CLI에 Access Key와 Secret Access Key 설정
    subprocess.run(["aws", "configure", "set", "aws_access_key_id", access_key_id])
    subprocess.run(["aws", "configure", "set", "aws_secret_access_key", secret_access_key])
    print("AWS CLI에 로그인되었습니다.")

# 한글 월을 숫자 월로 변환하는 사전
month_map = {
    "1월": "01", "2월": "02", "3월": "03", "4월": "04",
    "5월": "05", "6월": "06", "7월": "07", "8월": "08",
    "9월": "09", "10월": "10", "11월": "11", "12월": "12"
}

def convert_to_utc(kst_time_str):
    # 한글 월을 숫자 월로 치환
    for korean_month, numeric_month in month_map.items():
        kst_time_str = kst_time_str.replace(korean_month, numeric_month)

    # 'KST'와 요일 같은 불필요한 텍스트를 제거
    kst_time_str = re.sub(r'[^\d\s]', '', kst_time_str)  # 숫자와 공백만 남기고 모두 제거
    kst_time_str = re.sub(r'\s+', ' ', kst_time_str).strip()  # 중복된 공백 제거
    
    # 정규 표현식을 이용해 시간 문자열에서 필요한 정보를 추출
    time_pattern = r"(\d{4}) (\d{2}) (\d{2}) (\d{2}) (\d{2}) (\d{2})"
    match = re.search(time_pattern, kst_time_str)
    
    if match:
        year, month, day, hour, minute, second = match.groups()
        # KST는 UTC+9 이므로 9시간을 빼서 UTC로 변환
        kst_time = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
        utc_time = kst_time - timedelta(hours=9)
        return utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    else:
        raise ValueError(f"시간 형식을 인식하지 못했습니다: {kst_time_str}")

def execute_aws_cloudtrail(start_time_kst, end_time_kst, output_file, log_Profile='lookupIam'):
    # Convert KST to UTC
    start_time_utc = convert_to_utc(start_time_kst)
    end_time_utc = convert_to_utc(end_time_kst)
    output_path = os.path.join("..", output_file)
    
    # Construct the AWS CLI command
    command = [
        "aws", "cloudtrail", "lookup-events",
        "--start-time", start_time_utc,
        "--end-time", end_time_utc,
        "--region", "us-east-1",  # 원하는 리전으로 변경 가능
        "--output", "json",
        "--profile", log_Profile
    ]
    
    # Execute the command and save the output to a file
    with open(output_path, "w") as outfile:
        subprocess.run(command, stdout=outfile)
        print(f"CloudTrail logs saved to {output_file}")

def process_timeline(timeline_file, log_Profile, output_prefix):
    with open(timeline_file, "r", encoding="utf-8") as file:
        lines = file.readlines()
    
    # start와 end 시간 추출
    events = []
    for i in range(0, len(lines), 2):
        start_line = lines[i].strip()
        end_line = lines[i+1].strip()
        
        # 정규 표현식으로 시간 부분만 추출
        start_time_match = re.search(r'start (.+)', start_line)
        end_time_match = re.search(r'end (.+)', end_line)
        
        if start_time_match and end_time_match:
            start_time = start_time_match.group(1)
            end_time = end_time_match.group(1)
            events.append((start_time, end_time))
    output_index = int(output_prefix[-1])
    # 각 시간 구간에 대해 CloudTrail 로그 요청 실행
    for idx, (start_time, end_time) in enumerate(events):
        output_file = f"{output_prefix[:-1]}{output_index+idx}.json"
        print(f"Processing: {start_time} to {end_time}")
        execute_aws_cloudtrail(start_time, end_time, output_file, log_Profile)

# AWS 로그인
with open("origin_key.json", "r") as f:
    credentials = json.load(f)
    access_key_id = credentials.get("access_key_id")
    secret_access_key = credentials.get("secret_access_key")
    aws_cli_login(access_key_id, secret_access_key)

# 프로필 입력받기
log_Profile = input("log를 다운로드 할 수 있는 프로필(예: LoggingIAM): ")

# 타임라인 파일 처리
timeline_file = "timeline.txt"
output_prefix = input("저장할 파일 이름의 접두어 (예: cloudtrail_logs): ")

# 타임라인 파일에서 시간 구간을 처리하여 AWS CLI 명령 실행
process_timeline(timeline_file, log_Profile, output_prefix)