import psycopg2
from configparser import ConfigParser
import json
import jsonpickle


class Db:
    def config(filename='config.ini', section='postgresql'):
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(section, filename))

        return db

    def update(filename, data):
        """ update vendor name based on the vendor id """
        sql = """ UPDATE qa_audio
                    SET json_data = %s
                    SET status = 'processed'
                    WHERE filename = %s"""

        conn = None
        updated_rows = 0
        try:
            # read database configuration
            params = Db.config()
            # connect to the PostgreSQL database
            conn = psycopg2.connect(**params)
            # create a new cursor
            cur = conn.cursor()
            # execute the UPDATE  statement
            cur.execute(sql, (json.dumps(data), filename))
            # get the number of updated rows
            updated_rows = cur.rowcount
            # Commit the changes to the database
            conn.commit()
            # Close communication with the PostgreSQL database
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()

        return updated_rows

    def get_files():
        global result

        conn = None
        try:
            result = []
            params = Db.config()
            conn = psycopg2.connect(**params)
            cur = conn.cursor()
            cur.execute("SELECT filename FROM qa_audio where status = 'pending'")
            row = cur.fetchone()

            while row is not None:
                result.append(row)
                row = cur.fetchone()

            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        finally:
            if conn is not None:
                conn.close()
        return result
