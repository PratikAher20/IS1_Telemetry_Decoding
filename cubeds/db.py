import psycopg2
import psycopg2.extras
import cubeds.pylogger
import cubeds.exceptions


class Database:
    created_tables = False

    def __init__(self, config):
        self._logger = cubeds.pylogger.get_logger(__name__)
        self.config = config
        self.conn = None
        self.dbname = self.config.config['database']['postgresql'][self.config.yaml_key]['dbname']
        self.password = self.config.config['database']['postgresql'][self.config.yaml_key]['password']
        self.user = self.config.config['database']['postgresql'][self.config.yaml_key]['user']
        self.host = self.config.config['database']['postgresql'][self.config.yaml_key]['host']
        self.port = self.config.config['database']['postgresql'][self.config.yaml_key]['port']
        self.index_key = 'time_index'
        self.index_min = 568085317
        self.index_max = 789010117

        self.page_size = 1000

        self.auth_string = "dbname=" + self.dbname \
                           + " user=" + self.user \
                           + " password=" + self.password \
                           + " port=" + str(self.port) \
                           + " host=" + self.host

        self.table_cmd = """CREATE TABLE IF NOT EXISTS telemetry( 
                                t INTEGER NOT NULL, 
                                tlm_val float NOT NULL,
                                mnemonic VARCHAR NOT NULL REFERENCES telemetry_definitions(mnemonic),
                                PRIMARY KEY (t, mnemonic));"""

        self.package_cmd = """CREATE TABLE IF NOT EXISTS telemetry_packages(
                                package VARCHAR NOT NULL PRIMARY KEY,
                                apid INTEGER UNIQUE NOT NULL,
                                size INTEGER NOT NULL);"""

        self.tlm_defs_cmd = """CREATE TABLE IF NOT EXISTS telemetry_definitions(
                                mnemonic VARCHAR PRIMARY KEY UNIQUE,
                                package VARCHAR REFERENCES telemetry_packages(package) NOT NULL,
                                states JSON,
                                unit VARCHAR,
                                max_val NUMERIC DEFAULT NULL,
                                min_val NUMERIC DEFAULT NULL,
                                conv VARCHAR DEFAULT '0:1');"""

        self.insert_package = """INSERT INTO telemetry_packages (package, apid, size) VALUES %s ON CONFLICT DO NOTHING;"""

        self.insert_tlm_def = """INSERT INTO telemetry_definitions (
                                                    mnemonic, package, states, unit, max_val, min_val, conv)
                                        VALUES %s ON CONFLICT DO NOTHING;"""

        self.index_cmd = """CREATE INDEX IF NOT EXISTS common
                                ON telemetry (mnemonic, t);"""

        self.insert_query = """INSERT INTO telemetry (t, tlm_val, mnemonic) VALUES %s
                                ON CONFLICT
                                DO NOTHING"""
        self.cluster_cmd = """CLUSTER telemetry USING common;"""

    def __del__(self):
        """
        Safely closes class.
        :return:
        """
        self.close()

    def connect(self):
        try:
            conn = psycopg2.connect(self.auth_string)
            self._logger.verbose("Connected to database "+self.dbname)
            conn.autocommit = True
            self.conn = conn

        except psycopg2.OperationalError as e:
            self._logger.fatal(e)
            self._logger.fatal("Cannot connect to database. Exiting.")
            raise e

    def close(self):
        if self.conn is not None:
            self._logger.verbose("Closed DB connection to database "+self.dbname)
            self.conn.close()
            self.conn = None

    def get_cursor(self):
        return self.conn.cursor()

    def cluster(self):
        cur = self.conn.cursor()
        cur.execute(self.cluster_cmd)
        self.conn.commit()
        cur.close()
        self._logger.info("Clustered db")

