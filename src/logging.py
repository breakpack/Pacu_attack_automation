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
    
    # "월"과 같은 한글 및 불필요한 문자를 제거하고 변환
    cleaned_time_str = re.sub(r'[^\d\s:,]', '', kst_time_str)  # 숫자, 공백, 콜론, 쉼표 외 문자 제거
    cleaned_time_str = re.sub(r'\s+', ' ', cleaned_time_str)  # 중복된 공백 제거
    
    # KST is UTC+9, so we subtract 9 hours to convert to UTC
    kst_time = datetime.strptime(cleaned_time_str, "%m %d, %Y, %H:%M:%S")
    utc_time = kst_time - timedelta(hours=9)
    return utc_time.strftime("%Y-%m-%dT%H:%M:%SZ")

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

with open("origin_key.json", "r") as f:
    credentials = json.load(f)
    access_key_id = credentials.get("access_key_id")
    secret_access_key = credentials.get("secret_access_key")
    aws_cli_login(access_key_id, secret_access_key)
    
log_Profile = input("log를 다운로드 할 수 있는 프로필(예: LoggingIAM): ")

# 시간 입력받기 (KST 형식, 예: 9월 10, 2024, 18:36:28)
start_time_kst = input("시작 시간 (예: 9월 10, 2024, 18:36:28): ")
end_time_kst = input("종료 시간 (예: 9월 10, 2024, 18:36:28): ")

# 출력 파일 이름 입력받기
output_file = input("저장할 파일 이름 (예: cloudtrail_logs.json): ")

# 입력받은 시간대로 AWS CLI 명령 실행
execute_aws_cloudtrail(start_time_kst, end_time_kst, output_file, log_Profile)