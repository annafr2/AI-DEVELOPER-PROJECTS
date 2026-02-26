import ollama

# 1. הטקסטים - נקצר מעט כדי שיהיה עוד יותר מהר
needle = "CRITICAL FACT: The secret code is 9988."
haystack_filler =  "The wrong code is 1122. The wrong code is 3344. " * 100
def create_context(position):
    if position == 'start':
        return needle + " " + haystack_filler
    elif position == 'end':
        return haystack_filler + " " + needle
    elif position == 'middle':
        mid = len(haystack_filler) // 2
        return haystack_filler[:mid] + " " + needle + " " + haystack_filler[mid:]

def run_experiment():
    positions = ['start', 'middle', 'end']
    print("Starting FAST Experiment...")
    
    for pos in positions:
        print(f"\n--- Testing Position: {pos} ---")
        context = create_context(pos)
        
        # שינינו כאן ל-tinyllama
        response = ollama.chat(model='tinyllama', messages=[
            {'role': 'user', 'content': f"Context:\n{context}\n\nQuestion: What is the secret code?"}
        ])
        
        answer = response['message']['content']
        is_correct = "9988" in answer
        print(f"Result: {'✅ SUCCESS' if is_correct else '❌ FAILED'}")

if __name__ == "__main__":
    run_experiment()