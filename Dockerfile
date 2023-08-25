# 기본 이미지를 지정
FROM python:3.10

# WORKDIR 키워드를 사용해 작업 디렉터리를 /app 으로 설정
WORKDIR /app

# requirements.txt 파일을 로컬 디렉터리에서 도커 컨테이너의 작업 디렉토리로 복사
COPY requirements.txt /app/requirements.txt

# pip 패키지를 업그레이드하고 requirements.txt를 기반으로 의존 라이브러리를 설치
RUN pip install --upgrade pip && pip install -r /app/requirements.txt

# 로컬 네트워크에서 애플리케이션에 접속할 수 있는 포트 번호를 설정
EXPOSE 8000

# 나머지 파일을 도커 컨테이너의 작업 디렉터리로 복사
COPY ./ /app

# CMD 명령을 사용해 애플리케이션 실행
CMD ["python", "main.py"]
