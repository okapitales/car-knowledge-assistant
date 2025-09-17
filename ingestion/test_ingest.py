import pytest
from ingest import clean_text, chunk_text, run_pipeline

def test_clean_text_removes_html():
    raw = "This is <b>bold</b> text!"
    cleaned = clean_text(raw)
    assert "<b>" not in cleaned
    assert "bold" in cleaned

def test_clean_text_removes_special_chars():
    raw = "Hello@@ World###"
    cleaned = clean_text(raw)
    assert "@" not in cleaned
    assert "#" not in cleaned

def test_chunk_text_splits_correctly():
    docs = ["word"] * 1000
    chunks = chunk_text(docs, chunk_size=100, overlap=10)
    assert all(len(c.split()) <= 100 for c in chunks)
    assert len(chunks) > 1

def test_pipeline_runs():
    docs = ["Hello world", "Another document"]
    chunks = run_pipeline(docs, "test_output")
    assert len(chunks) > 0
