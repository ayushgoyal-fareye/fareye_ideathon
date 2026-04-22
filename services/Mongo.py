from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from pydantic import BaseModel,HttpUrl
from typing import List,Dict
import numpy as np
from datetime import datetime
class MongoData(BaseModel):
    jira_id:str
    problem:str
    prob_emb:List[float]
    Screenshots:Dict[str,str]
    RCA:str
    solution:str
    assignee:str
    clientId:str
    updatedDate: datetime

class MongoDBManager:
    def __init__(self, host="localhost", port=27017, db_name="support_db"):
        """Initializes the connection to the Docker MongoDB instance."""
        try:
            self.client = MongoClient(f"mongodb://{host}:{port}/", serverSelectionTimeoutMS=5000)
            # Trigger a call to verify connection is alive
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.collection = self.db["TICKETS"]
            print("Successfully connected to MongoDB.")
        except ConnectionFailure:
            print("Could not connect to MongoDB. Is your Docker container running?")
            raise

    def insert_incident(self, data: MongoData) -> bool:
        """
        Takes a MongoData Pydantic model and inserts it into the database.
        Returns True on success, False otherwise.
        """
        try:
            # .model_dump() converts the Pydantic model into a Python Dictionary
            # which is the format PyMongo requires.
            document = data.model_dump()
            
            # Since JSON/MongoDB keys must be strings, Pydantic handles the 
            # conversion of HttpUrl objects inside the dictionary automatically.
            result = self.collection.insert_one(document)
            
            print(f"Data inserted successfully with ID: {result.inserted_id}")
            return True
        except PyMongoError as e:
            print(f"Database error occurred: {e}")
            return False

    def close_connection(self):
        """Properly close the client connection."""
        self.client.close()
    def find_similar_problems(self, query_embedding: List[float], top_k: int = 3):
   
        try:
            # 1. Fetch tickets (limiting fields to save memory)
            all_tickets = list(self.collection.find({}, {

                "jira_id": 1, "prob_emb": 1, "problem": 1, "solution": 1, "RCA": 1,"assignee":1,"updatedDate":1,"client_id":1
            }))
            
            if not all_tickets:
                return []

            query_vec = np.array(query_embedding)
            results = []

            # 2. Calculate similarity for every ticket
            for ticket in all_tickets:
                ticket_vec = np.array(ticket.pop("prob_emb"))
                
                # Cosine Similarity calculation
                norm_product = np.linalg.norm(query_vec) * np.linalg.norm(ticket_vec)
                similarity = np.dot(query_vec, ticket_vec) / norm_product if norm_product != 0 else 0
                
                # Store the ticket data along with its score
                results.append({
                    "ticket": ticket,
                    "score": round(float(similarity) * 100, 2)
                })

            
            results.sort(key=lambda x: x["score"], reverse=True)
            
            return results[:top_k]

        except Exception as e:
            print(f"Search failed: {e}")
            return []