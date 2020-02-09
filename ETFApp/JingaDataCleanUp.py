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


class CleanData(object):

    def __init__(self):pass

    def deleteColumns(self,data,columnListForDeletion):
        for i in columnListForDeletion:
            del data[i]
        return data

    # from '1999-03-10 00:00:00' to '1999-03-10'
    def convertdateToNormalDay(self,data,columnToBeConverted):
        for i in columnToBeConverted:
            data[i] = data[i].apply(lambda x: x.strftime('%Y-%m-%d'))
        return data

    def rearrangeColumnSequence(self,data,columnArrangement):
        return data[columnArrangement]

    def addCommaToColumnFigures(self,data,columnsToAddComma):
        for i in columnsToAddComma:
            data[i] = data[i].apply(lambda x: "{:,}".format(x))
        return data

    def reNameColumns(self,data,renamedColumns):
        data.columns=renamedColumns
        return data



class CleanETFDailyData(CleanData):
    
    def __init__(self,data):
        super(CleanETFDailyData,self).__init__()
        self.data=data
    
    def execute(self):
         # Delete Following List of Columns
        DeleteColumns=['_id','holdings','ETFhomepage','CommissionFree','AnnualDividendYield','InceptionDate','ETFdbCategory','Structure']
        self.data=self.deleteColumns(self.data,DeleteColumns)

        # Rearrange Columns
        RearrangeColumns = ['ETFTicker','ExpenseRatio','TotalAssetsUnderMgmt','SharesOutstanding','IndexTracker','NumberOfHolding','AverageVolume','ETFName','Issuer','AnnualDividendRate','DividendDate','Dividend','PERatio','Beta','OverAllRating','LiquidityRating','ExpensesRating','ReturnsRating','VolatilityRating','DividendRating','ConcentrationRating','ESGScore']
        self.data=self.rearrangeColumnSequence(self.data,RearrangeColumns)

        # Rename Columns
        RenameColumns=['ETF Ticker','Expense Ratio','Total Assets Under Mgmt.','Shares Outstanding','Index Tracker','Number Of Holding','Average Volume','ETF Name','Issuer','Annual Dividend Rate','Dividend Date','Dividend','PE Ratio','Beta','Over All Rating','Liquidity Rating','Expenses Rating','Returns Rating','Volatility Rating','Dividend Rating','Concentration Rating','ESG Score']
        self.data=self.reNameColumns(self.data,RenameColumns)
        
        return self.data


    

