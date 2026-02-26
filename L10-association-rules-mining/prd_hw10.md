# Product Requirements Document (PRD)
## Association Rules Mining System for Supermarket Purchase Pattern Analysis

---

### 📄 Document Information
- **Project Name**: Association Rules Mining System
- **Version**: 1.0
- **Date**: October 2024
- **Status**: Completed
- **Stakeholders**: Data Science Course Instructors, Students

---

## 1. Executive Summary

### 1.1 Problem Statement
Supermarkets need to understand customer purchase patterns to optimize product placement, create effective promotions, and increase basket size. The challenge is identifying which products are frequently bought together in non-obvious combinations.

### 1.2 Solution Overview
Develop an automated system that discovers association rules in transaction data, specifically identifying when purchasing 3 specific products strongly predicts the purchase of 2 other products, measured by the LIFT metric.

### 1.3 Success Criteria
- Find at least one valid 3→2 association rule
- Achieve Lift value > 1.2 (indicating meaningful association)
- Process results within reasonable time (<5 minutes)
- Generate clear visualizations and reports

---

## 2. Product Requirements

### 2.1 Functional Requirements

#### 2.1.1 Data Input
- **FR-01**: System must accept transaction data in binary matrix format (0/1)
- **FR-02**: Support for 169 unique product columns
- **FR-03**: Handle minimum 1000 transactions
- **FR-04**: Support both synthetic and real transaction data

#### 2.1.2 Core Analysis
- **FR-05**: Calculate Support metric for all itemsets
- **FR-06**: Calculate Confidence for valid rule combinations
- **FR-07**: Calculate Lift as primary optimization metric
- **FR-08**: Find rules specifically in 3→2 pattern (3 antecedents, 2 consequents)

#### 2.1.3 Optimization
- **FR-09**: Filter products by frequency before analysis
- **FR-10**: Limit analysis to top N most frequent products (configurable)
- **FR-11**: Show progress during long computations
- **FR-12**: Support parameter tuning (min_support, min_confidence)

#### 2.1.4 Output
- **FR-13**: Display top rules sorted by Lift
- **FR-14**: Generate 4 visualization graphs
- **FR-15**: Export results to CSV format
- **FR-16**: Highlight best rule (highest Lift)

### 2.2 Non-Functional Requirements

#### 2.2.1 Performance
- **NFR-01**: Complete analysis in <5 minutes for 30 products
- **NFR-02**: Handle up to 10,000 transactions
- **NFR-03**: Memory usage <2GB

#### 2.2.2 Usability
- **NFR-04**: Clear progress indicators during processing
- **NFR-05**: Interpretable output with explanations
- **NFR-06**: Error messages for invalid inputs

#### 2.2.3 Reliability
- **NFR-07**: Handle edge cases (no rules found, empty data)
- **NFR-08**: Validate rule patterns (ensure 3→2 format)
- **NFR-09**: Consistent results for same input

---

## 3. Technical Specifications

### 3.1 Architecture

```
┌─────────────────┐
│   Input Layer   │
│  (CSV/Matrix)   │
└────────┬────────┘
         │
┌────────▼────────┐
│ Preprocessing   │
│ - Validation    │
│ - Filtering     │
└────────┬────────┘
         │
┌────────▼────────┐
│  Core Engine    │
│ - Support Calc  │
│ - Confidence    │
│ - Lift          │
└────────┬────────┘
         │
┌────────▼────────┐
│  Optimization   │
│ - Top N Items   │
│ - Pruning       │
└────────┬────────┘
         │
┌────────▼────────┐
│  Output Layer   │
│ - Visualizations│
│ - CSV Export    │
│ - Reports       │
└─────────────────┘
```

### 3.2 Algorithms

#### 3.2.1 Support Calculation
```
Support(X) = |Transactions containing X| / |Total Transactions|
```

#### 3.2.2 Confidence Calculation
```
Confidence(X→Y) = Support(X∪Y) / Support(X)
```

#### 3.2.3 Lift Calculation
```
Lift(X→Y) = Support(X∪Y) / (Support(X) × Support(Y))
```

### 3.3 Data Structures

```python
# Transaction Matrix
DataFrame: [n_transactions × n_products] binary matrix

# Rule Structure
{
    'antecedent': str,     # "product1 + product2 + product3"
    'consequent': str,     # "product4 + product5"
    'support': float,      # 0.0 - 1.0
    'confidence': float,   # 0.0 - 1.0
    'lift': float         # 0.0 - ∞
}
```

---

## 4. User Interface Specifications

### 4.1 Console Output

```
🔍 Searching for association rules...
==================================================
⚡ FAST MODE: Using top 25 most frequent items
Checking 31,250 combinations...
Progress: 10,000/31,250 (32.0%)

✅ Found 72,980 unique 3→2 rules!

🏆 BEST 3→2 RULE (Highest Lift):
==================================================
Rule: milk + butter + eggs → bread + cheese
Lift: 50.35
```

### 4.2 Visualizations

1. **Histogram**: Lift value distribution
2. **Scatter Plot**: Support vs Confidence (colored by Lift)
3. **Bar Chart**: Top 15 rules by Lift
4. **Heatmap**: Product correlation matrix

### 4.3 CSV Output Format

| lift | confidence | support | consequents | antecedents |
|------|-----------|---------|-------------|-------------|
| 50.35 | 0.72 | 0.015 | bread + cheese | milk + butter + eggs |

---

## 5. Development Process

### 5.1 Phase 1: Initial Implementation (First Hour)
- ✅ Basic association rules algorithm
- ✅ Support, Confidence, Lift calculations
- ❌ Performance issues - code stuck for 30+ minutes on 169 products

### 5.2 Phase 2: Debugging & Optimization (Second Hour)
- ✅ Identified the problem: 10.9 billion combinations!
- ✅ Reduced to top 25-30 products only
- ✅ Added progress tracking
- ✅ Code now runs in seconds instead of hours

### 5.3 Phase 3: Pattern Correction (Third Hour)
- ✅ Fixed issue: was getting 1→1, 2→1 patterns
- ✅ Enforced strict 3→2 pattern as required
- ✅ Filtered results to show only valid patterns

### 5.4 Phase 4: Final Results & Documentation (Fourth Hour)
- ✅ Successfully generated 72,980 valid rules
- ✅ Created visualizations
- ✅ Exported results to CSV
- ✅ Documented the solution

---

## 6. Testing Strategy

### 6.1 Unit Tests
- Support calculation accuracy
- Confidence calculation with zero support
- Lift calculation edge cases

### 6.2 Integration Tests
- End-to-end processing
- CSV import/export
- Visualization generation

### 6.3 Performance Tests
- 25 products: <10 seconds
- 30 products: <30 seconds
- 40 products: <3 minutes

### 6.4 Edge Cases
- No rules found
- All products have same frequency
- Empty transaction matrix
- Single transaction

---

## 7. Deployment & Usage

### 7.1 Installation
```bash
pip install pandas numpy matplotlib
```

### 7.2 Basic Usage
```python
python association_rules.py
```

### 7.3 Custom Data
```python
# Replace line 45-60 with:
df = pd.read_csv('your_data.csv')
```

---

## 8. Results & Impact

### 8.1 Achievements
- ✅ Successfully found 72,980 valid 3→2 rules
- ✅ Achieved maximum Lift of 50+
- ✅ Processing time reduced from 30+ minutes to <1 minute
- ✅ Generated comprehensive visualizations

### 8.2 Business Value
- **Product Placement**: Place associated products near each other
- **Promotions**: Bundle products with high Lift values
- **Inventory**: Stock associated products together
- **Recommendations**: "Customers who bought X also bought Y"

### 8.3 Technical Learnings
1. Exponential complexity requires smart optimization
2. Parameter tuning crucial for sparse data
3. Visualization aids pattern interpretation
4. Real data produces better patterns than synthetic

---

## 9. Future Enhancements

### 9.1 Short Term
- [ ] Support for different rule patterns (2→3, 4→1, etc.)
- [ ] Parallel processing for faster computation
- [ ] Interactive parameter adjustment GUI

### 9.2 Long Term
- [ ] Machine learning integration for rule prediction
- [ ] Real-time rule updates with streaming data
- [ ] Multi-store comparison analysis
- [ ] Temporal pattern analysis (seasonal rules)

---

## 10. Appendix

### 10.1 Glossary
- **Support**: Frequency of itemset occurrence
- **Confidence**: Conditional probability
- **Lift**: Association strength metric
- **Antecedent**: IF part of rule (X)
- **Consequent**: THEN part of rule (Y)

### 10.2 Performance Complexity

| Operation | Complexity |
|-----------|-----------|
| Support calculation | O(n) |
| All combinations | O(C(n,3) × C(n,2)) |
| Sorting | O(r log r) |

Where n = products, r = rules found

### 10.3 References
- Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules.
- Market Basket Analysis techniques
- Python itertools documentation

---

**Document Approval**
- Author: Data Science Student
- Reviewer: Course Instructor
- Status: Final
- Grade Target: Maximum Lift Achievement