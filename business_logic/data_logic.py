from pydantic import BaseModel,HttpUrl
from typing import List,Dict
from tools.RAG import RAG
from tools.Image import ImageComparator
from services.Mongo import MongoDBManager
from tools.claude import TicketResolver
class Data(BaseModel):
    problem:str
    Screenshots:List[str]
    RCA:str
    solution:str

class MongoData(BaseModel):
    problem:str
    prob_emb:List[float]
    Screenshots:Dict[str,str]
    RCA:str
    solution:str

class Query(BaseModel):
    problem:str
    Screenshots:List[str]
class Data_Logic:

    def __init__(self):
        self.RAGTool:RAG=RAG()
        self.ImageTool:ImageComparator=ImageComparator()
        self.mongodb:MongoDBManager=MongoDBManager()
        self.ticketsol:TicketResolver=TicketResolver()
    def add_data(self,data:Data):

        try:
            Prob_emb=self.RAGTool.create_text_embedding(data.problem)
            
            my_dict={}
            for i in data.Screenshots:
                hash=self.ImageTool.get_phash(i)
                if(str(hash)=="error"):
                    raise Exception("something broke")
                my_dict[str(i)]=str(hash)
            mydata = MongoData(
            problem=data.problem,
            prob_emb=Prob_emb,
            Screenshots=my_dict,
            RCA=data.RCA,
            solution=data.solution
            )
            
            return self.mongodb.insert_incident(mydata);
        
        except Exception as e:
            print(e)
            return False;
    # def search_results(self,query:Query):

    #     prob_emb=self.RAGTool.create_text_embedding(query.problem)
    #     tickets=self.mongodb.find_similar_problems(prob_emb,2)

        
    #     return self.ticketsol.get_solution(query.problem,tickets)
    def search_results(self,query:str):

        prob_emb=self.RAGTool.create_text_embedding(query)
        tickets=self.mongodb.find_similar_problems(prob_emb,2)

        
        return self.ticketsol.get_solution(query,tickets)
        

     
        


