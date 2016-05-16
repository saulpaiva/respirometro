from scipy.fftpack import fft
import numpy as np

class FreqAnalysis(object):
    '''
        
    '''
    def __init__(self, array, dataRate):
        '''
            
        '''
        try:
            if(len(array) %2 != 0):
                array = array[0:-1]
            self._srcdata = np.array(array, dtype = np.float64)
            self._dataRate = dataRate
            self.data = np.array(array, dtype = np.float64)
            self.dataLen = len(array)
        except TypeError:
            print("Não foi possível criar o objeto.")
        

    def fft(self):
        '''

        '''
        fftImage = 2.0/self.dataLen * np.abs(fft(self.data)[0:int(self.dataLen/2)])
        fftDomain = np.linspace(0.0, 
                1/(2*self.dataRate), self.dataLen/2)

        return (fftImage, fftDomain)

    def smooth(self, order, times):
        '''
            Aplica um filtro smooth no atual atributo 'data' 'times' vezes e
            com ordem 'order'.
            Filtro smooth é um filtro de média móvel, ou seja, produz a média
            aritmética a cada ponto(elemento) e seus vizinhos. A quantidade de
            vizinhos a serem usados é difinido por 'order', sendo 'order' vizihos
            atrás e 'order' vizinhos a frente.
            
        '''
        elements = 2*order + 1 
        lenght = len(self.data)
        smoothData = [0]*len(self.data)
        smoothData[0] = self.data[0]
        smoothData[-1] = self.data[-1]
        try:
            for k in range(times):
                if(2*order+1 > lenght):
                    for i in range(1, lenght-1):
                        aux = 0
                        finalIndex = 2*i + 1
                        initialIndex = 0
                        if(finalIndex >= lenght):
                            initialIndex = finalIndex - lenght
                            finalIndex = lenght
                            
                        for j in range(initialIndex, finalIndex):
                            aux += self.data[j]
                        smoothData[i] = aux/(finalIndex- initialIndex)
                else:
                    for i in range(1, order+1):
                        aux = 0
                        for j in range(0, i*2 +1):
                            aux += self.data[j]
                        smoothData[i] = aux/(2*i +1)
                    
                    for i in range(order + 1, lenght-order):
                        aux = 0
                        for j in range(i-order, i+order+1):
                            aux += self.data[j]
                        smoothData[i] = aux/elements

                    for i in range(lenght-order, lenght-1):
                        aux = 0
                        finalElements = lenght - i-1
                        print('I: {} FE: {}'.format(i, finalElements))
                        for j in range(i - finalElements, lenght):
                            aux += self.data[j]
                            print('J: {} Aux: {}'.format(j, aux))
                        smoothData[i] = aux/(2*finalElements +1)

                self.data = smoothData          
            self.data = np.array(self.data, dtype = np.float64)
    
        except IndexError:
            print ("ERRO: ordem de filtro muito alta, sua ordem pode ser no "
                    "máximo número de elementos dividido por dois menos um.\n"
                    "Nesse caso: {0}. ({1}/2 - 1)".format(len(self.data)/2 -1, 
                        len(self.data)))
    
    def removeDC(self):
        '''
            Remove a componente DC (currente contínua do sinal), ou seja, a compo-
            nente referente a frequência '0'.
        '''
        try:
            self.data = self.data - sum(self.data)/len(self.data) 
        except ZeroDivisionError:
            del self
    
    def statistics(self, array):
        '''
            mean(array)
        
        '''
        return {'Mean': mean(array), '' }

    @property
    def dataRate(self):
        return self._dataRate
    
    @property
    def rawData(self):
        return self._srcdata

if __name__ == '__main__':
    y = np.linspace(0, 9, 10)
    test = FreqAnalysis(y, 2)
    test.smooth(11,1)
    print(test.data)
    test.removeDC() 
