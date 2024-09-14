import os
import subprocess

def run_terraform(directory="terraform_iam_role"):
    # Terraform 초기화
    print("Terraform 초기화 중...")
    subprocess.run(["terraform", "init"], cwd=directory)
    
    # Terraform 적용
    print("Terraform 적용 중...")
    subprocess.run(["terraform", "apply", "-auto-approve"], cwd=directory)
    
    print("Terraform 적용이 완료되었습니다.")

if __name__ == "__main__":
    terraform_dir = "terraform_iam_role"
    
    # 해당 디렉터리가 존재하는지 확인
    if os.path.exists(terraform_dir):
        # Terraform 실행
        run_terraform(terraform_dir)
    else:
        print(f"디렉터리 {terraform_dir} 가 존재하지 않습니다. 먼저 Terraform 파일을 생성하세요.")