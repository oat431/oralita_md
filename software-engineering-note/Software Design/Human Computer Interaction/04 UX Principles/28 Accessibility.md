# 28 Accessibility (A11y)

> **Design for everyone — including people with disabilities.**

Accessibility is not a feature. It's a requirement. ~15% of the world's population has some form of disability. Accessible design helps everyone — not just people with permanent disabilities, but also people with temporary impairments (broken arm, lost glasses) and situational limitations (bright sunlight, loud environment).

---

## The Four Principles (POUR)

| Principle | Meaning | Example |
|-----------|---------|---------|
| **Perceivable** | Users can perceive the content | Text alternatives for images, captions for video |
| **Operable** | Users can operate the interface | Keyboard navigation, enough time to read, no seizure triggers |
| **Understandable** | Users can understand the content | Clear language, predictable navigation, input assistance |
| **Robust** | Works with assistive technologies | Semantic HTML, ARIA labels, screen reader compatible |

---

## Quick Wins (High Impact, Low Effort)

| Check | How |
|-------|-----|
| **Color contrast** | Text vs background ≥ 4.5:1 (body), ≥ 3:1 (large text). Use WebAIM contrast checker. |
| **Keyboard navigation** | Can you complete every task using only Tab, Enter, Escape? |
| **Alt text on images** | Every `<img>` has `alt=""` — descriptive for content, empty for decoration |
| **Focus indicators** | Visible outline on the currently focused element. Never `outline: none` without replacement. |
| **Form labels** | Every input has a `<label>` — not just placeholder text |
| **Heading hierarchy** | One `<h1>`, then `<h2>` → `<h3>` in order. Never skip levels for visual styling. |
| **Touch targets** | ≥ 44×44px. No tiny close buttons. |

---

## Who Benefits from Accessibility

| Disability Type | Examples | Design Considerations |
|----------------|----------|---------------------|
| **Visual** | Blindness, low vision, color blindness | Screen readers, contrast, don't use color alone |
| **Hearing** | Deafness, hard of hearing | Captions, transcripts, visual alerts |
| **Motor** | Limited dexterity, tremors, paralysis | Keyboard nav, large touch targets, voice input |
| **Cognitive** | Dyslexia, ADHD, memory issues | Clear language, consistent layout, reduce distractions |

---

## Accessibility = Better UX for Everyone

| Accessibility Feature | Benefits Everyone |
|----------------------|-------------------|
| High contrast text | Easier to read in bright sunlight |
| Keyboard shortcuts | Power users love them |
| Captions on video | Watch in noisy environments or without sound |
| Clear, simple language | Everyone understands faster |
| Large touch targets | No more fat-finger errors |

---

## Resources

- WCAG 2.2 Guidelines — https://www.w3.org/WAI/standards-guidelines/wcag/
- WebAIM Contrast Checker — https://webaim.org/resources/contrastchecker/
- The A11y Project — https://www.a11yproject.com/
