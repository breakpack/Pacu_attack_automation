import subprocess

def destroy_terraform():
    # Terraform 파일이 위치한 디렉터리
    terraform_dir = "terraform_iam"
    
    # Terraform destroy 명령 실행
    print("Terraform 리소스를 삭제 중입니다...")
    result = subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=terraform_dir, capture_output=True, text=True)
    
    # 명령이 실패했는지 확인
    if result.returncode == 0:
        print("Terraform 리소스 삭제 완료.")
    else:
        print(f"Terraform 리소스 삭제 실패. 에러 메시지: {result.stderr}")

if __name__ == "__main__":
    # Terraform 리소스 삭제
    destroy_terraform()