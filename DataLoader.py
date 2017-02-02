import numpy as np


def LoadData(FileName):
    '''
    Loads hollow data into structured numpy array of floats and returns a tuple
    of column headers along with the structured array.
    '''

    data = np.genfromtxt(FileName, names=True, delimiter=',')
    return data.dtype.names, data


def SegmentDataByAspect(FileName):
    '''
    Loads hollow data into structured numpy array of floats, and splits the
    data into separate structured arrays by aspect band and returns a tuple
    of column headers along with the structured arrays.
    '''
    Headers, A = LoadData(FileName)

    NE = A[(A['Aspect'] >= 0) & (A['Aspect'] <= 85)]
    SE = A[(A['Aspect'] > 85) & (A['Aspect'] <= 165)]
    E = A[(A['Aspect'] >= 0) & (A['Aspect'] <= 165)]
    W = A[(A['Aspect'] > 165)]

    return Headers, NE, SE, E, W


def DataFilter(DataFile, Parameter, Value):
    '''
    Split hollows around Value of a given property. returns Small and
    Large, two lists of IDs corresponding to hollows above and below the
    median.
    '''
    Headers, A = LoadData(DataFile)

    Small = A[(A[Parameter] < Value)]['ID']
    Large = A[(A[Parameter] >= Value)]['ID']

    return Small, Large


def VegDataFilter(DataFile):
    '''
    Split hollows into vegetation categories of a given property. returns
    4 lists of IDs corresponding to specific vegetation types
    '''
    Headers, A = LoadData(DataFile)

    a = A[(A['Veg'] == 1)]['ID']
    b = A[(A['Veg'] == 2)]['ID']
    c = A[(A['Veg'] == 3)]['ID']
    d = A[(A['Veg'] == 4)]['ID']

    return a, b, c, d
