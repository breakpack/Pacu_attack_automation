import subprocess
import json

def aws_cli_login(access_key_id, secret_access_key):
    # AWS CLI에 Access Key와 Secret Access Key 설정
    subprocess.run(["aws", "configure", "set", "aws_access_key_id", access_key_id])
    subprocess.run(["aws", "configure", "set", "aws_secret_access_key", secret_access_key])
    print("AWS CLI에 로그인되었습니다.")

def get_user_id():
    # 'aws sts get-caller-identity' 명령 실행
    result = subprocess.run(["aws", "sts", "get-caller-identity"], capture_output=True, text=True)
    
    # 명령 실행에 실패한 경우 오류 메시지 출력
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None

    # 결과를 JSON으로 파싱
    try:
        identity = json.loads(result.stdout)
        user_id = identity.get("UserId", None)
        return user_id
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
        return None

if __name__ == "__main__":
    # Access Key와 Secret Access Key가 저장된 파일 불러오기
    with open("access_key.json", "r") as f:
        credentials = json.load(f)

    access_key_id = credentials.get("access_key_id")
    secret_access_key = credentials.get("secret_access_key")
    
    if access_key_id and secret_access_key:
        # AWS CLI에 로그인
        aws_cli_login(access_key_id, secret_access_key)
        
        # 로그인한 사용자 정보 가져오기
        user_id = get_user_id()
        if user_id:
            print(f"User ID: {user_id}")
        else:
            print("User ID를 가져올 수 없습니다.")
    else:
        print("Access Key 정보를 불러오지 못했습니다.")