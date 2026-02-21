from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from pathlib import Path
import langchain

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR.parent

DATA_DIR = SRC_DIR / "data"
SOURCE_DIR = DATA_DIR / "contexte_metier_mobilite311.md"

with open(SOURCE_DIR, "r", encoding="utf-8") as f:
    markdown_document = f.read()

headers_to_split_on = [
    ("#", "Dataset"),
    ("##", "Nom de la colonne"),
    ("###", "Type de valeur"),
    ("####", "Énumération"),
    ("#####", "Description"),
]

markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=headers_to_split_on, 
    strip_headers=True 
)
md_header_splits = markdown_splitter.split_text(markdown_document)

# afficher les chunks et leur metadata
for i, doc in enumerate(md_header_splits):
    print(f"Chunk {i}:")
    print(f"Metadata: {doc.metadata}")
    print(f"Contenu: {doc.page_content}")
    print("---")