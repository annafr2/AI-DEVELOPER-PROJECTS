import ollama
import time

# --- הגדרות הניסוי ---
needle = "CRITICAL FACT: The secret code is 9988."
# יצרנו "מסמך" של כ-200 מילים (טקסט סתמי)
one_document_content = "The quick brown fox jumps over the lazy dog. The weather is nice. " * 20 

# רשימת כמויות המסמכים לבדיקה (מותאם ל-TinyLlama)
doc_counts = [2, 4, 6, 8, 10, 12, 15]

def run_size_experiment():
    results = []
    print(f"{'Docs':<5} | {'Words':<8} | {'Time (s)':<8} | {'Result':<10}")
    print("-" * 45)

    for num_docs in doc_counts:
        # 1. בניית הטקסט (Context Accumulation)
        # אנחנו יוצרים רשימה של מסמכים ריקים
        context_parts = [one_document_content] * num_docs
        
        # מכניסים את ה"מחט" למסמך שבאמצע הערימה
        middle_index = num_docs // 2
        context_parts[middle_index] = context_parts[middle_index] + " " + needle
        
        # מחברים הכל לטקסט אחד ארוך
        full_context = "\n\n".join(context_parts)
        
        # חישוב אורך המילים (בשביל המחקר)
        word_count = len(full_context.split())

        # 2. הרצת הניסוי ומדידת זמנים
        start_time = time.time()
        
        try:
            response = ollama.chat(model='tinyllama', messages=[
                {'role': 'user', 'content': f"Context:\n{full_context}\n\nQuestion: What is the secret code?"}
            ])
            answer = response['message']['content']
        except Exception as e:
            answer = "Error"
        
        end_time = time.time()
        latency = end_time - start_time

        # 3. בדיקת דיוק
        is_correct = "9988" in answer
        status = "PASS" if is_correct else "FAIL"

        # 4. הדפסת התוצאה לטבלה
        print(f"{num_docs:<5} | {word_count:<8} | {latency:.2f}     | {status}")
        
        results.append((num_docs, word_count, latency, is_correct))

    # סיכום גרפי קטן בסוף
    print("\n--- Summary Analysis ---")
    for r in results:
        bar = "#" * int(r[2] * 2) # אורך הפס לפי הזמן שלקח
        status = "V" if r[3] else "X"
        print(f"Docs {r[0]:2}: [{status}] Time: {bar}")

if __name__ == "__main__":
    run_size_experiment()