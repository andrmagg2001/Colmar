import sqlite3

#comando per stampare quantità:
#SELECT prodotti.prodotto, SUM(relazione.quantità) FROM clienti,prodotti,relazione WHERE clienti.cliente = 'Colmar' AND relazione.idCliente = clienti.id AND relazione.idProdotto = prodotti.id GROUP BY prodotti.prodotto;

conn = sqlite3.connect('database.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS clienti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS prodotti (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prodotto TEXT
)
''')

cur.execute('''
CREATE TABLE IF NOT EXISTS relazione (
    idCliente INTEGER,
    idProdotto INTEGER,
    quantità INTEGER,
    data TEXT DEFAULT (date('now'))           
)
''')


conn.commit()
conn.close()