# Architecture

## Goal

`audit-graph-explorer` models governance pressure as a relationship problem rather than only a record-keeping problem. The graph focuses on:

- users and teams
- assets and environments
- vendors and regions
- policies, approvals, exceptions, and incidents

The point is to make “how did this risk connect?” answerable in a few steps.

## Graph Shape

### Core entities

- `User`
- `Team`
- `Vendor`
- `Policy`
- `Approval`
- `Exception`
- `Incident`
- `Asset`
- `Region`
- `Environment`

### Relationship types

- `MEMBER_OF`
- `OPERATES_IN`
- `DEPLOYED_IN`
- `LOCATED_IN`
- `OWNED_BY`
- `SUBJECT_TO`
- `GUARDED_BY`
- `REQUESTED_FOR`
- `AFFECTS`
- `APPROVED_BY`
- `VIOLATES`
- `INTRODUCED_BY`
- `TRIGGERED_BY`
- `ASSIGNED_TO`
- `DEPENDS_ON`
- `USES`

## Investigation Patterns

### 1. Explanation path

Given an exception or incident, find the shortest path to a tier-0 asset, critical vendor, or policy owner.

### 2. Blast radius

Start from a vendor, approval, or asset and enumerate all downstream assets, exceptions, and incidents within a bounded number of hops.

### 3. Owner pressure

Group unresolved exceptions by owner and team so the next coordination move is obvious.

### 4. Approval lineage

Trace which approvals introduced or amplified policy debt.

## Local-First Design

The repo ships with:

- Cypher schema and seed files for a real Neo4j load
- a JSON snapshot that mirrors the graph
- Python logic for local shortest-path and blast-radius reporting
- PNG proof assets generated from the local report

This keeps the project usable without forcing a local Neo4j install on day one.

