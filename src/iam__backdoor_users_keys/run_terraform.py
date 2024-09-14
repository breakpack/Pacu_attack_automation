import os
import subprocess
import json

def run_terraform():
    # Terraform 파일이 위치한 디렉터리
    terraform_dir = "terraform_iam"
    
    # Terraform 초기화
    subprocess.run(["terraform", "init"], cwd=terraform_dir)
    
    # Terraform 적용
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=terraform_dir)
    
    print("Terraform apply complete.")

def get_terraform_outputs():
    # Terraform output 명령어 실행
    terraform_dir = "terraform_iam"
    result = subprocess.run(["terraform", "output", "-json"], capture_output=True, text=True, cwd=terraform_dir)
    
    # JSON 형식의 출력 결과 파싱
    outputs = json.loads(result.stdout)
    
    access_key_id = outputs.get("access_key_id", {}).get("value", None)
    secret_access_key = outputs.get("secret_access_key", {}).get("value", None)
    
    return access_key_id, secret_access_key

def save_keys_to_json(access_key_id, secret_access_key, file_name="access_key.json"):
    # Access Key와 Secret Key를 JSON 파일로 저장
    data = {
        "access_key_id": access_key_id,
        "secret_access_key": secret_access_key
    }
    
    with open(file_name, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Access Key와 Secret Key가 {file_name}에 저장되었습니다.")

if __name__ == "__main__":
    # Terraform 실행 (apply)
    run_terraform()

    # Terraform 출력에서 Access Key와 Secret Access Key를 가져옴
    access_key_id, secret_access_key = get_terraform_outputs()
    
    if access_key_id and secret_access_key:
        print(f"Access Key ID: {access_key_id}")
        print(f"Secret Access Key: {secret_access_key}")
        
        # Access Key와 Secret Access Key를 JSON 파일로 저장
        save_keys_to_json(access_key_id, secret_access_key)
    else:
        print("Access Key 정보를 가져올 수 없습니다.")