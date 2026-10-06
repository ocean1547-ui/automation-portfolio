# 📊 DBAS 5115 Data & PostgreSQL Cheat Sheet

## 1. 🐙 Git 필수 제출 명령어 (과제 제출용)
작업이 끝난 후 VS Code 터미널(`bash`)에 순서대로 입력합니다.
```bash
# 1. 모든 변경된 파일 추가
git add .

# 2. 변경 내용에 이름표(메시지) 붙이기
git commit -m "작업 내용 설명 적기"

# 3. 깃허브로 최종 전송
git push
```

## 2. 🐘 PostgreSQL 터미널 명령어
Codespaces 터미널에서 데이터베이스에 접속하고 확인할 때 사용합니다
```bash
# DB 접속 (비밀번호 입력창이 뜨면 타이핑 후 엔터 - 화면에 안 보여도 입력되고 있음)
psql -d postgres -h localhost -U postgres

# 접속 후 테이블 목록 보기
\dt

# psql 터미널 종료하고 빠져나오기
\q
```

## 3. 🐼 Pandas: 데이터 불러오기 (CSV & API)
파일 데이터 (CSV)
```python
import pandas as pd

# 1. 기본 불러오기
df = pd.read_csv('파일명.csv')

# 2. UnicodeDecodeError 발생 시 (엑셀/윈도우 호환)
df = pd.read_csv('파일명.csv', encoding='cp949') # 한글 윈도우용
# 또는
df = pd.read_csv('파일명.csv', encoding='latin1') # 영문/기타
```

웹 데이터 (API / JSON)

B. API (JSON) 데이터 읽기
```python
import pandas as pd
import requests

api_url = "https://api.domain.com/data?per_page=200"
response = requests.get(api_url)
df_api = pd.DataFrame(response.json())
```

C. 웹 스크래핑 (Worldometers 웹사이트 표 긁어오기)
```python
import pandas as pd

url = "https://www.worldometers.info/..."
# 웹페이지의 모든 HTML <table> 요소를 리스트로 가져옴
tables = pd.read_html(url)
# 보통 첫 번째 표([0])가 메인 데이터임
df_web = tables[0]
```

## 4. 🔍 Pandas: 데이터 탐색 및 통계 (EDA)
데이터가 잘 들어왔는지 검사할 때 무조건 쓰는 4가지 필수 코드입니다.
```python
# 1. 위에서부터 5줄 미리보기
display(df.head())

# 2. 데이터 형식, 결측치(빈칸), 총 데이터 개수 확인
df.info()

# 3. 기초 통계 (평균, 최대/최소, 개수 등) - 문자 데이터까지 보려면 include='all'
display(df.describe(include='all'))

# 4. 특정 열(Column)의 항목별 개수 세기 (예: 종류별 개수)
df['컬럼명'].value_counts()
```

💡 꿀팁: 숫자 깨짐(과학적 표기법) 방지
GDP나 금액 등 큰 숫자가 1.23e+09처럼 보일 때, 라이브러리 불러오는 곳 바로 아래에 추가합니다.
```python
# 달러($)나 일반 숫자 형식(소수점 2자리, 쉼표 포함)으로 깔끔하게 표시
pd.options.display.float_format = '{:,.2f}'.format
```

## 5. 📊 완벽한 시각화 (Matplotlib)
과학적 표기법(1.23e+09)을 달러 표시로 바꾸는 옵션과, 글자 겹침을 방지하는 정밀한 그래프 템플릿입니다.
```python
import matplotlib.pyplot as plt

# 과학적 표기법(지수) 방지 및 소수점 2자리 달러 콤마 포맷
pd.options.display.float_format = '{:,.2f}'.format

# 차트 그리기 시작
plt.figure(figsize=(10, 6))

# X축, Y축 데이터를 직접 지정하는 바 차트 (Top 5 GDP 실습용)
plt.bar(top_5['Country'], top_5['2025'], color='forestgreen')

# 라벨 및 타이틀 세팅
plt.title('Top 5 Countries for GDP in 2025')
plt.xlabel('Country')
plt.ylabel('GDP ($)')

# 디테일 마무리
plt.xticks(rotation=45) # X축 글자 대각선 회전 (안 겹치게)
plt.tight_layout()      # 그래프 여백 자동 최적화
plt.show()              # 화면에 출력
```

## 6. 🔍 데이터 정제 및 조작 (Pandas 핵심 연산)
데이터를 가져온 후 원하는 입맛대로 요리하는 코드입니다.

기초 통계 연산 (Cat Facts 실습 활용)
```python
# 특정 열(컬럼)만 따로 빼내기
lengths = df_api['length']

# 최댓값, 최솟값, 평균 구하기
max_val = lengths.max()
min_val = lengths.min()
mean_val = lengths.mean()

print(f"최대: {max_val}, 최소: {min_val}, 평균: {mean_val:.1f}")
```

데이터 정렬 및 추출 (GDP 상위 5개국 추출 실습 활용)
```python
# 특정 컬럼('2025') 기준으로 내림차순(큰 숫자가 위로) 정렬
df_sorted = df_csv.sort_values(by='2025', ascending=False)

# 위에서부터 5개만 짤라내기 (Top 5)
top_5 = df_sorted.head(5)
```
