
## `숙제 3`
```
├── Build_Summary.py
└── conf.py
```
- nps_summary table을 생성하는 SQL
```sql
WITH temp AS 
(
SELECT LEFT(created_at,10) AS date, 
SUM(CASE WHEN score > 8 THEN 1 WHEN score < 7 THEN -1 ELSE 0 END) as sum,
COUNT(*) as cnt 
FROM skh951225.nps 
GROUP BY 1
)
SELECT date, 
ROUND(sum::float/NULLIF(cnt,0)*100,2) 
FROM temp;
```
- conf.py 파일에 schema, table, sql 등의 정보를 담고 있습니다.
- Build_Summary.py는 conf.py를 import 하여 해당 정보를 사용하고 있습니다.
