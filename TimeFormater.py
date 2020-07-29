from builtins import str
from builtins import object
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *

from datetime import datetime
from datetime import timedelta

#Convenient function to debug
log = lambda m: QgsMessageLog.logMessage(m, "visualist")

EXCEL = ['ExcelDate', 'ExcelTime', 'ExcelDateTime']
DATE = [EXCEL[0], '%d.%m.%Y', '%d-%m-%Y']
TIME = [EXCEL[1], '%H:%M:%S']
DURATION = [EXCEL[1], '%S', '%H:%M:%S']
DATETIME = [EXCEL[2], '%d.%m.%y %H:%M:%S', '%d.%m.%Y %H:%M:%S', '%d/%m/%Y %H:%M:%S', '%Y-%m-%d %H:%M:%S']

T1 = 'time1'
T2 = 'time2'
D1 = 'date1'
D2 = 'date2'
DUR = 'duration'
FEAT = 'feature'

#time = (year,month,day,hour,minute,second)
class temporalAnalyser(object):

    def __init__(self, layer, feedback):

        self.feedback = feedback

        self.fields = {D1:None, T1:None, D2:None, T2:None, DUR:None}
        self.formats = {D1:None, T1:None, D2:None, T2:None, DUR:None}
        self.parsed = {} #key: feature id, value: parsed {D1:None, T1:None, D2:None, T2:None, DUR:None}
        self.empty = {D1:0, T1:0, D2:0, T2:0, DUR:0} #To show number of missing data

        self.dataLayer = layer
        self.dataId = layer.id()

    def tr(self, text, context = "temporalAnalyser"):
        return QApplication.translate(context, text)

    def setLayer(self, layer):
        self.dataLayer = layer

    def parse(self):
        provider = self.dataLayer.dataProvider()
        for feat in provider.getFeatures():
            self.parseFeature(feat)
        error = "<b>"+self.tr("Empty or unparsable values")+":</b><br >"
        e = False
        for k, v in self.empty.items():
            if v > 0: e = True
            error += "<b>" + str(v) + "</b> "+self.tr("values for")+" " + str(k).upper() + "<br >"
        if e:
            self.feedback.reportError(self.tr('{}').format(error))

    def parseFeature(self, feat):
        line = {D1:None, T1:None, D2:None, T2:None, DUR:None}
        attrMap = feat.attributes()
        provider = self.dataLayer.dataProvider()
        for key, v in self.fields.items():
            if v == None:
                continue
            k = provider.fieldNameIndex(v)
            value = attrMap[int(k)]

            format = self.formats[key]
            if format in EXCEL:
                try: parsed = xlToDt(value, format)
                except: parsed = None
            else:
                if str(format) == '%S':
                    t = int(value)
                    h = int(t / 3600)
                    m = int((t-h * 3600) / 60)
                    s = int(t - h * 3600 - m * 60)
                    parsed = datetime(1900, 1, 1, h, m, s)
                else:
                    parsed = datetime.strptime(str(value), str(format))
            if parsed is None:
                self.empty[key] += 1
            line[key] = parsed
        self.parsed[feat.id()] = line


    def setDateTime(self, date1, time1):
        self.fields['date1'] = date1
        self.fields['time1'] = time1

    def setDateTimeDuration(self, date1, time1, duration):
        self.setDateTime(date1, time1)
        self.fields['duration'] = duration
        self.fields['date2'] = None
        self.fields['time2'] = None

    def setDateTimes(self, date1, time1, date2, time2):
        self.setDateTime(date1, time1)
        self.fields['date2'] = date2
        self.fields['time2'] = time2
        self.fields['duration'] = None

    def setFormatersDateTime(self, date1, time1):
        self.formats['date1'] = date1
        self.formats['time1'] = time1

    def setFormatersDateTimeDuration(self, date1, time1, duration):
        self.setFormatersDateTime(date1, time1)
        self.formats['duration'] = duration
        self.formats['date2'] = None
        self.formats['time2'] = None

    def setFormatersDateTimes(self, date1, time1, date2, time2):
        self.setFormatersDateTime(date1, time1)
        self.formats['date2'] = date2
        self.formats['time2'] = time2
        self.formats['duration'] = None

def getDates(data, i):
    dt1,dt2 = None, None
    if data[D1][i] is not None:
        if data[T1][i] is not None and len(data[T1]) > 0:
            dt1 = datetime.combine(data[D1][i].date(), data[T1][i].time())
        else:
            dt1 = data[D1][i]
    elif data[T1][i] is not None:
        dt1 = data[T1][i]

    if data[D2][i] is not None and len(data[D2]) > 0:
        if data[T2][i] is not None and len(data[T2]) > 0:
            dt2 = datetime.combine(data[D2][i].date(), data[T2][i].time())
        else:
            dt2 = data[D2][i]
    elif data[DUR][i] is not None and len(data[DUR]) > 0:
        if dt1 is not None:
            t = data[DUR][i].time()
            delta = timedelta(hours=t.hour,minutes=t.minute, seconds=t.second)
            dt2 = dt1 + delta
    if dt2 is None: dt2 = dt1
    return [dt1, dt2]

def xlToDt(excel, type):
    if excel is None or len(excel) == 0:
        return None
    t = xlrd.xldate_as_tuple(float(excel), 0)
    #self.warning(str(excel)+" -> "+str(t))
    if type == EXCEL[0]:
        return datetime(t[0], t[1], t[2], 0, 0, 0)
    elif type == EXCEL[1]:
        return datetime(1900, 1, 1, t[3], t[4], t[5])
    elif type == EXCEL[2]:
        return datetime(t[0], t[1], t[2], t[3], t[4], t[5])
    else:
        return None
