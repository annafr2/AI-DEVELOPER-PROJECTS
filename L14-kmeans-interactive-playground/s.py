def frequency_analysis(text):
    freq = {}
    total = len([c for c in text if c.isalpha()])

    for char in text.upper():
        if char.isalpha():
                    freq[char] = freq.get(char, 0) + 1
    # Convert to percentages 
    for char in freq:
            freq[char] = (freq[char] / total) * 100 
    return sorted(freq.items(), 
                    key=lambda x: x[1], 
                    reverse=True)

# Example usage
text = "e vjdfnvblcfe mm edvdxdv ldmvfdlkmbfkl skdfmbdfkmbfklm kdmbhflkvdsnvdsknvkanamkjbdndmn " 
result = frequency_analysis(text)
for char, percentage in result[:5]:
    print(f"{char}: {percentage:.2f}%")