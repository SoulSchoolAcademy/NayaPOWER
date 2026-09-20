import unittest
from memory_runtime import validate_note, NOTE_ID_RE


def base():
    return {
        "id":"SN-20260823-220000-example",
        "type":"lesson","title":"Example durable lesson","status":"ACTIVE",
        "created_at":"2026-08-23T22:00:00-07:00","effective_at":"2026-08-23T22:00:00-07:00","superseded_at":None,
        "source":{"kind":"conversation","path":"conversation://example","commit":None,"conversation_ref":"example"},
        "summary":"A durable lesson stored for future retrieval and continuity.",
        "what_happened":"A useful discovery was made.","what_we_learned":["Store durable knowledge structurally."],
        "why_it_matters":"Future sessions can retrieve the lesson.","what_changed":["Added the lesson to memory."],
        "next_best_action":"Validate and index the note.","tags":["memory","continuity"],"aliases":["restore memory","context recovery"],
        "relationships":{"related":[],"supersedes":None,"superseded_by":None,"depends_on":[]}
    }

class SmartNoteTests(unittest.TestCase):
    def test_id_format(self):
        self.assertTrue(NOTE_ID_RE.match(base()["id"]))

    def test_valid_note(self):
        self.assertEqual(validate_note(base(),"fixture"),[])

    def test_rejects_missing_timestamp(self):
        n=base(); n["created_at"]="2026-08-23T22:00:00"
        self.assertTrue(validate_note(n,"fixture"))

    def test_superseded_requires_chain(self):
        n=base(); n["status"]="SUPERSEDED"
        self.assertTrue(validate_note(n,"fixture"))

    def test_canonical_cannot_be_superseded(self):
        n=base(); n["status"]="CANONICAL"; n["relationships"]["superseded_by"]="SN-20260823-220001-new"
        self.assertTrue(validate_note(n,"fixture"))

if __name__=="__main__": unittest.main()
