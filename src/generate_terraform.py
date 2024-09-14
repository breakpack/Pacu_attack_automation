import os
import json
import random
import string

# 5자리 랜덤 문자열 생성 함수
def generate_random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def create_terraform_files(user_name, policy_name, policy_document):
    # Terraform 파일을 생성할 디렉토리
    directory = "terraform_iam"
    
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    # main.tf 파일 작성 (IAM 사용자 생성 및 정책 할당)
    with open(os.path.join(directory, "main.tf"), "w") as f:
        f.write(f"""
provider "aws" {{
  region = "us-east-1"  # 원하는 리전으로 변경
}}

# IAM 사용자 생성
resource "aws_iam_user" "{user_name}" {{
  name = "{user_name}"
}}

# IAM 사용자 정책 생성
resource "aws_iam_user_policy" "{policy_name}" {{
  name   = "{policy_name}"
  user   = aws_iam_user.{user_name}.name
  policy = <<POLICY
{policy_document}
POLICY
}}

# Access Key 생성
resource "aws_iam_access_key" "{user_name}_access_key" {{
  user = aws_iam_user.{user_name}.name
}}

# Access Key 출력
output "access_key_id" {{
  value = aws_iam_access_key.{user_name}_access_key.id
}}

output "secret_access_key" {{
  value     = aws_iam_access_key.{user_name}_access_key.secret
  sensitive = true
}}
""")
    
    print(f"Terraform configuration file has been created in {directory}/main.tf")

def load_policy_from_file(json_file):
    # JSON 파일에서 정책을 로드
    try:
        with open(json_file, 'r') as f:
            policy_document = json.load(f)
        # JSON 내용을 문자열로 변환하여 Terraform 파일에 삽입 가능하게 만듦
        return json.dumps(policy_document, indent=4)
    except FileNotFoundError:
        print(f"Error: {json_file} not found.")
        return None

if __name__ == "__main__":
    # 사용자 이름과 정책 이름을 5자리 랜덤 문자열로 생성
    user_name = generate_random_string()
    policy_name = generate_random_string()
    
    # JSON 파일로부터 정책 로드
    json_file = input("정책을 선택해 주세요(ex iam__backdoor_assume_role_policy.json): ")
    if json_file == '':
      json_file = 'iam__backdoor_assume_role_policy.json'
    policy_document = load_policy_from_file(json_file)
    
    if policy_document:
        # Terraform 파일 생성
        create_terraform_files(user_name, policy_name, policy_document)