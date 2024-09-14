import json
import os
import pty
import subprocess

# JSON 파일 경로
json_file_path = "../access_key.json"

# JSON 파일 읽기
with open(json_file_path, 'r') as f:
    credentials = json.load(f)

# access_key_id와 secret_access_key 가져오기
access_key_id = credentials["access_key_id"]
secret_access_key = credentials["secret_access_key"]

# Pacu 실행을 위한 pty 사용
def run_pacu():
    master, slave = pty.openpty()  # 가상 터미널(PTY) 생성
    process = subprocess.Popen(
        ["pacu"], 
        stdin=slave, 
        stdout=slave, 
        stderr=subprocess.PIPE, 
        text=True
    )
    os.close(slave)
    return process, master

# Pacu 프로세스 실행
pacu_process, pacu_stdout_fd = run_pacu()

# 세션 선택 자동화 (새 세션 0 선택)
os.write(pacu_stdout_fd, b"0\n")  # '0'을 선택해서 새 세션 시작
os.write(pacu_stdout_fd, f"set_keys {access_key_id} {secret_access_key}\n".encode())

# 이후 상호작용을 위해 출력을 지속적으로 보여줌
try:
    while True:
        output = os.read(pacu_stdout_fd, 1024).decode()
        if output:
            print(output.strip())

except KeyboardInterrupt:
    pacu_process.terminate()
    print("\nPacu process terminated.")
finally:
    os.close(pacu_stdout_fd)