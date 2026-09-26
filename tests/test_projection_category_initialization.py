from pathlib import Path


def test_projection_category_is_initialized_before_use():
    source = Path("supabase/functions/v7-smart-note-canonical/index.ts").read_text(encoding="utf-8")
    use = source.index("projection_category:projectionCategory")
    declaration = source.index("const projectionCategory=")
    assert declaration < use, "projectionCategory is referenced before initialization"


def test_projection_topic_is_initialized_before_use():
    source = Path("supabase/functions/v7-smart-note-canonical/index.ts").read_text(encoding="utf-8")
    use = source.index("projection_topic:projectionTopic")
    declaration = source.index("const projectionTopic=")
    assert declaration < use, "projectionTopic is referenced before initialization"
