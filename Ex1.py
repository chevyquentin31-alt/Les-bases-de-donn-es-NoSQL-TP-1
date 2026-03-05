from pymongo import MongoClient

dns = "mongodb+srv://etoily:VzFtdG1CfaXZQdsv@cluster0.litqpm3.mongodb.net/?appName=Cluster0"
client = MongoClient(dns, ssl=True)
db = client.ecommerce

db.users.drop()
db.products.drop()
db.orders.drop()

db.users.insert_many([
    {"nom": "Alice Dupont", "age": 25, "ville": "Paris"},
    {"nom": "Bob Martin", "age": 32, "ville": "Lyon"},
    {"nom": "Claire Morel", "age": 28, "ville": "Paris"}
])

db.products.insert_many([
    {"nom": "Clavier mécanique", "prix": 89.99, "categorie": "Informatique"},
    {"nom": "Souris sans fil", "prix": 45.50, "categorie": "Informatique"},
    {"nom": "Casque audio", "prix": 120.00, "categorie": "Audio"},
    {"nom": "Câble USB-C", "prix": 12.99, "categorie": "Accessoires"}
])

db.orders.insert_one({
    "utilisateur": "Alice Dupont",
    "produits": ["Clavier mécanique", "Câble USB-C"],
    "total": 102.98
})

print("Tous les utilisateurs :")
for u in db.users.find(): print(u)

print("\nProduits > 50€ :")
for p in db.products.find({"prix": {"$gt": 50}}): print(p)

print("\nUtilisateurs à Paris :")
for u in db.users.find({"ville": "Paris"}): print(u)

print("\nToutes les commandes :")
for o in db.orders.find(): print(o)

db.users.update_one({"nom": "Bob Martin"}, {"$set": {"age": 33}})
print("\nBob Martin mis à jour")

db.products.delete_one({"nom": "Câble USB-C"})
print("Câble USB-C supprimé")