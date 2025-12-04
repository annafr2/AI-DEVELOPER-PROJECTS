import ollama
import time

# --- 1. הכנת הנתונים (הדאטה) ---
# שאלה: מה תופעות הלוואי של התרופה "Xylophone"?
question = "What are the side effects of the drug Xylophone?"

# מסמך המטרה (עם התשובה) - זה מה ש-RAG אמור למצוא
target_doc = """
Medical Report: Drug Xylophone.
Category: Antiviral.
Usage: Treats severe flu.
Side Effects: The main side effects of Xylophone are severe dizziness and purple spots on the skin. 
Patients should drink water.
"""

# מסמכי רעש (Filler) - כדי לבלבל את המודל בהקשר המלא
# ניצור 19 מסמכים בנושאים אחרים (משפטים, טכנולוגיה)
distractor_1 = "Legal Contract: The tenant agrees to pay rent on the 1st of each month. " * 20
distractor_2 = "Tech News: The new iPhone 25 will have a holographic screen and no buttons. " * 20
distractor_3 = "Cooking Recipe: To make a pizza, mix flour and water. Add tomato sauce. " * 20

# יצירת רשימה של 20 מסמכים (1 רלוונטי + 19 לא רלוונטיים)
all_documents = [target_doc] + ([distractor_1, distractor_2, distractor_3] * 7)
# (יש לנו עכשיו 22 מסמכים בערך)

def run_experiment_3():
    print(f"--- Experiment 3: RAG Impact ---\n")
    
    # --- מצב A: ללא RAG (כל המסמכים ביחד) ---
    print("Running Mode A: FULL CONTEXT (All documents)...")
    full_context = "\n\n".join(all_documents)
    
    start_time = time.time()
    response_full = ollama.chat(model='tinyllama', messages=[
        {'role': 'user', 'content': f"Context:\n{full_context}\n\nQuestion: {question}"}
    ])
    end_time = time.time()
    
    ans_full = response_full['message']['content']
    time_full = end_time - start_time
    # בדיקה האם המילים "purple spots" או "dizziness" מופיעות
    success_full = "dizziness" in ans_full.lower() or "purple" in ans_full.lower()

    print(f"Time: {time_full:.2f}s")
    print(f"Result: {'✅ PASS' if success_full else '❌ FAIL'}")
    print(f"Answer snippet: {ans_full[:100]}...\n")


    # --- מצב B: עם RAG (רק המסמך הרלוונטי) ---
    print("Running Mode B: RAG SIMULATION (Only relevant doc)...")
    # כאן אנחנו מדמים שהמנוע מצא רק את המסמך הנכון
    rag_context = target_doc 
    
    start_time = time.time()
    response_rag = ollama.chat(model='tinyllama', messages=[
        {'role': 'user', 'content': f"Context:\n{rag_context}\n\nQuestion: {question}"}
    ])
    end_time = time.time()
    
    ans_rag = response_rag['message']['content']
    time_rag = end_time - start_time
    success_rag = "dizziness" in ans_rag.lower() or "purple" in ans_rag.lower()

    print(f"Time: {time_rag:.2f}s")
    print(f"Result: {'✅ PASS' if success_rag else '❌ FAIL'}")
    print(f"Answer snippet: {ans_rag[:100]}...\n")

    # --- סיכום ---
    print("-" * 30)
    print(f"Summary Comparison:")
    print(f"Full Context: {time_full:.2f}s | Correct? {success_full}")
    print(f"RAG Mode:     {time_rag:.2f}s  | Correct? {success_rag}")
    print("-" * 30)

if __name__ == "__main__":
    run_experiment_3()