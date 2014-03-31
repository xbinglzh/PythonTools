
class CodeUtil:

    def __h2b__(self,x):
        result = []
        if x==0:
            return ['0']
        while x != 1:
            result.append(str(x%2))
            x /= 2
        result.append('1')
        result.reverse()

        if len(result) % 4 != 0:
            for i in range(0,(4 - len(result) % 4)):
                result.insert(0,'0')

        return "".join(result)

    def c2u(self,x):
        result = ''

        if 0x0 <= x and x <= 0x7F:
            result =  self.__h2b__(x)

        elif 0x80 <= x and x <= 0x7FF:
            if len(self.__h2b__(x)) == 8:
                tmp = '000' + self.__h2b__(x)
            else:
                tmp = self.__h2b__(x)[1:]
            result = '110'+ tmp[0:5] + '10' + tmp[5:]

        elif 0x800 <= x and x <= 0xFFFF:

            if len(self.__h2b__(x)) == 12:
                tmp = '0000' + self.__h2b__(x)
            else:
                tmp = self.__h2b__(x)

            result = '1110'+ tmp[0:4] + '10' + tmp[4:10] + '10' + tmp[10:]

        return self.__b2h__(result)

    def  __b2h__(self,x):
        hex = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9' , 'A' , 'B' , 'C' , 'D' , 'E' , 'F']
        result = []

        def getValue(bin):
            value = 0
            for i in range(4):
                value += int(bin[i]) * 2**(3-i)
            return value

        for i in range(len(x)/4):
            result.append(hex[getValue(x[i*4:(i+1)*4])])

        return result
