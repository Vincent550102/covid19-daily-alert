import psycopg2
class DATABASE:
    def __init__(self):
        DATABASE_URL = 'postgres://hqvrhtvsxacall:b01c9ac3e91caa3d577045584dece21204afbf21d0719eeda86abf705ae2e751@ec2-18-214-195-34.compute-1.amazonaws.com:5432/d1o8sm789444ro'
        self.conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        self.cursor = self.conn.cursor()

    def Insert(self, uid):
        SQL_order = f'INSERT INTO user_data (uid,isopen) VALUES (%s, %s);'
        val = ("{uid}", True)
        self.cursor.execute(SQL_order, val)
        self.conn.commit()
        self.Close()

    def Select(self):
        SQL_order = 'SELECT * FROM user_data WHERE isopen = true'
        self.cursor.execute(SQL_order)
        self.conn.commit()
        data = self.cursor.fetchall()
        self.Close()
        return data

    def Close(self):
        self.conn.close()
        self.cursor.close()