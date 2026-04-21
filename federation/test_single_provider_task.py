import requests

#obserwacje
data_a = requests.get("http://127.0.0.1:8001/observations").json()

#query
obj_a = requests.get("http://127.0.0.1:8001/observations/OBJ-003").json()
obj_b = requests.get("http://127.0.0.1:8002/observations/OBJ-003").json()

#wydruk
print("satellite_A:")
print("NUMBER OF OBSERVATIONS:", len(data_a))
print("OBJ-003 RESULTS:", len(obj_a))

print("\nsatellite_B:")
print("OBJ-003 RESULTS:", len(obj_b))

print("\nCOMPARISON:")
if len(obj_a) > 0 and len(obj_b) > 0:
    print("OBJ-003 is present in both providers.")
