from pymongo import MongoClient

dns = "mongodb+srv://etoily:VzFtdG1CfaXZQdsv@cluster0.litqpm3.mongodb.net/?appName=Cluster0"
client = MongoClient(dns, ssl=True)
db = client.social_app

# Nettoyage
db.users.drop()
db.publications.drop()

# Utilisateurs
users = db.users.insert_many([
    {"nom": "Alice Dupont", "email": "alice@mail.com", "age": 25, "ville": "Paris"},
    {"nom": "Bob Martin", "email": "bob@mail.com", "age": 32, "ville": "Lyon"},
    {"nom": "Claire Morel", "email": "claire@mail.com", "age": 28, "ville": "Marseille"}
])
alice_id, bob_id, claire_id = users.inserted_ids

# Publications
db.publications.insert_many([
    {"auteur": "Alice Dupont", "auteur_id": alice_id, "contenu": "Mon premier post !", "date": "2026-03-01", "commentaires": [], "likes": ["Bob Martin", "Claire Morel"]},
    {"auteur": "Alice Dupont", "auteur_id": alice_id, "contenu": "Paris sous la neige", "date": "2026-03-02", "commentaires": [], "likes": ["Bob Martin"]},
    {"auteur": "Bob Martin", "auteur_id": bob_id, "contenu": "Un foot ce weekend ?", "date": "2026-03-02", "commentaires": [], "likes": ["Alice Dupont", "Claire Morel", "Bob Martin"]},
    {"auteur": "Claire Morel", "auteur_id": claire_id, "contenu": "Cool !", "date": "2026-03-03", "commentaires": [], "likes": []},
    {"auteur": "Bob Martin", "auteur_id": bob_id, "contenu": "Nouvel article sur mon blog", "date": "2026-03-04", "commentaires": [], "likes": ["Alice Dupont"]}
])

# Commentaires
db.publications.update_one({"contenu": "Mon premier post !"}, {"$push": {"commentaires": {"auteur": "Bob Martin", "texte": "Bienvenue !", "date": "2026-03-01"}}})
db.publications.update_one({"contenu": "Mon premier post !"}, {"$push": {"commentaires": {"auteur": "Claire Morel", "texte": "Contente de te voir ici", "date": "2026-03-01"}}})
db.publications.update_one({"contenu": "Un foot ce weekend ?"}, {"$push": {"commentaires": {"auteur": "Alice Dupont", "texte": "Dispo dimanche", "date": "2026-03-03"}}})

# Like en plus
db.publications.update_one({"contenu": "Cool !"}, {"$push": {"likes": "Alice Dupont"}})

# --- Requêtes ---

print("Toutes les publications :")
for p in db.publications.find():
    print(f"  {p['auteur']}: {p['contenu']} ({len(p['likes'])} likes)")

print("\nPublications d'Alice :")
for p in db.publications.find({"auteur": "Alice Dupont"}):
    print(f"  {p['contenu']}")

print("\nCommentaires du premier post :")
post = db.publications.find_one({"contenu": "Mon premier post !"})
for c in post["commentaires"]:
    print(f"  {c['auteur']}: {c['texte']}")

print("\nPost avec le plus de likes :")
top = list(db.publications.aggregate([{"$addFields": {"nb_likes": {"$size": "$likes"}}}, {"$sort": {"nb_likes": -1}}, {"$limit": 1}]))
print(f"  {top[0]['auteur']}: {top[0]['contenu']} ({top[0]['nb_likes']} likes)")

print("\nNombre de posts par utilisateur :")
for r in db.publications.aggregate([{"$group": {"_id": "$auteur", "nb": {"$sum": 1}}}]):
    print(f"  {r['_id']}: {r['nb']}")