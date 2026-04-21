import duckdb

federated_query = """
    SELECT 'satellite_A' AS provider, * FROM 'http://127.0.0.1:8001/observations.csv'
    UNION ALL
    SELECT 'satellite_B' AS provider, * FROM 'http://127.0.0.1:8002/observations.csv'
    UNION ALL
    SELECT 'ground_station' AS provider, * FROM 'http://127.0.0.1:8003/observations.csv'
"""

con = duckdb.connect()

total = con.execute(f"SELECT count(*) FROM ({federated_query})").fetchone()[0]
obj_003 = con.execute(f"SELECT count(*) FROM ({federated_query}) WHERE object_id='OBJ-003'").fetchone()[0]

stats = con.execute(f"""
    SELECT provider, count(*) 
    FROM ({federated_query}) 
    GROUP BY provider 
    ORDER BY count(*) DESC
""").fetchall()

print(f"TOTAL OBSERVATIONS: {total}")
print(f"OBJ-003 OBSERVATIONS: {obj_003}")

for provider, count in stats:
    print(f"{provider}: {count}")

print("\nLARGEST PROVIDER:")
print(stats[0][0])

