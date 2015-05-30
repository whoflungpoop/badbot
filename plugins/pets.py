import time


def pets_init_db(db=None):
    db.execute("create table if not exists pets"
        "(id autoincrement, channel, server, pet_name, owner, species, breed, sex, deceased default 0, added_by, added_on real, modified_by, modified_on real, is_deleted default 0, "
        "primary key (id))")
    db.execute("create table if not exists pets_pics"
        "(id autoincrement, pet_id, added_by, url, is_deleted default 0, "
        "primary key (id),"
        "foreign key(pet_id) references pets(id))"


@hook.singlethread
def pets_crond(db=None):
    pets_init_db(db)


@hook.command
def pets(inp, nick='', chan='', server='', db=None):
    inputs = inp.split(" ")
    user = inputs[0].lower()
    pet_name = inputs[1].lower()
    result = db.execute("select pets.pet_name, pets.owner, pets.species, pets.breed, pets.sex, pets_pics.url "
        "from pets join pets_pics on pets_pics.pet_id = pets.id "
        "where pets.owner = ? and pets.pet_name = ?", (user, pet_name))


@hook.command
def pets_add(inp, nick='', chan='', server='', db=None, autohelp=True):
    """.pets_add pet_name,dog_or_cat_or_bird,breed_of_animal,m_or_f"""
    inputs = inp.split(",")
    for i in inputs:
        i.trim()

    pet_name = inputs[0].title()
    species = inputs[1].title()
    breed = inputs[2].title()
    sex = inputs[3].upper()

    db.execute("insert into pets(channel, server, pet_name, owner, species, breed, sex, added_by, added_on, is_deleted)" 
        "(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (chan, server, pet_name, owner, species, breed, sex, nick, time.time(), 0))


@hook.command
def pets_update(inp, nick='', db=None, autohelp=True):
    """.pets_update pet_id,pet_name,dog_or_cat_or_bird,breed_of_animal,m_or_f"""
    inputs = inp.split(",")
    for i in inputs:
        i.trim()

    pet_id = int(inputs[0])
    pet_name = inputs[1].title()
    species = inputs[2].title()
    breed = inputs[3].title()
    sex = inputs[4].upper()

    db.execute("update pets set pet_name = ?, owner = ?, species = ?, breed = ?, sex = ?, modified_by = ?, modified_on = ? where id = ?",
        (pet_name, owner, species, breed, sex, nick, time.time())


@hook.command
def pets_add_pic(inp, nick='', db=None, autohelp=True):
    """.pets_add_pic pet_id,url or .pets_add_pic username,pet_name,url"""
    inputs = inp.split(",")
    for i in inputs:
        i.trim()

    pet_id = -1
    if len(inputs) == 2:
        pet_id = int(inputs[0])
        
    elif len(inputs) == 3:
        result = db.execute("select id from pets where lower(owner) = ? and lower(pet_name) = ?",
            (inputs[0].lower(), inputs[1].lower())).fetchone()
        if result:
            pet_id = result[0]
        else:
            return u"Couldn't find that pet in the database!"

    if pet_id != -1:
        db.execute("insert into pets_pics(pet_id, added_by, url, is_deleted) "
            "values(?, ?, ?, ?)", (pet_id, nick, inputs[1], 0))
    else:
        return u"Something got messed up and couldn't insert picture into database. Perhaps that pet id doesn't exist."