import sqlite3

conn = sqlite3.connect('polymath.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()


def createTableIfNecesary():
    cursor.execute('''CREATE TABLE IF NOT EXISTS categories
                 (id INTEGER,
                  parent_id INTEGER,
                  level INTEGER,
                  name TEXT,
                  auto_pay_enabled INTEGER,
                  best_offer_enabled INTEGER,
                  b2b_enabled INTEGER,
                  expired INTEGER,
                  leaf_category INTEGER,
                  LSD INTEGER,
                  ORPA INTEGER,
                  ORRA INTEGER,
                  virtual INTEGER)''')
    conn.commit()


def insertList(categoriesList):
    cursor.executemany(
        '''INSERT INTO categories 
                (id,
                parent_id,
                level,
                name,
                auto_pay_enabled,
                best_offer_enabled,
                b2b_enabled,
                expired,
                leaf_category,
                LSD,
                ORPA,
                ORRA,
                virtual) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        categoriesList)
    conn.commit()


def getAll():
    cursor.execute('SELECT * FROM categories')
    return cursor.fetchall()


def getWithChildren(id):
    cursor.execute('''
        with recursive
        descendants as
          ( select id, parent_id, 1 as level_c
            from categories
          union all
            select d.parent_id, c.id, d.level_c + 1
            from descendants as d
              join categories c on d.id = c.parent_id
          where c.id = ?
          ) 
        select *
        from descendants 
        order by parent_id, level_c ;
    ''', [id])
    return cursor.fetchall()


def closeConn():
    conn.close()
