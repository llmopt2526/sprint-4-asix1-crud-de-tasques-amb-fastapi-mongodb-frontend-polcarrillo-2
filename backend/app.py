import os
from typing import Optional, List
from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import AsyncMongoClient
from pymongo import ReturnDocument

# --- Inicialització ---
app = FastAPI(
    title="Gestor de Llibres API",
    summary="API per gestionar una col·lecció de llibres amb FastAPI i MongoDB"
)

# --- Configuració de la connexió amb MongoDB ---
# Es requereix la variable d'entorn MONGODB_URL [cite: 139]
client = AsyncMongoClient("mongodb+srv://Polete:Polpol_6@cluster0.9mclpso.mongodb.net")
db = client.Gestor_de_llibres
llibre_collection = db.get_collection("llibres")

# Tipus per manejar el format de ObjectId de MongoDB [cite: 151]
PyObjectId = Annotated[str, BeforeValidator(str)]

# --- Definició dels models (Pydantic) ---
class LlibreModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    titol: str = Field(...)
    autor: str = Field(...)
    estat: str = Field(pattern="^(pendent|llegit)$") # Validació d'estat 
    valoracio: int = Field(..., ge=0, le=10) # Valoració (ex: 0-10) 
    categoria: str = Field(...)
    persona: str = Field(...)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "titol": "El Quixot",
                "autor": "Miguel de Cervantes",
                "estat": "llegit",
                "valoracio": 9,
                "categoria": "Clàssic",
                "persona": "Joan"
            }
        }
    )

class UpdateLlibreModel(BaseModel):
    """Model per a actualitzacions parcials"""
    titol: Optional[str] = None
    autor: Optional[str] = None
    estat: Optional[str] = None
    valoracio: Optional[int] = None
    categoria: Optional[str] = None
    persona: Optional[str] = None
    model_config = ConfigDict(arbitrary_types_allowed=True)

# --- Endpoints API (CRUD) ---

@app.post("/llibres/", response_description="Afegir un nou llibre", status_code=status.HTTP_201_CREATED, response_model=LlibreModel)
async def create_llibre(llibre: LlibreModel = Body(...)):
    """Crear un nou element (C) [cite: 189]"""
    new_llibre = await llibre_collection.insert_one(
        llibre.model_dump(by_alias=True, exclude={"id"})
    )
    created_llibre = await llibre_collection.find_one({"_id": new_llibre.inserted_id})
    return created_llibre

@app.get("/llibres/", response_description="Llistar tots els llibres", response_model=List[LlibreModel])
async def list_llibres():
    """Llistar tots els elements (R) [cite: 190]"""
    return await llibre_collection.find().to_list(1000)

@app.get("/llibres/{id}", response_description="Obtenir un llibre per ID", response_model=LlibreModel)
async def show_llibre(id: str):
    if (llibre := await llibre_collection.find_one({"_id": ObjectId(id)})) is not None:
        return llibre
    raise HTTPException(status_code=404, detail=f"Llibre {id} no trobat")

@app.put("/llibres/{id}", response_description="Editar un llibre existent", response_model=LlibreModel)
async def update_llibre(id: str, llibre: UpdateLlibreModel = Body(...)):
    """Editar un element existent (U) [cite: 191]"""
    llibre_data = {k: v for k, v in llibre.model_dump(exclude_unset=True).items()}
    
    if len(llibre_data) >= 1:
        update_result = await llibre_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": llibre_data},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
    
    if (existing_llibre := await llibre_collection.find_one({"_id": ObjectId(id)})) is not None:
        return existing_llibre
        
    raise HTTPException(status_code=404, detail=f"Llibre {id} no trobat")

@app.delete("/llibres/{id}", response_description="Eliminar un llibre")
async def delete_llibre(id: str):
    """Eliminar un element (D) [cite: 192]"""
    delete_result = await llibre_collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Llibre {id} no trobat")

# Endpoint per filtrar per categoria [cite: 198]
@app.get("/llibres/categoria/{categoria}", response_model=List[LlibreModel])
async def filter_by_category(categoria: str):
    return await llibre_collection.find({"categoria": categoria}).to_list(1000)