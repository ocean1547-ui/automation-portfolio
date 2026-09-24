# GitHub에 올리기 — 처음부터 따라하기

이 폴더(`portfolio/`)는 이미 git 저장소로 만들어져 있고 첫 커밋까지
되어 있어요. 아래 순서대로만 하면 GitHub에 올라갑니다.

## 1단계. GitHub 계정 만들기 (5분)

1. https://github.com 접속 → **Sign up** 클릭
2. 이메일, 비밀번호, 사용자 이름(username) 입력
   - username이 GitHub 주소가 돼요: `github.com/사용자이름`
3. 이메일 인증 완료

## 2단계. 새 저장소(Repository) 만들기 (2분)

1. 로그인 후 오른쪽 위 **+** → **New repository** 클릭
2. Repository name: `automation-portfolio` 입력
3. **Public** 선택 (포트폴리오니까 공개로!)
4. "Add a README file" 체크는 **하지 마세요** (이미 있어요)
5. **Create repository** 클릭

## 3단계. 내 컴퓨터에 git 설치 확인 (1분)

터미널(Windows면 Git Bash, Mac이면 Terminal)을 열고:

```bash
git --version
```

버전이 나오면 OK. 안 나오면:
- Windows: https://git-scm.com 에서 "Git for Windows" 설치
- Mac: `xcode-select --install` 실행

## 4단계. 내 정보 등록 (1분, 최초 1회만)

```bash
git config --global user.name "내이름"
git config --global user.email "깃헙가입이메일@example.com"
```

> 지금 이 폴더에는 임시로 `james@example.com`으로 커밋되어 있어요.
> 위 명령으로 본인 정보를 등록한 뒤, 나중에 커밋할 때부터는 본인 이름으로 기록돼요.

## 5단계. 이 폴더를 GitHub에 연결하고 올리기 (2분)

터미널에서 이 폴더로 이동한 뒤:

```bash
cd ~/workspace/portfolio   # 이 폴더의 실제 경로로 변경

# GitHub 저장소와 연결 (사용자이름 부분을 본인 것으로!)
git remote add origin https://github.com/사용자이름/automation-portfolio.git

# 올리기
git push -u origin main
```

> `main` 브랜치가 없다고 나오면 먼저 `git branch -M main` 실행 후 다시 push.

로그인이 필요하다고 나오면:
- 사용자 이름 입력 후 비밀번호 대신 **Personal Access Token** 사용
- 토큰 발급: GitHub → Settings → Developer settings → Personal access tokens → Generate new token (repo 권한 체크)

## 6단계. 확인

브라우저에서 `https://github.com/사용자이름/automation-portfolio` 접속.
README와 데모 GIF 3개가 보이면 성공!

## 앞으로 코드 고쳤을 때 올리는 법

```bash
git add -A
git commit -m "수정한 내용 설명"
git push
```

이 세 줄이면 끝이에요.
