import mysql.connector

import config


class DataBase(mysql.connector.connection.MySQLConnection):
    def __init__(self):
        try:
            super().__init__(host=config.DB_HOST, user=config.DB_USER, password=config.DB_PASS, database=config.DB_NAME)
        except mysql.connector.Error as e:
            print(e)
        self.crs = self.cursor()

    def __enter__(self):
        self.__init__()
        return self

    def __exit__(self,*args,**kwargs):
        self.close()

    def test_connection(self):
        cursor = self.cursor()
        cursor.execute(f'SELECT * FROM {config.TABLE_COUNTRIES}')
        results = cursor.fetchall()
        if results:
            print('DataBase working')
            return True
        else:
            print('DataBase error!')
            return False

    def table_exists(self, name):
        cursor = self.cursor()
        sql = 'SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s'
        cursor.execute(sql, (name,))
        return bool(cursor.fetchone()[0])

    def set_record(self, table, record, many=False, skip_existing=False, print_sql=False):
        sql = self.build_setter_sql(table, record.keys() if not many else record[0].keys())
        if print_sql:
            print(sql)
        if many:
            self.crs.executemany(sql, tuple([tuple(r.values()) for r in record]))
        else:
            try:
                self.crs.execute(sql, tuple(record.values()))
                return self.crs.lastrowid
            except mysql.connector.errors.IntegrityError:
                if skip_existing:
                    return None
                else:
                    raise mysql.connector.errors.IntegrityError
            except mysql.connector.errors.DatabaseError:
                print(record)
                print(sql)
                raise mysql.connector.errors.DatabaseError
            
    def get_record(self, table, columns_to_select=None, conditions=None, write_if_new=True, all_rows=False, print_sql=False):
        conditions = conditions or {}
        sql = self.build_getter_sql(table, columns_to_select, conditions.keys())
        if print_sql:
            print(sql)
        self.crs.execute(sql, tuple(conditions.values()))
        if all_rows:
            rows = self.crs.fetchall()
            return rows
        else:
            row = self.crs.fetchone()
            if not row and write_if_new:
                return [self.set_record(table, conditions)]
            return row
        
    def update_record(self, table, record, conditions=None):
        sql = self.build_updater_sql(table, record.keys(),conditions.keys())
        values = tuple(record.values())+tuple(conditions.values())
        self.crs.execute(sql, values)

    def delete_record(self, table, conditions=None):
        if not conditions:
            raise KeyError
        sql = self.get_deleter_sql(table, conditions.keys())
        self.crs.execute(sql, tuple(conditions.values()))

    def delete_table(self, table):
        sql = f'DROP {table}'
        self.crs.execute(sql)

    @staticmethod
    def build_getter_sql(table, keys, cond_keys):
        sql_template = f'SELECT KEYS FROM {table}'
        key_str = ''
        cond_str = ''
        if not keys:
            key_str = '*,'
        else:
            for k in keys:
                key_str += f'`{k}`,'
        sql = sql_template.replace('KEYS', key_str[:-1])
        if cond_keys:
            sql += ' WHERE CONDS'
            for ck in cond_keys:
                cond_str += ck + '=%s AND '
            sql = sql.replace('CONDS', cond_str[:-5])
        return sql

    @staticmethod
    def build_setter_sql(table, keys):
        sql_template = f'INSERT INTO {table}(KEYS) VALUES (VALS)'
        key_str = ''
        val_str = ''
        for k in keys:
            key_str += f'`{k}`,'
            val_str += '%s,'
        sql = sql_template.replace('KEYS', key_str[:-1])
        sql = sql.replace('VALS', val_str[:-1])
        return sql

    @staticmethod
    def build_updater_sql(table, keys, cond_keys):
        sql_template = f'UPDATE {table} SET KEYS'
        key_str = ''
        cond_str = ''
        for k in keys:
            key_str += f'`{k}`=%s,'
        sql = sql_template.replace('KEYS', key_str[:-1])
        if cond_keys:
            sql += ' WHERE CONDS'
            for ck in cond_keys:
                cond_str += ck + '=%s AND '
            sql = sql.replace('CONDS', cond_str[:-5])
        return sql

    @staticmethod
    def get_deleter_sql(table, cond_keys):
        sql = f'DELETE FROM {table} WHERE CONDS'
        cond_str = ''
        for ck in cond_keys:
            cond_str += ck + '=%s AND '
            sql = sql.replace('CONDS', cond_str[:-5])
        return sql


if __name__ == '__main__':
    with DataBase() as db:
        print(db.table_exists('event_meta'))
