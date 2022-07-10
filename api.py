import uvicorn
from fastapi import Body, FastAPI
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from keybert import KeyBERT
import spacy
from keyphrase_vectorizers import KeyphraseCountVectorizer

app = FastAPI()

@app.post("/KeyphraseCountVectorizer/get_feature_names_out")
async def keyphrase_vectorizer_get_feature_names(doc: str = Body()):
    vectorizer = KeyphraseCountVectorizer()
    print('doc =', doc)
    vectorizer.fit([doc, "whatever whatever whatever"])
    return list(vectorizer.get_feature_names_out())

@app.post("/spaCy/noun_chunks")
async def spacy_noun_chunks(doc: str = Body()):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(doc)
    return [chunk.text for chunk in doc.noun_chunks]

@app.post("/KeyBERT/extract_phrase")
async def key_bert_extract_phrase(
    min_keyphrase_length: int = 1, 
    max_keyphrase_length: int = 3,
    diversity: float = 0.9,
    top_n: int = 20,
    doc: str = Body()
):
    # https://github.com/MaartenGr/KeyBERT
    kw_model = KeyBERT()
    keyphrase_ngram_range=(min_keyphrase_length, max_keyphrase_length)
    return kw_model.extract_keywords(doc, 
        keyphrase_ngram_range=keyphrase_ngram_range,
        stop_words='english',
        top_n=top_n,
        use_mmr=True,
        diversity=diversity
    )

@app.get("/")
async def dashboard():
    return RedirectResponse("/docs")

if __name__ == "__main__":
    uvicorn.run("api:app")