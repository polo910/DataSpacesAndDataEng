import duckdb

sat_a = "http://127.0.0.1:8001/observations.csv"
sat_b = "http://127.0.0.1:8002/observations.csv"

con = duckdb.connect()

count_a = con.execute(f"SELECT count(*) FROM '{sat_a}'").fetchone()[0]
obj_a = con.execute(f"SELECT count(*) FROM '{sat_a}' WHERE object_id='OBJ-003'").fetchone()[0]

count_b = con.execute(f"SELECT count(*) FROM '{sat_b}'").fetchone()[0]
obj_b = con.execute(f"SELECT count(*) FROM '{sat_b}' WHERE object_id='OBJ-003'").fetchone()[0]

print(f"satellite_A:\nTOTAL: {count_a}\nOBJ-003: {obj_a}")
print(f"\nsatellite_B:\nTOTAL: {count_b}\nOBJ-003: {obj_b}")


print("\nSCHEMA COMPARISON:")

try:
    con.execute(f"SELECT * FROM '{sat_a}' UNION ALL SELECT * FROM '{sat_b}'")
    print("satellite_A and satellite_B are compatible")
except:
    print("Schemas are DIFFERENT!")
