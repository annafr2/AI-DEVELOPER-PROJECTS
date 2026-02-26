# Technical Planning & Architecture

## System Architecture

### Component Breakdown

#### 1. Core NLP Module (Stage 1)
**Purpose**: Foundation for text vectorization and similarity measurement

**Components**:
- **Tokenizer**: Convert text to numerical tokens
  - Options: sentence-transformers, OpenAI embeddings, or custom
  - Recommended: sentence-transformers (all-MiniLM-L6-v2) for local, fast embeddings

- **Embedder**: Convert tokens to dense vector representations
  - Input: String (sentence)
  - Output: numpy array (vector of size 384 or 768 depending on model)

- **Similarity Calculator**: Compute cosine distance
  - Formula: `1 - cosine_similarity(v1, v2)`
  - Input: Two vectors
  - Output: Float (0 = identical, 1 = completely different)

**Implementation Details**:
```python
# Pseudo-code structure
class TextVectorizer:
    def __init__(self, model_name):
        # Load embedding model

    def embed(self, text: str) -> np.ndarray:
        # Convert text to vector

    def cosine_distance(self, vec1, vec2) -> float:
        # Calculate distance
```

#### 2. Translation Agents (Stage 2)

**Agent Base Class**:
```python
class TranslationAgent:
    def __init__(self, source_lang, target_lang):
        self.source = source_lang
        self.target = target_lang

    def translate(self, text: str) -> str:
        # Call LLM API with translation prompt
```

**Agent 1: EN→RU**
- Source: English
- Target: Russian
- API: Claude/OpenAI with translation prompt

**Agent 2: RU→HE**
- Source: Russian
- Target: Hebrew
- API: Claude/OpenAI with translation prompt

**Agent 3: HE→EN**
- Source: Hebrew
- Target: English
- API: Claude/OpenAI with translation prompt

**Agent 4: Generator**
- Generates 100 diverse English sentences
- Categories: questions, statements, idioms, technical, casual
- Ensures variety for meaningful testing

#### 3. Pipeline Orchestrator (Stage 3)

**Purpose**: Coordinate agent execution and data flow

```python
class TuringMachinePipeline:
    def __init__(self):
        self.generator = Agent4()
        self.en_to_ru = Agent1()
        self.ru_to_he = Agent2()
        self.he_to_en = Agent3()
        self.vectorizer = TextVectorizer()

    def run(self) -> Results:
        # 1. Generate sentences
        # 2. Process through translation chain
        # 3. Calculate distances
        # 4. Generate visualization
```

#### 4. Analysis & Visualization Module (Stage 3)

**Metrics**:
- Individual cosine distances (100 values)
- Average error across all sentences
- Standard deviation
- Min/Max errors

**Visualization**:
- Line plot: X=sentence index (0-99), Y=cosine distance
- Horizontal line showing average
- Title and labels
- Save as PNG

## Data Flow

```
┌─────────────┐
│  Agent 4    │ Generates 100 sentences
│ (Generator) │
└──────┬──────┘
       │ List[str] (English)
       ▼
┌─────────────┐
│  Agent 1    │ EN → RU
│  (EN→RU)    │
└──────┬──────┘
       │ List[str] (Russian)
       ▼
┌─────────────┐
│  Agent 2    │ RU → HE
│  (RU→HE)    │
└──────┬──────┘
       │ List[str] (Hebrew)
       ▼
┌─────────────┐
│  Agent 3    │ HE → EN
│  (HE→EN)    │
└──────┬──────┘
       │ List[str] (English)
       ▼
┌─────────────┐
│ Vectorizer  │ Calculate distances
│  & Analyzer │ between original & final
└──────┬──────┘
       │
       ▼
┌─────────────┐
│Visualization│ Generate graph + metrics
│   Module    │
└─────────────┘
```

## Technology Decisions

### Option 1: Local Embeddings (Recommended for Stage 1)
**Pros**:
- Fast, no API costs
- Good for testing
- sentence-transformers library is mature

**Cons**:
- May not capture multilingual nuances perfectly

### Option 2: OpenAI Embeddings
**Pros**:
- High quality
- Multilingual support

**Cons**:
- API costs
- Slower

### Translation API Choice
- **Claude API**: High quality translations, good reasoning
- **OpenAI GPT-4**: Also good quality
- **Google Translate API**: Faster but less context-aware

**Recommendation**: Start with Claude API for consistency

## File Structure

```
L13/
├── CLAUDE.MD           # Project overview (this file)
├── PLANNING.MD         # Technical architecture
├── TASKS.MD            # Implementation tasks
├── PRD.MD              # Product requirements
├── requirements.txt    # Python dependencies
├── main.py             # Entry point
├── vectorizer.py       # Stage 1: Tokenization & distance
├── agents.py           # Stage 2: Translation agents
├── pipeline.py         # Stage 3: Orchestration
├── visualize.py        # Stage 3: Graphing
└── results/            # Output directory
    ├── metrics.json
    └── error_graph.png
```

## Dependencies

```
sentence-transformers  # For embeddings
anthropic             # Claude API
numpy                 # Vector operations
scikit-learn          # Cosine similarity
matplotlib            # Visualization
python-dotenv         # Environment variables
```

## Error Handling

1. **API Failures**: Retry logic with exponential backoff
2. **Empty Translations**: Log and skip sentence
3. **Invalid Vectors**: Validate dimensions match
4. **Rate Limits**: Implement delay between requests

## Testing Strategy

### Stage 1 Tests
- Test embedding generation with known sentences
- Test cosine distance with identical sentences (should be ~0)
- Test with completely different sentences (should be high)

### Stage 2 Tests
- Test each agent individually with known translations
- Verify output language is correct
- Handle edge cases (empty strings, special characters)

### Stage 3 Tests
- End-to-end test with 5 sentences
- Verify all metrics are calculated
- Verify graph is generated

## Performance Considerations

- **Batch Processing**: Process translations in batches if API supports
- **Caching**: Cache embeddings to avoid recomputation
- **Parallel Execution**: Consider async for independent operations
- **Progress Tracking**: Show progress for 100 sentence processing
