# Google Ads Dummy API

A Python library that simulates the Google Ads API for development and testing purposes.

## Purpose

This library provides a realistic simulation of Google Ads API responses without requiring:
- Real Google Ads credentials
- Active campaigns or ad spend
- API quota consumption
- Network calls to Google services

**Use Case:** Develop and test marketing data pipelines, analytics systems, and campaign monitoring tools without depending on production Google Ads accounts.

## What It Simulates

- Campaign hierarchy (Account → Campaign → Ad Group → Ad)
- Realistic performance metrics (impressions, clicks, conversions, cost)
- Temporal variation (daily performance fluctuations)
- Standard Google Ads data structures

## Target Users

- Data engineers building marketing analytics pipelines
- Developers creating campaign monitoring tools
- Teams needing reproducible test data for CI/CD
- Students learning marketing technology stack

## Core Features

### Realistic Data Generation
- Campaign names using marketing terminology
- Metrics following realistic distributions (CTR: 2-5%, CVR: 5-15%)
- Calculated fields (CPA, ROAS) derived from base metrics
- Temporal consistency (same campaign + date = same metrics)

### Validation
- All metrics validated at generation time
- Impossible values rejected (negative costs, CTR > 100%)
- Relationships enforced (clicks ≤ impressions)

### Flexible Configuration
- Configurable number of campaigns
- Adjustable metric ranges
- Date range selection
- Seed control for reproducibility

## API Overview

The library exposes a client interface that mirrors common Google Ads API patterns:

**Client instantiation** - Create a client instance with optional configuration

**Campaign retrieval** - List available campaigns with metadata

**Metrics queries** - Fetch performance data for specific campaigns and date ranges

**Batch operations** - Retrieve metrics for multiple campaigns efficiently

## Installation

Will be installable via pip once published. For development, install from source.

## Architecture

**Models layer** - Pydantic models for Campaign, AdGroup, Metrics with validation

**Generators layer** - Logic for creating realistic marketing data

**Client layer** - Public API that consumers interact with

**Configuration** - Centralized settings for data generation parameters

## Development Philosophy

This library prioritizes:
1. **Realism** - Data should resemble actual Google Ads responses
2. **Determinism** - Same inputs produce same outputs (testability)
3. **Validation** - Invalid data cannot be generated
4. **Simplicity** - Easy to integrate into existing projects

## Relationship to Real Google Ads API

This is a **simulation**, not a wrapper. It does not:
- Connect to Google services
- Require authentication
- Respect Google Ads API structure exactly
- Support all Google Ads features

It **does** provide:
- Similar data structures for common use cases
- Realistic metric relationships
- Sufficient fidelity for pipeline development
- Easy migration path (swap client implementation)

## Testing

The library includes comprehensive tests ensuring:
- Metrics stay within valid ranges
- Relationships between metrics are maintained
- Edge cases handled correctly (zero conversions, etc.)
- Deterministic output given same seed

## Future Enhancements

Potential additions based on user needs:
- Ad group and keyword level metrics
- Geographic and demographic breakdowns
- Hourly metrics (not just daily)
- Anomaly injection for testing alert systems

## Contributing

This is a personal project developed for portfolio purposes. Feedback and suggestions welcome.

## License

MIT License - free to use, modify, and distribute.

---

**Note:** This library was created as part of a data engineering portfolio project demonstrating:
- Python package development best practices
- Test-driven development
- API design
- Marketing technology domain knowledge
