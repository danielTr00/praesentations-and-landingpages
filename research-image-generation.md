# Research: Image Generation with Ollama x/z-image-turbo

## Model Capabilities (x/z-image-turbo)
- Based on Flux.1 model, optimized for speed
- Input: Text prompt + optional reference image
- Output: 1024x1024 or higher resolution images
- Best for: Photorealistic, abstract art, logos, UI assets

## Prompt Engineering Strategies

### 1. Style Consistency Framework
```
[Subject] in [Style] style with specific details:
- Color palette: #HEX values
- Mood/atmosphere
- Lighting description  
- Composition rules
- Technical specs (4k, vector-style, minimalist)
```

### 2. Subject-Specific Patterns

**For Financial Services Logos:**
"Minimalist geometric logo featuring [subject]. Navy blue (#0D1B2A) and gold (#C49E52) color scheme on white background. Professional, clean lines. No text. High contrast vector art style."

**For Hero Backgrounds:**
"Abstract geometric pattern suggesting security/protection. Navy gradient background (#0D1B2A to #1a2e4d) with subtle gold (#C49E52) accent shapes at 30% opacity. Professional financial aesthetic, no people or text."

### 3. Quality Boosters
- Add "high quality, detailed, professional" 
- Specify aspect ratio: "horizontal composition, 16:9 aspect ratio"
- Use "photorealistic" for product shots
- Use "vector illustration style" for icons/logos

### 4. Iterative Refinement Process
1. Generate base image with core prompt
2. View result with vision model
3. Refine prompt based on deficiencies  
4. Re-generate with adjusted parameters
5. Compare variations side-by-side

## Prompt Templates

### Hero Background Template:
```
Abstract geometric composition suggesting security and trust for financial services. 
Navy gradient from #0D1B2A to #1e293b with subtle gold accent lines at 20% opacity.
Minimalist, professional, modern aesthetic. No text or people. 
High resolution, suitable for website hero section background.
```

### Logo Template:
```
Minimalist professional logo for financial legal services. Geometric shield design 
with interlocking letters. Navy blue (#0D1B2A) and gold (#C49E52) palette on 
transparent background. Clean lines, modern vector style, high contrast.
No text elements in the logo mark itself.
```

### Icon Template:
```
Simple line art icon for [use case]. Single stroke, geometric style. Navy blue 
color (#0D1B2A) with optional gold accent. Minimalist design suitable for web UI, 
professional and clean. Square composition with clear negative space.
```

## Best Practices Discovered
1. **Specific hex codes** produce more consistent results than color names
2. **"Navy blue" alone is vague** - use #0D1B2A or specify depth
3. **Specify opacity percentages** for layering effects  
4. **Avoid too many elements** in single prompts for logos
5. **Test multiple variations** and keep the best 2-3
6. **Consistent aspect ratios** across image set improve brand coherence

## Testing Framework
For each generated image:
1. Check resolution (should be ≥1024px on shortest side)  
2. Verify color consistency with brand palette
3. Test at small sizes (16px, 32px, 64px) for legibility
4. Evaluate contrast ratio for accessibility (WCAG AA+)
5. Compress to WebP format for web delivery
