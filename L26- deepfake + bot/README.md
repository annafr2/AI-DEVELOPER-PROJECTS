# Deepfake Detection Bot - Project Documentation

## README.md

# 🤖 Deepfake Detection Bot

An AI-powered deepfake detection system using Google's Gemini-3-Flash-Preview model to analyze videos and identify synthetic content.

## 📋 Overview

This project implements an automated deepfake detector that analyzes video files for visual and audio anomalies indicative of AI-generated content. The system uses advanced AI analysis to detect common deepfake artifacts with high accuracy.

## 🎯 Project Goals

- Analyze videos to detect deepfake content
- Identify specific AI generation artifacts
- Provide detailed technical explanations
- Generate comprehensive analysis reports

## 🛠️ Technology Stack

- **AI Model:** Google Gemini-3-Flash-Preview
- **Language:** Python 3.12
- **Key Libraries:**
  - `google-genai` - Google Generative AI SDK
  - `python-dotenv` - Environment variable management
  - Standard libraries: `json`, `logging`, `pathlib`

## 📁 Project Structure
```
deepfake_bot/
├── deepfakeDetector.py          # Main detection script
├── deepfake_analysis_report.json # Analysis results
├── deepfake_analysis.log         # Detailed logs
├── img.jpeg                       # Source image
├── f1.mp4                         # Test video 1 (Deepfake)
├── f2.mp4                         # Test video 2 (Deepfake)
├── f3.mp4                         # Test video 3 (Real)
├── f4.mp4                         # Test video 4 (Deepfake)
├── f5.mp4                         # Test video 5 (Deepfake)
├── .env                           # API key configuration
├── README.md                      # This file
└── PRD.md                         # Product Requirements Document
```

## 🚀 Quick Start

### Prerequisites
```bash
python3 --version  # Requires Python 3.8+
```

### Installation
```bash
# 1. Clone or create project directory
mkdir deepfake_bot
cd deepfake_bot

# 2. Install dependencies
pip install google-genai python-dotenv

# 3. Set up API key
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# 4. Run the detector
python3 deepfakeDetector.py
```

## 📊 Experimental Results

### Test Setup

**Source Material:**
- Original image: `img.jpeg`
- Generated 4 deepfake videos using **Google Veo** (via Google Flow)
- Deepfake videos: `f1.mp4`, `f2.mp4`, `f4.mp4`, and `f5.mp4` (all synthetic)
- Real video: `f3.mp4` (authentic)

### Detection Results

#### Video 1 (f1.mp4)
```
🎯 Deepfake Suspicion: High
📈 Fakeness Score: 78/100
⏱️  Analysis Time: 9.05s

🔍 Detected Artifacts:
- Over-smoothed skin texture
- Synthetic audio quality
- Subtle edge flickering
- Unnatural mouth/lip-sync patterns
- Lack of eye micro-saccades
```

**Technical Analysis:**
The system detected AI generation through multiple indicators. The subject's skin showed unnatural smoothness lacking realistic pores. Audio exhibited synthetic tones, and lip-syncing showed occasional unnatural timing. Flickering was visible at face/hair boundaries, and eye movements lacked natural micro-saccades.

#### Video 2 (f2.mp4)
```
🎯 Deepfake Suspicion: High
📈 Fakeness Score: 78/100
⏱️  Analysis Time: 10.98s

🔍 Detected Artifacts:
- Unnatural eye gaze and lack of micro-saccades
- Infrequent and rigid blinking pattern
- Temporal shimmering/morphing around mouth and jawline
- Overly smoothed skin texture
- Slightly 'rubbery' lip-sync movement
```

**Technical Analysis:**
The video exhibited several high-quality AI generation hallmarks. Eyes were unnaturally fixed with minimal blinking. The mouth/chin area showed temporal inconsistencies with subtle morphing between frames. Skin texture was excessively smooth, and facial movements lacked organic complexity.


### Real Video Analysis (f3.mp4)

**Detection Result:**
```
🎯 Deepfake Suspicion: Low
📈 Fakeness Score: 12/100
⏱️  Analysis Time: 8.40s
```

**Artifacts Detected (Positive Indicators of Authenticity):**
- ✅ Minor digital compression artifacts (normal for video encoding)
- ✅ Natural skin texture with visible pores
- ✅ Consistent lighting and shadows across face and background

**Technical Reasoning:**

The video exhibits **high-fidelity facial dynamics** with natural characteristics:

1. **Facial Movements:**
   - Natural micro-expressions present
   - Realistic blinking patterns (frequency and timing)
   - Organic facial muscle movements

2. **Audio-Visual Synchronization:**
   - Perfect lip-sync with Hebrew speech
   - No blurring around mouth area
   - Natural tongue and teeth visibility

3. **Texture & Detail:**
   - Detailed skin texture with visible pores
   - No AI over-smoothing
   - Fine skin details preserved
   - Natural skin imperfections present

4. **Temporal Consistency:**
   - Sharp hair boundaries
   - Natural hair movement without flickering
   - Consistent frame-to-frame transitions

5. **Lighting & Environment:**
   - Lighting on face matches background
   - Natural shadow behavior
   - Consistent illumination patterns

6. **Audio Quality:**
   - Natural breathing sounds
   - Room acoustics present
   - No synthetic audio characteristics
   - Environmental noise consistent with real recording

---

#### Video 4 (f4.mp4)
```
🎯 Deepfake Suspicion: High
📈 Fakeness Score: 78/100
⏱️  Analysis Time: ~9s

🔍 Detected Artifacts:
- Over-smoothed skin texture
- Synthetic audio quality
- Temporal inconsistencies
- Unnatural facial movements
```

**Technical Analysis:**
Successfully detected as deepfake. The video showed similar AI generation artifacts as f1.mp4 and f2.mp4, including unnatural skin smoothing, synthetic audio characteristics, and temporal inconsistencies typical of Google Veo generated content.

---

### ⚠️ False Negative Case: Video 5 (f5.mp4)

**IMPORTANT:** This video is actually a **deepfake generated with Google Veo**, but the system **failed to detect it**.

```
🎯 Deepfake Suspicion: Low ❌ (INCORRECT)
📈 Fakeness Score: 12/100 ❌ (FALSE NEGATIVE)
⏱️  Analysis Time: 8.16s

🔍 Artifacts Detected:
   • None detected (system missed the AI generation)

💭 System's Reasoning (Incorrect):
   The system incorrectly assessed high temporal consistency, natural
   facial micro-expressions, precise lip-syncing, detailed skin texture,
   and sharp hair edges. The AI generation quality was so high that it
   fooled the detection system.

   THE PROMPT FOR GOOGLE FLOW IS:
   Create ultra-realistic self-recorded video message.

   DEVICE SIMULATION:
   Shot on iPhone 14 Pro (front camera), WhatsApp video call recording, 
   indoor natural lighting from window (right side), afternoon, subject 
   at arm's length distance, slightly above eye level angle.

   SUBJECT BEHAVIOR:
   Woman from reference image speaking casually to camera. Natural 
   conversation about project update. Speaking pattern: pauses, "um/ah" 
   fillers, slight head tilts, occasional glance to side (as if thinking), 
   returns to camera. Subtle smile appears mid-sentence.

   CRITICAL REALISM (ANTI-DETECTION):

   EYES: 
   - Micro-saccades every 0.5s (randomized)
   - Natural blink rate 16/min with variable duration
   - Wet eye reflections showing window shape
   - Pupils dilate slightly when smiling
   - NO fixed gaze >1.5s

   SKIN: 
   - ZERO smoothing filters
   - Visible pores (especially nose/forehead)
   - Fine lines around eyes
   - Subtle color variations (slight redness on cheeks)
   - 2-3 small freckles/blemishes
   - Realistic translucency
   - T-zone slight oiliness

   MOUTH: 
   - Sharp edges, visible teeth/tongue
   - Saliva reflection
   - Natural asymmetry in smile
   - Lip texture with vertical lines

   HAIR: 
   - Individual strand movement
   - 3-5 flyaway hairs
   - Subtle air movement
   - Realistic hair-skin gradient boundary

   MICRO-MOVEMENTS: 
   - Breathing visible in shoulders
   - Natural head wobble (can't hold still)
   - Eyebrow micro-raises
   - Nose wrinkles when smiling

   LIGHTING: 
   - Soft natural window light from right
   - Subtle shadows under chin/nose
   - Window reflection in eyes as catchlight
   - Warm color temperature (3200K)

   AUDIO: 
   - Natural breathing rhythm (audible inhales)
   - Subtle lip smacks, tongue clicks
   - Faint room tone ambience
   - Variable vocal pitch
   - 1-2 "um" fillers
   - Slight reverb matching small room
   - Microphone proximity bass boost

   IMPERFECTIONS: 
   - Slight camera shake (handheld)
   - 1-2 frames motion blur during head turn
   - Subtle auto-focus breathing
   - Realistic H.264 compression
   - Add faint timestamp overlay "18:34" top-left corner

   ENVIRONMENT: 
   - Plain wall background with very subtle texture
   - Slightly out of focus
   - Warm afternoon lighting
   OUTPUT: 
   MP4, H.264, 30fps, 1920x1080, AAC audio 48kHz, duration 10 seconds.
   ```

**Why This Failed:**
This represents a **high-quality AI-generated video** from Google Veo that successfully bypassed detection. The video exhibited:
- Extremely realistic skin texture that mimicked natural pores
- Convincing facial micro-expressions
- Natural-seeming temporal consistency
- High-quality audio synthesis

**Key Lesson:** Even advanced AI detection systems can be fooled by state-of-the-art video generation models like Google Veo. This demonstrates the ongoing "arms race" between AI generation and detection technologies.

---

## 🎓 Key Findings

### Detection Accuracy
- **Success Rate:** 80% (4/5 videos correctly classified)
  - ✅ 3 deepfakes correctly identified (f1, f2, f4)
  - ✅ 1 real video correctly identified (f3)
  - ❌ 1 false negative: f5 (deepfake misclassified as real)
- **Total Tests:** 5 videos analyzed
- **Average Analysis Time:** ~9 seconds per video

### Common Deepfake Indicators Detected
1. **Facial Analysis:**
   - Over-smoothed skin (lacks pores/texture)
   - Unnatural eye movements (no micro-saccades)
   - Rigid/infrequent blinking patterns

2. **Temporal Consistency:**
   - Edge flickering at face boundaries
   - Morphing around mouth/jawline
   - Frame-to-frame inconsistencies

3. **Audio-Visual Sync:**
   - Synthetic audio quality
   - Lip-sync timing issues
   - "Rubbery" mouth movements

## 🔬 Detection Methodology

The system analyzes videos across 10 critical dimensions:

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

### Scoring System

- **0-30:** Likely authentic (minor compression artifacts acceptable)
- **31-60:** Suspicious (multiple minor or 1-2 major artifacts)
- **61-85:** High suspicion (clear AI generation indicators)
- **86-100:** Almost certainly synthetic (multiple obvious artifacts)



## 🔐 Security & Privacy

- API keys stored in `.env` file (never in code)
- Local processing only (videos not stored on cloud)
- Comprehensive logging for audit trails
- No personally identifiable information retained

## 📝 Usage Example
```python
from deepfake_detector import DeepfakeDetector

# Initialize detector
detector = DeepfakeDetector()

# Analyze videos
videos = ["f1.mp4", "f2.mp4", "f3.mp4", "f4.mp4", "f5.mp4"]
for video in videos:
    detector.analyze_video(video)

# Generate report
detector.save_report("analysis_report.json")
```

## 🐛 Troubleshooting

### Common Issues

**1. API Quota Exceeded**
```
Error: 429 RESOURCE_EXHAUSTED
Solution: Wait 60 seconds or switch to gemini-flash-lite-latest
```

**2. Model Not Found**
```
Error: 404 models/xxx is not found
Solution: Use gemini-3-flash-preview or gemini-flash-latest
```

**3. Invalid API Key**
```
Error: GOOGLE_API_KEY missing
Solution: Check .env file contains valid key
```

## 📚 References

- [Google Gemini API Documentation](https://ai.google.dev/gemini-api/docs)
- [Deepfake Detection Research](https://arxiv.org/abs/2004.11138)
- [FaceForensics++ Dataset](https://github.com/ondyari/FaceForensics)

## 👩‍💻 Author

**Anna**  
Software Engineering Instructor  
Sami Shimon College

## 📄 License

Educational use only - Part of AI Developer Course assignment

## 🙏 Acknowledgments

- Google Gemini Team for the AI model
- Course instructor for project guidance
- Open-source community for tools and libraries

---

**Last Updated:** December 27, 2025  
**Version:** 1.0.0