# Smart Note Capture — Author's Door

This directory is the **one authored ingestion boundary** for Smart Notes. It is not the Brain and it is not the permanent human-readable library.

## One source in

Author **one conformant JSON capture** under:

`.naya/capture/`

Schema: `naya.smart-note-capture.v2`.

The JSON carries the structured human, child/simple, Naya/AI, machine, learning, applicability, connection, provenance and uncertainty views required by the governed pipeline.

## One governed path out

After the capture is authorized to merge, the existing pipeline persists and verifies the canonical Intelligent Block. The **only canonical renderer**:

`tools/smart_note_v2.py`

generates the readable projection under:

`BRAIN/05-MEMORY/SMART-NOTES/YYYY/MM/DD/CATEGORY/TOPIC/SUBTOPIC/SN-###/IB-....md`

The machine registry remains:

`.naya/memory/smart-notes/index.json`

The registry is an index/pointer surface. It is **not** the human Smart Note library.

## Flow

`INTENT → AUTHOR JSON → MERGE/AUTHORITY → PERSIST → VERIFY → PROJECT → SMART LINK → COLD RETRIEVE → COMPREHEND → APPLY → OBSERVE → VERIFY OUTCOME → LEARN → SUCCESSOR REUSE`

## MUST

- one changed capture per PR/run;
- explicit, unclaimed `smart_note_id`;
- `machine_view.raw_source_separate_from_distillation: true`;
- `machine_view.automatic_truth_ceiling: "CANDIDATE"`;
- use the canonical renderer and canonical Brain path;
- return the generated Smart Link only after the pipeline actually creates it;
- claim learning only after later behavioral proof.

## MUST NOT

- do **not** create `.naya/preview/`;
- do **not** hand-write a Brain Smart Note projection;
- do **not** create a second renderer;
- do **not** use `.naya/memory/smart-notes/YYYY/...` as the human projection path;
- do **not** call a capture VERIFIED, ACTIVE, LEARNED or RATIFIED without the evidence/authority that earns that state.

**Stored ≠ learned. Generated ≠ verified outcome. A page existing is not proof of successor behavior.**
