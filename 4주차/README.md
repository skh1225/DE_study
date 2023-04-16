## `숙제 1`
<img width="1494" alt="image" src="https://user-images.githubusercontent.com/95852887/232301071-52423cc2-7236-4ceb-8c0f-795448bb5b56.png">

## `숙제 3`
```
├── FullRefresh.py
└── IncrementalUpdate.py
```
`Variables`
- api_key : Open Weathermap API key
- gps_coordinates : {"Asia/Seoul":{"lat":37.3387,"lon":121.8853}}
- weather_url : https://api.openweathermap.org/data/2.5/onecall


## `숙제 4`
Q1. Airflow의 환경 설정이 들어있는 파일의 이름은?
 - A : airflow.cfg

Q2. 이 파일에서 Airflow를 API 형태로 외부에서 조작하고 싶다면 어느 섹션을
변경해야하는가?
 - A: airflow.cfg의 \[api\] 섹션

Q3. Variable에서 변수의 값이 encrypted가 되려면 변수의 이름에 어떤 단어들이
들어가야 하는데 이 단어들은 무엇일까? :)
 - A : 암호화되려면 변수의 이름에 "secure_" 또는 "encrypted_"와 같은 접두사를 붙이면 된다.

Q4. 이 환경 설정 파일이 수정되었다면 이를 실제로 반영하기 위해서 해야 하는
일은?
 - A : airflow 웹 서버와 스케줄러를 다시 시작해야 합니다.

Q5. DAGs 폴더에 새로운 Dag를 만들면 언제 실제로 Airflow 시스템에서 이를 알게
되나? 이 스캔주기를 결정해주는 키의 이름이 무엇인가?
 - A : airflow.cfg의 \[schedule\] 섹션의 min_file_process_interval을 변경하면 된다.(초 단위)
