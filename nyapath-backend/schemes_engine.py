import os
from pydantic import BaseModel, Field
from typing import List
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

class SchemeDetail(BaseModel):
    name: str = Field(description="Name of the incentive or scheme")
    benefit: str = Field(description="The primary benefit (e.g., '100% SGST refund for 10 years')")
    match_level: str = Field(description="'high', 'medium', or 'low' indicating how well the profile matches")
    tags: List[str] = Field(description="2-3 short tags (e.g., ['Tax', 'Zone D'])")
    eligibility_note: str = Field(description="Why this profile is eligible")

class SchemesOutput(BaseModel):
    schemes: List[SchemeDetail] = Field(description="List of applicable schemes")

def run_schemes_matcher(profile: dict):
    import rag_engine
    
    industry = profile.get("industry_type", "")
    district = profile.get("district", "")
    investment = profile.get("investment_scale_crores", 0)
    
    query = f"Incentives, subsidies, and schemes for {industry} industry in {district} Maharashtra, investment {investment} crores."
    context_text, _ = rag_engine.retrieve_context(query)
    
    llm = rag_engine.get_llm()
    parser = JsonOutputParser(pydantic_object=SchemesOutput)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert on Maharashtra industrial incentives (e.g., PSI 2019, IT Policy, Textile Policy). "
                   "Based on the user's project profile and context, suggest up to 3 applicable incentive schemes. "
                   "If no specific match exists, suggest general MSME or mega project schemes if investment allows.\n\n"
                   "Context: {context}\n\n"
                   "Return ONLY valid JSON matching the schema.\n\n{format_instructions}"),
        ("human", "Profile: {profile}")
    ])
    
    chain = prompt | llm | parser
    
    try:
        result = chain.invoke({
            "context": context_text,
            "profile": str(profile),
            "format_instructions": parser.get_format_instructions()
        })
        return result
    except Exception as e:
        print(f"Schemes matching failed: {e}")
        return {"schemes": []}
