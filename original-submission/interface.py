#pip install PyQt5
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QFrame
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QStackedWidget
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QGroupBox
from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simulador de Instruções")
        self.setGeometry(200, 200, 1100, 700)
        
        self.instrução_atual = None
        
        layout_inicial = QVBoxLayout(self)
        self.menu_stack = QStackedWidget()
        
        self.registrador_ax_input = QLineEdit("0000")
        self.registrador_bx_input = QLineEdit("0000")
        self.registrador_cx_input = QLineEdit("0000")
        self.registrador_dx_input = QLineEdit("0000")  
        
        self.registrador_cs_input = QLineEdit("4000")
        self.registrador_ss_input = QLineEdit("5000")
        self.registrador_ds_input = QLineEdit("6000")
        self.registrador_es_input = QLineEdit("7000")
        
        self.registrador_ip_input = QLineEdit("0100")  
        self.registrador_sp_input = QLineEdit("FFFF")  
        self.registrador_bp_input = QLineEdit("0000")  
        self.registrador_di_input = QLineEdit("0000")  
        self.registrador_si_input = QLineEdit("0000")  

        self.registrador_flag_input = QLineEdit()  
        
        self.input_addr = QLineEdit()
        self.input_addr.setPlaceholderText("ADDR")
        self.input_addr.setEnabled(False)
        
        self.input_port = QLineEdit()
        self.input_port.setPlaceholderText("PORT")
        self.input_port.setEnabled(False)
        
        self.memoria = bytearray(1048576)
        
        self.cor_borda_style = "background-color: #FFFFF0; border: 2px solid #FF0000; padding: 3px;"
        self.barramento_ativo_style = "background-color: #FFFFF0; border: 2px solid #FF0000; padding: 10px; font-weight: bold; font-size: 14px; color: black"
        self.barramento_inativo_style = "background-color: #EEEEEE; border: 1px dashed #999; padding: 10px; font-size: 14px; color: #777"
        
        self.demonstracao_estado = "Inicio"
        self.demonstracao_passo_interno = 0
        self.demonstracao_operacao = ""
        self.demonstracao_dst_str = ""
        self.demonstracao_src_str = ""
        self.demonstracao_addr_str = ""
        self.demonstracao_dados_dst = 0
        self.demonstracao_dados_src = 0
        self.demonstracao_endereco_calculado = 0
        self.demonstracao_tempo_byte = 0
        self.demonstracao_ip_inicial = 0
        
        self.operacao_c = QComboBox()
        self.operacao_c.addItems(["MOV", "PUSH", "POP", "XCHG",
                                    "ADD", "SUB", "MUL", "INC", "DEC","NEG","DIV",
                                    "AND", "OR", "XOR", "NOT",
                                    "CMP", "JMP", "JE", "JNE", "JG", "JGE", "JL", "JLE", "CALL", "RET", "IRET", "LOOP", "IN", "OUT"])
        self.operacao_c.currentTextChanged.connect(self.atualizar_interface)
        self.dst_c = QComboBox()
        self.dst_c.addItems(["AX", "BX", "CX", "DX", "[SI]", "[DI]"])
        self.src_c = QComboBox()
        self.src_c.addItems(["AX", "BX", "CX", "DX", "[SI]", "[DI]"])
        
        self.demonstracao_label_ax = QLabel("0000")
        self.demonstracao_label_bx = QLabel("0000")
        self.demonstracao_label_cx = QLabel("0000")
        self.demonstracao_label_dx = QLabel("0000")
        self.demonstracao_label_cs = QLabel("4000")
        self.demonstracao_label_ss = QLabel("5000")
        self.demonstracao_label_ds = QLabel("6000")
        self.demonstracao_label_es = QLabel("7000")
        self.demonstracao_label_ip = QLabel("0100")
        self.demonstracao_label_sp = QLabel("FFFF")
        self.demonstracao_label_bp = QLabel("0000")
        self.demonstracao_label_di = QLabel("0000")
        self.demonstracao_label_si = QLabel("0000")
        self.demonstracao_label_flag = QLabel("0000")
            
        self.label_demonstracao_intrucao = QLabel("Instrução: N/A")
        
        self.tela_barramento_endereco = QLabel("")
        self.tela_barramento_endereco.setAlignment(Qt.AlignCenter)
        self.tela_barramento_endereco.setWordWrap(True)
        self.tela_barramento_dados = QLabel("")
        self.tela_barramento_dados.setAlignment(Qt.AlignCenter)
        
        self.memoria_edicao_ef = QLineEdit("")
        self.memoria_edicao_ef.setPlaceholderText("Endereço Físico")
        self.memoria_edicao_valor = QLineEdit("")
        self.memoria_edicao_valor.setPlaceholderText("Valor do EF")
        
        self.log_memoria = QTextEdit()
        self.log_memoria.setReadOnly(True)
        self.log_memoria.setFontFamily("Courier")
        self.log_memoria.setStyleSheet("color: black;")
        
        self.lista_ADDR = ["JMP", "JE", "JNE", "JG", "JGE", "JL", "JLE", "CALL", "LOOP"]
                
        pagina_inicial = self.menu_principal()
        pagina_moves = self.menu_moves()
        pagina_arithmetic = self.menu_arithmetic()
        pagina_boolean = self.menu_boolean()
        pagina_compare = self.menu_compare()
        pagina_jxx = self.menu_jxx()
        pagina_registrador = self.menu_registradores()
        pagina_demonstracao = self.menu_demonstracao()
        
        self.menu_stack.addWidget(pagina_inicial)
        self.menu_stack.addWidget(pagina_moves)
        self.menu_stack.addWidget(pagina_arithmetic)
        self.menu_stack.addWidget(pagina_boolean)
        self.menu_stack.addWidget(pagina_compare)
        self.menu_stack.addWidget(pagina_jxx)
        self.menu_stack.addWidget(pagina_registrador)
        self.menu_stack.addWidget(pagina_demonstracao)
        
        self.label_resultado = QLabel("Selecione uma instrução")
        self.label_resultado.setAlignment(Qt.AlignCenter)
        self.label_resultado.setStyleSheet("font-size: 14px; color: #333; padding: 10px;")
        
        linha = QFrame()
        linha.setFrameShape(QFrame.HLine)
        linha.setFrameShadow(QFrame.Sunken)
        linha.setStyleSheet("background-color: black; max-height: 2px;")  
        
        layout_inicial.addWidget(self.label_resultado, 0)
        layout_inicial.addWidget(linha, 0)
        layout_inicial.addWidget(self.menu_stack, 1)  
        
    def menu_principal(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout_botoes = QHBoxLayout()
        
        btn_moves = QPushButton("Moves")
        btn_moves.clicked.connect(lambda: self.menu_stack.setCurrentIndex(1))
        layout_botoes.addWidget(btn_moves)
        
        btn_aritHmetic = QPushButton("Arithmetic")
        btn_aritHmetic.clicked.connect(lambda: self.menu_stack.setCurrentIndex(2))
        layout_botoes.addWidget(btn_aritHmetic)
        
        btn_boolean = QPushButton("Boolean")
        btn_boolean.clicked.connect(lambda: self.menu_stack.setCurrentIndex(3))
        layout_botoes.addWidget(btn_boolean)
        
        btn_compare = QPushButton("Test/Compare")
        btn_compare.clicked.connect(lambda: self.menu_stack.setCurrentIndex(4))
        layout_botoes.addWidget(btn_compare)
        
        layout.addLayout(layout_botoes)
        layout.addStretch(1)
        return pagina
    
    def menu_moves(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_mov = QPushButton(" MOV DST, SRC")
        btn_mov.clicked.connect(lambda: self.Registradores("Função MOV"))
        layout.addWidget(btn_mov)
        
        btn_push = QPushButton(" PUSH SRC")
        btn_push.clicked.connect(lambda: self.Registradores("Função PUSH"))
        layout.addWidget(btn_push)
        
        btn_pop = QPushButton(" POP DST")
        btn_pop.clicked.connect(lambda: self.Registradores("Função POP"))
        layout.addWidget(btn_pop)
        
        btn_xchg = QPushButton(" XCHG DST, SRC")
        btn_xchg.clicked.connect(lambda: self.Registradores("Função XCHG"))
        layout.addWidget(btn_xchg)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)

        layout.addStretch(1)
        return pagina
    
    def menu_arithmetic(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_add = QPushButton(" ADD DST, SRC")
        btn_add.clicked.connect(lambda: self.Registradores("Função ADD"))
        layout.addWidget(btn_add)
        
        btn_sub = QPushButton(" SUB DST, SRC")
        btn_sub.clicked.connect(lambda: self.Registradores("Função SUB"))
        layout.addWidget(btn_sub)
        
        btn_mul = QPushButton(" MUL SRC")
        btn_mul.clicked.connect(lambda: self.Registradores("Função MUL"))
        layout.addWidget(btn_mul)
        
        btn_inc = QPushButton(" INC DST")
        btn_inc.clicked.connect(lambda: self.Registradores("Função INC"))
        layout.addWidget(btn_inc)
        
        btn_dec = QPushButton(" DEC DST")
        btn_dec.clicked.connect(lambda: self.Registradores("Função DEC"))
        layout.addWidget(btn_dec)
        
        btn_neg = QPushButton(" NEG DST")
        btn_neg.clicked.connect(lambda: self.Registradores("Função NEG"))
        layout.addWidget(btn_neg)
        
        btn_div = QPushButton(" DIV SRC")
        btn_div.clicked.connect(lambda: self.Registradores("Função DIV"))
        layout.addWidget(btn_div)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_boolean(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        
        btn_and = QPushButton(" AND DST, SRC")
        btn_and.clicked.connect(lambda: self.Registradores("Função AND"))
        layout.addWidget(btn_and)
        
        btn_or = QPushButton(" OR DST, SRC")
        btn_or.clicked.connect(lambda: self.Registradores("Função OR"))
        layout.addWidget(btn_or)
        
        btn_xor = QPushButton(" XOR DST, SRC")
        btn_xor.clicked.connect(lambda: self.Registradores("Função XOR"))
        layout.addWidget(btn_xor)
        
        btn_not = QPushButton(" NOT DST")
        btn_not.clicked.connect(lambda: self.Registradores("Função NOT"))
        layout.addWidget(btn_not)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_compare(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_cmp = QPushButton(" CMP SRC1, SRC2")
        btn_cmp.clicked.connect(lambda: self.Registradores("Função CMP"))
        layout.addWidget(btn_cmp)
        
        btn_jmp = QPushButton(" JMP ADDR")
        btn_jmp.clicked.connect(lambda: self.Registradores("Função JMP"))
        layout.addWidget(btn_jmp)
        
        btn_jxx = QPushButton(" Jxx ADDR")
        btn_jxx.clicked.connect(lambda: self.menu_stack.setCurrentIndex(5))
        layout.addWidget(btn_jxx)
        
        btn_call = QPushButton(" CALL ADDR")
        btn_call.clicked.connect(lambda: self.Registradores("Função CALL"))
        layout.addWidget(btn_call)
        
        btn_ret = QPushButton(" RET")
        btn_ret.clicked.connect(lambda: self.Registradores("Função RET"))
        layout.addWidget(btn_ret)
        
        btn_iret = QPushButton(" IRET")
        btn_iret.clicked.connect(lambda: self.Registradores("Função IRET"))
        layout.addWidget(btn_iret)
        
        btn_loop = QPushButton(" LOOP ADDR")
        btn_loop.clicked.connect(lambda: self.Registradores("Função LOOP"))
        layout.addWidget(btn_loop)
        
        btn_in = QPushButton(" IN AX, PORT")
        btn_in.clicked.connect(lambda: self.Registradores("Função IN"))
        layout.addWidget(btn_in)
        
        btn_out = QPushButton(" OUT PORT, AX")
        btn_out.clicked.connect(lambda: self.Registradores("Função OUT"))
        layout.addWidget(btn_out)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_jxx(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        
        btn_je = QPushButton(" JE ADDR")
        btn_je.clicked.connect(lambda: self.Registradores("Função JE"))
        layout.addWidget(btn_je)
        
        btn_jne = QPushButton(" JNE ADDR")
        btn_jne.clicked.connect(lambda: self.Registradores("Função JNE"))
        layout.addWidget(btn_jne)
        
        btn_jg = QPushButton(" JG ADDR")
        btn_jg.clicked.connect(lambda: self.Registradores("Função JG"))
        layout.addWidget(btn_jg)
        
        btn_jge = QPushButton(" JGE ADDR")
        btn_jge.clicked.connect(lambda: self.Registradores("Função JGE"))
        layout.addWidget(btn_jge)
        
        btn_jl = QPushButton(" JL ADDR")
        btn_jl.clicked.connect(lambda: self.Registradores("Função JL"))
        layout.addWidget(btn_jl)
        
        btn_jle = QPushButton(" JLE ADDR")
        btn_jle.clicked.connect(lambda: self.Registradores("Função JLE"))
        layout.addWidget(btn_jle)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        layout.addStretch(1)
        return pagina
    
    def menu_registradores(self):
        pagina = QWidget()
        layout_2 = QVBoxLayout(pagina)
        layout_2_esquerda = QVBoxLayout()
        layout_2_direita = QVBoxLayout()
        layout_2_configuracao = QHBoxLayout()
        layout_2.setSpacing(10)
        
        Box_Style = "QGroupBox { border: 1px solid black; border-radius: 5px; margin-top: 1ex;}" "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px;}"
        
        Box_Geral = QGroupBox("Registrador Geral")
        Box_Geral.setStyleSheet(Box_Style)
        Geral = QGridLayout()
        Geral.addWidget(QLabel("AX:"), 0,0); Geral.addWidget(self.registrador_ax_input, 0,1)
        Geral.addWidget(QLabel("BX:"), 0,2); Geral.addWidget(self.registrador_bx_input, 0,3)
        Geral.addWidget(QLabel("CX:"), 1,0); Geral.addWidget(self.registrador_cx_input, 1,1)
        Geral.addWidget(QLabel("DX:"), 1,2); Geral.addWidget(self.registrador_dx_input, 1,3)
        Box_Geral.setLayout(Geral); layout_2_esquerda.addWidget(Box_Geral)
        
        Box_Segmentos = QGroupBox("Registrador de Segmentos")
        Box_Segmentos.setStyleSheet(Box_Style)
        Segmentos = QGridLayout()
        Segmentos.addWidget(QLabel("CS:"), 0,0); Segmentos.addWidget(self.registrador_cs_input, 0,1) 
        Segmentos.addWidget(QLabel("SS:"), 0,2); Segmentos.addWidget(self.registrador_ss_input, 0,3)
        Segmentos.addWidget(QLabel("DS:"), 1,0); Segmentos.addWidget(self.registrador_ds_input, 1,1)
        Segmentos.addWidget(QLabel("ES:"), 1,2); Segmentos.addWidget(self.registrador_es_input, 1,3)
        Box_Segmentos.setLayout(Segmentos); layout_2_esquerda.addWidget(Box_Segmentos)
        
        Box_Offsets = QGroupBox("Registrador de Offsets")
        Box_Offsets.setStyleSheet(Box_Style)
        Offsets = QGridLayout()
        Offsets.addWidget(QLabel("IP:"), 0,0); Offsets.addWidget(self.registrador_ip_input, 0,1)
        Offsets.addWidget(QLabel("SP:"), 0,2); Offsets.addWidget(self.registrador_sp_input, 0,3)
        Offsets.addWidget(QLabel("BP:"), 1,0); Offsets.addWidget(self.registrador_bp_input, 1,1)
        Offsets.addWidget(QLabel("DI:"), 1,2); Offsets.addWidget(self.registrador_di_input, 1,3)
        Offsets.addWidget(QLabel("SI:"), 2,0); Offsets.addWidget(self.registrador_si_input, 2,1)
        Box_Offsets.setLayout(Offsets); layout_2_esquerda.addWidget(Box_Offsets)
        
        Box_Flag = QGroupBox("Registrador de Flags")
        Box_Flag.setStyleSheet(Box_Style)
        Flag = QGridLayout()
        Flag.addWidget(QLabel("FLAGS:"), 0,0); Flag.addWidget(self.registrador_flag_input, 0,1)
        Box_Flag.setLayout(Flag); layout_2_esquerda.addWidget(Box_Flag)
        
        layout_2_esquerda.addStretch(1)
        layout_2_configuracao.addLayout(layout_2_esquerda, 4)
        
        Box_Instrução = QGroupBox("Instrução Atual")
        Box_Instrução.setStyleSheet(Box_Style)
        Instrucao = QGridLayout()
        Instrucao.addWidget(QLabel("Operação:"), 0,0); Instrucao.addWidget(self.operacao_c, 0,1)
        Instrucao.addWidget(QLabel("Destino (DST):"), 1,0); Instrucao.addWidget(self.dst_c, 1,1)
        Instrucao.addWidget(QLabel("Origem (SRC):"), 2,0); Instrucao.addWidget(self.src_c, 2,1)
        Instrucao.addWidget(QLabel("ADDR:"), 3, 0); Instrucao.addWidget(self.input_addr, 3,1)
        Instrucao.addWidget(QLabel("PORT:"), 4, 0); Instrucao.addWidget(self.input_port, 4,1)
        Box_Instrução.setLayout(Instrucao); layout_2_direita.addWidget(Box_Instrução)
        
        layout_2_direita.addStretch(1)
        layout_2_configuracao.addLayout(layout_2_direita, 1)
        
        layout_2.addLayout(layout_2_configuracao)
        
        btn_demonstrar = QPushButton(" Demonstrar a execução da Instrução")
        btn_demonstrar.setStyleSheet("font-size: 14px; background-color: #DDEEFF; padding: 8px;")
        btn_demonstrar.clicked.connect(self.iniciar_demonstracao)
        layout_2.addWidget(btn_demonstrar)
        
        btn_voltar = QPushButton(" Voltar ao Menu Principal")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout_2.addWidget(btn_voltar, alignment=Qt.AlignLeft)
        
        return pagina
    
    def menu_demonstracao(self):
        pagina = QWidget()
        layout = QHBoxLayout(pagina)
        
        parte_cpu = QVBoxLayout()
        Box_Style = "QGroupBox { border: 1px solid black; border-radius: 5px; margin-top: 1ex;}" "QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left; padding: 0 3px;}"

        self.label_demonstracao_intrucao.setStyleSheet("font-size: 16px; font-weight: bold; color: #000080; padding: 5px;")
        self.label_demonstracao_intrucao.setAlignment(Qt.AlignCenter)
        parte_cpu.addWidget(self.label_demonstracao_intrucao)
        
        Box_Geral = QGroupBox("Registrador Geral")
        Box_Geral.setStyleSheet(Box_Style)
        Geral = QGridLayout()
        Geral.addWidget(QLabel("AX:"), 0,0); Geral.addWidget(self.demonstracao_label_ax, 0,1)
        Geral.addWidget(QLabel("BX:"), 0,2); Geral.addWidget(self.demonstracao_label_bx, 0,3)
        Geral.addWidget(QLabel("CX:"), 1,0); Geral.addWidget(self.demonstracao_label_cx, 1,1)
        Geral.addWidget(QLabel("DX:"), 1,2); Geral.addWidget(self.demonstracao_label_dx, 1,3)
        Box_Geral.setLayout(Geral); parte_cpu.addWidget(Box_Geral)
        
        Box_Segmentos = QGroupBox("Registrador de Segmentos")
        Box_Segmentos.setStyleSheet(Box_Style)
        Segmentos = QGridLayout()
        Segmentos.addWidget(QLabel("CS:"), 0,0); Segmentos.addWidget(self.demonstracao_label_cs, 0,1) 
        Segmentos.addWidget(QLabel("SS:"), 0,2); Segmentos.addWidget(self.demonstracao_label_ss, 0,3)
        Segmentos.addWidget(QLabel("DS:"), 1,0); Segmentos.addWidget(self.demonstracao_label_ds, 1,1)
        Segmentos.addWidget(QLabel("ES:"), 1,2); Segmentos.addWidget(self.demonstracao_label_es, 1,3)
        Box_Segmentos.setLayout(Segmentos); parte_cpu.addWidget(Box_Segmentos)
        
        Box_Offsets = QGroupBox("Registrador de Offsets")
        Box_Offsets.setStyleSheet(Box_Style)
        Offsets = QGridLayout()
        Offsets.addWidget(QLabel("IP:"), 0,0); Offsets.addWidget(self.demonstracao_label_ip, 0,1)
        Offsets.addWidget(QLabel("SP:"), 0,2); Offsets.addWidget(self.demonstracao_label_sp, 0,3)
        Offsets.addWidget(QLabel("BP:"), 1,0); Offsets.addWidget(self.demonstracao_label_bp, 1,1)
        Offsets.addWidget(QLabel("DI:"), 1,2); Offsets.addWidget(self.demonstracao_label_di, 1,3)
        Offsets.addWidget(QLabel("SI:"), 2,0); Offsets.addWidget(self.demonstracao_label_si, 2,1)
        Box_Offsets.setLayout(Offsets); parte_cpu.addWidget(Box_Offsets)
        
        Box_Flag = QGroupBox("Registrador de Flags")
        Box_Flag.setStyleSheet(Box_Style)
        Flag = QGridLayout()
        Flag.addWidget(QLabel("FLAGS:"), 0,0); Flag.addWidget(self.demonstracao_label_flag, 0,1)
        Box_Flag.setLayout(Flag); parte_cpu.addWidget(Box_Flag)
        
        parte_cpu.addStretch(1)
        layout.addLayout(parte_cpu, 1)
        
        parte_central = QVBoxLayout()
        parte_central.setSpacing(20)
        
        Box_Barramento = QGroupBox("Fluxo de Barramento")
        Box_Barramento.setStyleSheet(Box_Style)
        layout_barramento = QVBoxLayout()
        layout_barramento.setSpacing(15)
        
        label_EF = QLabel("Barramento de Endereço (CPU → MEM)")
        label_EF.setStyleSheet("font-weight: bold; color: black;")
        self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
        layout_barramento.addWidget(label_EF)
        layout_barramento.addWidget(self.tela_barramento_endereco)
        
        Seta = QLabel("↓ ↑")
        Seta.setAlignment(Qt.AlignCenter)
        Seta.setStyleSheet("font-size: 20px; font-weight: bold; color: black;")
        layout_barramento.addWidget(Seta)
        
        label_dado = QLabel("Barramento de Dados (CPU ← MEM)")
        label_dado.setStyleSheet("font-weight: bold; color: black;")
        self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
        layout_barramento.addWidget(label_dado)
        layout_barramento.addWidget(self.tela_barramento_dados)
        
        Box_Barramento.setLayout(layout_barramento)
        parte_central.addWidget(Box_Barramento)
        parte_central.addStretch(1)
        
        btn_proximo = QPushButton("Próximo Passo →")
        btn_proximo.setStyleSheet("color: black")
        btn_proximo.clicked.connect(self.executar_passo_demonstracao)
        parte_central.addWidget(btn_proximo)
        
        btn_voltar = QPushButton("Voltar para a configuração")
        btn_voltar.clicked.connect(lambda: self.menu_stack.setCurrentIndex(6))
        parte_central.addWidget(btn_voltar)
        
        layout.addLayout(parte_central, 1)
        
        parte_memoria = QVBoxLayout()
        
        Box_Editor_Memoria = QGroupBox("Editor de Memória")
        Box_Editor_Memoria.setStyleSheet(Box_Style)
        layout_edicao = QGridLayout()
        layout_edicao.addWidget(QLabel("Endereço Físico:"), 0, 0)
        layout_edicao.addWidget(self.memoria_edicao_ef, 0, 1)
        layout_edicao.addWidget(QLabel("Valor:"), 1, 0)
        layout_edicao.addWidget(self.memoria_edicao_valor, 1, 1)
        
        btn_salvar_memoria = QPushButton("Salvar na Memória")
        btn_salvar_memoria.clicked.connect(self.salvar_memoria)
        layout_edicao.addWidget(btn_salvar_memoria, 2, 0, 1, 2)
        
        Box_Editor_Memoria.setLayout(layout_edicao)
        parte_memoria.addWidget(Box_Editor_Memoria)
        
        Box_Memoria_Log = QGroupBox("Memoria")
        Box_Memoria_Log.setStyleSheet(Box_Style)
        layout_log = QVBoxLayout()
        layout_log.addWidget(self.log_memoria)
        Box_Memoria_Log.setLayout(layout_log)
        parte_memoria.addWidget(Box_Memoria_Log)
        
        layout.addLayout(parte_memoria, 1)
        
        return pagina
        
    def salvar_memoria(self, text):
        try:
            ef_str = self.memoria_edicao_ef.text()
            valor_str = self.memoria_edicao_valor.text()
            
            if not ef_str or not valor_str:
                raise ValueError("Endereço físico e valor não podem estar vazios.")
            
            endereco_fisico = int(ef_str, 16)
            valor = int(valor_str, 16)
            
            info = ""
            if valor <= 0xFF:
                self.memoria[endereco_fisico] = valor
                info = f"Salvar: {valor:02X} em {endereco_fisico:X})"
            elif valor <= 0xFFFF:
                byte_baixo = valor & 0xFF
                byte_alto = (valor >> 8) & 0xFF
                self.memoria[endereco_fisico] = byte_baixo
                self.memoria[endereco_fisico + 1] = byte_alto
                info = f"Salvar: {valor:04X} em {endereco_fisico:X} )"
            else:
                raise ValueError("Valor excede 16 bits (FFFF)")
            
            self.log_memoria.setStyleSheet(self.cor_borda_style)
            self.log_memoria.append(info)
            
            QMessageBox.information(self, "Memória", "Valor salvo com sucesso na memória.")
        
        except ValueError as e:
            QMessageBox.warning(self, "Erro no Formato", f"Erro: {e}\n Use valores hexadecimais")
        except IndexError:
            QMessageBox.warning(self, "Erro de Endereço", f"Erro: Endereço 0x{endereco_fisico:X} esta fora do limite da memória.")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", str(e))
    
    def iniciar_demonstracao(self):
        self.demonstracao_estado = "Busca_Opcode"
        self.demonstracao_passo_interno = 0
        self.demonstracao_tempo_byte = 0
        self.resetar_demonstracao()
        self.log_memoria.clear()
        
        self.demonstracao_ip_inicial = int(self.registrador_ip_input.text(), 16)
        
        self.demonstracao_label_ax.setText(self.registrador_ax_input.text())
        self.demonstracao_label_bx.setText(self.registrador_bx_input.text())
        self.demonstracao_label_cx.setText(self.registrador_cx_input.text())
        self.demonstracao_label_dx.setText(self.registrador_dx_input.text())
        self.demonstracao_label_cs.setText(self.registrador_cs_input.text())
        self.demonstracao_label_ss.setText(self.registrador_ss_input.text())
        self.demonstracao_label_ds.setText(self.registrador_ds_input.text())
        self.demonstracao_label_es.setText(self.registrador_es_input.text())
        self.demonstracao_label_ip.setText(self.registrador_ip_input.text())
        self.demonstracao_label_sp.setText(self.registrador_sp_input.text())
        self.demonstracao_label_bp.setText(self.registrador_bp_input.text())
        self.demonstracao_label_di.setText(self.registrador_di_input.text())
        self.demonstracao_label_si.setText(self.registrador_si_input.text())
        self.demonstracao_label_flag.setText(self.registrador_flag_input.text())

        self.demonstracao_operacao = self.operacao_c.currentText()
        
        if not self.dst_c.isEnabled() or self.dst_c.currentText() in ["---", ""]:
            self.demonstracao_dst_str = "AX"
        else:
            self.demonstracao_dst_str = self.dst_c.currentText()
        
        if not self.src_c.isEnabled() or self.src_c.currentText() in ["---", ""]:
            self.demonstracao_src_str = "AX"
        else:
            self.demonstracao_src_str = self.src_c.currentText()
            
        
        valor_final = "0000"
        
        if self.input_port.isEnabled():
            valor_final = self.input_port.text().upper()
        elif self.input_addr.isEnabled():
            valor_final = self.input_addr.text().upper()
        if not valor_final: valor_final = "0000"
        self.demonstracao_addr_str = valor_final
        
        instrucao_formatada = ""
                    
        if  self.demonstracao_operacao == "IN":
            instrucao_formatada = f"IN {self.demonstracao_dst_str}, Port {valor_final}"
        elif self.demonstracao_operacao == "OUT":
            instrucao_formatada = f"OUT Port {valor_final}, {self.demonstracao_src_str}"
        elif self.demonstracao_operacao in self.lista_ADDR:
            if self.demonstracao_dst_str == "AX":
                instrucao_formatada = f"{self.demonstracao_operacao} {valor_final}"
            else:
                instrucao_formatada = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}"
        
        elif self.demonstracao_operacao in ["PUSH", "MUL", "DIV"]:
            instrucao_formatada = f"{self.demonstracao_operacao} {self.demonstracao_src_str}"
        elif self.demonstracao_operacao in ["POP", "INC", "DEC", "NEG", "NOT"]:
            instrucao_formatada = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}"
        else: 
            instrucao_formatada = f"{self.demonstracao_operacao}, {self.demonstracao_dst_str}, {self.demonstracao_src_str}"
                    
        self.label_demonstracao_intrucao.setText(f"Instrução: {instrucao_formatada}")
        
        self.menu_stack.setCurrentIndex(7)
        self.label_resultado.setText(f"Demonstrando: {instrucao_formatada}")
        
        EF_opcode = 0
        try:
            segmento_cs = int(self.demonstracao_label_cs.text(), 16)
            offset_ip = int(self.demonstracao_label_ip.text(), 16)
            EF_opcode = (segmento_cs * 16) + offset_ip
            
            self.memoria[EF_opcode] = 0xE9 if self.demonstracao_operacao == "JMP" else 0xFF
            if self.demonstracao_operacao in self.lista_ADDR and self.demonstracao_dst_str == "---":
                valor_int = int(valor_final, 16)
                byte_baixo = valor_int & 0xFF
                byte_alto = (valor_int >> 8) & 0xFF
                
                self.memoria[EF_opcode + 1] = byte_baixo
                self.memoria[EF_opcode + 2] = byte_alto
            
        except ValueError:
            pass
        except IndexError:
            QMessageBox.warning(self, "Erro de endereço"), f"Erro: Endereço CS:IP ({EF_opcode:X}) está fora da memória."
            self.menu_stack.setCurrentIndex(6)
            
    def executar_passo_demonstracao(self):
        self.resetar_demonstracao()
        self.log_memoria.setStyleSheet("")
        
        terminou = False
        
        try:
            operacao_visual = self.nome_visual(self.demonstracao_operacao)
            dst_visual = self.nome_visual(self.demonstracao_dst_str)
            src_visual = self.nome_visual(self.demonstracao_src_str)
            
            if self.demonstracao_estado == "Busca_Opcode":
                terminou = self.Passo_Busca(operacao_visual, self.demonstracao_operacao, "Busca_DST")
                if terminou:
                    if self.demonstracao_operacao in self.lista_ADDR:
                        self.demonstracao_estado = "Execucao_Salto"
                    elif self.demonstracao_operacao in ["RET", "IRET", "IN", "OUT"]:
                        self.demonstracao_estado = "Decodificacao"
                    elif self.demonstracao_operacao == "PUSH":
                        self.demonstracao_estado = "Busca_SRC"
                    else:
                        self.demonstracao_estado = "Busca_DST"
                    self.demonstracao_passo_interno = 0
                
            elif self.demonstracao_estado == "Busca_DST":
                terminou = self.Passo_Busca(dst_visual, self.demonstracao_dst_str, "Busca_SRC")
                if terminou:
                    if self.demonstracao_operacao in ["POP", "INC", "DEC", "NEG", "NOT",]:
                        self.demonstracao_estado = "Decodificacao"
                    else:
                        self.demonstracao_estado = "Busca_SRC"
                    self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Busca_SRC":
                terminou = self.Passo_Busca(src_visual, self.demonstracao_src_str, "Decodificação")
                if terminou:
                    self.demonstracao_estado = "Decodificacao"
                    self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Decodificacao":
                if self.Passo_Decodificacao():
                    if self.demonstracao_operacao == "IN":
                        self.demonstracao_estado = "Execucao_IN"
                    elif self.demonstracao_operacao == "OUT":
                        self.demonstracao_estado = "Execucao_OUT"
                    elif self.demonstracao_operacao == "IRET":
                        self.demonstracao_estado = "Execucao_IRET"
                    elif self.demonstracao_operacao == "RET":
                        self.demonstracao_estado = "Execucao_RET"
                    elif self.demonstracao_operacao in self.lista_ADDR and self.demonstracao_dst_str == "---":
                        self.demonstracao_estado = "Busca_ADDR"
                        self.demonstracao_passo_interno = 0
                    elif self.demonstracao_src_str.startswith("["):
                        self.demonstracao_estado = "Busca_Operando_SRC"
                    elif self.demonstracao_operacao == "PUSH":
                        self.demonstracao_estado = "execucao_push"
                    elif self.demonstracao_operacao == "POP":
                        self.demonstracao_estado = "execucao_pop"
                    else:
                        self.demonstracao_estado = "Execucao"
                    self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Execucao_IN":
                self.Passo_IN()
                terminou = self.Passo_IN()
                if terminou:
                    self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Execucao_OUT":
                self.Passo_OUT()
                self.demonstracao_estado = "Fim"
                self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Execucao_IRET":
                self.Passo_Iret()
                self.demonstracao_estado = "Fim"
                self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Execucao_RET":
                self.Passo_Ret()
                self.demonstracao_estado = "Fim"
                self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Busca_ADDR":
                terminou = self.Passo_ADDR()
                if terminou:
                    self.demonstracao_estado = "Execucao_Salto"
                    self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "Execucao_Salto":
                    self.Passo_Salto()
                    self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Busca_Operando_SRC":
                terminou_leitura = self.Passo_Leitura()
                if terminou_leitura:
                    if self.demonstracao_operacao == "PUSH":
                        self.demonstracao_estado = "execucao_push"
                    else:
                        self.demonstracao_estado = "Execucao"
                    self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "execucao_push":
                if self.Passo_Push():
                    self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0
                    
            elif self.demonstracao_estado == "execucao_pop":
                if self.Passo_Pop():
                    self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Execucao":
                if self.executar_passo_execucao():
                    if self.demonstracao_dst_str.startswith("["):
                        self.demonstracao_estado = "Escreve_Operando_DST"
                else:
                    self.demonstracao_estado = "Fim"
                self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Escreve_Operando_DST":
                if self.Passo_Escrita():  
                    self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0
            
            elif self.demonstracao_estado == "Fim":  
                self.tela_barramento_endereco.setText("Instrução Concluída.")
                self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
                self.tela_barramento_dados.setText("Ciclo finalizado.")
                self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
                
                perguta = QMessageBox.question( 
                                                self,
                                                "Continuar Execução?",
                                                "Instrução finalizada!\n Deseja configurar a proxima instrução mantendo o estado atual?",
                                                QMessageBox.Yes | QMessageBox.No,
                                                QMessageBox.Yes
                                                )
                
                if perguta == QMessageBox.Yes:
                    self.salvar_configuiracao()
                    self.label_resultado.setText(f"Estado preservado. IP atual: {self.registrador_ip_input.text()}")
                    self.menu_stack.setCurrentIndex(6)
                    
                self.demonstracao_estado = "Busca_Opcode"
                self.demonstracao_passo_interno = 0
                
        except Exception as e:
            self.tela_barramento_endereco.setText(f"Erro: {e}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_estado = "Fim"
        
    def acesso_memoria(self, tipo, endereço, dado, comentario=""):
        if tipo =="Leitura":
            direcao_dado = "←"
        else:
            direcao_dado ="→"
        
        dado_formatado = ""
        
        if comentario.startswith("(") and "Byte" not in comentario and "Valor" not in comentario:
            dado_formatado = comentario.strip("()")
        else:
            dado_formatado = f"{dado} {comentario}"
        
        linha_endereco = f"Endereço → {endereço}"
        linha_dado = f"Dado {direcao_dado} {dado_formatado}"
        
        self.log_memoria.append(linha_endereco)
        self.log_memoria.append(linha_dado)
        self.log_memoria.setStyleSheet(self.cor_borda_style)
    
    def Passo_Busca(self, nome_passo, dado_esperado, proximo_estado):
        if self.demonstracao_passo_interno ==0:
            self.demonstracao_label_cs.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Ciclo de busca: Identificando CS e IP (para {nome_passo})")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        
        elif self.demonstracao_passo_interno ==1:
            segmento = int(self.demonstracao_label_cs.text(), 16)
            offset = int(self.demonstracao_label_ip.text(), 16)
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo: (CS * 16) + IP\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            
            self.demonstracao_passo_interno = 2
            return False
        
        elif self.demonstracao_passo_interno == 2:
            dado = self.memoria[self.demonstracao_endereco_calculado]
            texto_visual = self.nome_visual(nome_passo)
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"← Memória retorna: {nome_passo} ")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            
            self.acesso_memoria("Leitura", f"{self.demonstracao_endereco_calculado:X}", nome_passo, f"({nome_passo})")
            self.demonstracao_passo_interno = 3
            
            return False
            
        elif self.demonstracao_passo_interno == 3:
            offset_incremento = 2
            
            self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
            try:
                offset_atual = int(self.demonstracao_label_ip.text(), 16)
            except ValueError:
                offset_atual = 0
                
            offset_novo = (offset_atual + offset_incremento) & 0xFFFF
            
            self.demonstracao_label_ip.setText(f"{offset_novo:04X}")
            self.registrador_ip_input.setText(f"{offset_novo:04X}")
            self.tela_barramento_endereco.setText("CPU (Interno): Incrementa IP em {offset_incremento} bytes")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)        
            
            self.demonstracao_passo_interno = 0    
            return True
        return False
    
    def Passo_Decodificacao(self):
        if self.demonstracao_passo_interno == 0:   
            valor_imediato = getattr(self, "demonstracao_addr_str", "0000")
            
            if self.demonstracao_operacao in self.lista_ADDR:
                texto_instrucao = f"{self.demonstracao_operacao} {valor_imediato}"
            elif self.demonstracao_operacao == "IN":
                texto_instrucao = f"IN {self.demonstracao_dst_str}, port {valor_imediato}"
            elif self.demonstracao_operacao == "OUT":
                texto_instrucao = f"OUT port {valor_imediato}, {self.demonstracao_dst_str}"
            elif self.demonstracao_operacao in ["PUSH", "MUL", "DIV"]:
                texto_instrucao = f"{self.demonstracao_operacao} {self.demonstracao_src_str}"
            elif self.demonstracao_operacao in ["POP", "INC","DEC", "NEG", "NOT"]:
                texto_instrucao = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}"
            else:
                texto_instrucao = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}, {self.demonstracao_src_str} "
                
            self.tela_barramento_endereco.setText(f"CPU (Interno): Decodificando\n{texto_instrucao}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        
        elif self.demonstracao_passo_interno == 1:
            if self.demonstracao_operacao in ["IN", "OUT"]:
                return True            
            if self.demonstracao_operacao in self.lista_ADDR and self.demonstracao_dst_str == "---":
                return True
            
            if self.demonstracao_src_str not in ["---", "", "ADDR"]:
                try:
                    self.demonstracao_dados_src = int(self.pegar_demonstracao_label(self.demonstracao_src_str).text(), 16)
                except:
                    self.demonstracao_dados_src = 0
        
            if self.demonstracao_dst_str not in ["---", "", "ADDR"]:
                try:
                    self.demonstracao_dados_dst = int(self.pegar_demonstracao_label(self.demonstracao_dst_str).text(), 16)
                except:
                    self.demonstracao_dados_dst = 0
            
            if self.demonstracao_src_str in ["AX", "BX", "CX", "DX"]:
                self.demonstracao_dados_src = int(self.pegar_demonstracao_label(self.demonstracao_src_str).text(), 16)
        
            if self.demonstracao_dst_str in ["AX", "BX", "CX", "DX"]:
                self.demonstracao_dados_dst = int(self.pegar_demonstracao_label(self.demonstracao_dst_str).text(), 16)
            return True
            
    def Passo_Leitura(self):       
        registrador_offset_label = self.pegar_demonstracao_label(self.demonstracao_src_str.strip("[]"))
        registrador_offset_nome = self.demonstracao_src_str.strip("[]")
        
        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Leitura de Dados (SRC): Identificando DS e {registrador_offset_nome} (p/ Byte Baixo)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        
        elif self.demonstracao_passo_interno == 1:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16)
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (SRC): (DS * 16) + {registrador_offset_nome}\n({segmento:X} * 16) + {offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            
            byte_baixo = self.memoria[self.demonstracao_endereco_calculado]
            byte_alto = self.memoria[self.demonstracao_endereco_calculado + 1]
            
            if byte_baixo == 0x00 and byte_alto == 0x00:
                self.tela_barramento_dados.setText("Dado vazio. Aguardando no editor...")
                self.tela_barramento_dados.setStyleSheet(self.cor_borda_style)
                
                self.memoria_edicao_ef.setText(f"{self.demonstracao_endereco_calculado:X}")
                self.memoria_edicao_ef.setStyleSheet(self.cor_borda_style)
                self.memoria_edicao_valor.setText("")
                self.memoria_edicao_valor.setPlaceholderText("Digite o valor")
                self.memoria_edicao_valor.setStyleSheet(self.cor_borda_style)
                self.memoria_edicao_valor.setFocus()
                return False
                
            self.demonstracao_passo_interno = 2
            return False
        
        elif self.demonstracao_passo_interno == 2:
            byte_baixo = self.memoria[self.demonstracao_endereco_calculado]
            self.demonstracao_tempo_byte = byte_baixo
            dado_str = f"{byte_baixo:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style) 
            self.tela_barramento_dados.setText(f"← Memória retorna o Byte baixo: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 3
            return False
            
        if self.demonstracao_passo_interno == 3:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)     
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Leitura (SRC): Identificando DS e {registrador_offset_nome}+1 (p/ Byte Alto)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 4
            return False
        
        elif self.demonstracao_passo_interno == 4:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16) + 1
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (SRC): (DS * 16) + {registrador_offset_nome}+1\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)  
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 5
            return False
        
        elif self.demonstracao_passo_interno == 5:
            byte_alto = self.memoria[self.demonstracao_endereco_calculado]
            dado_str = f"{byte_alto:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"← Memória retorna o Byte alto: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)            
            self.demonstracao_dados_src = (byte_alto << 8) | self.demonstracao_tempo_byte
            self.demonstracao_passo_interno = 6
            return False
            
        elif self.demonstracao_passo_interno == 6:
            self.tela_barramento_endereco.setText(f"CPU (Interno): Montando valor 16 bits\nValor: 0x{self.demonstracao_dados_src:04X}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            
            endereço_alto = self.demonstracao_endereco_calculado
            endereço_baixo = endereço_alto - 1
            dado_completo_str = f"{self.demonstracao_dados_src:04X}"
            
            self.acesso_memoria("Leitura", f"{endereço_baixo:X}", dado_completo_str, "(Valor 16-bits)")            
            self.demonstracao_passo_interno = 0
            return True
        return False
    
    def Passo_Push(self):
        try:
            sp_text = self.demonstracao_label_sp.text()
            ss_text = self.demonstracao_label_ss.text()
            sp_valor = int(sp_text, 16) if sp_text else 0 
            ss_valor = int(ss_text, 16) if ss_text else 0 
        except ValueError:
            sp_valor = 0
            ss_valor = 0
        
        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            sp_valor = int(self.demonstracao_label_sp.text(), 16)
            sp_novo = (sp_valor - 2) & 0xFFFF
            sp_valor_str = f"{sp_novo:04X}"
            
            self.demonstracao_label_sp.setText(sp_valor_str)
            self.registrador_sp_input.setText(sp_valor_str)
            
            self.tela_barramento_endereco.setText(f"Execução PUSH: Decrementa SP/nSP = {sp_valor:04X} - 2 = {sp_novo:04X}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 1
            return False
        
        sp_valor = int(self.demonstracao_label_sp.text(), 16) 
        ss_valor = int(self.demonstracao_label_ss.text(), 16)   
        valor_escrever = self.demonstracao_dados_src
        byte_baixo = valor_escrever & 0xFF
        byte_alto = (valor_escrever >> 8) & 0xFF
        
        if self.demonstracao_passo_interno == 1:
            self.demonstracao_label_ss.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Escrita PUSH: Identificando SS e SP(p/Byte baixo) ")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 2
            return False
        
        elif self.demonstracao_passo_interno == 2:
            self.demonstracao_endereco_calculado = (ss_valor * 16) + sp_valor
            calcular_str = f"Calculo PUSH: (SS * 16) + SP\n({ss_valor:X} * 16) + {sp_valor:X} = {self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calcular_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 3
            return False

        elif self.demonstracao_passo_interno == 3:
            dado_str = f"{byte_baixo:02X}"
            self.tela_barramento_dados.setText(f"→ CPU envia o Byte baixo: {dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.memoria[self.demonstracao_endereco_calculado] = byte_baixo
            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(PUSH: Byte baixo)")
            self.demonstracao_passo_interno = 4
            return False

        elif self.demonstracao_passo_interno == 4:
            self.demonstracao_label_ss.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Escrita PUSH: Identificando SS e SP(p/Byte alto) ")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 5
            return False

        elif self.demonstracao_passo_interno == 5:
            self.demonstracao_endereco_calculado = (ss_valor * 16) + (sp_valor + 1)
            calcular_str = f"Calculo PUSH: (SS * 16) + SP\n({ss_valor:X} * 16) + {sp_valor+1:X} = {self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calcular_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 6
            return False

        elif self.demonstracao_passo_interno == 6:
            dado_str = f"{byte_alto:02X}"
            self.tela_barramento_dados.setText(f"→ CPU envia o Byte alto: {dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.memoria[self.demonstracao_endereco_calculado] = byte_alto
            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(PUSH: Byte alto)")
            self.demonstracao_passo_interno = 0
            return True
        
        return False
    
    def Passo_Pop(self):
        try:
            sp_text = self.demonstracao_label_sp.text()
            ss_text = self.demonstracao_label_ss.text()
            sp_valor = int(sp_text, 16) if sp_text else 0 
            ss_valor = int(ss_text, 16) if ss_text else 0 
        except ValueError:
            sp_valor = 0
            ss_valor = 0
        
        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_ss.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Leitura PUSH: Identificando SS e SP(p/Byte baixo) ")            
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
            
        elif self.demonstracao_passo_interno == 1:
            self.demonstracao_endereco_calculado = (ss_valor * 16) + sp_valor
            calcular_str = f"Calculo PUSH: (SS * 16) = {self.demonstracao_endereco_calculado:X}"
            self.demonstracao_passo_interno = 2
            return False
        
        elif self.demonstracao_passo_interno == 2:
            if self.demonstracao_endereco_calculado < len(self.memoria):
                byte_baixo = self.memoria[self.demonstracao_endereco_calculado]
            else:
                byte_baixo = 0
            
            self.demonstracao_tempo_byte = byte_baixo
            self.tela_barramento_dados.setText(f"→ Memória retorna Byte baixo: {byte_baixo:02X}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.acesso_memoria(f"Leitura", f"{self.demonstracao_endereco_calculado:X}", f"{byte_baixo:02X}", "(POP baixo)")
            self.demonstracao_passo_interno = 3            
            return False

        elif self.demonstracao_passo_interno == 3:
            self.tela_barramento_endereco.setText(f"Leitura POP: Identificando SS e SP(p/Byte alto) ")            
            self.demonstracao_passo_interno = 4
            return False

        elif self.demonstracao_passo_interno == 4:
            self.demonstracao_endereco_calculado = (ss_valor * 16) + (sp_valor + 1)
            calcular_str = f"Calculo PUSH: (SS * 16) + SP\n({ss_valor:X} * 16) + {sp_valor+1:X} = {self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ Cálculo: (SS*16)+sp+1 = {self.demonstracao_endereco_calculado:X}")
            self.demonstracao_passo_interno = 5
            return False

        elif self.demonstracao_passo_interno == 5:
            if self.demonstracao_endereco_calculado < len(self.memoria):
                byte_alto = self.memoria[self.demonstracao_endereco_calculado]
            else:
                byte_alto = 0

            self.tela_barramento_dados.setText(f"← Memória retorna Byte alto: {byte_alto:02X}")
            self.acesso_memoria("Leitura", f"{self.demonstracao_endereco_calculado:X}", f"{byte_alto:02X}", "(POP alto)")
            valor_final = (byte_alto << 8) | self.demonstracao_tempo_byte
            self.demonstracao_dados_dst = valor_final
            self.demonstracao_passo_interno = 6
            return False

        elif self.demonstracao_passo_interno == 6:
            valor_final_str = f"{self.demonstracao_dados_dst:04X}"
            
            registrador_label = self.pegar_demonstracao_label(self.demonstracao_dst_str)
            registrador_label.setText(valor_final_str)
            registrador_label.setStyleSheet(self.cor_borda_style)
            
            if self.demonstracao_dst_str == "AX": self.registrador_ax_input.setText(valor_final_str)
            elif self.demonstracao_dst_str == "BX": self.registrador_bx_input.setText(valor_final_str)
            elif self.demonstracao_dst_str == "CX": self.registrador_cx_input.setText(valor_final_str)
            elif self.demonstracao_dst_str == "DX": self.registrador_dx_input.setText(valor_final_str)
            elif self.demonstracao_dst_str == "SI": self.registrador_si_input.setText(valor_final_str)
            elif self.demonstracao_dst_str == "DI": self.registrador_di_input.setText(valor_final_str)

            sp_novo = (sp_valor + 2) & 0xFFFF 
            self.demonstracao_label_sp.setText(f"{sp_novo:04X}")
            self.registrador_sp_input.setText(f"{sp_novo:04X}")
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"POP Concluído: {valor_final_str} → {self.demonstracao_dst_str}. SP Incrementado")            
            self.demonstracao_passo_interno = 0
            return True
        
        return False
    
    def Passo_ADDR(self):
    
        segmento = int(self.demonstracao_label_cs.text(), 16)
        offset = int(self.demonstracao_label_ip.text(), 16)
        ef_atual = (segmento * 16) + offset
        
        byte_baixo = self.memoria[ef_atual - 1]
        byte_alto = self.memoria[ef_atual]
        
        valor_final = (byte_alto << 8) | byte_baixo
        self.demonstracao_addr_str = f"{valor_final:04X}"
        
        novo_offset = offset + 2
        self.demonstracao_label_ip.setText(f"{novo_offset:04X}")
        self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
        
        self.tela_barramento_endereco.setText(f"Busca ADDR: Leu {self.demonstracao_addr_str} da memória")
        self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
        self.tela_barramento_dados.setText(f"Dados: {byte_baixo:02X} {byte_alto:02X}")
        self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
        
        self.acesso_memoria("Leitura", f"{ef_atual-1:X}", self.demonstracao_addr_str, "(ADDR)")
        
        self.demonstracao_passo_interno = 0
        return True
    
    def Passo_Salto(self):
        novo_ip = self.demonstracao_addr_str    
        flags = self.registrador_flag_input.text()
        
        ip_atual_int = int(self.demonstracao_label_ip.text(), 16)
        
        variavel_ZF = "ZF" in flags
        variavel_SF = "SF" in flags
        
        saltar = False
        motivo = ""
        
        if self.demonstracao_operacao == "JMP":
            saltar = True
            motivo = "Incodicional"
        
        elif self.demonstracao_operacao == "JE":
            if "ZF" in flags:
                saltar = True
                motivo = "ZF ligada (Iguais)"
            else:
                saltar = False
                motivo = "ZF desligada (Diferente)"
            
        elif self.demonstracao_operacao == "JNE":
            if "ZF" not in flags:
                saltar = not True
                motivo = "ZF desligado (Iguais)"
            else:
                saltar = False
                motivo = "ZF ligado (Diferente)"
                
        elif self.demonstracao_operacao == "JG":
            variavel_SF = "SF" in flags
            variavel_ZF = "ZF" in flags
            
            if (not variavel_SF) and (not variavel_ZF):
                saltar = True
                motivo = "Maior (positivo e não zero)"
            else:
                saltar = False
                motivo = "Menor  ou IGUAL"
                
        elif self.demonstracao_operacao == "JGE":
            if "SF" not in flags:
                saltar = True
                motivo = "Maior ou igual (positivo, igual e não zero)"
            else:
                saltar = False
                motivo = "Menor"
                
        elif self.demonstracao_operacao == "JL":
            if "SF" in flags:
                saltar = True
                motivo = "Menor"
            else:
                saltar = False
                motivo = "Maior ou igual"
                
        elif self.demonstracao_operacao == "JLE":
            variavel_SF = "SF" in flags
            variavel_ZF = "ZF" in flags
            
            if variavel_SF or variavel_ZF:
                saltar = True
                motivo = "Menor ou igual"
            else:
                saltar = False
                motivo = "Maior"
            
        elif self.demonstracao_operacao == "CALL":
            saltar = True
            motivo = "Chamada de sub-rotina"
            
            sp_atual = int(self.registrador_sp_input.text(), 16)
            ss_atual = int(self.registrador_ss_input.text(), 16)
            
            novo_sp = (sp_atual - 2) & 0xFFFF
            ip_retorno = int(self.demonstracao_label_ip.text(), 16)
            endereco_pilha = (ss_atual * 16) + novo_sp
            
            byte_baixo = ip_retorno & 0xFF
            byte_alto = (ip_retorno >> 8) & 0xFF
            
            self.memoria[endereco_pilha] = byte_baixo
            self.memoria[endereco_pilha + 1] = byte_alto
            
            sp_str = f"{novo_sp:04X}"
            self.registrador_sp_input.setText(sp_str)
            self.demonstracao_label_sp.setText(sp_str)
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_ss.setStyleSheet(self.cor_borda_style)
            
            self.log_memoria.append(f"Stack: Guardou o retorno {ip_retorno:04X} em {endereco_pilha:x}")
            self.tela_barramento_dados.setText(f"PUSH IP: {ip_retorno:04X}")
            
        elif self.demonstracao_operacao == "LOOP":
            try: 
                cx_valor = int(self.registrador_cx_input.text(), 16)
            except:
                cx_valor = 0
                
            cx_valor = (cx_valor - 1) & 0xFFFF
            cx_str = f"{cx_valor:04X}"
            
            self.registrador_cx_input.setText(cx_str)
            self.demonstracao_label_cx.setText(cx_str)
            self.demonstracao_label_cx.setStyleSheet(self.cor_borda_style)
            
            if cx_valor != 0:
                saltar = True
                motivo = f"CX chegou a 0"
            else:
                saltar = False
                motivo = f"CX é {cx_str}"
                            
        if saltar:
            self.registrador_ip_input.setText(novo_ip)
            self.demonstracao_label_ip.setText(novo_ip)
            self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
            
            self.tela_barramento_endereco.setText(f"Salto realizado para {novo_ip} ({motivo})")
            self.acesso_memoria("Leitura", f"{novo_ip}", "Opcode da próxima instrução", "(salto)")
            try:
                self.demonstracao_ip_inicial = int(novo_ip, 16)
            except:
                pass
        
        else:
            ip_atual = self.demonstracao_label_ip.text()
            self.tela_barramento_endereco.setText(f"Salto ignorado ({motivo}). Continua em {ip_atual}")
            try:
                self.demonstracao_ip_inicial = int(ip_atual, 16)
            except:
                pass
        
        self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
        self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
    
    def Passo_Ret(self):
        sp_val = int(self.registrador_sp_input.text(), 16)
        ss_val = int(self.registrador_ss_input.text(), 16)
        
        endereco_pilha = (ss_val * 16) + sp_val
        
        byte_baixo = self.memoria[endereco_pilha]
        byte_alto = self.memoria[endereco_pilha + 1]
        
        ip_retorno = (byte_alto << 8) | byte_baixo
        ip_retorno_str = f"{ip_retorno:04X}"
        
        self.registrador_ip_input.setText(ip_retorno_str)
        self.demonstracao_label_ip.setText(ip_retorno_str)
        self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
        
        novo_sp = (sp_val + 2) & 0xFFFF
        sp_str = f"{novo_sp:04X}"
        
        self.registrador_sp_input.setText(sp_str)
        self.demonstracao_label_sp.setText(sp_str)
        self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
        
        self.tela_barramento_endereco.setText(f"RETORNOU para {ip_retorno_str} (Lido da Pilha em {endereco_pilha:X})")
        self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
        self.tela_barramento_dados.setText(f"POP IP: {ip_retorno_str}")
        
        self.acesso_memoria("Leitura", f"{endereco_pilha:X}", ip_retorno_str, "(RET: IP Restaurado)")
        
        try:
            self.demonstracao_ip_inicial = ip_retorno
        except:
            pass
        
    def Passo_Iret(self):
        sp_valor = int(self.registrador_sp_input.text(), 16)
        ss_valor = int(self.registrador_ss_input.text(), 16)
        base_pilha = (ss_valor * 16) + sp_valor
        
        ip_baixo = self.memoria[base_pilha] 
        ip_alto = self.memoria[base_pilha + 1] 
        novo_ip = (ip_alto << 8) | ip_baixo
        
        cs_baixo = self.memoria[base_pilha + 2] 
        cs_alto = self.memoria[base_pilha + 3]
        novo_cs = (cs_alto << 8) | cs_baixo
        
        flag_baixo = self.memoria[base_pilha + 4] 
        flag_alto = self.memoria[base_pilha + 5]
        novo_flag_numero = (flag_alto << 8) | flag_baixo  
        
        self.registrador_ip_input.setText(f"{novo_ip:04X}")
        self.demonstracao_label_ip.setText(f"{novo_ip:04X}")
        
        self.registrador_cs_input.setText(f"{novo_cs:04X}")
        self.demonstracao_label_cs.setText(f"{novo_cs:04X}")
        
        lista_flags = []
        if novo_flag_numero & 0x0080: lista_flags.append("SF")
        if novo_flag_numero & 0x0040: lista_flags.append("ZF")
        if novo_flag_numero & 0x0001: lista_flags.append("CF")
        
        texto_flags = " ".join(lista_flags) if lista_flags else "---"
        
        self.registrador_flag_input.setText(texto_flags)
        self.demonstracao_label_flag.setText(texto_flags)
        
        self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
        self.demonstracao_label_cs.setStyleSheet(self.cor_borda_style)
        self.demonstracao_label_flag.setStyleSheet(self.cor_borda_style)

        novo_sp = (sp_valor + 6) & 0xFFFF        
        self.registrador_sp_input.setText(f"{novo_sp:04X}")
        self.demonstracao_label_sp.setText(f"{novo_sp:04X}")
        self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
        
        self.tela_barramento_endereco.setText(f"IRET: Retornou CS:IP ({novo_cs:04X}:{novo_ip:04X} e flags.")
        self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
        
        self.acesso_memoria("Leitura (Stack)", f"{base_pilha:X}..{base_pilha+5:X}", " Contexto restaurado", "(IP, CS, Flags)")
        try:
            self.demonstracao_ip_inicial = novo_ip
        except:
            pass
        
    def Passo_IN(self):
        porta = getattr(self, "demonstracao_addr_str", "0000")
        registrador_nome = self.demonstracao_dst_str.strip("[]")
        
        if registrador_nome in ["---", "", "None"]:
            registrador_nome = "AX"
        
        if self.demonstracao_passo_interno == 0:
            self.tela_barramento_endereco.setText(f"IN: Ler a porta {porta}. Aguardando dados...")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            
            self.memoria_edicao_ef.setText(porta)
            self.memoria_edicao_valor.clear()
            
            self.memoria_edicao_ef.setStyleSheet(self.cor_borda_style)
            self.memoria_edicao_valor.setStyleSheet("border: 2px solid blue; background-color: #E6F7FF")
            self.memoria_edicao_valor.setFocus()

            self.demonstracao_passo_interno = 1
            return False
        
        elif self.demonstracao_passo_interno == 1:
            texto_digitado = self.memoria_edicao_valor.text()
            
            if not texto_digitado:
                self.memoria_edicao_valor.setFocus()
                return False
                
            try:    
                valor_recebido = int(texto_digitado, 16) & 0xFFFF
                valor_str = f"{valor_recebido:04X}"
                self.salvar_input(registrador_nome, valor_str)
            
                try:
                    registrador_label = self.pegar_demonstracao_label(registrador_nome)
                    registrador_label.setText(valor_str)
                    registrador_label.setStyleSheet(self.cor_borda_style)
                except:
                    pass
                
                self.tela_barramento_dados.setText(f"← Dado recebido: {valor_str}")
                self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
                self.log_memoria.append(f"Hardware (IN): Porta {porta} enviou {valor_str} para {registrador_nome}")
                
                self.memoria_edicao_ef.setStyleSheet("")
                self.memoria_edicao_valor.setStyleSheet("")
                
                self.demonstracao_passo_interno = 0
                return True
        
            except:
                self.tela_barramento_dados.setText("Erro: Valor inválido.")
                self.memoria_edicao_valor.setFocus()
                return False
            
        return False
            
    def Passo_OUT(self):
        porta = self.demonstracao_addr_str
        registrador_nome = self.demonstracao_src_str
        
        try: 
            label_src = self.pegar_demonstracao_label(registrador_nome)
            valor_enviado = label_src.text()
            label_src.setStyleSheet(self.cor_borda_style)
        except:
            valor_enviado = "0000"
            
        self.memoria_edicao_ef.setText(porta)
        self.memoria_edicao_valor.setText(valor_enviado)
        
        self.memoria_edicao_ef.setStyleSheet(self.cor_borda_style)
        self.memoria_edicao_valor.setStyleSheet(self.cor_borda_style)
        
        self.tela_barramento_endereco.setText(f"OUT: Enviando dados para a porta {porta}")
        self.tela_barramento_endereco.setStyleSheet(self.cor_borda_style)
        
        self.tela_barramento_dados.setText(f"→ Saída: {valor_enviado}")
        self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
        
        self.log_memoria.append(f"Hardware (OUT): Enviou {valor_enviado} para a porta {porta}")
        return True
    
    def nome_visual(self, texto):
        t = texto.strip()
        if t == "[SI]":
            valor = self.registrador_si_input.text()
            return f"[{valor}]"
        
        if t == "[DI]":
            valor = self.registrador_di_input.text()
            return f"[{valor}]"
        
        if t == "ADDR" and self.input_addr.text():
            return self.input_addr.text().upper()
        
        if t == "PORT" and self.input_port.text():
            return self.input_port.text().upper()
        
        return texto
    
    def executar_passo_execucao(self):   
        registrador_dst_label = self.pegar_demonstracao_label(self.demonstracao_dst_str)
        registrador_src_label = self.pegar_demonstracao_label(self.demonstracao_src_str)
        
        if self.demonstracao_passo_interno == 0:
            operacao = self.demonstracao_operacao
            try:
                valor_dst = int(self.demonstracao_dados_dst)
            except:
                valor_dst = 0
                
            try:
                valor_src = int(self.demonstracao_dados_src)     
            except:
                valor_src = 0
            
            dst_str = f"{valor_dst:04X}"
            src_str = f"{valor_src:04X}"
            
            if operacao == "MOV":
                self.tela_barramento_endereco.setText(f"Execução: Movendo {src_str} para {self.demonstracao_dst_str}")
                registrador_dst_label.setText(src_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, src_str)
                
            elif operacao == "XCHG":
                self.tela_barramento_endereco.setText(f"Execução: Trocando {self.demonstracao_dst_str} com {self.demonstracao_src_str}")
                registrador_dst_label.setText(src_str)
                registrador_src_label.setText(dst_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                registrador_src_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, src_str)
                self.salvar_input(self.demonstracao_src_str, dst_str)
                
            elif operacao == "ADD":
                resultado = (valor_dst + valor_src) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: {dst_str} + {src_str} = {resultado_str}")
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "SUB":
                resultado = (valor_dst - valor_src) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: {dst_str} - {src_str} = {resultado_str}")
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "MUL":
                try:
                    valor_ax = int(self.demonstracao_label_ax.text(), 16)
                except:
                    valor_ax = 0
                    
                resultado_cheio = valor_dst * valor_src
                resultado_dx = (resultado_cheio >> 16) & 0xFFFF
                resultado_ax = resultado_cheio & 0xFFFF
                str_dx = f"{resultado_dx:04X}"
                str_ax = f"{resultado_ax:04X}"
                self.tela_barramento_endereco.setText(f"Execução: AX * {src_str} = {resultado_cheio:X}")
                self.demonstracao_label_dx.setText(str_dx)
                self.demonstracao_label_dx.setStyleSheet(self.cor_borda_style)
                self.salvar_input("DX", str_dx)
                self.demonstracao_label_ax.setText(str_ax)
                self.demonstracao_label_ax.setStyleSheet(self.cor_borda_style)
                self.salvar_input("AX", str_ax)
                
            elif operacao == "INC":
                resultado = (valor_dst + 1) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: INC {valor_dst} = {resultado_str}")
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "DEC":
                resultado = (valor_dst - 1) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: DEC {valor_dst} = {resultado_str}")
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "NEG":
                resultado = (0 - valor_dst) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: NEG {valor_dst} = {resultado_str}")
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "DIV":
                try:
                    valor_ax = int(self.demonstracao_label_ax.text(), 16)
                    valor_dx = int(self.demonstracao_label_dx.text(), 16)
                except:
                    valor_ax = 0
                    valor_dx = 0
                    
                dividendo = (valor_dx << 16) | valor_ax
                divisor = valor_src
                if divisor == 0:
                    self.tela_barramento_endereco.setText("Erro: Divisão por zero")
                    self.tela_barramento_endereco.setStyleSheet("background-color: red; color: white; font-weight: bold;")
                    return True
                quociente = dividendo // divisor
                resto = dividendo % divisor    
                resultado_ax = quociente & 0xFFFF
                resultado_dx = resto & 0xFFFF
                str_ax = f"{resultado_ax:04X}"
                str_dx = f"{resultado_dx:04X}"
                self.tela_barramento_endereco.setText(f"Execução: {dividendo:X} / {divisor:x} -> Quociente(AX):{str_ax}, Resto(DX): {str_dx}")
                self.demonstracao_label_ax.setText(str_ax)
                self.demonstracao_label_ax.setStyleSheet(self.cor_borda_style)
                self.salvar_input("AX", str_ax)
                self.demonstracao_label_dx.setText(str_dx)
                self.demonstracao_label_dx.setStyleSheet(self.cor_borda_style)
                self.salvar_input("DX", str_dx)      
                
            elif operacao == "AND":
                resultado = (valor_dst & valor_src) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: {dst_str} AND {src_str} = {resultado_str}")          
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
            
            elif operacao == "OR":
                resultado = (valor_dst | valor_src) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: {dst_str} OR {src_str} = {resultado_str}")          
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "XOR":
                resultado = (valor_dst ^ valor_src) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: {dst_str} XOR {src_str} = {resultado_str}")          
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "NOT":
                resultado = (~valor_dst) & 0xFFFF
                resultado_str = f"{resultado:04X}"
                self.tela_barramento_endereco.setText(f"Execução: NOT {dst_str} = {resultado_str}")          
                registrador_dst_label.setText(resultado_str)
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                self.salvar_input(self.demonstracao_dst_str, resultado_str)
                
            elif operacao == "CMP":
                resultado_interno = valor_dst - valor_src
                resultado_str = f"{(resultado_interno & 0xFFFF):04X}"
                flag_str = self.atualizar_flag(valor_dst, valor_src, "CMP")
                status = ""
                if resultado_interno == 0:
                    status = "Iguais"
                elif valor_dst < valor_src:
                    status = "Menor"
                else: 
                    status = "Maior"
                
                self.tela_barramento_endereco.setText(f"Execução: CMP {dst_str}, {src_str} -> {status}. Flags: {flag_str}")          
                registrador_dst_label.setStyleSheet(self.cor_borda_style)
                registrador_src_label.setStyleSheet(self.cor_borda_style)
                            
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            
            registrador_dst_label.setStyleSheet(self.cor_borda_style)
            
            self.demonstracao_passo_interno = 1
            return False
        elif self.demonstracao_passo_interno == 1:
            return True
            
    def Passo_Escrita(self):
        registrador_offset_label = self.pegar_demonstracao_label(self.demonstracao_dst_str.strip("[]"))
        registrador_offset_nome = self.demonstracao_dst_str.strip("[]")
        self.demonstracao_dados_dst = self.demonstracao_dados_src
        byte_baixo = self.demonstracao_dados_dst & 0xFF
        byte_alto = (self.demonstracao_dados_dst >> 8) & 0xFF
        
        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Escrita (DST): Identificando DS e {registrador_offset_nome} (p/ Byte Baixo)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False
        elif self.demonstracao_passo_interno == 1:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16)
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (DST): (DS * 16) + {registrador_offset_nome}\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 2
            return False
        elif self.demonstracao_passo_interno == 2:
            dado_str = f"{byte_baixo:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"→ CPU envia o Byte baixo: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.memoria[self.demonstracao_endereco_calculado] = byte_baixo
            
            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(Byte Baixo)")
            
            self.demonstracao_passo_interno = 3
            return False
        if self.demonstracao_passo_interno == 3:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Escrita (DST): Identificando DS e {registrador_offset_nome}+1 (p/ Byte Alto)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 4
            return False
            
        elif self.demonstracao_passo_interno == 4:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16) + 1
            
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo (DST): (DS * 16) + {registrador_offset_nome}+1\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            
            self.tela_barramento_endereco.setText (f"→ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 5
            return False
        
        elif self.demonstracao_passo_interno == 5:
            dado_str = f"{byte_alto:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"→ CPU envia o Byte alto: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.memoria[self.demonstracao_endereco_calculado] = byte_alto
    
            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(Byte Alto)")

            self.demonstracao_passo_interno = 0
            return True
        return False
    
    def atualizar_interface(self, texto):
        self.dst_c.setEnabled(True)
        self.src_c.setEnabled(True)
        
        self.input_addr.setEnabled(False)
        self.input_addr.setStyleSheet("background-color: #EEE;")
        self.input_port.setEnabled(False)
        self.input_port.setStyleSheet("background-color: #EEE")
        
        if texto == "IN":
            self.src_c.setEnabled(False)
            self.src_c.setCurrentText("---")
            self.input_port.setEnabled(True)
            self.input_port.setStyleSheet("background-color: white; border: 1px solid #444;")
            
        elif texto == "OUT":
            self.dst_c.setEnabled(False)
            self.dst_c.setCurrentText("---")
            self.input_port.setEnabled(True)
            self.input_port.setStyleSheet("background-color: white; border: 1px solid #444;")
                
        elif texto in ["PUSH", "MUL", "DIV",]:
            self.dst_c.setEnabled(False)
            self.dst_c.setCurrentText("---")
            
        elif texto in ["POP","INC", "DEC", "NEG", "NOT",]:
            self.src_c.setEnabled(False)
            self.src_c.setCurrentText("---")
            
        elif texto in self.lista_ADDR:
            self.dst_c.setEnabled(False)   
            self.dst_c.setCurrentText("---")
            self.src_c.setEnabled(False)   
            self.src_c.setCurrentText("---")
            self.input_addr.setEnabled(True)
            self.input_addr.setStyleSheet("background-color: white; border: 1px solid #444")
            
        elif texto in ["RET", "IRET"]:
            self.dst_c.setEnabled(False)
            self.dst_c.setCurrentText("---")
            
        elif texto == "IN":
            self.dst_c.setEnabled(False); self.dst_c.setCurrentText("---")
            self.input_addr.setEnabled(True)
            self.input_addr.setStyleSheet("background-color: white; border: 1px solid #444;")
            
        elif texto == "OUT":
            self.dst_c.setEnabled(False); self.dst_c.setCurrentText("---")
            self.input_addr.setEnabled(True)
            self.input_addr.setStyleSheet("background-color: white; border: 1px solid #444;")
            
            self.src_c.setEnabled(False)
            self.src_c.setCurrentText("---")
            
        else:
            if self.dst_c.isEnabled() and self.dst_c.currentText() == "---" :
                self.dst_c.setCurrentIndex(0)
            if self.src_c.isEnabled() and self.src_c.currentText() == "---": 
                self.src_c.setCurrentIndex(0)
    
    def salvar_configuiracao(self):
        self.registrador_ax_input.setText(self.demonstracao_label_ax.text())
        self.registrador_bx_input.setText(self.demonstracao_label_bx.text())
        self.registrador_cx_input.setText(self.demonstracao_label_cx.text())
        self.registrador_dx_input.setText(self.demonstracao_label_dx.text())
        self.registrador_cs_input.setText(self.demonstracao_label_cs.text())
        self.registrador_ss_input.setText(self.demonstracao_label_ss.text())
        self.registrador_ds_input.setText(self.demonstracao_label_ds.text())
        self.registrador_es_input.setText(self.demonstracao_label_es.text())
        self.registrador_ip_input.setText(self.demonstracao_label_ip.text())
        self.registrador_sp_input.setText(self.demonstracao_label_sp.text())
        self.registrador_bp_input.setText(self.demonstracao_label_bp.text())
        self.registrador_di_input.setText(self.demonstracao_label_di.text())
        self.registrador_si_input.setText(self.demonstracao_label_si.text())
        self.registrador_flag_input.setText(self.demonstracao_label_flag.text())
                    
    def pegar_demonstracao_label(self, registrador_nome):
        registrador_nome = registrador_nome.upper().strip("[]") 
        if registrador_nome == "AX": return self.demonstracao_label_ax
        if registrador_nome == "BX": return self.demonstracao_label_bx
        if registrador_nome == "CX": return self.demonstracao_label_cx
        if registrador_nome == "DX": return self.demonstracao_label_dx
        if registrador_nome == "SI": return self.demonstracao_label_si
        if registrador_nome == "DI": return self.demonstracao_label_di
        if registrador_nome == "BP": return self.demonstracao_label_bp
        return QLabel("Erro")
    
    def atualizar_flag(self, valor_dst, valor_src, operacao):
        novo_flag = 0
        resultado_interno = 0
        
        if operacao in ["CMP",]:
            resultado_interno = valor_dst - valor_src
            if valor_src > valor_dst:
                novo_flag = novo_flag | 0x0001
        
        elif operacao in []:
            resultado_interno = valor_dst + valor_src
            if resultado_interno > 0x0001:
                novo_flag = novo_flag | 0x0001
                
        else:
            resultado_interno = valor_dst
            
        resultado_bits = resultado_interno & 0XFFFF
        if resultado_bits == 0:
            novo_flag = novo_flag | 0x0040
        
        if resultado_bits & 0x0080:
            novo_flag = novo_flag | 0x0080
            
        lista_flag = []
        texto_tela = ""
        if novo_flag & 0x0080: lista_flag.append("SF")
        if novo_flag & 0x0040: lista_flag.append("ZF")
        if novo_flag & 0x0001: lista_flag.append("CF")

        if not lista_flag:
            texto_tela = "---"
        else:
            texto_tela = " ".join(lista_flag)
            
        flag_str = f"{novo_flag:04X}"
        self.demonstracao_label_flag.setText(texto_tela)
        self.demonstracao_label_flag.setStyleSheet(self.cor_borda_style)
        self.registrador_flag_input.setText(texto_tela)
        return texto_tela           
        
    def salvar_input(self, nome_registrador, valor_hex): 
        nome = nome_registrador.strip("[]")
        if nome == "AX": self.registrador_ax_input.setText(valor_hex)
        elif nome == "BX": self.registrador_bx_input.setText(valor_hex)
        elif nome == "CX": self.registrador_cx_input.setText(valor_hex)
        elif nome == "DX": self.registrador_dx_input.setText(valor_hex)
        elif nome == "SI": self.registrador_si_input.setText(valor_hex)
        elif nome == "DI": self.registrador_di_input.setText(valor_hex)
        elif nome == "BP": self.registrador_bp_input.setText(valor_hex)
        elif nome == "SP": self.registrador_sp_input.setText(valor_hex)
    
    def resetar_demonstracao(self):
        widgets = [
            self.demonstracao_label_ax, self.demonstracao_label_bx, self.demonstracao_label_cx, self.demonstracao_label_dx,
            self.demonstracao_label_cs, self.demonstracao_label_ss, self.demonstracao_label_ds, self.demonstracao_label_es,
            self.demonstracao_label_ip, self.demonstracao_label_sp, self.demonstracao_label_bp, self.demonstracao_label_di,
            self.demonstracao_label_si, self.demonstracao_label_flag, self.memoria_edicao_ef, self.memoria_edicao_valor
        ]
        for widget in widgets:
            widget.setStyleSheet("")
            
        self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
        self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
        
    def Registradores(self, funcao):
        self.instrução_atual = funcao
        self.label_resultado.setText(f"Configurando: {funcao}")
        
        todas_operacoes = {
            "Função MOV": "MOV", "Função PUSH": "PUSH", "Função POP": "POP",
            "Função XCHG": "XCHG", "Função ADD": "ADD", "Função SUB": "SUB",
            "Função MUL": "MUL", "Função INC": "INC", "Função DEC": "DEC",
            "Função NEG": "NEG", "Função DIV": "DIV", "Função AND": "AND",
            "Função OR": "OR", "Função XOR": "XOR", "Função NOT": "NOT",
            "Função CMP": "CMP", "Função JMP": "JMP", "Função JE": "JE",
            "Função JNE": "JNE", "Função JG": "JG", "Função JGE": "JGE",
            "Função JL": "JL", "Função JLE": "JLE", "Função CALL": "CALL",
            "Função RET": "RET", "Função IRET": "IRET", "Função LOOP": "LOOP",
            "Função IN": "IN", "Função OUT": "OUT", 
        }
        
        operacao = todas_operacoes.get(funcao, "MOV")
        self.operacao_c.setCurrentText(operacao)
        
        self.menu_stack.setCurrentIndex(6)
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())
