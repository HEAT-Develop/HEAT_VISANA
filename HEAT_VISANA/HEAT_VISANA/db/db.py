import mysql.connector
from mysql.connector import Error
import uuid



class DataBase():

    def __init__(self):
        self.user = "root"
        self.password = "HEAT1738"
        self.host = "localhost"
        try:
            mydb = mysql.connector.connect(   
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3" 
            )
            
            if mydb.is_connected():
                db_Info = mydb.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = mydb.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
                print("MySQL connection is closed")

    def get_year(self,y):

        
        try:

            mydb = mysql.connector.connect(
                
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3" 
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                mycursor = mydb.cursor()
                query = "SELECT year FROM missions WHERE year = %s"
                mycursor.execute(query,(y,))

                myresult = mycursor.fetchall()

                return myresult
            
            
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def get_month(self, mm):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3" 
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                mycursor = mydb.cursor()
                query = "SELECT month FROM missions WHERE month = %s"
                mycursor.execute(query,(mm,))

                myresult = mycursor.fetchall()

                return myresult
            
            
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def get_day(self,dd):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3" 
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                mycursor = mydb.cursor()
                query = "SELECT day FROM missions WHERE day = %s"
                mycursor.execute(query,(dd,))

                myresult = mycursor.fetchall()

                return myresult
            
            
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def get_minut(self,m):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3" 
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                mycursor = mydb.cursor()
                query = "SELECT min FROM missions WHERE min = %s"
                mycursor.execute(query,(m,))

                myresult = mycursor.fetchall()

                return myresult
            
            
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def get_second(self,s):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                mycursor = mydb.cursor()
                query = "SELECT sec FROM missions WHERE sec = %s"
                mycursor.execute(query,(s,))

                myresult = mycursor.fetchall()

                return myresult
            
            
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def get_hour(self,h):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"  
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                mycursor = mydb.cursor()
                query = "SELECT hour FROM missions WHERE hour = %s"
                mycursor.execute(query,(h,))

                myresult = mycursor.fetchall()

                return myresult
        except Error as e:
            print("Error while connecting to MySQL:", e)

    def get_name(self, y,mm,d,m,h,s, model, model_size):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            filename = f"{y}{mm:02d}{d:02d}_{h:02d}{m:02d}{s:02d}_l3.vtk"

            # Debugging: Check file path
            print(f"Constructed file path: {filename}")

            cursor = mydb.cursor()
            query = """SELECT vtk_file_path FROM missions 
            WHERE year = %s AND month = %s AND day = %s AND hour = %s AND min = %s AND sec = %s AND model = %s AND model_size = %s"""

            cursor.execute(query, (y,mm,d,m,h,s, model, model_size))
            myresult = cursor.fetchall()  # Fetching the single result

            return myresult
        except Error as e:
            print("Error while connecting to MySQL:", e)

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    def get_names(self, initial_year, initial_month, initial_day, initial_hour, initial_minute, initial_second,
                end_year, end_month, end_day, end_hour, end_minute, end_second, model, model_size):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            cursor = mydb.cursor()
            
            # Updated query with corrected parentheses
            query = """SELECT vtk_file_path FROM missions 
            WHERE (year > %s OR 
                    (year = %s AND month > %s) OR 
                    (year = %s AND month = %s AND day > %s) OR
                    (year = %s AND month = %s AND day = %s AND hour > %s) OR
                    (year = %s AND month = %s AND day = %s AND hour = %s AND min > %s) OR
                    (year = %s AND month = %s AND day = %s AND hour = %s AND min = %s AND sec >= %s))
            AND (year < %s OR 
                    (year = %s AND month < %s) OR
                    (year = %s AND month = %s AND day < %s) OR
                    (year = %s AND month = %s AND day = %s AND hour < %s) OR
                    (year = %s AND month = %s AND day = %s AND hour = %s AND min < %s) OR
                    (year = %s AND month = %s AND day = %s AND hour = %s AND min = %s AND sec <= %s))
            AND model = %s AND model_size = %s"""
            
            # Execute query with parameters
            cursor.execute(query, (initial_year, initial_year, initial_month, initial_year, initial_month, initial_day,
                                initial_year, initial_month, initial_day, initial_hour,
                                initial_year, initial_month, initial_day, initial_hour, initial_minute,
                                initial_year, initial_month, initial_day, initial_hour, initial_minute, initial_second,
                                end_year, end_year, end_month, end_year, end_month, end_day,
                                end_year, end_month, end_day, end_hour,
                                end_year, end_month, end_day, end_hour, end_minute,
                                end_year, end_month, end_day, end_hour, end_minute, end_second,
                                model, model_size))
            myresult = cursor.fetchall()
            file_paths = [row[0] for row in myresult]
            return file_paths
        except Error as e:
            print("Error while connecting to MySQL:", e)

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    def get_vtk_file_paths(self):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            cursor = mydb.cursor()

            # Define the SQL query
            query = """
                SELECT vtk_file_path 
                FROM missions 
                WHERE model = 'sfm' AND model_size = '50k'
            """

            # Execute the query
            cursor.execute(query)

            # Fetch all results
            results = cursor.fetchall()

            # Extract file paths from the results
            vtk_file_paths = [row[0] for row in results]
            
            # Print the file paths or return them
            for path in vtk_file_paths:
                print(path)

            return vtk_file_paths

        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    def get_all_names(self, model, model_size):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            cursor = mydb.cursor()

            # Simplified query to get all vtk_file_paths for a given model and model_size
            query = """SELECT vtk_file_path FROM missions 
                    WHERE model = %s AND model_size = %s"""

            # Execute the query
            cursor.execute(query, (model, model_size))
            myresult = cursor.fetchall()

            # Extract file paths from the query result
            file_paths = [row[0] for row in myresult]

            return file_paths

        except mysql.connector.Error as e:
            print("Error while connecting to MySQL:", e)
            return []

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    def insert_new_mission(self,name, level, mission, camera, year, month, day, hour, minute, sec, format, model, vtk_file_path, model_size):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                check_query = """
                SELECT COUNT(*) FROM missions
                WHERE year = %s AND month = %s AND day = %s

                AND hour = %s AND min = %s AND sec = %s

                AND model = %s AND model_size = %s
                """
                check_values = (year, month, day, hour, minute, sec, model, model_size)
                cursor.execute(check_query, check_values)
                record_exists = cursor.fetchone()[0]

                if record_exists > 0:
                                                    
                    print(name)

                    print("Record with the same timestamp already exists. No new record inserted.")
                    return

                insert_query = """
                INSERT INTO missions (name, level, mission, camera, year, month, day, hour, min, sec, format, model, vtk_file_path, model_size)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (name, level, mission, camera, year, month, day, hour, minute, sec, format, model, vtk_file_path, model_size)
                cursor.execute(insert_query, values)
                mydb.commit()

                #print(f"Record inserted successfully into the missions table. ID: {cursor.lastrowid}")

        except Error as e:
            print("Error while connecting to MySQL:", e)

        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
                print("MySQL connection is closed")

    def get_dates(self):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                # Query to get distinct dates from the table
                query = """
                SELECT DISTINCT 
                    CONCAT(year, '-', 
                        LPAD(month, 2, '0'), '-', 
                        LPAD(day, 2, '0'), ' ', 
                        LPAD(hour, 2, '0'), ':', 
                        LPAD(min, 2, '0'), ':', 
                        LPAD(sec, 2, '0')) AS datetime
                FROM missions
                ORDER BY datetime
                """

                cursor.execute(query)
                result = cursor.fetchall()  # Fetch all distinct dates

                # Extract the dates from the result tuples
                dates = [row[0] for row in result]

                return dates
            
        
            
        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    def get_dates_day(self):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                # Query to get distinct dates from the table
                query = """
                SELECT DISTINCT 
                    CONCAT(year, '-', 
                        LPAD(month, 2, '0'), '-', 
                        LPAD(day, 2, '0')) AS datetime
                FROM missions
                ORDER BY datetime
                """

                cursor.execute(query)
                result = cursor.fetchall()  # Fetch all distinct dates

                # Extract the dates from the result tuples
                dates = [row[0] for row in result]

                return dates
            
        
            
        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    def get_full_day(self,y, mm, d):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()
                query = """SELECT DISTINCT vtk_file_path FROM missions 
                        WHERE year = %s AND month = %s AND day = %s"""

                cursor.execute(query, (y, mm, d))
                result = cursor.fetchall()
                file_paths = [row[0] for row in result]  # Extract only the vtk_file_path from the result

                return file_paths

        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    
    def insert_new_model(self, name, asteroid, type, specification, file_path, size):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                insert_query = """
                INSERT INTO models (name, asteroid, type, specification, file_path, size)
                VALUES (%s, %s, %s, %s, %s, %s)
                """
                values = (name, asteroid, type, specification, file_path, size)

                cursor.execute(insert_query, values)
                mydb.commit()

                print(f"Record inserted successfully into the models table. ID: {cursor.lastrowid}")

        except Error as e:
            print("Error while connecting to MySQL:", e)

        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
                print("MySQL connection is closed")
    
    def model_in_db(self, name):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()
                query = "SELECT COUNT(*) FROM models WHERE LOWER(name) = %s"
                cursor.execute(query, (name.lower(),))
                count = cursor.fetchone()[0]

                print(f"Checking if model '{name}' exists. Count: {count}")

                return count > 0

        except Error as e:
            print("Error while connecting to MySQL:", e)
            return False

        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
                print("MySQL connection is closed")

    def get_model(self,size):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            cursor = mydb.cursor(buffered=True)
            query = """SELECT file_path FROM models 
            WHERE size = %s"""

            # Pass the 'size' parameter as a tuple
            cursor.execute(query, (size,))
            myresult = cursor.fetchone()

            if myresult:
                return myresult[0]  # Return the first element of the tuple (the file path)
            else:
                return None  # Return None if no result is found
        
        except Error as e:
            print("Error while connecting to MySQL:", e)

        finally:
            if mydb.is_connected():
                cursor.close()  # Close the cursor
                mydb.close()  # Close the connection
                print("MySQL connection is closed")

    def insert_new_rigion(self, region_name, depth, angle, slope, geo_diameter, geo_radius, centroid_x, centroid_y,centroid_z,crater_dimater):
        try:
            mydb = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )

            if mydb.is_connected():
                cursor = mydb.cursor()

                check_query = """
                SELECT COUNT(*) FROM regions
                WHERE name = %s 
                """
                check_values = (region_name,)
                cursor.execute(check_query, check_values)
                record_exists = cursor.fetchone()[0]

                if record_exists > 0:
                    print("Record with the same timestamp already exists. No new record inserted.")
                    return

                insert_query = """
                INSERT INTO regions (name, depth, angle_with_horizontal, avg_crater_slope, geodesic_diameter, geodesic_radius, centroid_x, centroid_y, centroid_z, crater_diameter)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (region_name, depth, angle, slope, geo_diameter, geo_radius, centroid_x, centroid_y,centroid_z, crater_dimater)

                cursor.execute(insert_query, values)
                mydb.commit()

        except Error as e:
            print("Error while connecting to MySQL:", e)
            

        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
                print("MySQL connection is closed")

    #new add to new tables for paper:

#----------------INSERT==FUNCTIONS-------------------------#

   

    def _conn(self):
        return mysql.connector.connect(
            host=self.host, user=self.user, password=self.password, database="hyb2_tir_lv3"
        )

    def add_asteroid(self, asteroid_name: str, alt_designation: str, notes: str, created_at):
     
        mydb = cur = None
        try:
            mydb = self._conn()
            cur = mydb.cursor()

            cur.execute(
                """
                SELECT asteroid_id
                FROM asteroids
                WHERE asteroid_name = %s OR alt_designation = %s
                LIMIT 1
                """,
                (asteroid_name, alt_designation)
            )
            row = cur.fetchone()
            if row:
                return row[0]  # existing asteroid info

            asteroid_id = str(uuid.uuid4())
            cur.execute(
                """
                INSERT INTO asteroids (asteroid_id, asteroid_name, alt_designation, notes, created_at)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (asteroid_id, asteroid_name, alt_designation, notes, created_at)
            )
            mydb.commit()

            cur.execute(
                """
                SELECT asteroid_id, asteroid_name, alt_designation, notes, created_at
                FROM asteroids
                WHERE asteroid_id = %s
                """,
                (asteroid_id,)
            )
            return asteroid_id 

        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None
        finally:
            try:
                if cur: cur.close()
                if mydb and mydb.is_connected(): mydb.close()
            except Exception:
                pass

    def add_mesh(self, asteroid_id, mesh_name, mesh_uri, polygon_count, vertex_count, fmt, checksum_sha256, created_at):
     
        mydb, cur = None, None
        try:
            mydb = self._conn(); cur = mydb.cursor()

            # Prefer stable uniqueness: check by (asteroid_id, mesh_name)
            cur.execute("""
                SELECT mesh_id FROM meshes
                WHERE asteroid_id = %s AND mesh_name = %s
                LIMIT 1
            """, (asteroid_id, mesh_name))
            row = cur.fetchone()
            if row:
                print("This mesh (by asteroid_id, mesh_name) already exists.")
                return row[0]

            # Optional: if mesh_uri should be unique globally, check it too
            cur.execute("SELECT mesh_id FROM meshes WHERE mesh_uri = %s LIMIT 1", (mesh_uri,))
            row = cur.fetchone()
            if row:
                print("This mesh (by mesh_uri) already exists.")
                return row[0]

            # Insert new with explicit UUID
            mesh_id = str(uuid.uuid4())
            cur.execute("""
                INSERT INTO meshes
                    (mesh_id, asteroid_id, mesh_name, mesh_uri, polygon_count, vertex_count, format, checksum_sha256, created_at)
                VALUES
                    (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (mesh_id, asteroid_id, mesh_name, mesh_uri, polygon_count, vertex_count, fmt, checksum_sha256, created_at))
            mydb.commit()
            print("Mesh inserted successfully.")
            return mesh_id

        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None
        finally:
            try:
                if cur: cur.close()
                if mydb and mydb.is_connected(): mydb.close()
            except Exception:
                pass
    
    def add_mesh_rigions(self, asteroid_id, mesh_id, region_name, region_uri, region_geom, region_polygon_ids, checksum_sha256, created_by, created_at):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            if mydb.is_connected():
                cursor = mydb.cursor()
                check_query = "SELECT COUNT(*) FROM mesh_regions WHERE region_uri = %s"
                cursor.execute(check_query, (region_uri,))
                record_exists = cursor.fetchone()[0]
                if record_exists >0:
                    print("This mesh already exists.")
                    return None
                insert_query = """
                INSERT INTO mesh_regions (asteroid_id, mesh_id, region_name, region_uri, region_polygon_ids, checksum_sha256, created_by, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (asteroid_id, mesh_id, region_name, region_uri, region_polygon_ids, checksum_sha256, created_by, created_at)
                cursor.execute(insert_query, values)
                mydb.commit()
                print("Mesh inserted successfully.")
        except Error as e:
            print("Error while connecting to MySQL: ", e)
            return None
        finally:
            if mydb.is_connected(): 
                cursor.close()
                mydb.close()
    
    def add_craters(self, asteroid_id, run_id, region_id, crater_code, crater_name, quality_score, crater_uri, created_at):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            if mydb.is_connected():
                cursor = mydb.cursor()
                # check_query = "SELECT COUNT(*) FROM craters WHERE crater_uri = %s"
                # cursor.execute(check_query, (crater_uri,))
                # record_exists = cursor.fetchone()[0]
                # if record_exists >0:
                #     print("This mesh already exists.")
                #     return record_exists
                crater_id = str(uuid.uuid4())
                insert_query = """
                INSERT INTO craters(crater_id,asteroid_id, run_id,region_id, crater_code, crater_name, quality_score, crater_uri, created_at)
                VALUES (%s,%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (crater_id,asteroid_id, run_id,region_id, crater_code, crater_name, quality_score, crater_uri, created_at)
                cursor.execute(insert_query, values)
                mydb.commit()
                print("Crater inserted successfully.")
                return crater_id 
                
                

        except Error as e:
            print("Error while connecting to MySQL: ", e)
            return None
        finally:
            if mydb.is_connected(): 
                cursor.close()
                mydb.close()
    
    def add_crater_morphology(self, crater_id, depth, angle_with_horizontal, avg_crater_slope, geodesic_diameter, geodesic_radius, centroid_x, centroid_y, centroid_z, crater_diameter, units):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            if mydb.is_connected():
                cursor = mydb.cursor()
                # check_query = "SELECT COUNT (*) FROM crater_morphology WHERE crater_id = %s"
                # cursor.execute(check_query, (crater_id,))
                # record_exists = cursor.fetchone()[0]
                # if record_exists > 0:
                #     print("This crater already exists.")
                #     return None
                insert_query = """
                INSERT INTO crater_morphology(crater_id, depth, angle_with_horizontal, avg_crater_slope, geodesic_diameter, geodesic_radius, centroid_x, centroid_y, centroid_z, crater_diameter, units)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (crater_id, depth, angle_with_horizontal, avg_crater_slope, geodesic_diameter, geodesic_radius, centroid_x, centroid_y, centroid_z, crater_diameter, units)
                cursor.execute(insert_query,values)
                mydb.commit()
                print("Crater Morphology is inserted successfully.")
        except Error as e:
            print("Error while connecting to MySQL: ", e)
            return e
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

    def add_crater_points(self, crater_id, seq, x, y, z):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            if mydb.is_connected():
                cursor = mydb.cursor()
                check_query = "SELECT COUNT (*) FROM crater_points WHERE crater_id = %s"
                cursor.execute(check_query, (crater_id,))
                record_exists = cursor.fetchone()[0]
                if record_exists > 0:
                    print("This crater already exists.")
                    return None
                insert_query = """
                INSERT INTO crater_points(crater_id, seq, x, y, z)
                VALUES (%s, %s, %s, %s, %s)
                """
                values = (crater_id, seq, x, y, z)
                cursor.execute(insert_query, values)
                mydb.commit()
                print("Crater points is added")
        except Error as e:
            print("Error while connecting to MySQL: ", e)
            return e
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()
    
    def add_crater_rim_polygons(self, rim_id, polygon_index):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            if mydb.is_connected():
                cursor = mydb.cursor()
                check_query = "SELECT COUNT (*) FROM crater_rim_polygons WHERE rim_id = %s"
                cursor.execute(check_query, (rim_id,))
                record_exists = cursor.fetchone()[0]
                if record_exists > 0:
                    print("This crater already exists.")
                    return None
                insert_query = """
                INSERT INTO crater_rim_polygons(rim_id, polygon_index)
                VALUES (%s, %s)
                """
                values = (rim_id, polygon_index)
                cursor.execute(insert_query, values)
                mydb.commit()
                print("Crater polygons is added")
        except Error as e:
            print("Error while connecting to MySQL: ", e)
            return e
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

    def add_crater_rims(self, crater_id, mesh_id, rim_center, rim_area, vertices_count, rim_polygon_ids, created_at, seed_points):   
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            if mydb.is_connected():
                cursor = mydb.cursor()
                
                insert_query = """
                INSERT INTO crater_rims( crater_id, mesh_id, rim_center, rim_area, vertices_count, rim_polygon_ids, created_at,seed_points)
                VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (crater_id, mesh_id, rim_center, rim_area, vertices_count, rim_polygon_ids, created_at, seed_points)
                cursor.execute(insert_query, values)
                mydb.commit()

        except Error as e:
            print("Error while connecting to MySQL: ", e)
            return e
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

    def add_run_info(self,asteroid_id, mesh_id,region_id, method_name, method_version, parameters, executed_by, executed_at, notes):
        try:
            mydb = mysql.connector.connect(
                host = self.host,
                user = self.user,
                password = self.password,
                database="hyb2_tir_lv3"
            )
            if mydb.is_connected():
                cursor = mydb.cursor()
                
                run_id = str(uuid.uuid4()) 
                insert_query = """
                INSERT INTO detection_runs(run_id, asteroid_id, mesh_id,region_id, method_name, method_version, parameters, executed_by, executed_at, notes)
                VALUES (%s, %s,%s, %s, %s, %s, %s, %s, %s, %s)
                """
                values = (run_id, asteroid_id, mesh_id, region_id, method_name, method_version, parameters, executed_by, executed_at, notes)
                cursor.execute(insert_query, values)
                mydb.commit()
                print("Run Information inserted successfully.")
                return run_id 

        except Error as e:
            print("Error while connecting to MySQL: ", e)
            return e
        finally:
            if mydb.is_connected():
                cursor.close()
                mydb.close()

#------------GET--INFORMATION-------------=#

    def get_info_region_from_path(self, region_uri):
        mydb, cur = None, None

        try:
            mydb = self._conn(); cur = mydb.cursor(dictionary=True)
            query = """
            SELECT region_id, asteroid_id, mesh_id, region_name
            FROM mesh_regions
            WHERE region_uri = %s
            LIMIT 1
            """
            cur.execute(query, (region_uri,))
            
            row = cur.fetchone()
            if row == None:
                region_id = str(uuid.uuid4())
                asteroid_id = str(uuid.uuid4())
                mesh_id = str(uuid.uuid4())
                row["region_id"] = region_id
                row["asteroid_id"] = asteroid_id
                row["mesh_id"] = mesh_id
                

            return row
        
        except Error as e:
            print("Error while connecting to MySQL:", e)
            return None
        finally:
            try:
                if cur: cur.close()
                if mydb and mydb.is_connected(): mydb.close()
            except Exception:
                pass

   