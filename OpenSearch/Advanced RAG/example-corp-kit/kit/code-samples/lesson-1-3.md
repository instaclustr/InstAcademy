# Lesson 1.3 code samples: Chunking, Ingestion & Retrieval Quality

## The full pipeline in this kit

```bash
cd generators
python generate_docs.py --pages 1000         # product documentation
python generate_integration_guides.py        # 50 integration guides
python generate_known_issues.py              # known issues database
python generate_api_reference.py             # API reference
python generate_tickets.py --count 10000     # 3 years of ticket history
python chunk_documents.py                    # parse -> chunk -> enrich
python generate_golden_set.py --count 300    # labeled eval queries
```

## Heading-based parent-child chunking (see chunk_documents.py)

Parents are H2 sections, children are paragraph groups under a token
budget, IDs are stable and idempotent:

```
DOC-00214#2      <- parent: "Common errors" section of DOC-00214
DOC-00214#2.0    <- child chunk 0 of that section
DOC-00214#2.1    <- child chunk 1
```

## Field-based structured chunks for tickets

Never flatten a ticket into one blob. Each chunk carries the subject,
the problem, and the resolution as labeled fields:

```json
{
  "chunk_id": "TKT-2026-000001#0.0",
  "doc_type": "support-ticket",
  "title": "ERR-1210 when opening a shared dashboard on mobile",
  "product_version": "5.0",
  "related_error_codes": ["ERR-1210"],
  "text": "Ticket: ...\n\nProblem: ...\n\nResolution: ..."
}
```

## Metadata stamped at parse time, used everywhere later

`source_id`, `section_path`, `doc_type`, `product_version`, `acl`,
`updated_at`. These power the 1.2 pre-filters and answer citations.

## Golden set format

```json
{
  "query_id": "Q-0001",
  "query": "what does ERR-4415 mean",
  "query_type": "error",
  "relevant_chunk_ids": ["KI-0010#0.0", "GUIDE-002#3.0", "DOC-00023#2.1"]
}
```

## Retrieval-only evaluation (hit rate@k, precision@k, MRR)

```bash
export OS_URL=https://user:pass@your-cluster:9200
python3 scripts/eval_retrieval.py --mode bm25 --k 5 --kb-only \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
python3 scripts/eval_retrieval.py --mode neural --k 5 --model-id <MODEL_ID> --kb-only \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
python3 scripts/eval_retrieval.py --mode hybrid --k 5 --kb-only \
  --model-id <MODEL_ID> --search-pipeline support-hybrid-rrf \
  --golden corpus/example-corp-corpus-v2.1.0/golden_set.jsonl
```

Run all three and screen-record the table: that is the ablation demo.
Triage rules: low hit rate points at parsing, chunking, or embeddings.
High hit rate with low MRR points at ranking or chunk granularity.
High precision@1 with low precision@5 points at noise in the context.
