class CleanDataForJinga(object):

    def __init__(self,data,columnRearrange,indexColumnName):
        self.data=data
        self.columnRearrange=columnRearrange
        self.indexColumnName=indexColumnName

    def CleanForEndUser(self):
        self.data[self.indexColumnName]=self.data.index
        self.data=self.data[self.columnRearrange]
        self.data=self.data.reset_index(drop=True)

        # Normalize Dates from '2020-01-01 00:00:00' to '2020-01-01' in pandas
        if self.indexColumnName=='Date':
            self.data['Date'] = self.data['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))
        return self.data



