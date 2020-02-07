class CleanDataForJinga(object):

    def __init__(self,data,columnRearrange,indexColumnName,reverse=None):
        self.data=data
        self.columnRearrange=columnRearrange
        self.indexColumnName=indexColumnName
        self.reverse=reverse

    def CleanForEndUser(self):
        print(self.data)
        print(self.indexColumnName)
        print(self.data.index)
        # Give index as one of the column name and deleted index
        self.data[self.indexColumnName]=self.data.index
        
        # Rearrange Column Names as desired to be displayed
        self.data=self.data[self.columnRearrange]

        # Remove the index from the dataframe
        self.data=self.data.reset_index(drop=True)

        # Normalize Dates from '2020-01-01 00:00:00' to '2020-01-01' in pandas
        if self.indexColumnName=='Date':
            self.data['Date'] = self.data['Date'].apply(lambda x: x.strftime('%Y-%m-%d'))

        # Check if Dataframe needs to be reversed
        if self.reverse:
            # Reverse the DataFrame as needed
            self.data=self.data.iloc[::-1]

        return self.data



