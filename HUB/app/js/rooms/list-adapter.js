/* LIST ADAPTER — smart note files -> note view-models.
 *
 * Canonical source: BRAIN/05-MEMORY/SMART-NOTES/2026/* IB-SMART-NOTE*.md.
 * Each file carries `# Title`, `## IN A NUTSHELL`, `**Truth state:**`,
 * `**Captured:**`, and its taxonomy in the path. Projection only:
 * unparseable files are skipped, never invented.
 *
 *   const notes = ListAdapter.parseNotes([{path, content}, ...]);
 *   // -> [{id, title, nutshell, truth, date, category, path}]
 *   // category: e.g. "SYSTEM-INTELLIGENCE/ACTIVE-INTELLIGENCE"
 *   sorted newest-first by date.
 */
(function(){
  'use strict';

  function parseNote(file){
    if(!file || typeof file.content !== 'string' || typeof file.path !== 'string') return null;
    var s = file.content;

    var titleMatch = s.match(/^#[ \t]+(.+)$/m);
    if(!titleMatch) return null; // title is required; without it, skip
    var title = titleMatch[1].trim().replace(/^[#\s\W]+/, '');

    var truthMatch = s.match(/\*\*Truth state:\*\*\s*([^\n*]+)/);
    var truth = truthMatch ? truthMatch[1].trim().toUpperCase().split(/\s/)[0] : 'UNKNOWN';

    var dateMatch = s.match(/\*\*Captured:\*\*\s*([0-9]{4}-[0-9]{2}-[0-9]{2})/);
    var date = dateMatch ? dateMatch[1] : '';

    var nutshell = '';
    var nutIdx = s.search(/##[ \t]*.*IN A NUTSHELL/);
    if(nutIdx >= 0){
      var rest = s.slice(nutIdx).split('\n').slice(1).join('\n');
      var end = rest.search(/^##[ \t]/m);
      if(end >= 0) rest = rest.slice(0, end);
      nutshell = rest.replace(/^>\s?/gm, '').replace(/\*\*/g, '')
                     .replace(/\s+/g, ' ').trim().slice(0, 1200);
    }

    var category = 'UNCATEGORIZED';
    var taxMatch = file.path.match(/SMART-NOTES\/2026\/[0-9]{2}\/[0-9]{2}\/([^/]+\/[^/]+)/);
    if(taxMatch) category = taxMatch[1];

    var base = file.path.split('/').pop() || '';
    var id = base.replace(/\.md$/i, '');

    return {
      id: id,
      title: title,
      nutshell: nutshell,
      truth: truth,
      date: date,
      category: category,
      path: file.path,
      body: s.trim()
    };
  }

  function parseNotes(files){
    var out = [];
    (files || []).forEach(function(f){
      try{
        var n = parseNote(f);
        if(n) out.push(n);
      }catch(err){ /* skip unparseable */ }
    });
    out.sort(function(a, b){ return String(b.date).localeCompare(String(a.date)); });
    return out;
  }

  window.ListAdapter = { parseNote: parseNote, parseNotes: parseNotes };
})();
