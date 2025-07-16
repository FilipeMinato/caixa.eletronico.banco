# Projeto 35 - Simulador de Caixa Eletrônico
# Este programa simula um caixa eletrônico.
# O usuário informa o valor desejado para saque e o programa calcula as cédulas necessárias.
# Também simula senha, reconhecimento facial e espera animada usando Tkinter.

import tkinter as tk
from tkinter import simpledialog, messagebox
import time  # Apenas se desejar usar pausas com time.sleep (não essencial aqui)

# =========================
# Função para cálculo das cédulas
# =========================
def calcular_cedulas(valor):
    """
    Calcula a quantidade de cédulas necessárias para o valor informado.
    Usa cédulas de 100, 50, 20, 10 e 5 reais.
    Retorna um dicionário com as cédulas e suas quantidades.
    Se sobrar valor que não pode ser sacado com as cédulas, retorna None.
    """
    cedulas = [100, 50, 20, 10, 5]
    resultado = {}  # Dicionário com cédulas e quantidades
    saldo = valor   # Valor restante a ser quebrado em notas

    for c in cedulas:
        qtd = saldo // c  # Quantas notas cabem dessa cédula
        if qtd > 0:
            resultado[c] = qtd
            saldo %= c     # Atualiza saldo restante

    if saldo != 0:
        return None  # Não foi possível formar o valor com as cédulas disponíveis
    return resultado

# =========================
# Função principal do saque
# =========================
def novo_saque():
    """
    Controla toda a lógica de um novo saque:
    - Pergunta o valor
    - Verifica se o valor é válido
    - Solicita senha de 6 dígitos
    - Simula reconhecimento facial
    - Mostra resultado com as cédulas usadas
    """
    try:
        # Pede valor ao usuário
        valor = simpledialog.askinteger("Valor do Saque", "Digite o valor do saque (mínimo R$10):")
        if valor is None:  # Usuário clicou em Cancelar
            return

        if valor < 10:
            messagebox.showwarning("Valor Inválido", "O valor mínimo para saque é R$10.")
            return

        # Calcula as cédulas
        resultado = calcular_cedulas(valor)
        if resultado is None:
            messagebox.showinfo("Atenção", "Para valores quebrados, entre na agência e saque com o operador.")
            return

        # Solicita senha
        senha = simpledialog.askstring("Senha", "Digite sua senha de 6 dígitos:", show="*")
        if senha is None or len(senha) != 6 or not senha.isdigit():
            messagebox.showerror("Erro", "Senha inválida. Tente novamente.")
            return

        # Simula reconhecimento facial com pergunta de confirmação
        facial = messagebox.askyesno("Reconhecimento Facial", "Realizando reconhecimento facial. \nClique 'Sim' para continuar.")
        if not facial:
            messagebox.showinfo("Erro", "Reconhecimento facial falhou. Tente novamente.")
            return

        # Cria janela de "aguarde"
        aguarde = tk.Toplevel(root)
        aguarde.title("Processando")
        tk.Label(
            aguarde,
            text="Aguarde enquanto seu dinheiro é liberado...",
            font=("Arial", 12)
        ).pack(padx=20, pady=20)

        root.update()  # Atualiza a interface antes do atraso
        root.after(2500, aguarde.destroy)  # Fecha a janela após 2.5 segundos

        # Mostra o resultado após tempo de processamento
        def mostrar_final():
            # Monta a mensagem com as cédulas utilizadas
            cedulas_msg = "\n".join([
                f"{qtd} nota(s) de R$ {valor}"
                for valor, qtd in sorted(resultado.items(), reverse=True)
            ])
            messagebox.showinfo(
                "Transação Finalizada",
                f"Saque de R$ {valor} realizado com sucesso!\n\n{cedulas_msg}"
            )

        # Agenda exibição final para após 2.6 segundos
        root.after(2600, mostrar_final)

    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")

# =========================
# Interface Gráfica com Tkinter
# =========================
root = tk.Tk()  # Cria a janela principal
root.title("Simulador de Caixa Eletrônico")

# Título do app
tk.Label(
    root,
    text="=== SIMULADOR DE CAIXA ELETRÔNICO ===",
    font=("Arial", 14, "bold")
).pack(pady=10)

# Informações sobre as notas disponíveis
tk.Label(
    root,
    text="Notas disponíveis: R$100, R$50, R$20, R$10 e R$5",
    font=("Arial", 12)
).pack()

# Informações adicionais
tk.Label(
    root,
    text="Saque mínimo: R$10\nPara valores quebrados, dirija-se à agência.",
    font=("Arial", 10)
).pack(pady=10)

# Botão para iniciar novo saque
tk.Button(
    root,
    text="Novo Saque",
    font=("Arial", 12),
    width=20,
    command=novo_saque
).pack(pady=20)

# Inicia o loop principal da interface
root.mainloop()
