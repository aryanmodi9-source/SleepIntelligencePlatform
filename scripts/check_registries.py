#!/usr/bin/env python3
"""Registry integrity check for Phase R (CLAUDE.md §33.1).

The canonical registry schemas live in SCHEMAS below. Each registry YAML file
carries a copy of its schema under `schema:` so it is self-describing; the
check fails if that copy drifts from the canonical one.

Checks performed:
  * every registry file exists, parses, and declares the canonical schema
  * every entry has the required fields, valid IDs, and valid enum values
  * IDs are unique and never reuse a retired ID (`retired_ids`)
  * with --since REF: no ID present at git REF has disappeared without being
    listed in `retired_ids` (IDs are stable and never reused)
  * every referenced ID exists (registry cross-references, and IDs mentioned
    in Markdown files under docs/)
  * every evidence record's source_id exists in sources.yaml
  * evidence read_level does not exceed its source's read_level
  * quantitative evidence without FULL_TEXT + location is UNVERIFIED_FIGURE (§7)
  * ABSTRACT_ONLY / SECONDARY_CITATION evidence cannot be STRONG for a
    quantitative claim (§9 access cap)
  * claim-status constraints (§10)
  * PROVISIONAL decisions carry rationale, invalidation conditions and the
    experiment needed for resolution; RESOLVED decisions record a human
    resolver (§35)
  * no RESOLVED decision relies solely on UNVERIFIED_FIGURE evidence or
    ABSTRACT_ONLY sources for quantitative justification
  * every requirement traces to at least one decision, or is labeled
    ENGINEERING_ASSUMPTION (§33.1, §39)

Usage:
  python scripts/check_registries.py            # run all checks
  python scripts/check_registries.py --since main
  python scripts/check_registries.py --init     # create missing empty registries

Exit status 0 when all checks pass, 1 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_VERSION = 1

# --------------------------------------------------------------------------
# Controlled vocabularies (CLAUDE.md section in brackets)
# --------------------------------------------------------------------------

PRIORITY = ["P0", "P1", "P2", "P3"]  # §4
READ_LEVEL = ["FULL_TEXT", "ABSTRACT_ONLY", "SECONDARY_CITATION"]  # §6
READ_LEVEL_RANK = {"SECONDARY_CITATION": 0, "ABSTRACT_ONLY": 1, "FULL_TEXT": 2}
EVIDENCE_TIER = [  # §5.2, in hierarchy order
    "SYSTEMATIC_REVIEW_OR_META_ANALYSIS",
    "METHODOLOGICAL_REVIEW",
    "PRIMARY_VALIDATION_STUDY",
    "OFFICIAL_DATASET_DOCUMENTATION",
    "STANDARD_OR_OFFICIAL_TECHNICAL_DOCUMENTATION",
    "CONFERENCE_PUBLICATION",
    "PREPRINT",
    "SECONDARY_TECHNICAL_SOURCE",
    # Not in the §5.2 hierarchy: project exploratory analysis (§7, §40).
    "PROJECT_ANALYSIS",
]
SOURCE_TYPE = [
    "JOURNAL_ARTICLE",
    "REVIEW_ARTICLE",
    "CONFERENCE_PAPER",
    "PREPRINT",
    "BOOK_OR_CHAPTER",
    "DATASET_DOCUMENTATION",
    "DATASET_PUBLICATION",
    "STANDARD",
    "DATASHEET",
    "TECHNICAL_DOCUMENTATION",
    "REGULATORY_DOCUMENT",
    "WEB_PAGE",
    "PROJECT_ANALYSIS_SCRIPT",
]
RETRIEVAL_STATUS = ["RETRIEVED", "METADATA_ONLY", "NOT_RETRIEVED", "FAILED"]
REFERENCE_STATUS = [  # §8, set during reference verification
    "VERIFIED_AND_REVIEWED",
    "VERIFIED_ABSTRACT_ONLY",
    "SECONDARY_ONLY",
    "UNRESOLVED",
    "KNOWN_TO_EXIST_NOT_REVIEWED",
    "NOT_YET_CHECKED",
]
EVIDENCE_STRENGTH = ["STRONG", "MODERATE", "LIMITED", "CONFLICTING", "INSUFFICIENT"]  # §9
STRENGTH_DIMENSIONS = [  # §9
    "consistency",
    "independent_datasets",
    "reference_standard_quality",
    "population_match",
    "sleep_sdb_relevance",
    "sensor_modality_match",
    "reflective_vs_transmissive",
    "read_level",
    "methodological_quality",
]
FIGURE_VERIFICATION = ["VERIFIED", "UNVERIFIED_FIGURE", "NOT_APPLICABLE"]  # §7
LOCATION_TYPE = ["table", "figure", "section", "page", "equation", "script"]  # §7, §40
CLAIM_STATUS = [  # §10
    "ESTABLISHED",
    "SUPPORTED",
    "CONTEXT_DEPENDENT",
    "PRELIMINARY",
    "CONFLICTING",
    "HYPOTHESIS",
    "UNKNOWN",
]
CONFIDENCE = ["HIGH", "MEDIUM", "LOW"]  # scale not defined in CLAUDE.md; project choice
DECISION_STATUS = ["OPEN", "PROVISIONAL", "RESOLVED", "REJECTED", "NOT_APPLICABLE"]  # §35
EXPERIMENT_STATUS = ["PROPOSED", "APPROVED", "RUNNING", "COMPLETED", "ABANDONED"]
REQUIREMENT_STATUS = ["DRAFT", "PROPOSED", "APPROVED", "DEFERRED", "REJECTED"]
TRACEABILITY_TYPE = ["EVIDENCE", "ENGINEERING_CONSTRAINT", "ENGINEERING_ASSUMPTION"]  # §36
GAP_CATEGORY = [  # §41
    "LITERATURE_GAP",
    "DATASET_GAP",
    "PHYSIOLOGICAL_GAP",
    "MEASUREMENT_GAP",
    "ALGORITHM_GAP",
    "VALIDATION_GAP",
    "HARDWARE_GAP",
    "EMBEDDED_GAP",
    "CLINICAL_TRANSLATION_GAP",
    "ACCESS_GAP",
]
PHASE = ["PHASE_R", "PHASE_E", "BOTH", "FUTURE"]
UNIT_OF_INFERENCE = ["sample", "pulse", "event", "window", "recording", "subject"]  # §33

# --------------------------------------------------------------------------
# Canonical schemas
#
# Field spec keys: type (str|int|bool|date|list|dict|any), required (key must
# be present), nullable (value may be null/empty), enum, ref (registry whose
# IDs the value(s) must reference), item_enum (for lists of enums).
# --------------------------------------------------------------------------


def f(type_, required=True, nullable=False, enum=None, ref=None, item_enum=None):
    spec = {"type": type_, "required": required, "nullable": nullable}
    if enum:
        spec["enum"] = enum
    if item_enum:
        spec["item_enum"] = item_enum
    if ref:
        spec["ref"] = ref
    return spec


SCHEMAS: dict[str, dict] = {
    "sources": {
        "path": "docs/evidence/sources.yaml",
        "id_field": "source_id",
        "id_pattern": r"^SRC-\d{3,}$",
        "section": "§6, §8",
        "fields": {
            "source_id": f("str"),
            "title": f("str"),
            "authors": f("list"),
            "year": f("int", nullable=True),
            "doi": f("str", nullable=True),
            "url": f("str", nullable=True),
            "source_type": f("str", enum=SOURCE_TYPE),
            "evidence_tier": f("str", enum=EVIDENCE_TIER),
            "retrieval_status": f("str", enum=RETRIEVAL_STATUS),
            "read_level": f("str", enum=READ_LEVEL),
            "access_date": f("date"),
            "retrieval_route": f("str", required=False, nullable=True),
            "reference_status": f("str", required=False, enum=REFERENCE_STATUS),
            "notes": f("str", required=False, nullable=True),
        },
    },
    "evidence": {
        "path": "docs/evidence/evidence.yaml",
        "id_field": "id",
        "id_pattern": r"^EVD-\d{3,}$",
        "section": "§7, §9, §37",
        "fields": {
            "id": f("str"),
            "source_id": f("str", ref="sources"),
            "claim": f("str"),
            "topic": f("str"),
            "research_question": f("str"),
            "read_level": f("str", enum=READ_LEVEL),
            "location": f("dict", nullable=True),  # {type: LOCATION_TYPE, ref: str}
            "quantitative": f("bool"),
            "figure_verification": f("str", enum=FIGURE_VERIFICATION),
            "evidence_strength": f("str", enum=EVIDENCE_STRENGTH),
            "strength_justification": f("dict"),  # {dimension: one-line reason}
            "population": f("str", nullable=True),
            "dataset": f("str", nullable=True),
            "modality": f("str", nullable=True),
            "reference_standard": f("str", nullable=True),
            "finding": f("str"),
            "limitations": f("str", nullable=True),
            "phase_e_implication": f("str", nullable=True),
            "reproducibility": f("dict", required=False, nullable=True),  # §40
        },
    },
    "claims": {
        "path": "docs/evidence/claims.yaml",
        "id_field": "id",
        "id_pattern": r"^CLM-\d{3,}$",
        "section": "§10, §38, §42",
        "fields": {
            "id": f("str"),
            "claim": f("str"),
            "claim_type": f("str"),
            "evidence_ids": f("list", nullable=True, ref="evidence"),
            "status": f("str", enum=CLAIM_STATUS),
            "confidence": f("str", enum=CONFIDENCE),
            "limitations": f("str", nullable=True),
            "decision_ids": f("list", nullable=True, ref="decisions"),
            "requirement_ids": f("list", nullable=True, ref="requirements"),
            # §42 assumption-challenge fields
            "supporting_evidence_ids": f("list", required=False, nullable=True, ref="evidence"),
            "contradicting_evidence_ids": f("list", required=False, nullable=True, ref="evidence"),
            "conditions_valid": f("str", required=False, nullable=True),
            "conditions_invalid": f("str", required=False, nullable=True),
            "phase_e_implication": f("str", required=False, nullable=True),
        },
    },
    "decisions": {
        "path": "docs/decisions/decisions.yaml",
        "id_field": "id",
        "id_pattern": r"^DEC-\d{3,}$",
        "section": "§35",
        "fields": {
            "id": f("str"),
            "question": f("str"),
            "status": f("str", enum=DECISION_STATUS),
            "priority": f("str", enum=PRIORITY),
            "evidence_ids": f("list", nullable=True, ref="evidence"),
            "candidate_options": f("list"),
            "advantages": f("any", nullable=True),
            "limitations": f("any", nullable=True),
            "experiments_required": f("list", nullable=True, ref="experiments"),
            "recommendation": f("str", nullable=True),
            "confidence": f("str", nullable=True, enum=CONFIDENCE),
            "phase_e_implication": f("str", nullable=True),
            "human_review_required": f("bool"),
            "provisional_rationale": f("str", required=False, nullable=True),
            "invalidation_conditions": f("str", required=False, nullable=True),
            "dataset_dependencies": f("list", required=False, nullable=True),  # §15
            "gap_ids": f("list", required=False, nullable=True, ref="gaps"),
            "resolved_by": f("str", required=False, nullable=True),
            "resolved_date": f("date", required=False, nullable=True),
            "history": f("list", required=False, nullable=True),  # decision updates, §11
        },
    },
    "experiments": {
        "path": "docs/experiments/experiments.yaml",
        "id_field": "id",
        "id_pattern": r"^EXP-[A-Z][A-Z0-9]*-\d{3,}$",
        "section": "§34",
        "fields": {
            "id": f("str"),
            "question": f("str"),
            "hypothesis": f("str"),
            "priority": f("str", enum=PRIORITY),
            "dataset": f("any"),
            "population": f("str", nullable=True),
            "input": f("str"),
            "reference": f("str"),
            "candidate_method": f("any"),
            "parameters": f("any", nullable=True),
            "primary_metric": f("str"),
            "secondary_metrics": f("list", nullable=True),
            "statistical_method": f("str"),
            "unit_of_inference": f("str", enum=UNIT_OF_INFERENCE),
            "decision_affected": f("list", ref="decisions"),
            "acceptance_condition": f("str"),
            "failure_condition": f("str"),
            "status": f("str", enum=EXPERIMENT_STATUS),
        },
    },
    "requirements": {
        "path": "docs/requirements/phase_e_requirements.yaml",
        "id_field": "id",
        "id_pattern": r"^REQ-\d{3,}$",
        "section": "§36, §39",
        "fields": {
            "id": f("str"),
            "requirement": f("str"),
            "reason": f("str"),
            "evidence_ids": f("list", nullable=True, ref="evidence"),
            "decision_ids": f("list", nullable=True, ref="decisions"),
            "experiment_ids": f("list", nullable=True, ref="experiments"),
            "priority": f("str", enum=PRIORITY),
            "dependency": f("any", nullable=True),
            "phase_e_component": f("str"),
            "acceptance_criterion": f("str"),
            "traceability_type": f("str", enum=TRACEABILITY_TYPE),
            "status": f("str", enum=REQUIREMENT_STATUS),
        },
    },
    "gaps": {
        "path": "docs/research_gaps.yaml",
        "id_field": "id",
        "id_pattern": r"^GAP-\d{3,}$",
        "section": "§41, §48.2",
        "fields": {
            "id": f("str"),
            "gap": f("str"),
            "category": f("str", enum=GAP_CATEGORY),
            "evidence_ids": f("list", nullable=True, ref="evidence"),
            "source_ids": f("list", required=False, nullable=True, ref="sources"),
            "why_it_matters": f("str"),
            "current_workaround": f("str", nullable=True),
            "experiment_needed": f("str", nullable=True),
            "experiment_ids": f("list", required=False, nullable=True, ref="experiments"),
            "priority": f("str", enum=PRIORITY),
            "phase_affected": f("str", enum=PHASE),
        },
    },
}

MD_ID_RE = re.compile(r"\b(SRC|EVD|CLM|DEC|REQ|GAP)-\d{3,}\b|\bEXP-[A-Z][A-Z0-9]*-\d{3,}\b")


def schema_doc(name: str) -> dict:
    """The schema block written into (and expected in) a registry file."""
    s = SCHEMAS[name]
    return {
        "schema_version": SCHEMA_VERSION,
        "registry": name,
        "spec_sections": s["section"],
        "id_field": s["id_field"],
        "id_pattern": s["id_pattern"],
        "fields": s["fields"],
    }


# --------------------------------------------------------------------------
# Checking
# --------------------------------------------------------------------------


class Report:
    def __init__(self) -> None:
        self.errors: list[str] = []

    def err(self, where: str, msg: str) -> None:
        self.errors.append(f"{where}: {msg}")


def is_empty(v) -> bool:
    return v is None or v == "" or v == [] or v == {}


def type_ok(type_: str, v) -> bool:
    if type_ == "any":
        return True
    if type_ == "str":
        return isinstance(v, str)
    if type_ == "int":
        return isinstance(v, int) and not isinstance(v, bool)
    if type_ == "bool":
        return isinstance(v, bool)
    if type_ == "list":
        return isinstance(v, list)
    if type_ == "dict":
        return isinstance(v, dict)
    if type_ == "date":
        if isinstance(v, dt.date):
            return True
        if isinstance(v, str):
            try:
                dt.date.fromisoformat(v)
                return True
            except ValueError:
                return False
    return False


def load_registries(rep: Report) -> dict[str, dict]:
    data: dict[str, dict] = {}
    for name, s in SCHEMAS.items():
        path = REPO_ROOT / s["path"]
        where = s["path"]
        if not path.exists():
            rep.err(where, "registry file missing (run with --init)")
            continue
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError as e:
            rep.err(where, f"YAML parse error: {e}")
            continue
        if not isinstance(doc, dict):
            rep.err(where, "top level must be a mapping")
            continue
        if doc.get("schema") != schema_doc(name):
            rep.err(where, "declared `schema` differs from canonical schema in check_registries.py")
        entries = doc.get("entries")
        if not isinstance(entries, list):
            rep.err(where, "`entries` must be a list")
            entries = []
        retired = doc.get("retired_ids") or []
        if not isinstance(retired, list):
            rep.err(where, "`retired_ids` must be a list")
            retired = []
        data[name] = {"entries": entries, "retired": retired}
    return data


def check_entries(data: dict[str, dict], rep: Report) -> dict[str, dict[str, dict]]:
    """Validate fields; return {registry: {id: entry}}."""
    index: dict[str, dict[str, dict]] = {}
    for name, d in data.items():
        s = SCHEMAS[name]
        idf, pat = s["id_field"], re.compile(s["id_pattern"])
        ids: dict[str, dict] = {}
        for rid in d["retired"]:
            if not isinstance(rid, str) or not pat.match(rid):
                rep.err(s["path"], f"retired id {rid!r} does not match {s['id_pattern']}")
        for i, e in enumerate(d["entries"]):
            where = f"{s['path']}[{i}]"
            if not isinstance(e, dict):
                rep.err(where, "entry must be a mapping")
                continue
            eid = e.get(idf)
            if isinstance(eid, str):
                where = f"{s['path']}:{eid}"
            if not isinstance(eid, str) or not pat.match(eid):
                rep.err(where, f"{idf} {eid!r} does not match {s['id_pattern']}")
            elif eid in ids:
                rep.err(where, "duplicate id")
            elif eid in d["retired"]:
                rep.err(where, "id is retired and must not be reused")
            else:
                ids[eid] = e
            for key in e:
                if key not in s["fields"]:
                    rep.err(where, f"unknown field {key!r}")
            for key, spec in s["fields"].items():
                if key not in e:
                    if spec["required"]:
                        rep.err(where, f"missing required field {key!r}")
                    continue
                v = e[key]
                if is_empty(v):
                    if not spec["nullable"] and spec["type"] != "bool":
                        rep.err(where, f"field {key!r} must not be empty")
                    continue
                if not type_ok(spec["type"], v):
                    rep.err(where, f"field {key!r} must be of type {spec['type']}")
                    continue
                if "enum" in spec and v not in spec["enum"]:
                    rep.err(where, f"field {key!r} value {v!r} not in {spec['enum']}")
        index[name] = ids
    return index


def as_list(v) -> list:
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def check_references(index: dict[str, dict[str, dict]], rep: Report) -> None:
    for name, ids in index.items():
        s = SCHEMAS[name]
        for eid, e in ids.items():
            for key, spec in s["fields"].items():
                target = spec.get("ref")
                if not target or key not in e or target not in index:
                    continue
                for ref in as_list(e[key]):
                    if ref not in index[target]:
                        rep.err(f"{s['path']}:{eid}", f"{key} references unknown id {ref!r}")


def check_markdown_refs(index: dict[str, dict[str, dict]], rep: Report) -> None:
    all_ids = {i for ids in index.values() for i in ids}
    retired = set()
    for name, s in SCHEMAS.items():
        path = REPO_ROOT / s["path"]
        if path.exists():
            doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            retired.update(doc.get("retired_ids") or [])
    for md in sorted((REPO_ROOT / "docs").rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for m in MD_ID_RE.finditer(text):
            ref = m.group(0)
            if ref not in all_ids and ref not in retired:
                line = text.count("\n", 0, m.start()) + 1
                rep.err(f"{md.relative_to(REPO_ROOT)}:{line}", f"references unknown id {ref}")


def evidence_is_verified_quant(ev: dict) -> bool:
    return (
        ev.get("quantitative") is True
        and ev.get("read_level") == "FULL_TEXT"
        and ev.get("figure_verification") == "VERIFIED"
        and isinstance(ev.get("location"), dict)
        and ev["location"].get("type") in LOCATION_TYPE
        and not is_empty(ev["location"].get("ref"))
    )


def check_evidence_rules(index: dict[str, dict[str, dict]], rep: Report) -> None:
    sources, evidence = index.get("sources", {}), index.get("evidence", {})
    for eid, ev in evidence.items():
        where = f"docs/evidence/evidence.yaml:{eid}"
        src = sources.get(ev.get("source_id"))
        rl = ev.get("read_level")
        if src and rl in READ_LEVEL_RANK and src.get("read_level") in READ_LEVEL_RANK:
            if READ_LEVEL_RANK[rl] > READ_LEVEL_RANK[src["read_level"]]:
                rep.err(where, f"read_level {rl} exceeds source read_level {src['read_level']}")
        loc = ev.get("location")
        if isinstance(loc, dict) and loc:
            if loc.get("type") not in LOCATION_TYPE:
                rep.err(where, f"location.type must be one of {LOCATION_TYPE}")
            if is_empty(loc.get("ref")):
                rep.err(where, "location.ref must be given")
        if ev.get("quantitative") is True:
            if ev.get("figure_verification") == "NOT_APPLICABLE":
                rep.err(where, "quantitative evidence needs VERIFIED or UNVERIFIED_FIGURE")
            if ev.get("figure_verification") == "VERIFIED" and not evidence_is_verified_quant(ev):
                rep.err(where, "VERIFIED figure requires read_level FULL_TEXT and a location (§7)")
            if rl in ("ABSTRACT_ONLY", "SECONDARY_CITATION") and ev.get("evidence_strength") == "STRONG":
                rep.err(where, f"{rl} evidence cannot be STRONG for a quantitative claim (§9)")
        elif ev.get("quantitative") is False and ev.get("figure_verification") not in (None, "NOT_APPLICABLE"):
            rep.err(where, "non-quantitative evidence must have figure_verification NOT_APPLICABLE")
        sj = ev.get("strength_justification")
        if isinstance(sj, dict):
            for dim, why in sj.items():
                if dim not in STRENGTH_DIMENSIONS:
                    rep.err(where, f"strength_justification dimension {dim!r} not in {STRENGTH_DIMENSIONS}")
                if not isinstance(why, str) or not why.strip():
                    rep.err(where, f"strength_justification[{dim}] must be a one-line reason")


def check_claim_rules(index: dict[str, dict[str, dict]], rep: Report) -> None:
    evidence = index.get("evidence", {})
    for cid, c in index.get("claims", {}).items():
        where = f"docs/evidence/claims.yaml:{cid}"
        evs = [evidence[e] for e in as_list(c.get("evidence_ids")) if e in evidence]
        status = c.get("status")
        if status == "ESTABLISHED":
            ok = any(
                ev.get("evidence_strength") in ("STRONG", "MODERATE") and ev.get("read_level") == "FULL_TEXT"
                for ev in evs
            )
            if not ok:
                rep.err(where, "ESTABLISHED requires >= MODERATE evidence from FULL_TEXT sources (§10)")
        if status in ("ESTABLISHED", "SUPPORTED") and any(
            ev.get("evidence_strength") == "CONFLICTING" for ev in evs
        ):
            rep.err(where, f"CONFLICTING evidence cannot support {status} (§10)")


def check_decision_rules(index: dict[str, dict[str, dict]], rep: Report) -> None:
    evidence, sources = index.get("evidence", {}), index.get("sources", {})
    for did, d in index.get("decisions", {}).items():
        where = f"docs/decisions/decisions.yaml:{did}"
        status = d.get("status")
        if status == "PROVISIONAL":
            for key in ("provisional_rationale", "invalidation_conditions", "experiments_required"):
                if is_empty(d.get(key)):
                    rep.err(where, f"PROVISIONAL decision requires {key} (§35)")
        if status == "RESOLVED":
            who = d.get("resolved_by")
            if is_empty(who) or str(who).strip().lower() in ("agent", "claude", "ai"):
                rep.err(where, "RESOLVED requires resolved_by naming the human owner (§35)")
            if is_empty(d.get("resolved_date")):
                rep.err(where, "RESOLVED requires resolved_date")
            quant = [evidence[e] for e in as_list(d.get("evidence_ids")) if e in evidence and evidence[e].get("quantitative")]
            if quant:
                def weak(ev: dict) -> bool:
                    src = sources.get(ev.get("source_id"), {})
                    return (
                        ev.get("figure_verification") == "UNVERIFIED_FIGURE"
                        or ev.get("read_level") != "FULL_TEXT"
                        or src.get("read_level") != "FULL_TEXT"
                    )
                if all(weak(ev) for ev in quant):
                    rep.err(
                        where,
                        "RESOLVED decision relies solely on UNVERIFIED_FIGURE / non-FULL_TEXT "
                        "evidence for quantitative justification (§33.1)",
                    )


def check_requirement_rules(index: dict[str, dict[str, dict]], rep: Report) -> None:
    for rid, r in index.get("requirements", {}).items():
        where = f"docs/requirements/phase_e_requirements.yaml:{rid}"
        tt = r.get("traceability_type")
        if is_empty(r.get("decision_ids")) and tt != "ENGINEERING_ASSUMPTION":
            rep.err(where, "requirement must trace to a decision or be ENGINEERING_ASSUMPTION (§33.1)")
        if tt == "EVIDENCE" and is_empty(r.get("evidence_ids")):
            rep.err(where, "traceability_type EVIDENCE requires evidence_ids")


def check_since(ref: str, index: dict[str, dict[str, dict]], data: dict[str, dict], rep: Report) -> None:
    for name, s in SCHEMAS.items():
        try:
            old = subprocess.run(
                ["git", "show", f"{ref}:{s['path']}"],
                cwd=REPO_ROOT, capture_output=True, text=True, check=True,
            ).stdout
        except subprocess.CalledProcessError:
            continue  # registry did not exist at ref
        old_doc = yaml.safe_load(old) or {}
        old_ids = {e.get(s["id_field"]) for e in old_doc.get("entries") or [] if isinstance(e, dict)}
        current = set(index.get(name, {})) | set(data.get(name, {}).get("retired", []))
        for missing in sorted(i for i in old_ids - current if i):
            rep.err(s["path"], f"id {missing} existed at {ref} but was removed without being retired")


def init_registries() -> int:
    created = 0
    for name, s in SCHEMAS.items():
        path = REPO_ROOT / s["path"]
        if path.exists():
            print(f"exists, not touched: {s['path']}")
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        header = (
            f"# {name} registry — single source of truth ({s['section']} of CLAUDE.md).\n"
            "# `schema` is generated from scripts/check_registries.py; do not edit it by hand.\n"
            "# IDs are stable and never reused: move removed IDs to `retired_ids`.\n"
        )
        body = yaml.safe_dump(
            {"schema": schema_doc(name), "retired_ids": [], "entries": []},
            sort_keys=False, allow_unicode=True, width=100,
        )
        path.write_text(header + body, encoding="utf-8")
        print(f"created: {s['path']}")
        created += 1
    return created


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--init", action="store_true", help="create missing registries with zero entries")
    ap.add_argument("--since", metavar="GIT_REF", help="also check that no ID present at GIT_REF vanished")
    args = ap.parse_args()

    if args.init:
        init_registries()

    rep = Report()
    data = load_registries(rep)
    index = check_entries(data, rep)
    check_references(index, rep)
    check_markdown_refs(index, rep)
    check_evidence_rules(index, rep)
    check_claim_rules(index, rep)
    check_decision_rules(index, rep)
    check_requirement_rules(index, rep)
    if args.since:
        check_since(args.since, index, data, rep)

    counts = ", ".join(f"{n}={len(index.get(n, {}))}" for n in SCHEMAS)
    if rep.errors:
        print(f"REGISTRY INTEGRITY CHECK: FAIL ({len(rep.errors)} error(s)) [{counts}]")
        for e in rep.errors:
            print(f"  - {e}")
        return 1
    print(f"REGISTRY INTEGRITY CHECK: PASS [{counts}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
