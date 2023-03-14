from Program.Production.Logger import Logger
#from numpy import loadtxt

"""
# params = {
#     'inKeys': k,
#     'inValues': [
#         [16.5, 18.5, 27.0, 25.0, 27.0, 21.0, 20.0, 20.0, 20.0, 31.0, 25.0, 21.5, 20.5, 20.0, 28.0, 20.0, 11.0, 14.0, 12.5, 21.5, 23.5, 20.5, 25.0, 22.5, 30.0, 23.0, 29.0, 22.5, 20.0, 17.5, 17.5,17.0, 19.5, 44.5, 19.5, 16.0, 12.0, 17.0, 20.5,12.0, 16.0, 11.5, 25.0, 16.0, 19.5, 16.0, 15.0, 14.0, 16.0, 7.0, 11.0, 33.5, 11.0, 15.5, 23.0, 18.5, 13.5, 17.0, 15.0, 14.5, 11.0, 9.5, 11.5, 10.0, 21.0, 16.0, 10.0, 9.0, 15.0, 22.5, 16.0, 15.5, 16.5, 12.5, 22.0, 12.0, 20.5, 11.0, 10.0, 10.0, 8.5, 8.5, 8.5, 9.5, 9.5, 9.5, 11.5, 13.0, 8.5],
#         [16.5, 18.5, 27.0, 25.0, 27.0, 21.0, 20.0, 20.0, 20.0, 31.0, 25.0, 21.5, 20.5, 20.0, 28.0, 20.0, 11.0, 14.0, 12.5, 21.5, 23.5, 20.5, 25.0, 22.5, 30.0, 23.0, 29.0, 22.5, 20.0, 17.5, 17.5,17.0, 19.5, 44.5, 19.5, 16.0, 12.0, 17.0, 20.5,12.0, 16.0, 11.5, 25.0, 16.0, 19.5, 16.0, 15.0, 14.0, 16.0, 7.0, 11.0, 33.5, 11.0, 15.5, 23.0, 18.5, 13.5, 17.0, 15.0, 14.5, 11.0, 9.5, 11.5, 10.0, 21.0, 16.0, 10.0, 9.0, 15.0, 22.5, 16.0, 15.5, 16.5, 12.5, 22.0, 12.0, 20.5, 11.0, 10.0, 10.0, 8.5, 8.5, 8.5, 9.5, 9.5, 9.5, 11.5, 13.0, 8.5],
#         [16.5, 18.5, 27.0, 25.0, 27.0, 21.0, 20.0, 20.0, 20.0, 31.0, 25.0, 21.5, 20.5, 20.0, 28.0, 20.0, 11.0, 14.0, 12.5, 21.5, 23.5, 20.5, 25.0, 22.5, 30.0, 23.0, 29.0, 22.5, 20.0, 17.5, 17.5,17.0, 19.5, 44.5, 19.5, 16.0, 12.0, 17.0, 20.5,12.0, 16.0, 11.5, 25.0, 16.0, 19.5, 16.0, 15.0, 14.0, 16.0, 7.0, 11.0, 33.5, 11.0, 15.5, 23.0, 18.5, 13.5, 17.0, 15.0, 14.5, 11.0, 9.5, 11.5, 10.0, 21.0, 16.0, 10.0, 9.0, 15.0, 22.5, 16.0, 15.5, 16.5, 12.5, 22.0, 12.0, 20.5, 11.0, 10.0, 10.0, 8.5, 8.5, 8.5, 9.5, 9.5, 9.5, 11.5, 13.0, 8.5],
#     ],
#     'outKeys': l,
# }
#print(params['outKeys'])
params = {
    'inKeys': ['p83', 'p84', 'p85', 'p86', 'p87', 'p88', 'p89', 'p90', 'p91', 'p92', 'p93', 'p94', 'p95', 'p96', 'p97', 'p100', 'p101', 'p102', 'p103', 'p104', 'p105', 'p106', 'p107', 'p108', 'p109', 'p110', 'p111', 'p112', 'p113', 'p114', 'p115', 'p116', 'p117', 'p118', 'p120', 'p123', 'p125', 'p126', 'p127', 'p128', 'p129', 'p130', 'p131', 'p132', 'p133', 'p134', 'p135', 'p136', 'p137', 'p138', 'p140', 'p143', 'p145', 'p146', 'p147', 'p148', 'p149', 'p150', 'p151', 'p152', 'p153', 'p154', 'p155', 'p156', 'p157', 'p158', 'p159', 'p160', 'p161', 'p162', 'p163', 'p164', 'p165', 'p166', 'p167', 'p168', 'p169', 'p170', 'p171', 'p172', 'p173', 'p174', 'p175', 'p176', 'p177', 'p178', 'p179', 'p180', 'p181'],
    'inValues': [
        [16.5, 18.5, 27.0, 25.0, 27.0, 21.0, 20.0, 20.0, 20.0, 31.0, 25.0, 21.5, 20.5, 20.0, 28.0, 20.0, 11.0, 14.0, 12.5, 21.5, 23.5, 20.5, 25.0, 22.5, 30.0, 23.0, 29.0, 22.5, 20.0, 17.5, 17.5,17.0, 19.5, 44.5, 19.5, 16.0, 12.0, 17.0, 20.5,12.0, 16.0, 11.5, 25.0, 16.0, 19.5, 16.0, 15.0, 14.0, 16.0, 7.0, 11.0, 33.5, 11.0, 15.5, 23.0, 18.5, 13.5, 17.0, 15.0, 14.5, 11.0, 9.5, 11.5, 10.0, 21.0, 16.0, 10.0, 9.0, 15.0, 22.5, 16.0, 15.5, 16.5, 12.5, 22.0, 12.0, 20.5, 11.0, 10.0, 10.0, 8.5, 8.5, 8.5, 9.5, 9.5, 9.5, 11.5, 13.0, 8.5],
        [16.5, 18.5, 27.0, 25.0, 27.0, 21.0, 20.0, 20.0, 20.0, 31.0, 25.0, 21.5, 20.5, 20.0, 28.0, 20.0, 11.0, 14.0, 12.5, 21.5, 23.5, 20.5, 25.0, 22.5, 30.0, 23.0, 29.0, 22.5, 20.0, 17.5, 17.5,17.0, 19.5, 44.5, 19.5, 16.0, 12.0, 17.0, 20.5,12.0, 16.0, 11.5, 25.0, 16.0, 19.5, 16.0, 15.0, 14.0, 16.0, 7.0, 11.0, 33.5, 11.0, 15.5, 23.0, 18.5, 13.5, 17.0, 15.0, 14.5, 11.0, 9.5, 11.5, 10.0, 21.0, 16.0, 10.0, 9.0, 15.0, 22.5, 16.0, 15.5, 16.5, 12.5, 22.0, 12.0, 20.5, 11.0, 10.0, 10.0, 8.5, 8.5, 8.5, 9.5, 9.5, 9.5, 11.5, 13.0, 8.5],
        [16.5, 18.5, 27.0, 25.0, 27.0, 21.0, 20.0, 20.0, 20.0, 31.0, 25.0, 21.5, 20.5, 20.0, 28.0, 20.0, 11.0, 14.0, 12.5, 21.5, 23.5, 20.5, 25.0, 22.5, 30.0, 23.0, 29.0, 22.5, 20.0, 17.5, 17.5,17.0, 19.5, 44.5, 19.5, 16.0, 12.0, 17.0, 20.5,12.0, 16.0, 11.5, 25.0, 16.0, 19.5, 16.0, 15.0, 14.0, 16.0, 7.0, 11.0, 33.5, 11.0, 15.5, 23.0, 18.5, 13.5, 17.0, 15.0, 14.5, 11.0, 9.5, 11.5, 10.0, 21.0, 16.0, 10.0, 9.0, 15.0, 22.5, 16.0, 15.5, 16.5, 12.5, 22.0, 12.0, 20.5, 11.0, 10.0, 10.0, 8.5, 8.5, 8.5, 9.5, 9.5, 9.5, 11.5, 13.0, 8.5],
    ],
    'outKeys': ['p36', 'p33', 'p35', 'p34', 'p50', 'p76', 'p56', 'p79', 'p52', 'p77', 'p54', 'p78', 'p57', 'p58', 'p80'],
}
"""
"""comment"""

class APParameters:

    """
    Класс параметров оптимизации. Включает в себя названия и значения переменных оптимизации.
    и названия параметров для целевой функции

    inputs:
    inKeys: названия варьируемых параметров
    nValues: значения варьируемых параметров
    outKeys: названия целевых параметров


    """
    def __init__(self,
        path = None,
        inKeys = [],
        inValues = [[]],
        outKeys = [],
    ):
        self._logger = Logger('log.txt')
        self._log_ = self._logger.log
        self.__path = path + '/' if path != None  else ''
        self.__inKeys = inKeys
        self.__inValues = inValues
        self.__outKeys = outKeys
        if path == None and len(inKeys) > 0 and len(inValues) > 0 and len(outKeys) > 0:
            self._log_('[APParameters] from input parameters')
            self.__initied = True
        else:
            self._log_('[APParameters] from file...')
            self.__initied = False
        self._log_('[APParameters]: ' + str(self.__class__.__name__))

    ''''''
    def __fromFile(self):
        #self.__initied = False
        self.__inKeys = []
        self.__inValues = []    # [ [] ]
        self.__outKeys = []
        with open(self.__path + 'input keys.txt') as f:
            self.__inKeys = f.read().splitlines()
        with open('input values.txt') as f:
            inValuesRow = []
            inStrValues = f.read().splitlines()
            for strValue in inStrValues:
                value = strValue.replace(',', '.')
                inValuesRow.append(float(value))
            self.__inValues.append(inValuesRow)
        lens = []
        for row in self.__inValues:
            lens.append(len(row))
            if len(self.__inKeys) != len(row):
                raise Exception('In Keys')
        self._log_('[APParameters] Number of inputs: ')
        self._log_(lens)
        with open('output keys.txt') as f:
            self.__outKeys = f.read().splitlines()
        if len(self.__inKeys) <= 0:
           raise Exception('111')
        self._log_('[APParameters] Number of input parameters: ' + str(len(self.__inKeys)))
        if len(self.__outKeys) <= 0:
            raise Exception('Output keys')
        self._log_('[APParameters] Number of output parameters: ' + str(len(self.__outKeys)))
        self.__initied = True

    ''''''
    def inputP(self):
        if not self.__initied:
            self.__fromFile()
            self._log_('[APParameters] from file: ')
        keys = {}
        index = 0
        self._log_('[APParameters] __InValues : '+str(self.__inValues))
        for key in self.__inKeys:
            if not key in keys.keys():
                keys[key] = []
            for row in self.__inValues:
                keys[key].append(row[index])
            index += 1
        self._log_('[APParameters] __InValues : '+str(self.__inValues))
        self._log_('[APParameters] inputP : '+str(keys))

        return keys
    ''''''
    def outputP(self):
        return self.__outKeys

    def inKeys(self):
        return self.__inKeys

    def inValues(self):
        return self.__inValues

    def outKeys(self):
        return self.__outKeys

    def activity_from_domain_model(self, objects: list):
        #self.__inValues.append(0)
        for object in objects:
            self.__inValues[0].append(object.object_info.object_activity)

    def from_domain_model(self, objects: list, last_index):
        for object in objects:
            self.__inValues[0].append(object.object_info.object_activity)
        for i in range(len(self.__inValues[0])):
            if not self.__inValues[0][i]:
                self.__inValues[0][i] = last_index+1
            else:
                self.__inValues[0][i] = 0

    def from_results(self, results: list):
        self.__inValues[0] = results.copy()



