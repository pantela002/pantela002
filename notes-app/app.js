import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';
import { SUPABASE_URL, SUPABASE_ANON_KEY } from './config.js';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
const $ = (id) => document.getElementById(id);

let notes = [];
let currentId = null;
let dirty = false;
let shownFor = null;

// ---------- Auth ----------

supabase.auth.onAuthStateChange((_event, session) => {
  if (session) showApp(session.user);
  else showLogin();
});

$('login-form').addEventListener('submit', async (e) => {
  e.preventDefault();
  const btn = e.submitter;
  btn.disabled = true;
  $('login-error').textContent = '';
  const { error } = await supabase.auth.signInWithPassword({
    email: $('email').value.trim(),
    password: $('password').value,
  });
  btn.disabled = false;
  if (error) $('login-error').textContent = 'Wrong email or password.';
  $('password').value = '';
});

$('logout').addEventListener('click', async () => {
  if (dirty && !confirm('You have unsaved changes. Log out anyway?')) return;
  await supabase.auth.signOut();
});

function showLogin() {
  shownFor = null;
  notes = [];
  currentId = null;
  dirty = false;
  $('note-list').replaceChildren();
  $('app-view').hidden = true;
  $('login-view').hidden = false;
  $('email').focus();
}

async function showApp(user) {
  $('login-view').hidden = true;
  $('app-view').hidden = false;
  $('user-email').textContent = user.email;
  if (shownFor === user.id) return; // token refresh, not a new login
  shownFor = user.id;
  await loadNotes();
}

// ---------- Notes ----------

async function loadNotes() {
  const { data, error } = await supabase
    .from('notes')
    .select('id, title, body, updated_at')
    .order('updated_at', { ascending: false });
  if (error) return alert('Could not load notes: ' + error.message);
  notes = data;
  renderList();
  closeEditor();
}

function renderList() {
  const q = $('search').value.trim().toLowerCase();
  const items = notes
    .filter((n) => !q || n.title.toLowerCase().includes(q) || n.body.toLowerCase().includes(q))
    .map((n) => {
      const li = document.createElement('li');
      li.className = n.id === currentId ? 'active' : '';
      const t = document.createElement('div');
      t.className = 't';
      t.textContent = n.title || 'Untitled';
      const d = document.createElement('div');
      d.className = 'd';
      d.textContent = new Date(n.updated_at).toLocaleString();
      li.append(t, d);
      li.addEventListener('click', () => openNote(n.id));
      return li;
    });
  $('note-list').replaceChildren(...items);
}

function confirmDiscard() {
  return !dirty || confirm('Discard unsaved changes?');
}

function openNote(id) {
  if (id !== currentId && !confirmDiscard()) return;
  const n = notes.find((x) => x.id === id);
  if (!n) return;
  currentId = id;
  dirty = false;
  $('title').value = n.title;
  $('body').value = n.body;
  $('save-state').textContent = 'Saved';
  $('delete').hidden = false;
  showEditor();
  renderList();
}

function newNote() {
  if (!confirmDiscard()) return;
  currentId = null;
  dirty = false;
  $('title').value = '';
  $('body').value = '';
  $('save-state').textContent = 'New note';
  $('delete').hidden = true;
  showEditor();
  renderList();
  $('title').focus();
}

function showEditor() {
  $('empty').hidden = true;
  $('editor-form').hidden = false;
  $('app-view').classList.add('editing');
}

function closeEditor() {
  currentId = null;
  dirty = false;
  $('editor-form').hidden = true;
  $('empty').hidden = false;
  $('app-view').classList.remove('editing');
  renderList();
}

async function save() {
  const fields = { title: $('title').value.trim(), body: $('body').value };
  if (!currentId && !fields.title && !fields.body) return;
  $('save-state').textContent = 'Saving…';

  const query = currentId
    ? supabase.from('notes').update(fields).eq('id', currentId)
    : supabase.from('notes').insert(fields);
  const { data, error } = await query.select('id, title, body, updated_at').single();

  if (error) {
    $('save-state').textContent = 'Not saved: ' + error.message;
    return;
  }
  notes = [data, ...notes.filter((n) => n.id !== data.id)];
  currentId = data.id;
  dirty = false;
  $('delete').hidden = false;
  $('save-state').textContent = 'Saved';
  renderList();
}

async function remove() {
  if (!currentId || !confirm('Delete this note?')) return;
  const { error } = await supabase.from('notes').delete().eq('id', currentId);
  if (error) return alert('Could not delete: ' + error.message);
  notes = notes.filter((n) => n.id !== currentId);
  closeEditor();
}

// ---------- Wiring ----------

$('new-note').addEventListener('click', newNote);
$('search').addEventListener('input', renderList);
$('delete').addEventListener('click', remove);
$('back').addEventListener('click', () => confirmDiscard() && closeEditor());
$('editor-form').addEventListener('submit', (e) => {
  e.preventDefault();
  save();
});
for (const id of ['title', 'body']) {
  $(id).addEventListener('input', () => {
    dirty = true;
    $('save-state').textContent = 'Unsaved changes';
  });
}
document.addEventListener('keydown', (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === 's' && !$('editor-form').hidden) {
    e.preventDefault();
    save();
  }
});
window.addEventListener('beforeunload', (e) => {
  if (dirty) e.preventDefault();
});
