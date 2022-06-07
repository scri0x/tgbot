import sqlite3

def college(idk, lang):
    conn = sqlite3.connect('databases/bachelor.db')
    cur = conn.cursor()

    cur.execute(
        f"SELECT groups.nomer, groups.name_{lang} FROM groups JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_groups = cur.fetchall()
    cur.execute(
        f"SELECT spec.group_nomer, spec.name_{lang}, spec.college_subject_{lang} FROM spec JOIN groups ON spec.group_nomer = groups.nomer JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_spec = cur.fetchall()
    text = ''
    for group in data_groups:
        group = list(group)
        text = text + f"<{group[1]}>\n"
        for spec in data_spec:
            spec = list(spec)
            if spec[0] == group[0]:
                text = text + f"-{spec[1]}-\n{spec[2]}\n\n"# подумай
    conn.close()
    return text


def get_lang(user_id):
    conn = sqlite3.connect('databases/users.db')
    cur = conn.cursor()

    cur.execute(f"SELECT user.lang FROM user WHERE user_id = {user_id};")
    data = cur.fetchall()
    conn.close()
    return data[0][0]


def update_lang(user_id,lang):
    conn = sqlite3.connect('databases/users.db')
    cur = conn.cursor()

    cur.execute(f"UPDATE user SET lang = '{lang}' WHERE user_id = {user_id};")
    conn.commit()


def insert_users(user_id, lang):
    conn = sqlite3.connect('databases/users.db')
    cur = conn.cursor()

    cur.execute(f"INSERT INTO user (user_id, lang) VALUES ({user_id},'{lang}')")
    conn.commit()

    conn.close()


def discount_drom_bd(percent, lang):
    conn = sqlite3.connect('databases/discount.db')
    cur = conn.cursor()
    cur.execute(f"SELECT data_{lang} FROM discount WHERE percent = '{percent}'")
    datas = cur.fetchall()

    match lang:
        case "kz":
            text = f"{percent} жеңілдік:\n"
        case "ru":
            text = f"{percent} скидка:\n"

    for index, data in enumerate(datas):
        text = text + f"{index + 1}){data[0]}\n\n"

    conn.close()
    return text


def magistracy(idk, lang):
    conn = sqlite3.connect('databases/magistracy.db')
    cur = conn.cursor()

    cur.execute(
        f"SELECT groups.nomer, groups.name_{lang} FROM groups JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_groups = cur.fetchall()
    cur.execute(
        f"SELECT spec.group_nomer, spec.name_{lang} FROM spec JOIN groups ON spec.group_nomer = groups.nomer JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_spec = cur.fetchall()
    text = ''
    for group in data_groups:
        group = list(group)
        text = text + f"<{group[1]}>\n"
        for spec in data_spec:
            spec = list(spec)
            if spec[0] == group[0]:
                text = text + "-" + spec[1] + "-\n"  # подумай
        text = text + '\n'
    conn.close()
    return text


def doctoranture(idk, lang):
    conn = sqlite3.connect('databases/doctoral.db')
    cur = conn.cursor()

    cur.execute(
        f"SELECT groups.nomer, groups.name_{lang} FROM groups JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_groups = cur.fetchall()
    cur.execute(
        f"SELECT spec.group_nomer, spec.name_{lang} FROM spec JOIN groups ON spec.group_nomer = groups.nomer JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_spec = cur.fetchall()
    text = ''
    for group in data_groups:
        group = list(group)
        text = text + f"<{group[1]}>\n"
        for spec in data_spec:
            spec = list(spec)
            if spec[0] == group[0]:
                text = text + "-" + spec[1] + "-\n"  # подумай
        text = text + '\n'
    conn.close()
    return text

def price(subject, lang):
    conn = sqlite3.connect('databases/bachelor.db')
    cur = conn.cursor()

    cur.execute(
        f"SELECT spec.nomer, spec.name_{lang}, all_prices.price FROM spec JOIN all_prices ON spec.nomer = all_prices.spec_nomer JOIN groups ON spec.group_nomer = groups.nomer WHERE groups.subject_{lang} = '{subject}';")
    data = cur.fetchall()
    text = f"{subject}\n"
    for spec in data:
        text = text + f"({spec[0]}) {spec[1]}: {spec[2]}\n\n"

    conn.close()
    return text

def subject_ball_from_bd(subject, year, lang):
    conn = sqlite3.connect('databases/bachelor.db')
    cur = conn.cursor()

    cur.execute(
        f"SELECT groups.nomer, groups.name_{lang}, year_{year}.grant, year_{year}.jk, year_{year}.ak FROM groups JOIN year_{year} ON groups.nomer = year_{year}.group_nomer WHERE groups.subject_{lang} = '{subject}' ORDER BY groups.nomer ASC;")
    data_groups = cur.fetchall()
    cur.execute(
        f"SELECT spec.group_nomer, spec.name_{lang} FROM spec JOIN groups ON groups.nomer = spec.group_nomer WHERE subject_{lang} = '{subject}' ORDER BY spec.group_nomer ASC;")
    data_spec = cur.fetchall()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name > 'year_';")
    tables = cur.fetchall()
    text = ''
    for group in data_groups:
        group = list(group)
        text = text + f"<{group[1]}>\n"
        for spec in data_spec:
            spec = list(spec)
            if spec[0] == group[0]:
                text = text + "-" + spec[1] + "-\n"  # подумай
        text = text + f"Бакалавриатқа бөлінген грант саны:{group[2]}\nЖалпы конкурс бойынша грантқа түскен минималды балл:{group[3]}\nАуылдық квотамен грантқа түскен минималды балл:{group[4]}\n\n"
    conn.close()

    return text, tables
    return text, tables


def discount_drom_bd(percent, lang):
    conn = sqlite3.connect('databases/discount.db')
    cur = conn.cursor()
    cur.execute(f"SELECT data_{lang} FROM discount WHERE percent = '{percent}'")
    datas = cur.fetchall()

    match lang:
        case "kz":
            text = f"{percent} жеңілдік:\n"
        case "ru":
            text = f"{percent} скидка:\n"

    for index, data in enumerate(datas):
        text = text + f"{index + 1}){data[0]}\n\n"

    conn.close()
    return text

def magistracy(idk, lang):
    conn = sqlite3.connect('databases/magistracy.db')
    cur = conn.cursor()

    cur.execute(
        f"SELECT groups.nomer, groups.name_{lang} FROM groups JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_groups = cur.fetchall()
    cur.execute(
        f"SELECT spec.group_nomer, spec.name_{lang} FROM spec JOIN groups ON spec.group_nomer = groups.nomer JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_spec = cur.fetchall()
    text = ''
    for group in data_groups:
        group = list(group)
        text = text + f"<{group[1]}>\n"
        for spec in data_spec:
            spec = list(spec)
            if spec[0] == group[0]:
                text = text + "-" + spec[1] + "-\n"  # подумай
        text = text + '\n'
    conn.close()
    return text

def doctoranture(idk, lang):
    conn = sqlite3.connect('databases/doctoral.db')
    cur = conn.cursor()

    cur.execute(
        f"SELECT groups.nomer, groups.name_{lang} FROM groups JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_groups = cur.fetchall()
    cur.execute(
        f"SELECT spec.group_nomer, spec.name_{lang} FROM spec JOIN groups ON spec.group_nomer = groups.nomer JOIN areas ON groups.area_nomer = areas.nomer JOIN idk ON areas.idk_nomer = idk.nomer WHERE idk.name_{lang} = '{idk}';")
    data_spec = cur.fetchall()
    text = ''
    for group in data_groups:
        group = list(group)
        text = text + f"<{group[1]}>\n"
        for spec in data_spec:
            spec = list(spec)
            if spec[0] == group[0]:
                text = text + "-" + spec[1] + "-\n"  # подумай
        text = text + '\n'
    conn.close()
    return text


def delete_user(user_id):
    conn = sqlite3.connect('databases/users.db')
    cur = conn.cursor()

    cur.execute(
        f"DELETE FROM user WHERE user_id = {user_id}"
    )
    conn.commit()
    conn.close()
