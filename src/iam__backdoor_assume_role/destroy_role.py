import os
import subprocess

def destroy_terraform(directory="terraform_iam_role"):
    # Terraform destroy 명령 실행
    print("Terraform 리소스를 삭제 중입니다...")
    result = subprocess.run(["terraform", "destroy", "-auto-approve"], cwd=directory)
    
    # 명령이 실패한 경우 오류 메시지 출력
    if result.returncode != 0:
        print(f"Terraform 리소스 삭제 중 오류가 발생했습니다: {result.stderr}")
    else:
        print("Terraform 리소스 삭제가 완료되었습니다.")

if __name__ == "__main__":
    terraform_dir = "terraform_iam_role"
    
    # 해당 디렉터리가 존재하는지 확인
    if os.path.exists(terraform_dir):
        # Terraform 실행
        destroy_terraform(terraform_dir)
    else:
        print(f"디렉터리 {terraform_dir} 가 존재하지 않습니다. 먼저 Terraform 파일을 생성하세요.")