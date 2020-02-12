class Pagination:
    def __init__(self, offset, pages=[], count=5):
        self.offset = offset
        self.pages = pages
        self.count = count
        self.range = [i for i in range(1,len(self.pages)//self.count)]

    def getNextPage(self):
        if self.range[0] < self.offset+1 < self.range[-1]:
            return self.offset+1
        else:
            return self.range[0]

    def getPrevPage(self):
        if self.range[0] < self.offset-1 < self.range[-1]:
            return self.offset-1
        else:
            return self.range[0]

    def getCurrPage(self):
        return self.offset

    def getPaginated(self):
        return self.pages[(self.offset-1)*self.count:(self.offset)*self.count]

    def getListPages(self):
        '''
            Returns list of pages w selected count
        '''
        pass
