from enum import Enum


class PerfilDeAcesso(Enum):
    # GARAGEM E RECEPÇÃO
    A_B_C = "INICIAIS (A - B - C) - GARAGEM E RECEPÇÃO"
    D_E_F_G = "INICIAIS (D - E - F - G) - GARAGEM E RECEPÇÃO"
    H_I_J_K = "INICIAIS (H - I - J - K) - GARAGEM E RECEPÇÃO"
    L_M = "INICIAIS (L - M) - GARAGEM E RECEPÇÃO"
    N_O_P_Q_R = "INICIAIS (N - O - P - Q - R) - GARAGEM E RECEPÇÃO"
    S_T_U_V_W_X_Y_Z = "INICIAIS (S - T - U - V - W - X - Y - Z) - GARAGEM E RECEPÇÃO"

    # RECEPÇÃO
    # A_B_C = "INICIAIS (A - B - C) - RECEPÇÃO"
    # D_E_F_G = "INICIAIS (D - E - F - G) - RECEPÇÃO"
    # H_I_J_K = "INICIAIS(H - I - J - K) - RECEPÇÃO"
    # L_M = "INICIAIS (L - M) - RECEPÇÃO"
    # N_O_P_Q_R = "INICIAIS  (N - O - P - Q - R) - RECEPÇÃO"
    # S_T_U_V_W_X_Y_Z = "INICIAIS (S - T - U - V - W - X - Y - Z) - RECEPÇÃO"


def descobrir_perfil(letra):
    """Retorna o valor do Enum correto baseado na letra e no acesso à garagem."""
    letra = letra.upper()

    if letra in "ABC":
        return PerfilDeAcesso.A_B_C.value  # if tem_garagem else PerfilDeAcesso.A_B_C_REC.value
    elif letra in "DEFG":
        return PerfilDeAcesso.D_E_F_G.value  # if tem_garagem else PerfilDeAcesso.D_E_F_G_REC.value
    elif letra in "HIJK":
        return PerfilDeAcesso.H_I_J_K.value  # if tem_garagem else PerfilDeAcesso.H_I_J_K_REC.value
    elif letra in "LM":
        return PerfilDeAcesso.L_M.value  # if tem_garagem else PerfilDeAcesso.L_M_REC.value
    elif letra in "NOPQR":
        return PerfilDeAcesso.N_O_P_Q_R.value  # if tem_garagem else PerfilDeAcesso.N_O_P_Q_R_REC.value
    elif letra in "STUVWXYZ":
        return PerfilDeAcesso.S_T_U_V_W_X_Y_Z.value  # if tem_garagem else PerfilDeAcesso.S_T_U_V_W_X_Y_Z_REC.value
    else:
        # Fallback de segurança caso comecem com números ou símbolos
        return PerfilDeAcesso.A_B_C.value
