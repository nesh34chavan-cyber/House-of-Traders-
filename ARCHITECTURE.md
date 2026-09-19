# Architecture Decision Record — V0.1

## Principles
1. Data, analysis, risk, and execution are separate services/modules.
2. No live execution in V0.1.
3. AI cannot invent live prices or probabilities; it consumes validated tool outputs.
4. Every strategy result must be reproducible from versioned data + parameters.
5. Broker adapters are replaceable.

## Planned data model
- instruments
- ticks
- candles
- sessions
- market_features
- signals
- strategies
- backtest_runs
- orders
- fills
- positions
- journal_entries
- research_runs

## Planned event flow
`provider -> normalizer -> validator -> event bus -> time-series store -> feature engine -> research/signal services -> risk -> paper execution -> journal`
