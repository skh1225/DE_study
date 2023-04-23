config = {
        'schema' : 'skh951225',
        'table': 'nps_summary',
        'input_tables': ['skh951225.nps'],
        'sql' : """WITH temp AS (
            SELECT LEFT(created_at,10) AS date, 
            SUM(CASE WHEN score > 8 THEN 1 WHEN score < 7 THEN -1 ELSE 0 END) as sum,
            COUNT(*) as cnt 
            FROM skh951225.nps 
            GROUP BY 1
            )
            SELECT date, 
            ROUND(sum::float/NULLIF(cnt,0)*100,2) 
            FROM temp;"""
}

def input_check():
  return

def ouput_check():
  return
