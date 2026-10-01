# 🔱 Power Button Law V1

## 1. Role

A NayaNET button converts:

**INTENT → ACTION**

Therefore primary button design is not finishing polish. It is core product design.

## 2. Button anatomy

A production Power Button should define:

1. material body;
2. precise perimeter edge;
3. upper specular highlight;
4. lower physical depth;
5. cast shadow;
6. semantic accent field;
7. label;
8. icon/glyph where useful;
9. focus treatment;
10. state feedback.

## 3. Resting state

The button should already feel actionable without screaming.

Use:
- dark obsidian/graphite core;
- strong text contrast;
- restrained semantic border/accent;
- subtle inner highlight;
- believable elevation.

Do not require hover to reveal that it is clickable.

## 4. Hover state

Desktop hover should communicate recognition:
- lift approximately 2px;
- sharpen edge;
- slightly brighten semantic accent;
- strengthen icon;
- adjust cast shadow.

Target transition: approximately **160–240ms** using the Naya motion signature.

No default infinite pulse.

## 5. Press state

Press must feel physical:
- translate toward the surface;
- compress scale only subtly;
- reduce cast shadow;
- deepen core;
- preserve label sharpness.

The visual press precedes or accompanies the causal action.

## 6. Focus state

Keyboard focus must be:
- immediately visible;
- aesthetically integrated;
- not dependent on hover;
- at least as easy to identify as mouse hover.

Never remove outline without replacing it with an equivalent or stronger focus indicator.

## 7. Loading state

After a consequential click:
- prevent accidental duplicate execution where needed;
- preserve button width;
- show precise progress/processing state;
- keep label or outcome context understandable.

Do not replace the whole button with an unlabeled spinner.

## 8. Success state

Use brief confirmation when appropriate:
- check/resolved glyph;
- semantic light;
- changed label;
- resulting content/state.

The primary proof of success is the actual consequence, not a green animation.

## 9. Error state

Errors must be:
- readable;
- local when possible;
- actionable;
- honest.

Never leave the button appearing successful after failure.

## 10. Disabled state

Disabled means:
- non-interactive;
- reduced energy;
- sufficient text contrast;
- reason discoverable when important.

Do not use opacity so low that text becomes inaccessible.

## 11. Button hierarchy

### Primary
One dominant next action per decision context.

### Secondary
Supportive actions with lower energy.

### Tertiary
Quiet utility.

### Destructive
Distinct, deliberate, confirmation where consequence warrants.

Never make every action "primary."

## 12. Label law

Labels must be:
- clear;
- outcome-oriented where useful;
- specific;
- concise.

Prefer:
- **Enter NayaNET**
- **Review Today's Intelligence**
- **Connect GitHub**
- **Keep Private**
- **Share With NayaNET**

Avoid:
- Submit
- Go
- Click Here
- meaningless cleverness.

## 13. Icon law inside buttons

Icons:
- support comprehension;
- never replace essential labels without strong reason;
- belong to the same NayaNET glyph family;
- use consistent size/alignment.

## 14. Touch law

Minimum interactive target should generally be **44×44 CSS px** or larger.

Primary mobile actions should feel generous.

## 15. Causal law

A beautiful button that does nothing is a defect.

Every live button must have:

`CONTROL → INTENT → AUTHORITY/SCOPE → CAPABILITY → OBSERVATION → RESULT → STATE/EVIDENCE`

If capability is unavailable, show unavailable state. Do not leave an apparently-live dead control.

## 16. Acceptance

A Power Button passes when:
- it is readable;
- obviously actionable;
- physically responsive;
- keyboard-visible;
- touch-friendly;
- semantically colored;
- truthful;
- tied to a real consequence;
- visually consistent with NayaNET;
- beautiful at rest.

**A button should feel engineered, not styled.**
