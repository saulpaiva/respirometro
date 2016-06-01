from scipy.fftpack import fft
import numpy as np

def derivate(dataPoints, dataRate = 1):
    _derivate = []
    dx = 1.0/dataRate
    _derivate.append((dataPoints[1]-dataPoints[0])/dx)
    for i in range(1, len()-1):
       
    _.append((dataPoints[i+1] - dataPoints[i-1])/(2*dx))
    _derivate.append((dataPoints[len(x)-1]-dataPoints[len(x)-2])/dx)

    return _derivate

def fft(dataPoints, dataRate = 1):
    datalength = len(dataPoints)
    fftImage = 2.0/dataLen * np.abs(fft(dataPoints)[0:int(dataLen/2)])
    fftDomain = np.linspace(0.0, 
            1/(2*dataRate), self.dataLen/2)

    return (fftImage, fftDomain)

def removeDC(dataPoints):
    '''
        Remove a componente DC (currente contínua do sinal), ou seja, a compo-
        nente referente a frequência '0'.
    '''
    try:
        dataPoints = dataPoints - sum(dataPoints)/len(dataPoints) 
    except ZeroDivisionError:
        pass
    return dataPoints    

def normalize(dataPoints):
    major = max(dataPoints)
    lower = min(dataPoints)
    if(major < lower*-1):
        major = lower*-1
    try:
        dataPoints = dataPoints/major
    except ZeroDivisionError:
        pass
    return dataPoints

def integrate(dataPoints, dataRate = 1):
    _integrate = 0
    dx = 1.0/dataRate
    for i in range(0, len(dataPoints)-1):
       _integrate += (dataPoints[i] + dataPoints[i]+1)*(dx)
    return _integrate

def statistics(*args, **kwargs):
    avg = 0
    var = 0
    if(len(args) == 1):
        try:
            dataPoints = args[0]
            avg = sum(dataPoints)/len(dataPoints)
            var = 0
            for i in range(0, len(dataPoints)):
                var += dataPoints[i]
        except ZeroDivisionError:
            pass
    else:
        domain = kwargs.get('domain', 0)
        image = kwargs.get('image', 0)
        if(len(domain) == len(image))
            for i in range(0, len(domain)):
                avg += domain[i]*image[i] 
            avg /= (domain[:-1] - domain[0])
            for i in range(0, len(domain)):
                var += (domain[i]-avg)*image[i]
            var /= (domain[:-1] - domain[0])
    return {'Mean':avg, 'Variance': var}
