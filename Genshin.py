from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

dns = "mongodb+srv://etoily:VzFtdG1CfaXZQdsv@cluster0.litqpm3.mongodb.net/?appName=Cluster0"
client = MongoClient(dns, ssl=True)
db = client.genshin_db
collection = db.characters

def serialize(doc):
    doc["_id"] = str(doc["_id"])
    return doc

@app.route("/items", methods=["POST"])
def create_item():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({"message": "Personnage ajouté", "id": str(result.inserted_id)}), 201

@app.route("/items", methods=["GET"])
def get_items():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    skip = (page - 1) * limit
    items = list(collection.find().skip(skip).limit(limit))
    return jsonify({"page": page, "total": collection.count_documents({}), "results": [serialize(i) for i in items]})

@app.route("/items/<id>", methods=["GET"])
def get_item(id):
    doc = collection.find_one({"_id": ObjectId(id)})
    if not doc:
        return jsonify({"error": "Non trouvé"}), 404
    return jsonify(serialize(doc))

@app.route("/search", methods=["GET"])
def search():
    keyword = request.args.get("keyword", "")
    element = request.args.get("element")
    rarete = request.args.get("rarete", type=int)
    query = {}
    if keyword:
        query["$or"] = [
            {"nom": {"$regex": keyword, "$options": "i"}},
            {"description": {"$regex": keyword, "$options": "i"}}
        ]
    if element:
        query["element"] = {"$regex": element, "$options": "i"}
    if rarete:
        query["rarete"] = rarete
    results = list(collection.find(query))
    return jsonify({"count": len(results), "results": [serialize(r) for r in results]})

if __name__ == "__main__":
    if collection.count_documents({}) == 0:
        collection.insert_many([
            {"nom": "Hu Tao", "element": "Pyro", "arme": "Lance", "rarete": 5, "description": "Directrice du Wangsheng Funeral Parlor"},
            {"nom": "Xiangling", "element": "Pyro", "arme": "Lance", "rarete": 4, "description": "Jeune chef cuisinière de Liyue"},
            {"nom": "Furina", "element": "Hydro", "arme": "Épée", "rarete": 5, "description": "Ancienne Archon Hydro de Fontaine"},
            {"nom": "Kazuha", "element": "Anemo", "arme": "Épée", "rarete": 5, "description": "Samouraï errant d'Inazuma"},
            {"nom": "Fischl", "element": "Electro", "arme": "Arc", "rarete": 4, "description": "Investigatrice de l'Adventurers Guild"}
        ])
    app.run(debug=True)