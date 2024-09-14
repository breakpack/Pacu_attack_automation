import os
import json

def load_trust_policy(json_file):
    # JSON 파일에서 신뢰 정책을 로드
    try:
        with open(json_file, 'r') as f:
            trust_policy = json.load(f)
        # JSON 내용을 문자열로 변환하여 Terraform 파일에 삽입 가능하게 만듦
        return json.dumps(trust_policy, indent=4)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return None

def create_terraform_role_file(role_name, trust_policy_document, policy_arn=None):
    # Terraform 파일을 생성할 디렉터리
    directory = "terraform_iam_role"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # Terraform 파일 생성
    with open(os.path.join(directory, "main.tf"), "w") as f:
        f.write(f"""
provider "aws" {{
  region = "us-east-1"
}}

# IAM 역할 생성
resource "aws_iam_role" "{role_name}" {{
  name = "{role_name}"
  assume_role_policy = <<POLICY
{trust_policy_document}
POLICY
}}

""")
        # 권한 정책을 추가할 경우
        if policy_arn:
            f.write(f"""
# AdministratorAccess 정책 연결
resource "aws_iam_role_policy_attachment" "{role_name}_policy_attachment" {{
  role       = aws_iam_role.{role_name}.name
  policy_arn = "{policy_arn}"
}}

""")
        
        # 역할 ARN 출력
        f.write(f"""
output "role_arn" {{
  value = aws_iam_role.{role_name}.arn
}}
""")

    print(f"Terraform configuration file has been created in {directory}/main.tf")

if __name__ == "__main__":
    # 역할 이름과 신뢰 정책 파일 경로 입력받기
    # role_name = input("생성할 역할 이름을 입력하세요: ")
    role_name = "testrole"
    # json_file = input("신뢰 관계(Trust Relationship) JSON 파일 경로를 입력하세요 (예: trust_policy.json): ")
    json_file = "trust.json"
    # 신뢰 정책을 담은 JSON 파일로부터 신뢰 정책 로드
    trust_policy_document = load_trust_policy(json_file)
    
    # 기본적으로 AdministratorAccess 정책 추가
    # use_admin_policy = input("AdministratorAccess 정책을 추가하시겠습니까? (y/n): ").strip().lower()
    use_admin_policy = "y"
    policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess" if use_admin_policy == 'y' else None
    
    if trust_policy_document:
        # Terraform 파일 생성
        create_terraform_role_file(role_name, trust_policy_document, policy_arn)
    else:
        print("신뢰 정책을 로드하는 데 실패했습니다.")