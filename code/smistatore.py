class Smistatore:

    contatorePanni : int = 0

    def __init__(self, azienda : str):
        """
        Costruttore per la classe Smistatore, questa classe ha l'obiettivo di 
        modellare gli smistatori

        ## args: 
        - **azienda** : il nome dell'azienda a cui viene associato il buco
        """

        self.azienda = azienda


    @classmethod
    def incremento(self, incr : int = 1) -> None:
        """
        Questo metodo di classe viene evocato ogni volta che un panno passa 
        davanti al sensore, oppure l'utente clicca sul tasto '+' 

        ## args:
        - **incr** : valore da incrementare, di base 1
        """
        self.contatorePanni += incr


    @classmethod
    def decremento(self, decr : int = 1) -> None:
        """
        Questo metodo di classe viene evocato ogni volta che la conta va rimodellata
        per decrementare il contatore, di base decrementa di 1

        ## args: 
        - **incr** : valore da decrementare, di base 1
        """
        self.contatorePanni -= 1

    @classmethod
    def reset(self) -> None:
        """
        Questo metodo di classe viene evocato per ripristinare il contatore
        """
        self.contatorePanni = 0