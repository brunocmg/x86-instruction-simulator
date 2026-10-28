from selectors import selectors

def mov():
  cs, ss, ds, es = selectors()
  ax = input("Registrador Geral (AX): ").upper()
  ip = input("Valor de IP: ").upper()
  dst = input("Destino da instrução (DST): ").upper()
  src = input("Source da instrução (SRC): ").upper()

  ef_inteiro = (int(cs, 16) << 4) + int(ip, 16)

  ef_resultado = hex(ef_inteiro)

  print(f"EF = ({ip} x 10) + 0000 = {ef_resultado[2:].upper()}")

  

  print(ef_resultado[2:].upper())

mov()
