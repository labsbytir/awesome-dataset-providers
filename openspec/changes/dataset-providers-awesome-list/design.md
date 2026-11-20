# Design

## Context

Static awesome list repo. Python collector fetches data.gov organizations and Harvard Dataverse datasets, writes JSON and README.

## Goals / Non-Goals

**Goals:** reproducible data collection, readable awesome list.
**Non-Goals:** live hosting, full 300k dataset crawl.

## Decisions

- Use data.gov v4 API and Harvard Dataverse v1 API.
- Store raw JSON under data/.
- Generate README tables from JSON.

## Risks / Trade-offs

- API rate limits -> sleep between calls.
- Missing fields -> leave blank.
