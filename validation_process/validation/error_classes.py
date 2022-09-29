# tutti gli errori hanno:
# - una proprietà che ne specifica il tipo (oc-format-compliance, syntactic, semantic)
# - delle  proprietà che equivalgono ai messaggi da mandare a schermo; questi includono la spiegazione dell'errore,
# la posizione dell'errore, e l'azione consigliata per correggere l'errore


class Error:
    def __init__(self, errtype, position, message):
        self.errtype = errtype
        self.position = position
        self.message = message

