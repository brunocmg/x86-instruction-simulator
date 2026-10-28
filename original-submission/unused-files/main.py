print("\n-------------")
print("INTERFACE")
print("-------------")
print("1. MOVES")
print("2. ARITHMETIC")
print("3. BOOLEAN")
print("4. TEST/COMPARE")
print("-------------")

tipo_instrucao = input("Qual o tipo de instrução desejada? ")
while True:
    try:
        opcao = int(tipo_instrucao)
        
        match opcao:
            case 1:
                print("\n Você selecionou o conjunto de instrução MOVES")
                print("\n---------------------------")
                print("INTERFACE INSTRUÇÕES MOVES")
                print("----------------------------")
                print("1. MOV DST, SRC")
                print("2. PUSH SRC")
                print("3. POP DST")
                print("4. XCHG DST, SRC")
                print("--------------------------")
                
                instrucao = input("Qual instrução desejada? ")

                opcao_de_instrucao = int(instrucao)

                match opcao_de_instrucao:
                    case 1:
                        #input registrador dentro de uma variavel registrador
                        print("FUNÇÃO MOV")
                    case 2:
                        print("FUNÇÃO PUSH")
                    case 3:
                        print("FUNÇÃO POP")
                    case 4:
                        print("FUNÇÃO XCHG")
                
            case 2:
                print("\n Você selecionou o conjunto de instrução ARITHMETIC")
                print("\n---------------------------")
                print("INTERFACE INSTRUÇÕES ARITHMETIC")
                print("----------------------------")
                print("1. ADD DST, SRC")
                print("2. SUB DST, SRC")
                print("3. MUL SRC")
                print("4. INC DST")
                print("5. DEC DST")
                print("6. NEG DST")
                print("7. DIV SRC")
                print("--------------------------")

                instrucao = input("Qual instrução desejada? ")

                opcao_de_instrucao = int(instrucao)

                match opcao_de_instrucao:
                    case 1:
                        print("FUNÇÃO ADD")
                    case 2:
                        print("FUNÇÃO SUB")
                    case 3:
                        print("FUNÇÃO MUL")
                    case 4:
                        print("FUNÇÃO INC")
                    case 5:
                        print("FUNÇÃO DEC")
                    case 6:
                        print("FUNÇÃO NEG")
                    case 7:
                        print("FUNÇÃO DIV")
                
            case 3:
                print("\n Você selecionou o conjunto de instrução BOOLEAN")
                print("\n---------------------------")
                print("INTERFACE INSTRUÇÕES BOOLEAN")
                print("----------------------------")
                print("1. AND DST, SRC")
                print("2. OR DST, SRC")
                print("3. XOR DST, SRC")
                print("4. NOT DST")
                print("--------------------------")

                instrucao = input("Qual instrução desejada? ")

                opcao_de_instrucao = int(instrucao)

                match opcao_de_instrucao:
                    case 1:
                        print("FUNÇÃO AND")
                    case 2:
                        print("FUNÇÃO OR")
                    case 3:
                        print("FUNÇÃO XOR")
                    case 4:
                        print("FUNÇÃO NOT")
                
            case 4:
                print("\n Você selecionou o conjunto de instrução TEST/COMPARE")
                print("\n---------------------------")
                print("INTERFACE INSTRUÇÕES TEST/COMPARE")
                print("----------------------------")
                print("1. CMP SRC1, SRC2")
                print("2. JMP ADDR")
                print("3. Jxx ADDR")
                print("4. CALL ADDR")
                print("5. RET")
                print("6. IRET")
                print("7. LOOP ADDR")
                print("8. IN AX, PORT")
                print("9. OUT ADDR")
                print("--------------------------")

                instrucao = input("Qual instrução desejada? ")

                opcao_de_instrucao = int(instrucao)

                match opcao_de_instrucao:
                    case 1:
                        print("CMP SRC1, SRC2")
                    case 2:
                        print("JMP ADDR")
                    case 3:
                        print("Jxx ADDR")
                    case 4:
                        print("CALL ADDR")
                    case 5:
                        print("RET")
                    case 6:
                        print("IRET")
                    case 7:
                        print("LOOP ADDR")
                    case 8:
                        print("IN AX, PORT")                 
                    case 9:
                        print("OUT ADDR")
        break
            
    except ValueError:
        print(" Opção inválida. Por favor, insira um número entre 1 e 4.")
    
