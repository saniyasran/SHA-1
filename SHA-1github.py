
def sha1(text):
    #STEP ONE

    char = []
    #creates an empty array, and array is named char
    ascii = []
    #another array, named as ascii
    binary = []
    #another array, named as binary
    for letter in text:
        #using a for loop to get each character in our text
        char.append(letter)
        #the append function will add each letter to the char array
        asciivalue = ord(letter)
        #this converts each letter to ascii value
        ascii.append(asciivalue)
        #adds asciivalue (which we stored each letter -> ascii in) to the ascii array
        
        #STEP TWO and THREE

        binaryvalue = format(asciivalue, '08b')
        #make each asciivalue letter into binary, then stores it under "binaryvalue"
        #or an easier way below:
        #binaryvalue = bin(asciivalue)
        binary.append(binaryvalue)
        #stores all those values in binary array

        #STEP FOUR 

    mystr = ""
    #creates an empty string
    for value in binary:
        #uses a for loop for each binary group
        mystr = mystr + str(value)
        #str(value) adds each binary group to the empty string
    mystr = mystr + str(1)
    #str(1) adds the number one to the end of the string
    

#STEP FIVE

    while len(mystr) % 512 != 448:
        mystr = mystr + str(0)
    
    #use a while loop to create that situation until it becomes true
    #so while the reminder of the length divided by 512 does not equal 448, it will keep adding str(0), which adds number zero to the string
    #when the remainder is 448, it will stop

#STEP SIX

    length = 0
    #intialize outside of for loop so we can use later
    for value in binary: 
    #take each value in binary array
        length = length + len(value)
        #length is now equal to length plus the value which is eight, and add eight each time it goes through the loop
        #repeats for each value
    
    binaryvalue2 = bin(length)
    #convert length (48) to binary using bin function
    

    #STEP SEVEN

    binaryvalue2 = str(binaryvalue2[2:])
    #converts binary value into string
    while len(binaryvalue2) != 64:
        #len is an inbuilt function that will check the length of the value stored in binaryvalue2
        binaryvalue2 = str(0) + binaryvalue2
        #while loop for when length of binary value is not 64, itll add a zero to the beggining of binaryvalue2 until it is 64
    

#STEP EIGHT

    mystrnew = mystr + binaryvalue2
    #mystrnew will add together mystr and binaryvalue2 (also a string)
    

#STEP NINE
    chunk = []
    j = 0
    while j < len(mystrnew):
        #this is a while loop for until j is less than the length of mystrnew
        s = mystrnew[j:j+512]
        #variable s will store the substring each time it gets from the loop. starting from zero to 512, then 512 to 1023 and so on. until j is greater than the length of mystrnew, then itll stop.
        chunk.append(s)
        #adds the s, which contains the substring to the array
        #so itll look like ['0101(512 times)','0101(512 times)']
        j = j+512
        #we need this to change j to 512 each time
    
#STEP TEN
    binarray = []
    #create new array to store the values in chunk splitting as 16 of 32 bit words
    for value in chunk:
        i = 0 
        binsubarray = []
        #created the subarray
        while i < len(value):
            s = mystrnew[i:i+32]
            #while i is less than 512, then itll add 32 to each round until i becomes 512
            binsubarray.append(s)
            #adds the s values to the subarray
            i = i+32
            #in order to change i to 32 after each round, otherwise i will never equal 512
        binarray.append(binsubarray)
        length = len(binarray)
  
        #adds the values in binsubarray to binarray 
        #this allows us to break into 32 bits

#STEP ELEVEN
#instead of 16 chunks, we want 80
    for arr in binarray:
        i = 16
        count = 0
        #bc we have 16 chunks
        while i <= 79:
            #keep looping until we have 80 chunks
            count = count + 1 
            wordA = arr[i-3]
            #i minus the third chunk
            wordB = arr[i-8]
            #i minus the eight chunk
            wordC = arr[i-14]
            wordD = arr[i-16]
            #these functions chose certain chunks
            xorA = int(wordA, 2)^int(wordB, 2)
            #int function converts the wordA to int with base 2 (which means binary) and XORs with word B
            xorA = bin(xorA)[2:].zfill(32)
            #using [2:] will remove the 0b (by starting from the second character til the end) and then fill the the XOR until its 32
            xorB = int(xorA, 2)^int(wordC,2)
            #XOR the xorA with the wordC in the same process
            xorB = bin(xorB)[2:].zfill(32)
            xorC = int(xorB, 2)^int(wordD,2)
            xorC = bin(xorC)[2:].zfill(33)
            #XOR the xorC with the wordD in the same process, but with 33 to maintain 32 bits 80 words
            xorC = xorC[1:-1]+xorC[0]
            #now we do a left shit, to make the algorithm more complex
            arr.append(xorC)
            #adds to the array
            i = i + 1 


#STEP TWELVE
# initlaize varibales from the chunks in our array
        h0 = str(arr[0])
        #storing each value as a string because it keeps the zeros on the left side
        h1 = str(arr[1])
        h2 = str(arr[3])
        h3 = str(arr[4])
        h4 = str(arr[5])
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4

#STEP THIRTEEN 
        for i in range(length):
            #takes the entire length of the binarray
            for j in range(80):
                #the length of arr is 80, so we will go for that range
                if j<20:
                    BandC = int(b,2) & int(c,2) 
                    #using and operation, and then we convert the b variable to int as a binary number (,2 gives binary base) and then we use '&' to use the and function
                    notB = ~(int(b,2))
                    #now we are using not operation to negate the b variable 
                    notb = format(notB, '32b')
                    #now were making this number into 32 bits because each chunk is 32 bits
                    bandc = format(BandC, '32b')
                    #now were making bandc into 32 bits as well
                    f = int(notb,2) | int(bandc,2)
                    #this is the or operation, here we are converting notb into a binary number and bandc into binary number
                    f = format(f, '32b')
                    #then we make it 32 bits
                    k = '01011010100000100111100110011001'
                elif j < 40:
                    bxorc=int(b,2) ^ int(c,2)
                    bxorc=format(bxorc, '32b')
                    f = int(bxorc,2) | int(d,2)
                    f = format(f, '32b')
                    k = '01101110110110011110101110100001'
                elif j < 60:
                    bxorc=int(b,2) ^ int(c,2)
                    bxorc=format(bxorc, '32b')
                    f = int(bxorc,2) | int(d,2)
                    f = format(f, '32b')
                    k = '01101110110110011110101110100001'                   
                    BandC = int(b,2) & int(c,2)
                    bandc = format(BandC, '32b')
                    BandD = int(b,2) & int(d,2)
                    bandd = format(BandD, '32b')
                    CandD = int(c,2) & int(d,2)
                    candd = format(CandD, '32b')
                    pref = int(bandc,2) | int(bandd,2)
                    pref = format(pref, '32b')
                    f = int(pref,2) | int(candd,2)
                    f = format(f, '32b')
                    k = '10001111000110111011110011011100'
                else:
                    bxorc=int(b,2) ^ int(c,2)
                    bxorc=format(bxorc, '32b')
                    f = int(bxorc,2) | int(d,2)
                    f = format(f, '32b')
 
                    k = '11001010011000101100000111010110'
                word = binarray[i][j]
                a = a[5:]+a[0:5]
                tempA = bin(int(f,2) + int(a,2))




#text = input()
#text = input("Enter the text: ")
text = "A Test"
sha1(text)
    
    
