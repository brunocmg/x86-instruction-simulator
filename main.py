# Simulador de Instruções x86 (modo real) - versão corrigida
# pip install PyQt5
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

        self.instrucao_atual = None

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
        self.registrador_flag_input.setPlaceholderText("SF ZF CF OF")

        self.input_addr = QLineEdit()
        self.input_addr.setPlaceholderText("ADDR")
        self.input_addr.setEnabled(False)

        self.input_port = QLineEdit()
        self.input_port.setPlaceholderText("PORT")
        self.input_port.setEnabled(False)

        self.memoria = bytearray(1048576)
        # Endereços físicos que já receberam um valor (pelo editor ou pela CPU).
        # Permite distinguir "posição nunca preenchida" de "posição com valor 0000".
        self.enderecos_definidos = set()
        # Escritas em memória geradas pela execução, feitas passo a passo depois dela.
        self.demonstracao_escritas_pendentes = []

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
                                  "ADD", "SUB", "MUL", "INC", "DEC", "NEG", "DIV",
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

    # ------------------------------------------------------------------ menus
    def _botao_menu(self, layout, texto, acao):
        botao = QPushButton(texto)
        botao.clicked.connect(acao)
        layout.addWidget(botao)
        return botao

    def _botao_voltar(self, layout):
        botao = QPushButton(" Voltar ao Menu Principal")
        botao.clicked.connect(lambda: self.menu_stack.setCurrentIndex(0))
        layout.addWidget(botao, alignment=Qt.AlignLeft)

    def _botoes_instrucao(self, layout, itens):
        for texto, nome in itens:
            self._botao_menu(layout, texto, lambda _=False, n=nome: self.Registradores(f"Função {n}"))

    def menu_principal(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        layout_botoes = QHBoxLayout()

        self._botao_menu(layout_botoes, "Moves", lambda: self.menu_stack.setCurrentIndex(1))
        self._botao_menu(layout_botoes, "Arithmetic", lambda: self.menu_stack.setCurrentIndex(2))
        self._botao_menu(layout_botoes, "Boolean", lambda: self.menu_stack.setCurrentIndex(3))
        self._botao_menu(layout_botoes, "Test/Compare", lambda: self.menu_stack.setCurrentIndex(4))

        layout.addLayout(layout_botoes)
        layout.addStretch(1)
        return pagina

    def menu_moves(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        self._botoes_instrucao(layout, [(" MOV DST, SRC", "MOV"), (" PUSH SRC", "PUSH"),
                                        (" POP DST", "POP"), (" XCHG DST, SRC", "XCHG")])
        self._botao_voltar(layout)
        layout.addStretch(1)
        return pagina

    def menu_arithmetic(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        self._botoes_instrucao(layout, [(" ADD DST, SRC", "ADD"), (" SUB DST, SRC", "SUB"),
                                        (" MUL SRC", "MUL"), (" INC DST", "INC"),
                                        (" DEC DST", "DEC"), (" NEG DST", "NEG"), (" DIV SRC", "DIV")])
        self._botao_voltar(layout)
        layout.addStretch(1)
        return pagina

    def menu_boolean(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        self._botoes_instrucao(layout, [(" AND DST, SRC", "AND"), (" OR DST, SRC", "OR"),
                                        (" XOR DST, SRC", "XOR"), (" NOT DST", "NOT")])
        self._botao_voltar(layout)
        layout.addStretch(1)
        return pagina

    def menu_compare(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        self._botoes_instrucao(layout, [(" CMP SRC1, SRC2", "CMP"), (" JMP ADDR", "JMP")])
        self._botao_menu(layout, " Jxx ADDR", lambda: self.menu_stack.setCurrentIndex(5))
        self._botoes_instrucao(layout, [(" CALL ADDR", "CALL"), (" RET", "RET"), (" IRET", "IRET"),
                                        (" LOOP ADDR", "LOOP"), (" IN AX, PORT", "IN"),
                                        (" OUT PORT, AX", "OUT")])
        self._botao_voltar(layout)
        layout.addStretch(1)
        return pagina

    def menu_jxx(self):
        pagina = QWidget()
        layout = QVBoxLayout(pagina)
        self._botoes_instrucao(layout, [(" JE ADDR", "JE"), (" JNE ADDR", "JNE"), (" JG ADDR", "JG"),
                                        (" JGE ADDR", "JGE"), (" JL ADDR", "JL"), (" JLE ADDR", "JLE")])
        self._botao_voltar(layout)
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
        Geral.addWidget(QLabel("AX:"), 0, 0); Geral.addWidget(self.registrador_ax_input, 0, 1)
        Geral.addWidget(QLabel("BX:"), 0, 2); Geral.addWidget(self.registrador_bx_input, 0, 3)
        Geral.addWidget(QLabel("CX:"), 1, 0); Geral.addWidget(self.registrador_cx_input, 1, 1)
        Geral.addWidget(QLabel("DX:"), 1, 2); Geral.addWidget(self.registrador_dx_input, 1, 3)
        Box_Geral.setLayout(Geral); layout_2_esquerda.addWidget(Box_Geral)

        Box_Segmentos = QGroupBox("Registrador de Segmentos")
        Box_Segmentos.setStyleSheet(Box_Style)
        Segmentos = QGridLayout()
        Segmentos.addWidget(QLabel("CS:"), 0, 0); Segmentos.addWidget(self.registrador_cs_input, 0, 1)
        Segmentos.addWidget(QLabel("SS:"), 0, 2); Segmentos.addWidget(self.registrador_ss_input, 0, 3)
        Segmentos.addWidget(QLabel("DS:"), 1, 0); Segmentos.addWidget(self.registrador_ds_input, 1, 1)
        Segmentos.addWidget(QLabel("ES:"), 1, 2); Segmentos.addWidget(self.registrador_es_input, 1, 3)
        Box_Segmentos.setLayout(Segmentos); layout_2_esquerda.addWidget(Box_Segmentos)

        Box_Offsets = QGroupBox("Registrador de Offsets")
        Box_Offsets.setStyleSheet(Box_Style)
        Offsets = QGridLayout()
        Offsets.addWidget(QLabel("IP:"), 0, 0); Offsets.addWidget(self.registrador_ip_input, 0, 1)
        Offsets.addWidget(QLabel("SP:"), 0, 2); Offsets.addWidget(self.registrador_sp_input, 0, 3)
        Offsets.addWidget(QLabel("BP:"), 1, 0); Offsets.addWidget(self.registrador_bp_input, 1, 1)
        Offsets.addWidget(QLabel("DI:"), 1, 2); Offsets.addWidget(self.registrador_di_input, 1, 3)
        Offsets.addWidget(QLabel("SI:"), 2, 0); Offsets.addWidget(self.registrador_si_input, 2, 1)
        Box_Offsets.setLayout(Offsets); layout_2_esquerda.addWidget(Box_Offsets)

        Box_Flag = QGroupBox("Registrador de Flags")
        Box_Flag.setStyleSheet(Box_Style)
        Flag = QGridLayout()
        Flag.addWidget(QLabel("FLAGS:"), 0, 0); Flag.addWidget(self.registrador_flag_input, 0, 1)
        Box_Flag.setLayout(Flag); layout_2_esquerda.addWidget(Box_Flag)

        layout_2_esquerda.addStretch(1)
        layout_2_configuracao.addLayout(layout_2_esquerda, 4)

        Box_Instrucao = QGroupBox("Instrução Atual")
        Box_Instrucao.setStyleSheet(Box_Style)
        Instrucao = QGridLayout()
        Instrucao.addWidget(QLabel("Operação:"), 0, 0); Instrucao.addWidget(self.operacao_c, 0, 1)
        Instrucao.addWidget(QLabel("Destino (DST):"), 1, 0); Instrucao.addWidget(self.dst_c, 1, 1)
        Instrucao.addWidget(QLabel("Origem (SRC):"), 2, 0); Instrucao.addWidget(self.src_c, 2, 1)
        Instrucao.addWidget(QLabel("ADDR:"), 3, 0); Instrucao.addWidget(self.input_addr, 3, 1)
        Instrucao.addWidget(QLabel("PORT:"), 4, 0); Instrucao.addWidget(self.input_port, 4, 1)
        Box_Instrucao.setLayout(Instrucao); layout_2_direita.addWidget(Box_Instrucao)

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
        Geral.addWidget(QLabel("AX:"), 0, 0); Geral.addWidget(self.demonstracao_label_ax, 0, 1)
        Geral.addWidget(QLabel("BX:"), 0, 2); Geral.addWidget(self.demonstracao_label_bx, 0, 3)
        Geral.addWidget(QLabel("CX:"), 1, 0); Geral.addWidget(self.demonstracao_label_cx, 1, 1)
        Geral.addWidget(QLabel("DX:"), 1, 2); Geral.addWidget(self.demonstracao_label_dx, 1, 3)
        Box_Geral.setLayout(Geral); parte_cpu.addWidget(Box_Geral)

        Box_Segmentos = QGroupBox("Registrador de Segmentos")
        Box_Segmentos.setStyleSheet(Box_Style)
        Segmentos = QGridLayout()
        Segmentos.addWidget(QLabel("CS:"), 0, 0); Segmentos.addWidget(self.demonstracao_label_cs, 0, 1)
        Segmentos.addWidget(QLabel("SS:"), 0, 2); Segmentos.addWidget(self.demonstracao_label_ss, 0, 3)
        Segmentos.addWidget(QLabel("DS:"), 1, 0); Segmentos.addWidget(self.demonstracao_label_ds, 1, 1)
        Segmentos.addWidget(QLabel("ES:"), 1, 2); Segmentos.addWidget(self.demonstracao_label_es, 1, 3)
        Box_Segmentos.setLayout(Segmentos); parte_cpu.addWidget(Box_Segmentos)

        Box_Offsets = QGroupBox("Registrador de Offsets")
        Box_Offsets.setStyleSheet(Box_Style)
        Offsets = QGridLayout()
        Offsets.addWidget(QLabel("IP:"), 0, 0); Offsets.addWidget(self.demonstracao_label_ip, 0, 1)
        Offsets.addWidget(QLabel("SP:"), 0, 2); Offsets.addWidget(self.demonstracao_label_sp, 0, 3)
        Offsets.addWidget(QLabel("BP:"), 1, 0); Offsets.addWidget(self.demonstracao_label_bp, 1, 1)
        Offsets.addWidget(QLabel("DI:"), 1, 2); Offsets.addWidget(self.demonstracao_label_di, 1, 3)
        Offsets.addWidget(QLabel("SI:"), 2, 0); Offsets.addWidget(self.demonstracao_label_si, 2, 1)
        Box_Offsets.setLayout(Offsets); parte_cpu.addWidget(Box_Offsets)

        Box_Flag = QGroupBox("Registrador de Flags")
        Box_Flag.setStyleSheet(Box_Style)
        Flag = QGridLayout()
        Flag.addWidget(QLabel("FLAGS:"), 0, 0); Flag.addWidget(self.demonstracao_label_flag, 0, 1)
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

    # ----------------------------------------------------------- memória
    def escrever_byte(self, endereco, valor):
        """Escreve um byte na memória e marca o endereço como definido."""
        self.memoria[endereco] = valor & 0xFF
        self.enderecos_definidos.add(endereco)

    def salvar_memoria(self, _checked=False):
        endereco_fisico = 0
        try:
            ef_str = self.memoria_edicao_ef.text().strip()
            valor_str = self.memoria_edicao_valor.text().strip()

            if not ef_str or not valor_str:
                raise ValueError("Endereço físico e valor não podem estar vazios.")

            endereco_fisico = int(ef_str, 16)
            valor = int(valor_str, 16)

            if not 0 <= endereco_fisico < len(self.memoria):
                raise IndexError

            info = ""
            if len(valor_str) <= 2 and valor <= 0xFF:
                self.escrever_byte(endereco_fisico, valor)
                info = f"Salvar: {valor:02X} em {endereco_fisico:X}"
            elif valor <= 0xFFFF:
                if endereco_fisico + 1 >= len(self.memoria):
                    raise IndexError
                self.escrever_byte(endereco_fisico, valor & 0xFF)
                self.escrever_byte(endereco_fisico + 1, (valor >> 8) & 0xFF)
                info = f"Salvar: {valor:04X} em {endereco_fisico:X}"
            else:
                raise ValueError("Valor excede 16 bits (FFFF)")

            self.log_memoria.setStyleSheet(self.cor_borda_style)
            self.log_memoria.append(info)

            QMessageBox.information(self, "Memória", "Valor salvo com sucesso na memória.")

        except ValueError as e:
            QMessageBox.warning(self, "Erro no Formato", f"Erro: {e}\n Use valores hexadecimais")
        except IndexError:
            QMessageBox.warning(self, "Erro de Endereço", f"Erro: Endereço 0x{endereco_fisico:X} está fora do limite da memória.")
        except Exception as e:
            QMessageBox.critical(self, "Erro Inesperado", str(e))

    # ------------------------------------------------------ demonstração
    def precisa_ler_destino(self):
        """True quando o destino é um operando de memória cujo valor atual é usado pela operação."""
        return (self.demonstracao_dst_str.startswith("[")
                and self.demonstracao_operacao in ["ADD", "SUB", "INC", "DEC", "NEG", "AND", "OR", "XOR", "NOT", "XCHG", "CMP"])

    def gravar_operando(self, operando, valor_hex):
        """Registrador: atualiza na hora. Memória: agenda a escrita (feita nos passos seguintes)."""
        if operando.startswith("["):
            self.demonstracao_escritas_pendentes.append((operando, int(valor_hex, 16)))
        else:
            label = self.pegar_demonstracao_label(operando)
            label.setText(valor_hex)
            label.setStyleSheet(self.cor_borda_style)
            self.salvar_input(operando, valor_hex)

    def iniciar_demonstracao(self):
        self.demonstracao_estado = "Busca_Opcode"
        self.demonstracao_passo_interno = 0
        self.demonstracao_tempo_byte = 0
        self.demonstracao_escritas_pendentes = []
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
        if not valor_final:
            valor_final = "0000"
        self.demonstracao_addr_str = valor_final

        instrucao_formatada = ""

        if self.demonstracao_operacao == "IN":
            instrucao_formatada = f"IN {self.demonstracao_dst_str}, Port {valor_final}"
        elif self.demonstracao_operacao == "OUT":
            instrucao_formatada = f"OUT Port {valor_final}, {self.demonstracao_src_str}"
        elif self.demonstracao_operacao in self.lista_ADDR:
            instrucao_formatada = f"{self.demonstracao_operacao} {valor_final}"
        elif self.demonstracao_operacao in ["RET", "IRET"]:
            instrucao_formatada = self.demonstracao_operacao
        elif self.demonstracao_operacao in ["PUSH", "MUL", "DIV"]:
            instrucao_formatada = f"{self.demonstracao_operacao} {self.demonstracao_src_str}"
        elif self.demonstracao_operacao in ["POP", "INC", "DEC", "NEG", "NOT"]:
            instrucao_formatada = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}"
        else:
            instrucao_formatada = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}, {self.demonstracao_src_str}"

        self.label_demonstracao_intrucao.setText(f"Instrução: {instrucao_formatada}")

        self.menu_stack.setCurrentIndex(7)
        self.label_resultado.setText(f"Demonstrando: {instrucao_formatada}")

        EF_opcode = 0
        try:
            segmento_cs = int(self.demonstracao_label_cs.text(), 16)
            offset_ip = int(self.demonstracao_label_ip.text(), 16)
            EF_opcode = (segmento_cs * 16) + offset_ip

            # Opcode ilustrativo (não é a codificação real). Não sobrescreve o que o usuário já gravou ali.
            if EF_opcode not in self.enderecos_definidos:
                self.memoria[EF_opcode] = 0xE9 if self.demonstracao_operacao == "JMP" else 0xFF

        except ValueError:
            pass
        except IndexError:
            QMessageBox.warning(self, "Erro de endereço", f"Erro: Endereço CS:IP ({EF_opcode:X}) está fora da memória.")
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
                    if self.demonstracao_operacao in ["POP", "INC", "DEC", "NEG", "NOT"]:
                        self.demonstracao_estado = "Decodificacao"
                    else:
                        self.demonstracao_estado = "Busca_SRC"
                    self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "Busca_SRC":
                terminou = self.Passo_Busca(src_visual, self.demonstracao_src_str, "Decodificacao")
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
                    elif self.demonstracao_src_str.startswith("["):
                        self.demonstracao_estado = "Busca_Operando_SRC"
                    elif self.precisa_ler_destino():
                        self.demonstracao_estado = "Busca_Operando_DST"
                    elif self.demonstracao_operacao == "PUSH":
                        self.demonstracao_estado = "execucao_push"
                    elif self.demonstracao_operacao == "POP":
                        self.demonstracao_estado = "execucao_pop"
                    else:
                        self.demonstracao_estado = "Execucao"
                    self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "Execucao_IN":
                if self.Passo_IN():
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

            elif self.demonstracao_estado == "Execucao_Salto":
                self.Passo_Salto()
                self.demonstracao_estado = "Fim"
                self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "Busca_Operando_SRC":
                if self.Passo_Leitura("SRC"):
                    if self.demonstracao_operacao == "PUSH":
                        self.demonstracao_estado = "execucao_push"
                    elif self.precisa_ler_destino():
                        self.demonstracao_estado = "Busca_Operando_DST"
                    else:
                        self.demonstracao_estado = "Execucao"
                    self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "Busca_Operando_DST":
                if self.Passo_Leitura("DST"):
                    self.demonstracao_estado = "Execucao"
                    self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "execucao_push":
                if self.Passo_Push():
                    self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "execucao_pop":
                if self.Passo_Pop():
                    if self.demonstracao_escritas_pendentes:
                        self.demonstracao_estado = "Escreve_Operando_DST"
                    else:
                        self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "Execucao":
                houve_erro = self.executar_passo_execucao()
                if not houve_erro and self.demonstracao_escritas_pendentes:
                    self.demonstracao_estado = "Escreve_Operando_DST"
                else:
                    self.demonstracao_estado = "Fim"
                self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "Escreve_Operando_DST":
                operando, valor = self.demonstracao_escritas_pendentes[0]
                if self.Passo_Escrita(operando, valor):
                    self.demonstracao_escritas_pendentes.pop(0)
                    if not self.demonstracao_escritas_pendentes:
                        self.demonstracao_estado = "Fim"
                    self.demonstracao_passo_interno = 0

            elif self.demonstracao_estado == "Fim":
                self.tela_barramento_endereco.setText("Instrução Concluída.")
                self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
                self.tela_barramento_dados.setText("Ciclo finalizado.")
                self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)

                pergunta = QMessageBox.question(
                    self,
                    "Continuar Execução?",
                    "Instrução finalizada!\n Deseja configurar a proxima instrução mantendo o estado atual?",
                    QMessageBox.Yes | QMessageBox.No,
                    QMessageBox.Yes
                )

                if pergunta == QMessageBox.Yes:
                    self.salvar_configuracao()
                    self.label_resultado.setText(f"Estado preservado. IP atual: {self.registrador_ip_input.text()}")
                    self.menu_stack.setCurrentIndex(6)

                self.demonstracao_estado = "Busca_Opcode"
                self.demonstracao_passo_interno = 0
                self.demonstracao_escritas_pendentes = []

        except Exception as e:
            self.tela_barramento_endereco.setText(f"Erro: {e}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_estado = "Fim"
            self.demonstracao_passo_interno = 0
            self.demonstracao_escritas_pendentes = []

    def acesso_memoria(self, tipo, endereço, dado, comentario=""):
        if tipo == "Leitura":
            direcao_dado = "←"
        else:
            direcao_dado = "→"

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
        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_cs.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Ciclo de busca: Identificando CS e IP (para {nome_passo})")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False

        elif self.demonstracao_passo_interno == 1:
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
            _ = self.memoria[self.demonstracao_endereco_calculado]  # valida o endereço
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
            self.tela_barramento_endereco.setText(f"CPU (Interno): Incrementa IP em {offset_incremento} bytes")
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
                texto_instrucao = f"OUT port {valor_imediato}, {self.demonstracao_src_str}"
            elif self.demonstracao_operacao in ["RET", "IRET"]:
                texto_instrucao = self.demonstracao_operacao
            elif self.demonstracao_operacao in ["PUSH", "MUL", "DIV"]:
                texto_instrucao = f"{self.demonstracao_operacao} {self.demonstracao_src_str}"
            elif self.demonstracao_operacao in ["POP", "INC", "DEC", "NEG", "NOT"]:
                texto_instrucao = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}"
            else:
                texto_instrucao = f"{self.demonstracao_operacao} {self.demonstracao_dst_str}, {self.demonstracao_src_str} "

            self.tela_barramento_endereco.setText(f"CPU (Interno): Decodificando\n{texto_instrucao}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False

        elif self.demonstracao_passo_interno == 1:
            if self.demonstracao_operacao in ["IN", "OUT", "RET", "IRET"]:
                return True

            if self.demonstracao_src_str not in ["---", "", "ADDR"]:
                try:
                    self.demonstracao_dados_src = int(self.pegar_demonstracao_label(self.demonstracao_src_str).text(), 16)
                except ValueError:
                    self.demonstracao_dados_src = 0

            if self.demonstracao_dst_str not in ["---", "", "ADDR"]:
                try:
                    self.demonstracao_dados_dst = int(self.pegar_demonstracao_label(self.demonstracao_dst_str).text(), 16)
                except ValueError:
                    self.demonstracao_dados_dst = 0
            return True
        return False

    def Passo_Leitura(self, lado="SRC"):
        """Lê 16 bits da memória apontada por DS:[SI] ou DS:[DI] (lado = 'SRC' ou 'DST')."""
        operando = self.demonstracao_src_str if lado == "SRC" else self.demonstracao_dst_str
        registrador_offset_nome = operando.strip("[]")
        registrador_offset_label = self.pegar_demonstracao_label(registrador_offset_nome)

        if self.demonstracao_passo_interno == 0:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Leitura de Dados ({lado}): Identificando DS e {registrador_offset_nome} (p/ Byte Baixo)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False

        elif self.demonstracao_passo_interno == 1:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16)
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo ({lado}): (DS * 16) + {registrador_offset_nome}\n({segmento:X} * 16) + {offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)

            ef = self.demonstracao_endereco_calculado
            _ = self.memoria[ef + 1]  # valida o endereço

            # Posição nunca preenchida: espera o usuário informar o valor no editor
            # (um valor 0000 digitado pelo usuário conta como preenchido).
            if ef not in self.enderecos_definidos and (ef + 1) not in self.enderecos_definidos:
                self.tela_barramento_dados.setText("Dado vazio. Aguardando no editor...")
                self.tela_barramento_dados.setStyleSheet(self.cor_borda_style)

                self.memoria_edicao_ef.setText(f"{ef:X}")
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

        elif self.demonstracao_passo_interno == 3:
            self.demonstracao_label_ds.setStyleSheet(self.cor_borda_style)
            registrador_offset_label.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"Leitura ({lado}): Identificando DS e {registrador_offset_nome}+1 (p/ Byte Alto)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 4
            return False

        elif self.demonstracao_passo_interno == 4:
            segmento = int(self.demonstracao_label_ds.text(), 16)
            offset = int(registrador_offset_label.text(), 16) + 1
            self.demonstracao_endereco_calculado = (segmento * 16) + offset
            calculo_str = f"Cálculo ({lado}): (DS * 16) + {registrador_offset_nome}+1\n(0x{segmento:X} * 16) + 0x{offset:X} = 0x{self.demonstracao_endereco_calculado:X}"
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
            valor_lido = (byte_alto << 8) | self.demonstracao_tempo_byte
            if lado == "SRC":
                self.demonstracao_dados_src = valor_lido
            else:
                self.demonstracao_dados_dst = valor_lido
            self.demonstracao_passo_interno = 6
            return False

        elif self.demonstracao_passo_interno == 6:
            valor_lido = self.demonstracao_dados_src if lado == "SRC" else self.demonstracao_dados_dst
            self.tela_barramento_endereco.setText(f"CPU (Interno): Montando valor 16 bits\nValor: 0x{valor_lido:04X}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)

            endereco_alto = self.demonstracao_endereco_calculado
            endereco_baixo = endereco_alto - 1
            self.acesso_memoria("Leitura", f"{endereco_baixo:X}", f"{valor_lido:04X}", "(Valor 16-bits)")
            self.demonstracao_passo_interno = 0
            return True
        return False

    # ------------------------------------------------------------- pilha
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

            self.tela_barramento_endereco.setText(f"Execução PUSH: Decrementa SP\nSP = {sp_valor:04X} - 2 = {sp_novo:04X}")
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
            self.tela_barramento_endereco.setText("Escrita PUSH: Identificando SS e SP (p/ Byte baixo)")
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
            self.escrever_byte(self.demonstracao_endereco_calculado, byte_baixo)
            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(PUSH: Byte baixo)")
            self.demonstracao_passo_interno = 4
            return False

        elif self.demonstracao_passo_interno == 4:
            self.demonstracao_label_ss.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText("Escrita PUSH: Identificando SS e SP (p/ Byte alto)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 5
            return False

        elif self.demonstracao_passo_interno == 5:
            self.demonstracao_endereco_calculado = (ss_valor * 16) + (sp_valor + 1)
            calcular_str = f"Calculo PUSH: (SS * 16) + SP + 1\n({ss_valor:X} * 16) + {sp_valor + 1:X} = {self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calcular_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 6
            return False

        elif self.demonstracao_passo_interno == 6:
            dado_str = f"{byte_alto:02X}"
            self.tela_barramento_dados.setText(f"→ CPU envia o Byte alto: {dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.escrever_byte(self.demonstracao_endereco_calculado, byte_alto)
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
            self.tela_barramento_endereco.setText("Leitura POP: Identificando SS e SP (p/ Byte baixo)")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 1
            return False

        elif self.demonstracao_passo_interno == 1:
            self.demonstracao_endereco_calculado = (ss_valor * 16) + sp_valor
            calcular_str = f"Calculo POP: (SS * 16) + SP\n({ss_valor:X} * 16) + {sp_valor:X} = {self.demonstracao_endereco_calculado:X}"
            self.tela_barramento_endereco.setText(f"→ {calcular_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.demonstracao_passo_interno = 2
            return False

        elif self.demonstracao_passo_interno == 2:
            if self.demonstracao_endereco_calculado < len(self.memoria):
                byte_baixo = self.memoria[self.demonstracao_endereco_calculado]
            else:
                byte_baixo = 0

            self.demonstracao_tempo_byte = byte_baixo
            self.tela_barramento_dados.setText(f"← Memória retorna Byte baixo: {byte_baixo:02X}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.acesso_memoria("Leitura", f"{self.demonstracao_endereco_calculado:X}", f"{byte_baixo:02X}", "(POP baixo)")
            self.demonstracao_passo_interno = 3
            return False

        elif self.demonstracao_passo_interno == 3:
            self.tela_barramento_endereco.setText("Leitura POP: Identificando SS e SP (p/ Byte alto)")
            self.demonstracao_passo_interno = 4
            return False

        elif self.demonstracao_passo_interno == 4:
            self.demonstracao_endereco_calculado = (ss_valor * 16) + (sp_valor + 1)
            self.tela_barramento_endereco.setText(f"→ Cálculo: (SS*16)+SP+1 = {self.demonstracao_endereco_calculado:X}")
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

            # Destino em memória: a escrita é feita nos passos seguintes
            self.gravar_operando(self.demonstracao_dst_str, valor_final_str)

            sp_novo = (sp_valor + 2) & 0xFFFF
            self.demonstracao_label_sp.setText(f"{sp_novo:04X}")
            self.registrador_sp_input.setText(f"{sp_novo:04X}")
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.tela_barramento_endereco.setText(f"POP Concluído: {valor_final_str} → {self.demonstracao_dst_str}. SP Incrementado")
            self.demonstracao_passo_interno = 0
            return True

        return False

    # ----------------------------------------------------------- saltos
    def Passo_Salto(self):
        novo_ip = f"{int(self.demonstracao_addr_str, 16) & 0xFFFF:04X}"
        flags = set(self.registrador_flag_input.text().upper().replace(",", " ").split())

        ZF = "ZF" in flags
        SF = "SF" in flags
        OF = "OF" in flags

        operacao = self.demonstracao_operacao
        saltar = False
        motivo = ""

        if operacao == "JMP":
            saltar = True
            motivo = "Incondicional"

        elif operacao == "JE":
            saltar = ZF
            motivo = "ZF ligada (iguais)" if ZF else "ZF desligada (diferentes)"

        elif operacao == "JNE":
            saltar = not ZF
            motivo = "ZF desligada (diferentes)" if not ZF else "ZF ligada (iguais)"

        elif operacao == "JG":
            saltar = (not ZF) and (SF == OF)
            motivo = "Maior (ZF desligada e SF = OF)" if saltar else "Menor ou igual"

        elif operacao == "JGE":
            saltar = (SF == OF)
            motivo = "Maior ou igual (SF = OF)" if saltar else "Menor (SF diferente de OF)"

        elif operacao == "JL":
            saltar = (SF != OF)
            motivo = "Menor (SF diferente de OF)" if saltar else "Maior ou igual"

        elif operacao == "JLE":
            saltar = ZF or (SF != OF)
            motivo = "Menor ou igual" if saltar else "Maior"

        elif operacao == "CALL":
            saltar = True
            motivo = "Chamada de sub-rotina"

            sp_atual = int(self.registrador_sp_input.text(), 16)
            ss_atual = int(self.registrador_ss_input.text(), 16)

            novo_sp = (sp_atual - 2) & 0xFFFF
            ip_retorno = int(self.demonstracao_label_ip.text(), 16)
            endereco_pilha = (ss_atual * 16) + novo_sp

            self.escrever_byte(endereco_pilha, ip_retorno & 0xFF)
            self.escrever_byte(endereco_pilha + 1, (ip_retorno >> 8) & 0xFF)

            sp_str = f"{novo_sp:04X}"
            self.registrador_sp_input.setText(sp_str)
            self.demonstracao_label_sp.setText(sp_str)
            self.demonstracao_label_sp.setStyleSheet(self.cor_borda_style)
            self.demonstracao_label_ss.setStyleSheet(self.cor_borda_style)

            self.log_memoria.append(f"Stack: Guardou o retorno {ip_retorno:04X} em {endereco_pilha:X}")
            self.tela_barramento_dados.setText(f"PUSH IP: {ip_retorno:04X}")

        elif operacao == "LOOP":
            try:
                cx_valor = int(self.registrador_cx_input.text(), 16)
            except ValueError:
                cx_valor = 0

            cx_valor = (cx_valor - 1) & 0xFFFF
            cx_str = f"{cx_valor:04X}"

            self.registrador_cx_input.setText(cx_str)
            self.demonstracao_label_cx.setText(cx_str)
            self.demonstracao_label_cx.setStyleSheet(self.cor_borda_style)

            if cx_valor != 0:
                saltar = True
                motivo = f"CX = {cx_str} (diferente de 0)"
            else:
                saltar = False
                motivo = "CX chegou a 0"

        if saltar:
            self.registrador_ip_input.setText(novo_ip)
            self.demonstracao_label_ip.setText(novo_ip)
            self.demonstracao_label_ip.setStyleSheet(self.cor_borda_style)

            self.tela_barramento_endereco.setText(f"Salto realizado para {novo_ip} ({motivo})")
            self.acesso_memoria("Leitura", f"{novo_ip}", "Opcode da próxima instrução", "(salto)")
            self.demonstracao_ip_inicial = int(novo_ip, 16)

        else:
            ip_atual = self.demonstracao_label_ip.text()
            self.tela_barramento_endereco.setText(f"Salto ignorado ({motivo}). Continua em {ip_atual}")
            try:
                self.demonstracao_ip_inicial = int(ip_atual, 16)
            except ValueError:
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

        self.demonstracao_ip_inicial = ip_retorno

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
        if novo_flag_numero & 0x0800: lista_flags.append("OF")
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

        self.tela_barramento_endereco.setText(f"IRET: Retornou CS:IP ({novo_cs:04X}:{novo_ip:04X}) e flags.")
        self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)

        self.acesso_memoria("Leitura (Stack)", f"{base_pilha:X}..{base_pilha + 5:X}", " Contexto restaurado", "(IP, CS, Flags)")
        self.demonstracao_ip_inicial = novo_ip

    # --------------------------------------------------------------- E/S
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

                registrador_label = self.pegar_demonstracao_label(registrador_nome)
                registrador_label.setText(valor_str)
                registrador_label.setStyleSheet(self.cor_borda_style)

                self.tela_barramento_dados.setText(f"← Dado recebido: {valor_str}")
                self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
                self.log_memoria.append(f"Hardware (IN): Porta {porta} enviou {valor_str} para {registrador_nome}")

                self.memoria_edicao_ef.setStyleSheet("")
                self.memoria_edicao_valor.setStyleSheet("")

                self.demonstracao_passo_interno = 0
                return True

            except ValueError:
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
        except Exception:
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

    # ------------------------------------------------------- execução
    def executar_passo_execucao(self):
        """Executa a operação. Retorna True se houve erro (divisão por zero ou overflow)."""
        registrador_dst_label = self.pegar_demonstracao_label(self.demonstracao_dst_str)
        registrador_src_label = self.pegar_demonstracao_label(self.demonstracao_src_str)

        operacao = self.demonstracao_operacao
        self.demonstracao_escritas_pendentes = []

        try:
            valor_dst = int(self.demonstracao_dados_dst)
        except (TypeError, ValueError):
            valor_dst = 0

        try:
            valor_src = int(self.demonstracao_dados_src)
        except (TypeError, ValueError):
            valor_src = 0

        dst_str = f"{valor_dst:04X}"
        src_str = f"{valor_src:04X}"

        if operacao == "MOV":
            self.tela_barramento_endereco.setText(f"Execução: Movendo {src_str} para {self.demonstracao_dst_str}")
            self.gravar_operando(self.demonstracao_dst_str, src_str)

        elif operacao == "XCHG":
            self.tela_barramento_endereco.setText(f"Execução: Trocando {self.demonstracao_dst_str} com {self.demonstracao_src_str}")
            self.gravar_operando(self.demonstracao_dst_str, src_str)
            self.gravar_operando(self.demonstracao_src_str, dst_str)

        elif operacao == "ADD":
            resultado_str = f"{(valor_dst + valor_src) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: {dst_str} + {src_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "SUB":
            resultado_str = f"{(valor_dst - valor_src) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: {dst_str} - {src_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "MUL":
            resultado_cheio = valor_dst * valor_src
            str_dx = f"{(resultado_cheio >> 16) & 0xFFFF:04X}"
            str_ax = f"{resultado_cheio & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: AX * {src_str} = {resultado_cheio:X}")
            self.gravar_operando("DX", str_dx)
            self.gravar_operando("AX", str_ax)

        elif operacao == "INC":
            resultado_str = f"{(valor_dst + 1) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: INC {dst_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "DEC":
            resultado_str = f"{(valor_dst - 1) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: DEC {dst_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "NEG":
            resultado_str = f"{(0 - valor_dst) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: NEG {dst_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "DIV":
            try:
                valor_ax = int(self.demonstracao_label_ax.text(), 16)
                valor_dx = int(self.demonstracao_label_dx.text(), 16)
            except ValueError:
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
            if quociente > 0xFFFF:
                self.tela_barramento_endereco.setText("Erro: Overflow na divisão (o quociente não cabe em AX)")
                self.tela_barramento_endereco.setStyleSheet("background-color: red; color: white; font-weight: bold;")
                return True
            str_ax = f"{quociente:04X}"
            str_dx = f"{resto:04X}"
            self.tela_barramento_endereco.setText(f"Execução: {dividendo:X} / {divisor:X} -> Quociente(AX): {str_ax}, Resto(DX): {str_dx}")
            self.gravar_operando("AX", str_ax)
            self.gravar_operando("DX", str_dx)

        elif operacao == "AND":
            resultado_str = f"{(valor_dst & valor_src) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: {dst_str} AND {src_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "OR":
            resultado_str = f"{(valor_dst | valor_src) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: {dst_str} OR {src_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "XOR":
            resultado_str = f"{(valor_dst ^ valor_src) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: {dst_str} XOR {src_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "NOT":
            resultado_str = f"{(~valor_dst) & 0xFFFF:04X}"
            self.tela_barramento_endereco.setText(f"Execução: NOT {dst_str} = {resultado_str}")
            self.gravar_operando(self.demonstracao_dst_str, resultado_str)

        elif operacao == "CMP":
            resultado_interno = valor_dst - valor_src
            flag_str = self.atualizar_flag(valor_dst, valor_src, "CMP")
            if resultado_interno == 0:
                status = "Iguais"
            elif valor_dst < valor_src:
                status = "Menor"
            else:
                status = "Maior"

            self.tela_barramento_endereco.setText(f"Execução: CMP {dst_str}, {src_str} -> {status}. Flags: {flag_str}")
            registrador_src_label.setStyleSheet(self.cor_borda_style)

        self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
        self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)

        registrador_dst_label.setStyleSheet(self.cor_borda_style)

        self.demonstracao_passo_interno = 0
        return False

    def Passo_Escrita(self, operando, valor):
        """Escreve 16 bits na memória apontada por DS:[SI] ou DS:[DI] (operando = '[SI]' ou '[DI]')."""
        registrador_offset_nome = operando.strip("[]")
        registrador_offset_label = self.pegar_demonstracao_label(registrador_offset_nome)
        byte_baixo = valor & 0xFF
        byte_alto = (valor >> 8) & 0xFF

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
            self.escrever_byte(self.demonstracao_endereco_calculado, byte_baixo)

            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(Byte Baixo)")

            self.demonstracao_passo_interno = 3
            return False

        elif self.demonstracao_passo_interno == 3:
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

            self.tela_barramento_endereco.setText(f"→ {calculo_str}")
            self.tela_barramento_endereco.setStyleSheet(self.barramento_ativo_style)
            self.tela_barramento_dados.setStyleSheet(self.barramento_inativo_style)
            self.demonstracao_passo_interno = 5
            return False

        elif self.demonstracao_passo_interno == 5:
            dado_str = f"{byte_alto:02X}"
            self.tela_barramento_endereco.setStyleSheet(self.barramento_inativo_style)
            self.tela_barramento_dados.setText(f"→ CPU envia o Byte alto: 0x{dado_str}")
            self.tela_barramento_dados.setStyleSheet(self.barramento_ativo_style)
            self.escrever_byte(self.demonstracao_endereco_calculado, byte_alto)

            self.acesso_memoria("Escrita", f"{self.demonstracao_endereco_calculado:X}", dado_str, "(Byte Alto)")

            self.demonstracao_passo_interno = 0
            return True
        return False

    # ------------------------------------------------------ interface
    def atualizar_interface(self, texto):
        self.dst_c.setEnabled(True)
        self.src_c.setEnabled(True)

        self.input_addr.setEnabled(False)
        self.input_addr.setStyleSheet("background-color: #EEE;")
        self.input_port.setEnabled(False)
        self.input_port.setStyleSheet("background-color: #EEE")

        if texto == "IN":
            self.src_c.setEnabled(False)
            self.input_port.setEnabled(True)
            self.input_port.setStyleSheet("background-color: white; border: 1px solid #444;")

        elif texto == "OUT":
            self.dst_c.setEnabled(False)
            self.input_port.setEnabled(True)
            self.input_port.setStyleSheet("background-color: white; border: 1px solid #444;")

        elif texto in ["PUSH", "MUL", "DIV"]:
            self.dst_c.setEnabled(False)

        elif texto in ["POP", "INC", "DEC", "NEG", "NOT"]:
            self.src_c.setEnabled(False)

        elif texto in self.lista_ADDR:
            self.dst_c.setEnabled(False)
            self.src_c.setEnabled(False)
            self.input_addr.setEnabled(True)
            self.input_addr.setStyleSheet("background-color: white; border: 1px solid #444")

        elif texto in ["RET", "IRET"]:
            self.dst_c.setEnabled(False)
            self.src_c.setEnabled(False)

    def salvar_configuracao(self):
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
        """Atualiza as flags (SF, ZF, OF, CF) para o resultado de valor_dst - valor_src (CMP)."""
        novo_flag = 0

        if operacao == "CMP":
            resultado_interno = valor_dst - valor_src
            resultado_bits = resultado_interno & 0xFFFF
            if valor_src > valor_dst:
                novo_flag |= 0x0001  # CF (empréstimo)
            if ((valor_dst ^ valor_src) & (valor_dst ^ resultado_bits)) & 0x8000:
                novo_flag |= 0x0800  # OF (estouro com sinal)
        else:
            resultado_bits = valor_dst & 0xFFFF

        if resultado_bits == 0:
            novo_flag |= 0x0040  # ZF

        if resultado_bits & 0x8000:
            novo_flag |= 0x0080  # SF (bit de sinal de 16 bits)

        lista_flag = []
        if novo_flag & 0x0080: lista_flag.append("SF")
        if novo_flag & 0x0040: lista_flag.append("ZF")
        if novo_flag & 0x0800: lista_flag.append("OF")
        if novo_flag & 0x0001: lista_flag.append("CF")

        texto_tela = " ".join(lista_flag) if lista_flag else "---"

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
        self.instrucao_atual = funcao
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


def _excecao_nao_tratada(tipo, valor, tb):
    """Evita que um erro inesperado derrube o programa (o PyQt5 aborta por padrão)."""
    sys.__excepthook__(tipo, valor, tb)
    QMessageBox.critical(None, "Erro inesperado", f"{tipo.__name__}: {valor}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    sys.excepthook = _excecao_nao_tratada
    ex = Interface()
    ex.show()
    sys.exit(app.exec_())
