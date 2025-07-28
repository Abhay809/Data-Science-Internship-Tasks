import os
os.environ["TRANSFORMERS_NO_TF"] = "1"  # Disable TensorFlow to avoid Keras issue

import faiss
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
from langchain.text_splitter import CharacterTextSplitter


# -------- Load Embedding Model (optimized for Q&A) --------
embedder = SentenceTransformer("multi-qa-MiniLM-L6-cos-v1")

# -------- Load Generator Model --------
gen_model_name = "google/flan-t5-base"  # You can change to flan-t5-large if you have GPU
tokenizer = AutoTokenizer.from_pretrained(gen_model_name)
generator = AutoModelForSeq2SeqLM.from_pretrained(gen_model_name)

# -------- Load and Chunk Documents --------
def load_documents(folder_path):
    documents = []
    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                documents.append(f.read())
    return documents

def chunk_documents(documents, chunk_size=300, chunk_overlap=50):
    text_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = []
    for doc in documents:
        chunks.extend(text_splitter.split_text(doc))
    return chunks

# -------- Embed and Index Chunks --------
def create_faiss_index(chunks):
    embeddings = embedder.encode(chunks, show_progress_bar=True)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    return index, embeddings, chunks

# -------- Query and Generate Response --------
def generate_answer(query, index, chunks, top_k=5):
    query_embedding = embedder.encode([query])
    D, I = index.search(query_embedding, top_k)

    # Fetch top-k relevant chunks
    retrieved_chunks = [chunks[i] for i in I[0]]

    # Optional keyword-based filter to avoid unrelated text
    query_keywords = query.lower().split()
    filtered_chunks = [
        chunk for chunk in retrieved_chunks
        if any(keyword in chunk.lower() for keyword in query_keywords)
    ]

    # Use filtered chunks if available
    context = "\n".join(filtered_chunks if filtered_chunks else retrieved_chunks)

    # Improved prompt with clear structure
    prompt = f"""You are a knowledgeable cricket and AI assistant. Use only the context below to answer the question.

Context:
{context}

Question: {query}
Answer:"""

    inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)

    outputs = generator.generate(
        **inputs,
        max_length=200,
        num_beams=5,
        temperature=0.7,
        early_stopping=True
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)



# -------- Run the Chatbot --------
if __name__ == "__main__":
    docs = load_documents("documents")  # Folder must contain doc1.txt, doc2.txt
    chunks = chunk_documents(docs)
    index, embeddings, chunks = create_faiss_index(chunks)

    print("✅ RAG Chatbot is ready! Ask your cricket-related questions.")
    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break
        response = generate_answer(query, index, chunks)
        print(f"Bot: {response}")
