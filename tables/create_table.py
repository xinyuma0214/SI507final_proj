import csv, sqlite3
conn = sqlite3.connect('wildland_fire.sqlite')
cur = conn.cursor()

drop_parks = '''
    DROP TABLE IF EXISTS "parks";
'''

create_parks = '''
    CREATE TABLE IF NOT EXISTS "parks" (
        "uni_number" INTEGER PRIMARY KEY,
        "parkCode" TEXT NOT NULL, 
        "park" TEXT NOT NULL, 
        "state" TEXT NOT NULL, 
        "category" TEXT, 
        "address" TEXT NOT NULL, 
        "zipcode" TEXT NOT NULL,
        "phone" TEXT NOT NULL,
        "acres" TEXT NOT NULL
        );
'''
cur.execute(drop_parks)
cur.execute(create_parks)

with open('parks.csv','r') as parks: 
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(parks) # comma is default delimiter
    to_db = [(i['uni_number'], i['parkCode'], i['park'], i['state'], i['category'], i['address'],i['zipcode'],i['phone'],i['acres']) for i in dr]

cur.executemany("INSERT INTO parks VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)

# create table wildland fire
drop_fire = '''
    DROP TABLE IF EXISTS "fire"
'''

create_fire = '''
    CREATE TABLE IF NOT EXISTS "fire" (
        "OBJECTID" TEXT PRIMARY KEY,
        "UnitCode" TEXT NOT NULL,
        "UnitName" TEXT NOT NULL,
        "FireCause" TEXT NOT NULL,
        "SizeClass" TEXT NOT NULL,
        "FinalAcres" REAL NOT NULL,
        "FireDiscoveryDateTime" INTEGER NOT NULL
        
    );
'''

cur.execute(drop_fire)
cur.execute(create_fire)

with open('fire.csv','r') as fire: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr2 = csv.DictReader(fire) 
    to_db2 = [(i['OBJECTID'], i['UnitCode'], i['UnitName'], i['FireCause'], i['SizeClass'], i['FinalAcres'], i['FireDiscoveryDateTime']) for i in dr2]

cur.executemany("INSERT INTO fire VALUES (?, ?, ?, ?, ?, ?, ?);", to_db2)


conn.commit()
conn.close()