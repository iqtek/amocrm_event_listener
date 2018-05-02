from settings import MYSQL_SETTINGS as DB
from settings import MYSQL_MAPPING as DB_MAPPING
import db
import pprint
from lib.ami import Ami as Ami
from lib.logutils import get_pretty_logger
__all__ = ["worker", ]

class Cdr(object):
    """Cdr"""

    event = {
        "Cdr",
        "Dial",
    }

    def __init__(self, *args, **kwargs):
        self._logger = get_pretty_logger(self.__class__)
        self.columns = set([])
        self.settings = kwargs.get("settings", {})
        self.ami = Ami.getInstance()
        self.db = db.DB()
        self.db.host(DB["host"]).user(DB["user"]).password(DB["password"]).db(DB["dbname"]).connect()

        cursor = self.db.query("""\
             SHOW COLUMNS FROM  `cdr`
         """)

        while (1):
            row = cursor.fetchone ()
            if row == None:
                  break
            self.columns.add(row[0].lower())
        cursor.close()

    def handle_Cdr(self, ami, event):
        fields = set([])
        cdrdict = {}
        cdrevent = {}
        for k, v in event.iteritems():
            for eventname, cdrname in DB_MAPPING.iteritems():
                if (k == eventname):
                    cdrdict[cdrname] = v
            cdrevent[k.lower()] = v
            fields.add(k.lower())
        cdrfields = set.intersection(self.columns, fields)

        for fld in cdrfields:
            cdrdict[fld] = cdrevent[fld]

        self._logger.info(pprint.pformat(event))
        self._logger.info(pprint.pformat(cdrevent))

        marks = ', '.join(['\'%s\''] * len(cdrdict))
        tables = ', '.join(cdrdict.keys())
        qry = "INSERT INTO cdr (%s) VALUES (%s)" % (tables, marks)
        cursor = self.db.query(qry % tuple(cdrdict.values()))

#Event: Dial
#Privilege: call,all
#SubEvent: Begin
#Channel: SIP/470-000079dd
#Destination: SIP/474-000079de
#CallerIDNum: 470
#CallerIDName: 470
#UniqueID: 1372066112.31203
#DestUniqueID: 1372066112.31204
#Dialstring: 474

    def handle_Dial(self, ami, event):
        if (event['SubEvent'] == 'Begin'):
            self._logger.info(pprint.pformat(event))
            try:
                qry = "INSERT INTO dial_log (`time`,`uniqueid`,`channel`,`dstuid`,`dstchannel`,`callerid`,`dial`) VALUES (NOW(), '%s', '%s', '%s', '%s', '%s', '%s')" % (event['UniqueID'], event['Channel'], event['DestUniqueID'], event['Destination'], event['CallerIDNum'], event['Dialstring'])
                cursor = self.db.query(qry)
                qry = "DELETE FROM `dial_log` WHERE `time`<=DATE_SUB(NOW(), INTERVAL 2 MINUTE)"
                cursor = self.db.query(qry)
            except:
                pass

worker = Cdr()