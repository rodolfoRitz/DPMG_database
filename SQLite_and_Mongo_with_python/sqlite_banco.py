import sqlite3

try:
    # Represents the connection to the on-disk database.
    con = sqlite3.connect("tutorial.db")

    # Fetch results from SQL queriesusing a database cursor. 
    cursor = con.cursor()

    # Execute statements like "CREATE TABLE", by calling:
    cursor.execute("CREATE TABLE if not exists caracters(name, race, powerscore)")
    cursor.execute("""INSERT INTO caracters VALUES
                  ('Orc', 'Axeblade', 8.2),
                  ('Elf', 'Legolas', 7.5)""")

    # Execute "executemany" statement to insert three or more rows.
    # data = [
    #     ("Monty Python Live at the Hollywood Bowl", 1982, 7.9),
    #     ("Monty Python's The Meaning of Life", 1983, 7.5),
    #     ("Monty Python's Life of Brian", 1979, 8.0),
    # ]
    # cursor.executemany("INSERT INTO movie VALUES(?, ?, ?)", data)
    # con.commit()  # Remember to commit the transaction after executing INSERT.

    # Assign the result to "res", and call res.fetchone() to fetch the resulting row:
    res = cursor.execute("SELECT name FROM sqlite_master")

    # Atribuindo todos os resultados na variavel.
    res = cursor.fetchall()
    print(res)

    # Atribuindo um resultado na variavel.
    res = cursor.fetchone()
    print(res)

    # Iterando diretamente sobre o cursor
    for row in cursor.execute("SELECT name, race, powerscore FROM caracters"):
        print(f'Dentro do row: {row}')

except sqlite3.Error as e:
    print(f"Erro ao acessar o banco de dados: {e}")
# finally:
#     if con:
#  Closing connection.
#         con.close()
