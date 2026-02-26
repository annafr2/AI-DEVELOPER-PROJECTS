# Product Requirements Document (PRD)
## Multi-Agent Translation Turing Machine

### Document Information
- **Version**: 1.0
- **Date**: 2025-10-28
- **Status**: Draft

---

## 1. Executive Summary

### 1.1 Purpose
To build an experimental system that measures semantic degradation when text undergoes sequential machine translation through multiple languages.

### 1.2 Problem Statement
Machine translation is imperfect. When text is translated through multiple languages sequentially, meaning can be lost or distorted. This project quantifies that degradation.

### 1.3 Goals
- Measure translation quality degradation through multi-language chains
- Visualize semantic drift across 100 diverse sentences
- Provide quantitative metrics for translation reliability
- Demonstrate vector space analysis of natural language

---

## 2. Product Overview

### 2.1 Product Description
A Python-based system that:
1. Generates 100 English sentences
2. Translates them through a chain: English → Russian → Hebrew → English
3. Compares original vs. final sentences using vector embeddings
4. Outputs metrics and visualizations

### 2.2 Target Users
- Researchers studying machine translation quality
- NLP engineers testing translation systems
- Data scientists interested in semantic similarity
- Educators teaching about information loss in transformations

### 2.3 Success Metrics
- System successfully processes 100 sentences without errors
- Cosine distance calculations are mathematically valid (0 ≤ distance ≤ 1)
- Average error is calculated and reported
- Visualization clearly shows degradation patterns
- Execution time is reasonable (< 30 minutes for 100 sentences)

---

## 3. Functional Requirements

### 3.1 Core Features

#### FR-1: Sentence Generation
**Priority**: High
**Description**: Generate 100 diverse English sentences

**Requirements**:
- FR-1.1: System shall generate exactly 100 sentences
- FR-1.2: Sentences shall cover diverse categories:
  - Simple declarative statements
  - Questions
  - Complex sentences with clauses
  - Idiomatic expressions
  - Technical/domain-specific language
- FR-1.3: Generated sentences shall be saved to file
- FR-1.4: Sentences shall be reproducible (same output on repeat runs)
- FR-1.5: Each sentence shall be 5-50 words long

**Acceptance Criteria**:
- ✓ 100 valid English sentences are generated
- ✓ Sentences represent diverse language patterns
- ✓ Output is saved to file

---

#### FR-2: Translation Agent 1 (EN→RU)
**Priority**: High
**Description**: Translate English sentences to Russian

**Requirements**:
- FR-2.1: Shall accept English text as input
- FR-2.2: Shall output valid Russian text
- FR-2.3: Shall preserve meaning to the best of system's ability
- FR-2.4: Shall handle special characters, punctuation, and numbers
- FR-2.5: Shall log all translations

**Acceptance Criteria**:
- ✓ Russian output is grammatically valid
- ✓ Meaning is preserved from English source
- ✓ Special cases are handled properly

---

#### FR-3: Translation Agent 2 (RU→HE)
**Priority**: High
**Description**: Translate Russian sentences to Hebrew

**Requirements**:
- FR-3.1: Shall accept Russian text as input
- FR-3.2: Shall output valid Hebrew text
- FR-3.3: Shall preserve meaning from Russian source
- FR-3.4: Shall handle Cyrillic to Hebrew script conversion
- FR-3.5: Shall log all translations

**Acceptance Criteria**:
- ✓ Hebrew output is grammatically valid
- ✓ Meaning is preserved from Russian source
- ✓ Right-to-left text is handled correctly

---

#### FR-4: Translation Agent 3 (HE→EN)
**Priority**: High
**Description**: Translate Hebrew sentences back to English

**Requirements**:
- FR-4.1: Shall accept Hebrew text as input
- FR-4.2: Shall output valid English text
- FR-4.3: Shall preserve meaning from Hebrew source
- FR-4.4: Shall handle Hebrew to Latin script conversion
- FR-4.5: Shall log all translations

**Acceptance Criteria**:
- ✓ English output is grammatically valid
- ✓ Meaning is preserved from Hebrew source
- ✓ Output is comparable to original English

---

#### FR-5: Text Vectorization
**Priority**: High
**Description**: Convert text to numerical vector representations

**Requirements**:
- FR-5.1: Shall embed English sentences into dense vectors
- FR-5.2: Vector dimensions shall be consistent (all same size)
- FR-5.3: Shall use state-of-the-art embedding model
- FR-5.4: Embeddings shall capture semantic meaning
- FR-5.5: Shall cache embeddings to avoid recomputation

**Acceptance Criteria**:
- ✓ All sentences are successfully embedded
- ✓ Vector dimensions match (e.g., all 384-d or 768-d)
- ✓ Similar sentences have similar vectors

---

#### FR-6: Cosine Distance Calculation
**Priority**: High
**Description**: Calculate semantic similarity between original and final sentences

**Requirements**:
- FR-6.1: Shall calculate cosine distance for all 100 sentence pairs
- FR-6.2: Distance values shall be in range [0, 1]
  - 0 = identical meaning
  - 1 = completely different meaning
- FR-6.3: Calculation shall be mathematically accurate
- FR-6.4: Shall handle edge cases (zero vectors, NaN values)
- FR-6.5: Results shall be saved to file

**Acceptance Criteria**:
- ✓ All 100 distances are calculated
- ✓ All values are in valid range [0, 1]
- ✓ Distances reflect actual semantic similarity

---

#### FR-7: Metrics Calculation
**Priority**: High
**Description**: Compute aggregate statistics on translation degradation

**Requirements**:
- FR-7.1: Shall calculate average cosine distance
- FR-7.2: Shall calculate standard deviation
- FR-7.3: Shall identify minimum distance (best preserved)
- FR-7.4: Shall identify maximum distance (most degraded)
- FR-7.5: Shall save metrics to JSON file
- FR-7.6: Shall print metrics to console

**Acceptance Criteria**:
- ✓ Average error is displayed
- ✓ All 100 individual distances are reported
- ✓ Statistics are mathematically correct
- ✓ Output is formatted clearly

---

#### FR-8: Visualization
**Priority**: High
**Description**: Generate graph showing error per sentence

**Requirements**:
- FR-8.1: X-axis shall be sentence index (0-99)
- FR-8.2: Y-axis shall be cosine distance (0-1)
- FR-8.3: Graph shall show line plot with markers
- FR-8.4: Graph shall include horizontal line for average
- FR-8.5: Graph shall have clear title, labels, and legend
- FR-8.6: Graph shall be saved as PNG file
- FR-8.7: Graph shall be high resolution (at least 1200x800)

**Acceptance Criteria**:
- ✓ Graph is generated successfully
- ✓ All 100 data points are visible
- ✓ Average line is clearly marked
- ✓ Graph is readable and informative
- ✓ File is saved to results/ directory

---

### 3.2 Pipeline Features

#### FR-9: Sequential Processing
**Priority**: High
**Description**: Process sentences through complete translation chain

**Requirements**:
- FR-9.1: Shall process sentences in order: Agent4 → Agent1 → Agent2 → Agent3
- FR-9.2: Output of each agent becomes input to next
- FR-9.3: Shall handle all 100 sentences
- FR-9.4: Shall continue on individual failures (with logging)
- FR-9.5: Shall track progress (e.g., "Processing 42/100...")

**Acceptance Criteria**:
- ✓ All agents execute in correct order
- ✓ Data flows correctly between agents
- ✓ Progress is visible to user

---

### 3.3 Error Handling

#### FR-10: Robustness
**Priority**: Medium
**Description**: Handle errors gracefully without crashing

**Requirements**:
- FR-10.1: Shall retry API calls on failure (up to 3 times)
- FR-10.2: Shall log all errors with timestamps
- FR-10.3: Shall skip problematic sentences and continue
- FR-10.4: Shall report skipped sentences in final output
- FR-10.5: Shall handle API rate limiting

**Acceptance Criteria**:
- ✓ System doesn't crash on API errors
- ✓ Errors are logged appropriately
- ✓ User is informed of issues

---

## 4. Non-Functional Requirements

### 4.1 Performance
- **NFR-1**: System shall process 100 sentences in under 30 minutes
- **NFR-2**: API calls shall have timeout of 60 seconds
- **NFR-3**: Memory usage shall not exceed 2GB

### 4.2 Reliability
- **NFR-4**: System shall complete successfully 95% of the time
- **NFR-5**: Individual sentence failures shall not stop entire pipeline

### 4.3 Usability
- **NFR-6**: User shall run system with single command: `python main.py`
- **NFR-7**: Output shall be clearly formatted and easy to understand
- **NFR-8**: Error messages shall be actionable

### 4.4 Maintainability
- **NFR-9**: Code shall follow PEP 8 style guidelines
- **NFR-10**: All functions shall have docstrings
- **NFR-11**: Code shall have type hints
- **NFR-12**: Dependencies shall be documented in requirements.txt

### 4.5 Security
- **NFR-13**: API keys shall be stored in .env file (not in code)
- **NFR-14**: .env file shall be in .gitignore
- **NFR-15**: No sensitive data shall be logged

### 4.6 Portability
- **NFR-16**: System shall work on Windows, Mac, and Linux
- **NFR-17**: System shall work with Python 3.8+

---

## 5. Technical Requirements

### 5.1 Dependencies
- Python 3.8 or higher
- sentence-transformers (for embeddings)
- anthropic or openai (for translation API)
- numpy (for vector operations)
- scikit-learn (for cosine similarity)
- matplotlib (for visualization)
- python-dotenv (for environment variables)

### 5.2 APIs
- LLM API for translations (Claude, OpenAI, or similar)
- Embedding model (local or API-based)

### 5.3 Data Storage
- Input: Generated sentences (JSON or TXT)
- Intermediate: Translation results at each stage
- Output:
  - metrics.json (all metrics and distances)
  - error_graph.png (visualization)
  - full_results.json (detailed breakdown)

---

## 6. Output Specifications

### 6.1 Console Output
```
Multi-Agent Translation Turing Machine
=====================================

Stage 1: Generating 100 sentences...
✓ Complete

Stage 2: Translating through chain...
Processing: 100/100 [████████████████] 100%
✓ Complete

Stage 3: Calculating metrics...
✓ Complete

Results:
--------
Average Cosine Distance: 0.342
Standard Deviation: 0.128
Minimum Distance: 0.089 (Sentence #42)
Maximum Distance: 0.687 (Sentence #73)

Detailed distances:
Sentence 0: 0.234
Sentence 1: 0.301
...
Sentence 99: 0.412

Graph saved to: ./results/error_graph.png
Metrics saved to: ./results/metrics.json
```

### 6.2 metrics.json Format
```json
{
  "summary": {
    "average_distance": 0.342,
    "std_dev": 0.128,
    "min_distance": 0.089,
    "max_distance": 0.687,
    "total_sentences": 100,
    "failed_sentences": 0
  },
  "distances": [
    {"index": 0, "distance": 0.234, "original": "...", "final": "..."},
    ...
  ]
}
```

### 6.3 Graph Specifications
- **Title**: "Translation Degradation: Cosine Distance per Sentence"
- **X-axis**: "Sentence Index" (0-99)
- **Y-axis**: "Cosine Distance" (0.0-1.0)
- **Series**: Blue line with circle markers
- **Average line**: Red dashed horizontal line
- **Grid**: Light gray
- **Size**: 1200x800 pixels
- **Format**: PNG with transparent background

---

## 7. User Stories

### US-1: Research Use Case
**As a** translation researcher
**I want to** measure semantic degradation through translation chains
**So that** I can quantify information loss in multi-hop translation

### US-2: Comparative Analysis
**As a** NLP engineer
**I want to** compare different translation services
**So that** I can choose the most reliable one for my application

### US-3: Educational Use
**As an** educator
**I want to** demonstrate information theory concepts
**So that** students can see real-world examples of information loss

---

## 8. Success Criteria

### 8.1 Must Have (MVP)
- ✓ Generate 100 sentences
- ✓ Translate through EN→RU→HE→EN chain
- ✓ Calculate cosine distances
- ✓ Output average error
- ✓ Display all distances
- ✓ Generate graph

### 8.2 Should Have
- ✓ Robust error handling
- ✓ Progress tracking
- ✓ Detailed logging
- ✓ Save intermediate results
- ✓ Reproducible results

### 8.3 Could Have (Future)
- Multiple language chains for comparison
- Web interface
- Real-time visualization
- Statistical analysis
- Batch processing optimization

### 8.4 Won't Have (Out of Scope)
- Custom translation model training
- Real-time user input translation
- Language detection
- Grammar checking
- Human evaluation interface

---

## 9. Risks & Mitigations

### 9.1 Technical Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| API rate limiting | High | Medium | Implement delays, retry logic |
| API cost overruns | Medium | Low | Estimate costs upfront, set limits |
| Poor translation quality | High | Medium | Use high-quality API (Claude/GPT-4) |
| Embedding model limitations | Medium | Low | Test multiple models in Stage 1 |
| Long execution time | Low | Medium | Optimize with batching, async calls |

### 9.2 Project Risks

| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Scope creep | Medium | High | Stick to staged approach |
| Unclear requirements | Low | Low | This PRD defines requirements |
| Testing gaps | Medium | Medium | Follow test plan in TASKS.MD |

---

## 10. Timeline & Milestones

| Milestone | Deliverables | Target |
|-----------|--------------|--------|
| **Stage 1 Complete** | Vectorizer working, tests passing | After 2-4 hours |
| **Stage 2 Complete** | All 4 agents implemented and tested | After 6-10 hours |
| **Stage 3 Complete** | Full pipeline running, results generated | After 10-16 hours |
| **Final Review** | All documentation complete, code cleaned | After 16-18 hours |

---

## 11. Acceptance Criteria

The project is considered complete when:

1. ✓ All files in TASKS.MD are created
2. ✓ All Stage 1, 2, 3 tasks are completed
3. ✓ System processes 100 sentences successfully
4. ✓ All output requirements (Section 6) are met
5. ✓ Code is documented and follows style guidelines
6. ✓ README.md has usage instructions
7. ✓ Results are reproducible
8. ✓ No critical bugs remain

---

## 12. Appendix

### 12.1 Glossary
- **Cosine Distance**: 1 - cosine_similarity, measures vector dissimilarity
- **Embedding**: Dense vector representation of text
- **Semantic Degradation**: Loss of meaning through transformations
- **Turing Machine**: Named metaphorically; refers to sequential state transformations

### 12.2 References
- sentence-transformers documentation
- Claude API documentation
- Cosine similarity in NLP
- Machine translation evaluation metrics

### 12.3 Change Log
- **v1.0** (2025-10-28): Initial PRD creation
