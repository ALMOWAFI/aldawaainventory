# 📹 Video Testing Guide - Test Before You Invest!

## 🎯 Why Video Testing First?

Testing with videos before buying smart glasses is SMART because:
- ✅ **No hardware cost** - Use your phone
- ✅ **Test the whole system** - AI agents, decisions, human review
- ✅ **Find issues early** - Fix problems before going live
- ✅ **Train your team** - Practice without pressure
- ✅ **Build confidence** - See it work before investing

## 🚀 Quick Start Testing

### Step 1: Record Test Video

#### 📱 Using Your Phone
```markdown
1. Open camera app
2. Set to 1080p video
3. Hold phone steady
4. Walk through one aisle
5. Focus on each product for 2-3 seconds
6. Record for 2-5 minutes max
```

#### 🎥 What to Capture
- **Product fronts** - Show labels clearly
- **Barcodes** - Get close enough to read
- **Expiry dates** - Focus on date area
- **Shelf edges** - For quantity counting
- **Problem products** - Damaged, expired, etc.

### Step 2: Upload Video to n8n

#### Option A: Simple Web Upload
```html
<!-- Create simple upload page -->
<!DOCTYPE html>
<html>
<head>
    <title>Inventory Video Upload</title>
</head>
<body>
    <h1>Upload Inventory Video</h1>
    <form id="uploadForm">
        <input type="file" id="video" accept="video/*" required>
        <input type="text" id="workerId" placeholder="Your ID" required>
        <input type="text" id="location" placeholder="Aisle/Location" required>
        <button type="submit">Upload Video</button>
    </form>
    
    <div id="status"></div>

    <script>
    document.getElementById('uploadForm').onsubmit = async (e) => {
        e.preventDefault();
        const status = document.getElementById('status');
        status.textContent = 'Uploading...';
        
        const formData = new FormData();
        formData.append('video', document.getElementById('video').files[0]);
        formData.append('workerId', document.getElementById('workerId').value);
        formData.append('location', document.getElementById('location').value);
        
        try {
            const response = await fetch('YOUR_N8N_WEBHOOK_URL/inventory-video-upload', {
                method: 'POST',
                body: formData
            });
            
            if (response.ok) {
                status.textContent = '✅ Upload successful! Check dashboard for results.';
            } else {
                status.textContent = '❌ Upload failed. Try again.';
            }
        } catch (error) {
            status.textContent = '❌ Error: ' + error.message;
        }
    };
    </script>
</body>
</html>
```

#### Option B: Using cURL
```bash
curl -X POST YOUR_N8N_WEBHOOK_URL/inventory-video-upload \
  -F "video=@/path/to/your/video.mp4" \
  -F "workerId=emp001" \
  -F "location=aisle-3"
```

#### Option C: Using Postman
1. Create new POST request
2. Set URL: `YOUR_N8N_WEBHOOK_URL/inventory-video-upload`
3. Body → form-data
4. Add fields: video (file), workerId, location
5. Send

### Step 3: Watch the Magic Happen

The workflow will:
1. **Extract frames** - Every 0.5 seconds
2. **Detect products** - Using computer vision
3. **Read text** - OCR for expiry dates
4. **Identify products** - Match to database
5. **Make decisions** - Flag issues
6. **Generate report** - Show results

## 📊 Understanding Results

### Dashboard View
```json
{
  "summary": {
    "totalProducts": 45,
    "highConfidence": 38,
    "needsReview": 7,
    "expired": 2,
    "damaged": 3
  },
  
  "products": [
    {
      "productId": "MED-001",
      "name": "Aspirin 100mg",
      "confidence": 0.95,
      "quantity": 12,
      "expiryDate": "2024-12-31",
      "status": "OK",
      "frameImage": "base64..."
    }
  ],
  
  "reviewRequired": [
    {
      "frameTime": "0:23",
      "reason": "Cannot read expiry date",
      "image": "base64..."
    }
  ]
}
```

### What to Look For
- **✅ High confidence** (>90%) = System working well
- **⚠️ Medium confidence** (70-90%) = May need better video
- **❌ Low confidence** (<70%) = Needs manual review

## 🎬 Video Recording Best Practices

### DO ✅
- **Good lighting** - Natural or bright LED
- **Steady movement** - Walk slowly
- **Focus time** - 2-3 seconds per product
- **Multiple angles** - If product unclear
- **Test different times** - Morning vs afternoon light

### DON'T ❌
- **Rush** - Speed causes blur
- **Shake** - Use both hands
- **Skip products** - Capture everything
- **Poor lighting** - Avoid shadows
- **Vertical video** - Use horizontal

## 🧪 Test Scenarios

### Scenario 1: Normal Products
```markdown
1. Record aisle with regular products
2. Upload video
3. Check: 90%+ should be detected correctly
4. Review any flagged items
```

### Scenario 2: Problem Products
```markdown
1. Include some expired/damaged items
2. Upload video
3. Verify: System flags these correctly
4. Test human review process
```

### Scenario 3: Difficult Areas
```markdown
1. Record crowded shelves
2. Include poor lighting areas
3. Upload and check results
4. Identify improvement needs
```

## 📈 Measuring Success

### Phase 1: Basic Detection (Week 1)
- Goal: 80% product detection
- Metric: Products found vs actual
- Action: Improve video quality if low

### Phase 2: Accuracy (Week 2)  
- Goal: 90% correct identification
- Metric: Correct IDs vs total
- Action: Update product database

### Phase 3: Edge Cases (Week 3)
- Goal: 100% critical issues caught
- Metric: Expired/damaged detection
- Action: Refine detection rules

## 🔧 Troubleshooting

### Problem: Low Detection Rate
```javascript
// Adjust detection sensitivity
const detectionConfig = {
  confidence_threshold: 0.6,  // Lower from 0.7
  min_object_size: 50,        // Smaller objects
  enhance_contrast: true      // Better visibility
};
```

### Problem: Many False Positives
```javascript
// Increase confidence requirements
const detectionConfig = {
  confidence_threshold: 0.8,  // Higher threshold
  require_barcode: true,      // Must have barcode
  verify_text: true           // Cross-check OCR
};
```

### Problem: Slow Processing
- Reduce video resolution to 720p
- Shorter videos (2-3 minutes)
- Process one aisle at a time

## 💡 Pro Tips for Testing

### 1. Start Small
- Test 10 products first
- One shelf, not whole aisle
- 30-second video clips

### 2. Iterate Quickly
- Upload → Review → Adjust → Repeat
- Fix issues immediately
- Document what works

### 3. Involve Your Team
- Let workers try recording
- Get feedback on results
- Practice review process

### 4. Build Test Dataset
- Save good/bad examples
- Create training videos
- Document edge cases

## 🎯 When You're Ready for Smart Glasses

### Success Indicators
- ✅ 90%+ detection accuracy
- ✅ <5% need human review
- ✅ All edge cases handled
- ✅ Team comfortable with process
- ✅ ROI calculations positive

### Next Steps
1. **Choose smart glasses** - Based on your needs
2. **Pilot with one device** - Test in real conditions
3. **Train workers** - Using your video insights
4. **Scale gradually** - Add devices as needed

## 📝 Testing Checklist

- [ ] Record first test video
- [ ] Upload to n8n workflow
- [ ] Review detection results
- [ ] Test human review flow
- [ ] Try problem products
- [ ] Measure accuracy rates
- [ ] Document issues found
- [ ] Refine configuration
- [ ] Train team members
- [ ] Calculate time savings

## 🚀 Sample Testing Timeline

### Week 1: Basic Testing
- Day 1-2: Set up workflow, record first videos
- Day 3-4: Test detection, review results
- Day 5: Adjust parameters, document findings

### Week 2: Refinement
- Day 1-2: Test edge cases (damaged, expired)
- Day 3-4: Human review process testing
- Day 5: Team training on video recording

### Week 3: Validation
- Day 1-2: Full aisle tests
- Day 3-4: Accuracy measurements
- Day 5: Go/no-go decision for smart glasses

Remember: **Video testing is FREE** and gives you real data to make smart decisions! 🎉 