# PRD.md

# Product Requirements Document (PRD)
## Deepfake Detection Bot

**Version:** 1.0  
**Date:** December 27, 2025  
**Author:** Anna  
**Status:** Completed

---

## 1. Executive Summary

### 1.1 Product Overview
An AI-powered automated system that analyzes video files to detect deepfake content using Google's Gemini-3-Flash-Preview model. The system identifies visual and audio anomalies indicative of AI-generated synthetic media.

### 1.2 Business Objective
Develop a functional deepfake detection prototype as part of an AI Developer Course assignment, demonstrating practical application of generative AI for digital forensics.

### 1.3 Success Criteria
- Successfully detect deepfake videos with >70% confidence
- Process videos in <15 seconds
- Generate detailed technical reports
- Test detection capabilities against high-quality AI-generated videos (Google Veo)

---

## 2. Problem Statement

### 2.1 Background
Deepfake technology has advanced significantly, creating realistic synthetic videos that are difficult to distinguish from authentic content. This poses risks for misinformation, fraud, and identity theft.

### 2.2 Target Users
- Educational institutions
- Digital forensics researchers
- Content verification teams
- Media integrity analysts

### 2.3 User Pain Points
- Manual deepfake detection is time-consuming
- Requires specialized expertise
- Existing tools are expensive or inaccessible
- Need for automated, reliable detection

---

## 3. Product Requirements

### 3.1 Functional Requirements

#### FR-001: Video Analysis
**Priority:** P0 (Critical)  
**Description:** System must analyze video files for deepfake indicators

**Acceptance Criteria:**
- Accepts MP4 video format
- Analyzes videos up to 30 seconds
- Returns analysis within 15 seconds
- Supports multiple video processing

#### FR-002: Artifact Detection
**Priority:** P0 (Critical)  
**Description:** Detect specific AI generation artifacts

**Detection Categories:**
1. Facial micro-expressions
2. Blinking patterns
3. Lip-sync quality
4. Temporal consistency
5. Lighting & shadows
6. Hair & edge definition
7. Background artifacts
8. Audio anomalies
9. Eye movement patterns
10. Skin texture analysis

#### FR-003: Scoring System
**Priority:** P0 (Critical)  
**Description:** Provide quantitative deepfake likelihood score

**Score Ranges:**
- 0-30: Likely authentic
- 31-60: Suspicious
- 61-85: High suspicion
- 86-100: Almost certainly synthetic

#### FR-004: Report Generation
**Priority:** P1 (High)  
**Description:** Generate detailed JSON reports

**Report Contents:**
- Video filename
- Suspicion level (High/Medium/Low)
- Fakeness score (0-100)
- List of detected artifacts
- Technical reasoning
- Analysis timestamp
- Processing time

#### FR-005: Error Handling
**Priority:** P1 (High)  
**Description:** Robust error handling and retry logic

**Requirements:**
- Retry failed requests (max 3 attempts)
- Exponential backoff between retries
- Graceful degradation
- Comprehensive error logging

### 3.2 Non-Functional Requirements

#### NFR-001: Performance
- **Processing Time:** <15 seconds per video
- **API Calls:** Maximum 3 retries per video
- **Timeout:** 5 minutes maximum per analysis

#### NFR-002: Reliability
- **Success Rate:** >95% for valid videos
- **Uptime:** Dependent on Google API availability
- **Error Recovery:** Automatic retry on transient failures

#### NFR-003: Security
- **API Key Storage:** Environment variables only
- **Data Privacy:** No cloud storage of videos
- **Logging:** Comprehensive audit trail
- **PII Protection:** No retention of personal data

#### NFR-004: Usability
- **Setup Time:** <5 minutes
- **Documentation:** Complete README and PRD
- **Error Messages:** Clear and actionable
- **Output Format:** Human-readable and machine-parsable

#### NFR-005: Maintainability
- **Code Quality:** PEP 8 compliant Python
- **Logging:** Structured logging with multiple levels
- **Modularity:** Object-oriented design
- **Documentation:** Inline comments and docstrings

---

## 4. Technical Specifications

### 4.1 Technology Stack

| Component | Technology | Version | Justification |
|-----------|-----------|---------|---------------|
| Runtime | Python | 3.12+ | Modern, well-supported |
| AI Model | Gemini-3-Flash | Preview | State-of-the-art vision model |
| SDK | google-genai | Latest | Official Google SDK |
| Config | python-dotenv | Latest | Secure key management |

### 4.2 System Architecture
```
┌─────────────┐
│   User      │
└──────┬──────┘
       │
       v
┌─────────────────────────────────┐
│   DeepfakeDetector Class        │
│   ┌─────────────────────────┐   │
│   │ analyze_video()         │   │
│   ├─────────────────────────┤   │
│   │ _validate_json()        │   │
│   ├─────────────────────────┤   │
│   │ _display_result()       │   │
│   ├─────────────────────────┤   │
│   │ save_report()           │   │
│   └─────────────────────────┘   │
└────────────┬────────────────────┘
             │
             v
┌────────────────────────────────┐
│   Google Gemini API            │
│   (gemini-3-flash-preview)     │
└────────────┬───────────────────┘
             │
             v
┌────────────────────────────────┐
│   JSON Report + Logs           │
└────────────────────────────────┘
```

### 4.3 Data Flow

1. **Input:** User provides MP4 video files
2. **Processing:** System reads video as binary data
3. **API Call:** Sends video + prompt to Gemini API
4. **Analysis:** AI model analyzes video across 10 dimensions
5. **Response:** Returns JSON with findings
6. **Validation:** System validates JSON structure
7. **Output:** Displays results and saves report

### 4.4 API Integration

**Endpoint:** `https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent`

**Request:**
```json
{
  "model": "gemini-3-flash-preview",
  "contents": [
    {"text": "DETECTION_PROMPT"},
    {"inline_data": {"mime_type": "video/mp4", "data": "BASE64_VIDEO"}}
  ],
  "generationConfig": {
    "response_mime_type": "application/json",
    "temperature": 0.1
  }
}
```

**Response:**
```json
{
  "analysis_target": "filename.mp4",
  "is_deepfake_suspicion": "High",
  "fakeness_score": 78,
  "key_artifacts_detected": ["artifact1", "artifact2"],
  "reasoning": "Technical explanation",
  "confidence_level": "High"
}
```

---

## 5. Experimental Design

### 5.1 Test Dataset

**Source Image:** `img.jpeg`
- Single reference image of subject

**Generated Videos (Deepfakes):**
- **f1.mp4:** AI-generated deepfake using Google Veo
- **f2.mp4:** AI-generated deepfake using Google Veo
- **f4.mp4:** AI-generated deepfake using Google Veo
- **f5.mp4:** AI-generated deepfake using Google Veo (high-quality)

**Real Video:**
- **f3.mp4:** Authentic video of subject

**Video Specifications:**
- Format: MP4
- Duration: 5-10 seconds
- Resolution: Standard HD
- Generation Method: **Google Veo** (via Google Flow) for deepfakes

### 5.2 Test Scenarios

| Test ID | Video | Type | Expected Result | Actual Result | Status |
|---------|-------|------|-----------------|---------------|--------|
| TC-001 | f1.mp4 | Deepfake | Deepfake detected | High (78/100) | ✅ Pass |
| TC-002 | f2.mp4 | Deepfake | Deepfake detected | High (78/100) | ✅ Pass |
| TC-003 | f3.mp4 | Real | Authentic detected | Low (12/100) | ✅ Pass |
| TC-004 | f4.mp4 | Deepfake | Deepfake detected | High (78/100) | ✅ Pass |
| TC-005 | f5.mp4 | Deepfake | Deepfake detected | Low (12/100) | ❌ **FAIL** - False Negative |

### 5.3 Evaluation Metrics

**Quantitative:**
- Detection accuracy: 80% (4/5)
- True positives: 3/4 deepfakes detected (f1, f2, f4)
- True negatives: 1/1 real video identified (f3)
- False negative: 1 (f5 - high-quality Google Veo deepfake)
- False positive rate: 0%
- False negative rate: 25% (1/4)
- Average processing time: ~9s

**Qualitative:**
- Detailed artifact identification
- Coherent technical explanations
- Consistent scoring methodology

---

## 6. Experimental Results

### 6.1 Summary Statistics

| Metric | f1.mp4 | f2.mp4 | f3.mp4 | f4.mp4 | f5.mp4 | Average |
|--------|--------|--------|--------|--------|--------|---------|
| Type | Deepfake | Deepfake | Real | Deepfake | Deepfake | - |
| Suspicion Level | High | High | Low | High | Low ❌ | - |
| Fakeness Score | 78/100 | 78/100 | 12/100 | 78/100 | 12/100 ❌ | 51.6/100 |
| Processing Time | 9.05s | 10.98s | 8.40s | ~9s | 8.16s | ~9s |
| Artifacts Found | 5 | 5 | 0 | 4 | 0 ❌ | 2.8 |
| Detection Result | ✅ Correct | ✅ Correct | ✅ Correct | ✅ Correct | ❌ **Failed** | 80% |

### 6.2 Detailed Findings

#### f1.mp4 Analysis
**Artifacts Detected:**
1. Over-smoothed skin texture (lack of natural pores)
2. Synthetic audio quality (robotic tones)
3. Subtle edge flickering (hair/face boundaries)
4. Unnatural mouth/lip-sync patterns (timing issues)
5. Lack of eye micro-saccades (fixed gaze)

**Technical Assessment:**
Video exhibits multiple AI generation indicators. Skin shows unnatural smoothness characteristic of neural network processing. Audio waveforms display synthetic patterns. Temporal analysis reveals inconsistent frame transitions at facial boundaries.

#### f2.mp4 Analysis
**Artifacts Detected:**
1. Unnatural eye gaze (no micro-saccades)
2. Infrequent and rigid blinking (non-human pattern)
3. Temporal shimmering/morphing (mouth/jawline)
4. Overly smoothed skin texture (missing fine details)
5. "Rubbery" lip-sync movement (artificial kinematics)

**Technical Assessment:**
Video demonstrates advanced AI synthesis with detectable artifacts. Eye fixation patterns deviate from natural human behavior. Blinking frequency and timing suggest algorithmic generation. Morphing artifacts indicate frame-interpolation processing typical of GAN-based video synthesis.

#### f3.mp4 Analysis (Real Video)
**Detection Result:** ✅ Correctly identified as authentic
- Fakeness Score: 12/100 (Low suspicion)
- Natural skin texture with visible pores
- Organic facial movements and micro-expressions
- Consistent lighting and authentic audio

#### f4.mp4 Analysis (Deepfake)
**Detection Result:** ✅ Correctly identified as deepfake
- Fakeness Score: 78/100 (High suspicion)
- Similar artifacts to f1.mp4 and f2.mp4
- Google Veo generation characteristics detected

#### f5.mp4 Analysis (Deepfake - FALSE NEGATIVE)
**Detection Result:** ❌ **FAILED - Incorrectly classified as real**
- Fakeness Score: 12/100 (Low suspicion - INCORRECT)
- Type: High-quality Google Veo deepfake
- System failed to detect any artifacts
- Video quality was too sophisticated for current detection methods

**Why Detection Failed:**
This Google Veo-generated deepfake exhibited:
- Extremely realistic skin texture mimicking natural pores
- Convincing facial micro-expressions
- Natural temporal consistency without visible artifacts
- High-quality audio synthesis
- No detectable morphing or flickering

**Critical Lesson:** State-of-the-art AI video generation (Google Veo) can produce deepfakes sophisticated enough to bypass detection systems, demonstrating the ongoing challenge in the "AI arms race."

### 6.3 Key Insights

1. **Skin Texture:** Most consistent indicator for lower-quality deepfakes
2. **Eye Movements:** Critical differentiator when present
3. **Audio Quality:** Synthetic tones identifiable in most cases
4. **Temporal Consistency:** Morphing/flickering detectable in standard deepfakes
5. **Lip-Sync:** Sophisticated but detectable in f1, f2, f4
6. **⚠️ High-Quality Generation:** Google Veo can create undetectable deepfakes (f5.mp4)
7. **Detection Limitations:** System vulnerable to advanced AI generation models

---

## 7. Limitations & Future Work

### 7.1 Current Limitations

**Technical:**
- Dependent on Google API availability
- Limited to MP4 format
- Processing time varies with video length
- Requires internet connection

**Detection:**
- **Confirmed limitation:** Failed to detect high-quality Google Veo deepfake (f5.mp4)
- Vulnerable to state-of-the-art AI generation models
- Limited training data exposure
- Potential false positives on heavily compressed videos
- Audio analysis could be enhanced
- Detection capabilities lag behind generation technology advancement

### 7.2 Future Enhancements

**Phase 2 Features:**
1. Multi-format support (AVI, MOV, WebM)
2. Batch processing capabilities
3. Real-time webcam analysis
4. Custom model fine-tuning
5. Ensemble detection (multiple AI models)

**Phase 3 Features:**
1. Web-based interface
2. Database of known deepfakes
3. Similarity matching
4. Advanced audio forensics
5. Blockchain verification

---

## 8. Conclusion

### 8.1 Project Success

The deepfake detection bot achieved most primary objectives with important learnings:

✅ **Functional Requirements:** All FR-001 through FR-005 implemented
⚠️ **Accuracy:** 80% detection rate (4/5) - 1 false negative on high-quality Google Veo deepfake
✅ **Performance:** ~9-second average processing time
✅ **Reporting:** Comprehensive JSON reports generated
✅ **Reliability:** Robust error handling and retry logic

**Critical Finding:** The system successfully detected 3/4 deepfakes and correctly identified the real video, but failed on one high-quality Google Veo-generated video (f5.mp4), demonstrating that advanced AI generation can bypass current detection methods.  

### 8.2 Learning Outcomes

**Technical Skills:**
- Google Generative AI API integration
- Advanced prompt engineering
- JSON validation and parsing
- Production-grade error handling
- Structured logging implementation

**Domain Knowledge:**
- Deepfake detection methodologies
- AI-generated content artifacts
- Digital forensics principles
- Video analysis techniques

### 8.3 Real-World Applicability

This system demonstrates practical application of AI for:
- Media verification
- Content moderation
- Digital forensics
- Educational purposes
- Research prototyping

---

## 9. Appendices

### Appendix A: Detection Prompt

Full detection prompt used for analysis (see code for complete text).

### Appendix B: Sample Output
```json
{
  "analysis_date": "2025-12-27T21:14:12",
  "model_used": "gemini-3-flash-preview",
  "total_videos_analyzed": 5,
  "deepfake_generation_method": "Google Veo (via Google Flow)",
  "results": [...]
}
```

### Appendix C: References

1. [Google Gemini API Documentation](https://ai.google.dev)
2. [Deepfake Detection Survey](https://arxiv.org/abs/2004.11138)
3. [FaceForensics++ Dataset](https://github.com/ondyari/FaceForensics)

---

**Document Control:**
- Version: 1.0
- Last Updated: December 27, 2025
- Review Status: Final
- Approved By: Anna (Project Author)