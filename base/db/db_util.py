import datetime
import json
import re

import tornado.ioloop
import tornado_mysql.pools as pools

import config

illegal_sql_pat = re.compile(r'(--|;|\sor\s|exec\s|union\s)', re.I | re.M)


def check_sql_statement(sql):
    # sql = str(sql)
    # result = illegal_sql_pat.search(sql)
    # if result:
    #     raise ValueError()
    pass

def dbo_dict(func):
    async def _dbo(*args, **kwargs):
        try:
            dbc = TornadoMysqlUtils(args[0].db_name)
            sql, args, keys = func(*args, **kwargs)
            res = await dbc.exec_sql(sql, args, log_sql=True)
            # convert to dict.
            dikts = [dict(zip(keys, [x.decode('utf-8') if isinstance(x, bytes) else x for x in r])) for r in res]
            # remove None items.
            dikts = [{k: v for k, v in i.items() if v is not None} for i in dikts]

            dbc.commit()
            return (dikts, None)
        except Exception as e:
            raise e
        finally:
            dbc.close()

    return _dbo


def dbo_dict_with_null(func):
    async def _dbo(*args, **kwargs):
        try:
            dbc = TornadoMysqlUtils(args[0].db_name)
            sql, args, keys = func(*args, **kwargs)
            res = await dbc.exec_sql(sql, args)
            # convert to dict.
            dikts = [dict(zip(keys, [x.decode('utf-8') if isinstance(x, bytes) else x for x in r])) for r in res]
            # remove None items.
            dikts = [{k: v for k, v in i.items()} for i in dikts]

            dbc.commit()
            return (dikts, None)
        except Exception as e:
            raise e
        finally:
            dbc.close()

    return _dbo


def dbo(func):
    async def _dbo(*args, **kwargs):
        try:
            dbc = TornadoMysqlUtils(args[0].db_name)
            sql, args = func(*args, **kwargs)
            if not sql:
                return (None, None)
            res = await dbc.exec_sql(sql, args, transaction=kwargs.get('transaction'))
            dbc.commit()
            return (res, None)
        except Exception as e:
            return (None, str(e))
            # raise e
        finally:
            dbc.close()

    return _dbo


class DBClause():

    @staticmethod
    def insert(table, what, prikey=None):
        s = ", ".join(["%s = '%s'" % (k, v) for k, v in what.items() if k != prikey and v is not None])
        stmt = "INSERT INTO `%s` SET %s" % (table, s)

        # if prikey:
        #     stmt += ', %s = "%s"' % (prikey, what[prikey])
        #
        #     stmt += " ON DUPLICATE KEY UPDATE "
        #     stmt += s

        # End
        # stmt += ";"

        # klog.d(stmt)
        return stmt, None

    @staticmethod
    def insertbigdata(table, what, prikey=None):
        key, value = [], []
        for k, v in what.items():
            if k != prikey and v is not None:
                key.append(k)
                if isinstance(v, str):
                    value.append('"' + v + '"')
                elif '{' in str(v) or '(' in str(v) or '[' in str(v) or isinstance(v, list) or isinstance(v, dict):
                    value.append('"' + 'object' + '"')
                else:
                    value.append(str(v))
        if key:

            # k, v = ",".join(key),  '", "' .join(value)
            k, v = ",".join(key), ', '.join(value)
            # k, v = k, '"' + v + '"'
            # k, v = key, value
            stmt = "INSERT INTO `%s` (  %s  ) VALUES (  %s  )" % (table, k, v)
            for i in range(100):
                stmt += ", ( %s  )" % v
        # if prikey:
        #     stmt += ', %s = "%s"' % (prikey, what[prikey])
        #
        #     stmt += " ON DUPLICATE KEY UPDATE "
        #     stmt += s

        # End
        # stmt += ";"

        # klog.d(stmt)
        return stmt, None

    @staticmethod
    def update(table, what, where, pkey):
        s = ", ".join(["%s = '%s'" % (k, v) for k, v in what.items() if k != pkey and v is not None])
        if not s:
            return None, None
        stmt = "UPDATE `%s` SET %s" % (table, s)

        if where:
            s = " AND ".join(
                ['%s = "%s"' % (k, v) for k, v in where.items() if (not isinstance(v, list) and v is not None)])
            s2 = " AND ".join(
                [str(k) + ' IN ("' + '","'.join(v) + '") ' for k, v in where.items() if isinstance(v, list)])
            if s:
                if s2:
                    s += ' AND ' + s2
            else:
                s = s2

            stmt += " WHERE %s" % s if s else ''

        # End
        # stmt += ";"

        # klog.d(stmt)
        return stmt, None

    @staticmethod
    def replace_db(table, what, where, pkey, from_str, to_str):
        s = ", ".join(
            [("%s = REPLACE(%s,'" + from_str + "','" + to_str + "')") % (k, k) for k, v in what.items() if k != pkey])
        stmt = "UPDATE `%s` SET %s" % (table, s)

        if where:
            s = " AND ".join(
                ['%s = "%s"' % (k, v) for k, v in where.items() if (not isinstance(v, list) and v is not None)])
            s2 = " AND ".join(
                [str(k) + ' IN ("' + '","'.join(v) + '") ' for k, v in where.items() if isinstance(v, list)])
            if s:
                if s2:
                    s += ' AND ' + s2
            else:
                s = s2

            stmt += " WHERE %s" % s if s else ''

        # End
        # stmt += ";"
        # print('replace_db sql: ', stmt)
        # klog.d(stmt)
        return stmt, None

    @staticmethod
    def query(table, what, where, orderby=None, descend=True, limit=None, like=False, interval=None):
        pat = ",".join(what) if what else "*"
        stmt = "SELECT %s FROM `%s`" % (pat, table)
        if where and len(where) > 0:
            s = " AND ".join(['%s = "%s"' % (k, v) for k, v in where.items() if
                              not isinstance(v, list) and (not like or '%' not in v)])
            if like:
                sl = " AND ".join(
                    ['%s LIKE "%s"' % (k, v) for k, v in where.items() if not isinstance(v, list) and '%' in v])
                if sl:
                    s = s + ' AND ' + sl if s else sl
            s2 = " AND ".join([str(k) + ' IN ("' + '","'.join([str(x) for x in v]) + '") ' for k, v in where.items() if
                               isinstance(v, list)])
            if s:
                if s2:
                    s += ' AND ' + s2
            else:
                s = s2
            stmt += " WHERE %s" % s
            stmt = stmt + ' AND ' if where and interval else stmt
        if interval:
            stmt = stmt + " WHERE " if not where else stmt
            column, operate, para1 = interval[0], interval[1], interval[2]
            para2 = interval[3] if len(interval) == 4 else None
            comma_string = "" if para1.isdigit() else "'"
            stmt_between = ''
            if operate == 'between':
                stmt_between = column + " BETWEEN " + comma_string + para1 + comma_string + " AND " + comma_string + para2 + comma_string
            elif operate == '>':
                stmt_between = column + " > " + comma_string + para1 + comma_string
            elif operate == '<':
                stmt_between = column + " < " + comma_string + para2 + comma_string
            stmt += stmt_between
        if orderby:
            stmt += (' order by %s ' % orderby) + ('desc' if descend else 'asc')

        if isinstance(limit, str):
            stmt += ' LIMIT ' + str(limit)
        # End
        # stmt += ";"

        # klog.d(stmt)
        return stmt, None

    @staticmethod
    def search(table, what, column, search, limit=None):
        pat = ",".join(what) if what else "*"
        stmt = "SELECT %s FROM `%s`" % (pat, table)
        if column and len(column) > 0:
            s = " OR ".join(['%s LIKE "%s"' % (each, '%' + search + '%') for each in column])
            stmt += " WHERE %s" % s

        if isinstance(limit, int):
            stmt += ' LIMIT ' + str(limit)
        # End
        # stmt += ";"

        # klog.d(stmt)
        return stmt, None

    @staticmethod
    def delete(table, where):
        stmt = "DELETE FROM `%s` " % table

        if where:
            s = " AND ".join(['%s = \'%s\'' % (k, v) for k, v in where.items()])
            stmt += "WHERE %s" % s

        # End
        # stmt += ";"

        # klog.d(stmt)
        return stmt, None


class BaseDbModel(object):
    tab_name = ''
    db_name = ''
    pkey = ''
    db_connection = None

    def __init__(self, obj=None):
        if obj:
            if isinstance(obj, dict):
                self.from_dict(obj)
            # else :
            #     self.from_dict(obj.__dict__)
        pass

    async def select_one_r(self):
        r, m = await self.select()
        db_model = None

        if len(r):
            db_model = type(self)(r[0])

        return db_model

    async def select_all(self):
        r, m = await self.select()
        return [type(self)(row) for row in r]

    def strip_self(self):
        return {k: v for k, v in self.__dict__.items() if v is not None}

    def input(self, obj):
        return self

    def set_attrib(self, name, val):
        if name in self.__dict__:
            object.__setattr__(self, name, val)
        pass

    def get_attrib(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        return None

    def from_dict(self, obj):
        for k, v in obj.items():
            if k in self.__dict__:
                object.__setattr__(self, k, v)
        return self

    def output(self):
        return self

    def set_context(self, ctxt, key):
        if 'context' in self.__dict__ and key in ctxt:
            self.context = ctxt

    def get_context(self):
        if 'context' in self.__dict__:
            return self.context
        return None

    @dbo
    def insert(self, transaction=None):
        self_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, dict) or isinstance(value, list):
                self_dict[key] = json.dumps(value)
            else:
                self_dict[key] = value
        sql, args = DBClause.insert(self.__class__.tab_name, self_dict)
        # sql += ' on duplicate key update `serialno`= 2332'
        return sql, args

    @dbo
    def insertbigdata(self):
        self_dict = {}
        for key, value in self.__dict__.items():
            if isinstance(value, dict) or isinstance(value, list):
                self_dict[key] = json.dumps(value)
            else:
                self_dict[key] = value
        sql, args = DBClause.insertbigdata(self.__class__.tab_name, self_dict)
        return sql, args

    @dbo
    def insert_no_pkey(self, transaction=None):
        sql, args = DBClause.insert(self.__class__.tab_name, self.__dict__, prikey=self.__class__.pkey)
        return sql, args

    @dbo
    def insert_no_pkeybigdata(self):
        sql, args = DBClause.insertbigdata(self.__class__.tab_name, self.__dict__, prikey=self.__class__.pkey)
        return sql, args

    @dbo
    def update(self, where=None, no_pkey=True, transaction=None):
        if not where and self.__class__.pkey in self.__dict__:
            sql, args = DBClause.update(self.__class__.tab_name, self.__dict__,
                                        {self.__class__.pkey: self.__dict__[self.__class__.pkey]},
                                        self.__class__.pkey)
        else:
            sql, args = DBClause.update(self.__class__.tab_name, self.__dict__,
                                        where if isinstance(where, dict) else where.__dict__,
                                        self.__class__.pkey if no_pkey else None)

        return sql, args

    @dbo
    def replace_db(self, where=None, no_pkey=True, from_str=None, to_str=None):
        sql, args = None, None
        if from_str and to_str:
            if not where and self.__class__.pkey in self.__dict__:
                sql, args = DBClause.replace_db(self.__class__.tab_name, self.__dict__,
                                                {self.__class__.pkey: self.__dict__[self.__class__.pkey]},
                                                self.__class__.pkey, from_str, to_str)
            elif not where:
                sql, args = DBClause.replace_db(self.__class__.tab_name, self.__dict__, None,
                                                self.__class__.pkey if no_pkey else None, from_str, to_str)
            elif where:
                sql, args = DBClause.replace_db(self.__class__.tab_name, self.__dict__,
                                                where if where and isinstance(where, dict) else where.__dict__,
                                                self.__class__.pkey if no_pkey else None, from_str, to_str)

        return sql, args

    @dbo
    def delete(self):
        sql, args = DBClause.delete(self.__class__.tab_name,
                                    {k: v for k, v in self.__dict__.items() if v is not None})
        return sql, args

    @dbo_dict
    def select(self, partial=None, orderby=None, descend=True, limit=None, pkey=False, like=False, interval=None,
               transaction=None):
        keys = [k for k, v in self.__dict__.items()] if not partial else [k for k, v in partial.__dict__.items() if
                                                                          v is not None]
        sql, args = DBClause.query(self.__class__.tab_name, keys,
                                   {k: v for k, v in self.__dict__.items() if v is not None} if not pkey else {
                                       self.__class__.pkey: self.__dict__[self.__class__.pkey]},
                                   orderby=orderby, descend=descend, limit=limit, like=like, interval=interval)
        return sql, args, keys

    async def select_count(self):
        sql = "select count(1) from {}".format(self.tab_name)
        dbc = TornadoMysqlUtils(self.db_name)
        res = await dbc.exec_sql(sql, None, log_sql=True)
        count = res[0][0]
        return count

    @dbo_dict_with_null
    def select_with_null(self, partial=None, orderby=None, limit=None, pkey=False, like=False, interval=None):
        keys = [k for k, v in self.__dict__.items()] if not partial else [k for k, v in partial.__dict__.items() if
                                                                          v is not None]
        sql, args = DBClause.query(self.__class__.tab_name, keys,
                                   {k: v for k, v in self.__dict__.items() if v is not None} if not pkey else {
                                       self.__class__.pkey: self.__dict__[self.__class__.pkey]},
                                   orderby, limit, like=like, interval=interval)
        return sql, args, keys

    @dbo_dict
    def search(self, column, search, partial=None, limit=None):
        keys = [k for k, v in self.__dict__.items()] if not partial else [k for k, v in partial.__dict__.items() if
                                                                          v is not None]
        sql, args = DBClause.search(self.__class__.tab_name, keys, column, search, limit)
        return sql, args, keys

    def __str__(self):
        return json.dumps(self.__dict__)


class TornadoMysqlUtils:
    __pool = {}
    __con_age = {}
    CONNECTION_MAX_AGE = 60 * 10  # in seconds
    db_host = config.db_host
    db_user = config.db_user
    db_passwd = config.db_passwd
    db_port = config.db_port
    name = ''

    def __init__(self, db):
        self.dbname = db
        if not self.__pool:
            self.clean_old_con()

        self.dbc = self.__getConn(self.dbname)

    @classmethod
    def clean_old_con(cls):
        for db, pool in cls.__pool.items():
            if db in cls.__con_age:
                age = datetime.datetime.now() - cls.__con_age[db]  # timedelta
                if age.seconds > cls.CONNECTION_MAX_AGE and pool:
                    pool.close()
                pass
            pass
        obj = tornado.ioloop.IOLoop.instance()
        if obj:
            obj.add_timeout(datetime.timedelta(milliseconds=60 * 1000), cls.clean_old_con)
        pass

    def __getConn(self, dbname):
        """
        @return MySQLdb.connection
        """
        TornadoMysqlUtils.__con_age[dbname] = datetime.datetime.now()

        if dbname not in self.__pool or not self.__pool[dbname]:
            TornadoMysqlUtils.__pool[dbname] = pools.Pool(dict(
                host=self.db_host,
                port=self.db_port,
                user=self.db_user,
                passwd=self.db_passwd,
                db=dbname, use_unicode=False, charset='utf8'), max_idle_connections=3,
            )

        return self.__pool[dbname]

    async def exec_sql(self, sqltxt, args=None, exception=True, log_sql=True, transaction=None):
        if self.dbc != None:
            try:
                check_sql_statement(sqltxt)

                need_commit = False

                if transaction is None:
                    transaction = await self.dbc.begin()
                    need_commit = True
                cur = await transaction.execute(sqltxt, args)
                result = cur.fetchall()

                if need_commit:
                    await transaction.commit()
                return result
            except Exception as data:
                if exception:
                    raise data
        else:
            return None

    def close(self):
        pass

    def commit(self):
        pass
