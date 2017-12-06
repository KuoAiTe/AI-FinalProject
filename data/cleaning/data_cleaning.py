"""
Author: Ai-Te Kuo
Last edited: Dec 3, 2017

"""
if __name__ == "__main__":
    import pandas as pd
    fileName = 'data.csv'
    df = pd.read_csv(fileName, index_col=False)

    # Remove the counry which is not United Kingdom
    a = df.index[df["Country"] != 'United Kingdom']
    df = df.drop(a)

    # Remove the record with empty CustomerID
    b = df.index[df["CustomerID"].isnull()]
    df = df.drop(b)

    # Remove the cancellations
    c = []
    for index in df.index:
        InvoiceNo = df.at[index,'InvoiceNo']
        firstLetter = InvoiceNo[0]
        if not firstLetter.isnumeric():
            c.append(index)
    df = df.drop(c)

    t = df.InvoiceNo.unique()
    Count =0
    for InvoiceNo in t:
        df.loc[df['InvoiceNo'] == InvoiceNo, 'InvoiceNo'] = Count
        Count = Count + 1
        print( 'invoice',Count)

    t = df.CustomerID.unique()
    Count =0
    for CustomerID in t:
        df.loc[df['CustomerID'] == CustomerID, 'CustomerID'] = Count
        Count = Count + 1
        print('CustomerID',Count)

    Count = 0
    t = df.StockCode.unique()
    for StockCode in t:
        df.loc[df['StockCode'] == StockCode, 'StockCode'] = Count
        Count = Count + 1
        print('StockCode',Count)

    df.pop('Description');
    df.pop('InvoiceDate');
    df.pop('Country');
    df.pop('UnitPrice');
    df['CustomerID'] = df['CustomerID'].astype(int)

    df.to_csv('new.csv', index = False)
