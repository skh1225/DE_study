## `숙제 1`
<img width="1494" alt="image" src="https://user-images.githubusercontent.com/95852887/232301071-52423cc2-7236-4ceb-8c0f-795448bb5b56.png">

## `숙제 3`
```
├── FullRefresh.py
└── IncrementalUpdate.py
```
`Variables`
- `api_key` : Open Weathermap API key
- `gps_coordinates` : {"Asia/Seoul":{"lat":37.3387,"lon":121.8853}}
- `weather_url` : https://api.openweathermap.org/data/2.5/onecall


## `숙제 4`
Q1. Airflow의 환경 설정이 들어있는 파일의 이름은?
 - A : airflow.cfg

Q2. 이 파일에서 Airflow를 API 형태로 외부에서 조작하고 싶다면 어느 섹션을
변경해야하는가?
 - A: airflow.cfg의 \[api\] 섹션의 auth_backend를 airflow.api.auth.backend.basic_auth로 변경
 - A: 이러한 API을 통해 webserver, scheduler에 대한 monitoring을 걸 수 있다.
   - API로 Health check할 수 있는 endpoint가 있는데 이것을 통해 scheduler가 살았나 죽었나? 마지막 heartbeat는 언제인가?

Q3. Variable에서 변수의 값이 encrypted가 되려면 변수의 이름에 어떤 단어들이
들어가야 하는데 이 단어들은 무엇일까? :)
 - A : password, secret, passwd, authorization, api_key, apikey, access_token

Q4. 이 환경 설정 파일이 수정되었다면 이를 실제로 반영하기 위해서 해야 하는
일은?
 - A : airflow 웹 서버와 스케줄러를 다시 시작해야 합니다.

Q5. DAGs 폴더에 새로운 Dag를 만들면 언제 실제로 Airflow 시스템에서 이를 알게
되나? 이 스캔주기를 결정해주는 키의 이름이 무엇인가?
 - A : airflow.cfg의 \[schedule\] 섹션의 dag_dir_list_interval을 변경하면 된다.(초 단위, default 300)
