### Changelog

All notable changes to this project will be documented in this file. Dates are displayed in UTC.

#### [2.1.0](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v2.0.6...v2.1.0)

> 6 May 2026

- **security**: bump `requests` to `^2.33.0` — fixes insecure temp file reuse in `extract_zipped_paths()` (CVE Dependabot #18)
- **security**: bump `pytest` to `^9.0.3` — fixes vulnerable `tmpdir` handling (Dependabot #20)
- **security**: bump `black` to `^26.3.1` — fixes arbitrary file writes via unsanitized cache file name (Dependabot #16)
- **security**: `pygments` updated to `2.20.0` via transitive dep — fixes ReDoS via inefficient GUID regex (Dependabot #19)
- **breaking**: minimum Python version raised from 3.9 to 3.10 (Python 3.9 reached EOL October 2025)
- **fix**: `logging.basicConfig()` removed from module level — the SDK no longer hijacks the host application's root logger; use `logging.getLogger("api-to-dataframe")` to configure SDK logs
- **fix**: `raise ValueError` now includes the error message so callers catching the exception can inspect `str(e)`
- **fix**: `retries=0` no longer silently returns `None`; validation now requires `retries >= 1`
- **fix**: `bool` values are now rejected for `retries`, `initial_delay`, and `connection_timeout` (Python `bool` is a subclass of `int`)
- **fix**: retry decorator logic changed from `if / if / elif` to `if / elif / elif` (no behavior change, but eliminates dead code path)
- **change**: `connection_timeout` default raised from `1` to `10` seconds
- **chore**: added `__init__.py` to `models/` and `controller/` packages
- **chore**: removed spurious `logging = "^0.4.9.6"` PyPI dependency (stdlib `logging` is used)
- **chore**: CI/CD workflows updated from Python 3.9 to Python 3.10

#### [2.0.6](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v2.0.5...v2.0.6)

> January 2026

- chore: update `pyproject.toml` classifiers and metadata

#### [2.0.5](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v2.0.4...v2.0.5)

> January 2026

- chore: update dev dependencies (`pytest`, `requests`, `pandas`, `coverage`, `poetry-dynamic-versioning`)
- fix: update `poetry` install command in CI workflow
- tests: refactor `ClientBuilder` test suite

#### [2.0.4](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v2.0.3...v2.0.4)

> 2025

- chore: dependency maintenance (`pandas`, `pytest`, `requests`, `coverage`, `pylint`, `poetry-dynamic-versioning`)

#### [2.0.3](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v2.0.2...v2.0.3)

> 2025

- chore: dependency maintenance

#### [2.0.2](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v2.0.1...v2.0.2)

> 2025

- chore: version bump

#### [2.0.1](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v2.0.0...v2.0.1)

> 2025

- chore: dependency maintenance (`coverage`, `pylint`, `poetry-dynamic-versioning`)

#### [2.0.0](https://github.com/IvanildoBarauna/api-to-dataframe/compare/v1.5.2...v2.0.0)

> 2025

- **breaking**: removed OpenTelemetry integration (`otel-wrapper` dependency dropped); the library returns to a zero-observability-dependency model
- The public API surface (`ClientBuilder`, `RetryStrategies`) is unchanged from 1.x

#### [1.5.0](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.4.0...1.5.0)

> 10 March 2025

- feature: Comprehensive OpenTelemetry integration with otel-wrapper:
  - Added detailed tracing for all operations (HTTP requests, dataframe conversions, retries)
  - Added metrics for performance monitoring and error tracking
  - Added structured logging with contextual information
  - Improved error handling with detailed error context
  - Complete observability across all components using otel-wrapper

#### [1.4.0](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.11...1.4.0)

> 10 March 2025

- feature: add otel-wrapper
- feature: update logging implementation and version bump
- chore: deps
- chore: bump version

#### [1.3.11](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.10...1.3.11)

> 24 September 2024

- chore(deps-dev): bump pylint from 3.2.6 to 3.3.0 [`#64`](https://me.github.com/ivdatahub/api-to-dataframe/pull/64)
- chore(deps-dev): bump poetry-dynamic-versioning from 1.4.0 to 1.4.1 [`#63`](https://me.github.com/ivdatahub/api-to-dataframe/pull/63)
- chore(deps-dev): bump pytest from 8.3.2 to 8.3.3 [`#62`](https://me.github.com/ivdatahub/api-to-dataframe/pull/62)
- feature: added max of retries for protect APIServer [`#60`](https://me.github.com/ivdatahub/api-to-dataframe/pull/60)
- Update CI.yaml [`d423835`](https://me.github.com/ivdatahub/api-to-dataframe/commit/d4238353d9ef42adf7ced8ec46d65277e0bfc68e)
- Update CI.yaml [`378ba5d`](https://me.github.com/ivdatahub/api-to-dataframe/commit/378ba5d67237a2486ad2f2a40c3f348ad08de5b7)
- feature: excessive logs remove [`ee8f3ad`](https://me.github.com/ivdatahub/api-to-dataframe/commit/ee8f3ad02cf805fa752d42b3ffc11d76dd2030d5)

#### [1.3.10](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.9...1.3.10)

> 25 August 2024

- chore: bump version [`2c9f68b`](https://me.github.com/ivdatahub/api-to-dataframe/commit/2c9f68bf4f27a558c3cca6676c630a46fb754561)
- fix: log to quantity of reetries [`54a6bc5`](https://me.github.com/ivdatahub/api-to-dataframe/commit/54a6bc5d0d8fd809db62e67140e1954f7a06a920)

#### [1.3.9](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.8...1.3.9)

> 25 August 2024

- docs: adjusts README examples [`0df8389`](https://me.github.com/ivdatahub/api-to-dataframe/commit/0df8389c8558e8b472a037b0b15327d08d051460)

#### [1.3.8](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.7...1.3.8)

> 25 August 2024

- docs: Tables for better compreension of retry strategies [`54635cb`](https://me.github.com/ivdatahub/api-to-dataframe/commit/54635cbd2c391e990705558c261047d69e23f4da)
- feature: adjusts retry strategies [`0320bcf`](https://me.github.com/ivdatahub/api-to-dataframe/commit/0320bcfc87329b3c7970644f8619b3c0da0bc6b0)
- feature: added max of retries for protect APIServer [`8f46f1b`](https://me.github.com/ivdatahub/api-to-dataframe/commit/8f46f1b646b2e7763c2c9c60c171153f07a0c852)

#### [1.3.7](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.6...1.3.7)

> 9 August 2024

- Update pyproject.toml [`0c6965c`](https://me.github.com/ivdatahub/api-to-dataframe/commit/0c6965c2f2c36bdf9c09b900b184fccd3c02168f)
- Merge pull request #59 from IvanildoBarauna/dependabot/pip/black-24.8.0 [`1d38f46`](https://me.github.com/ivdatahub/api-to-dataframe/commit/1d38f46f49b63ec3eaa77164d64f9f78bfba5060)
- chore(deps-dev): bump coverage from 7.5.4 to 7.6.1 [`a049d29`](https://me.github.com/ivdatahub/api-to-dataframe/commit/a049d29320524434bcd1311516ef0d755fc89b1a)

#### [1.3.6](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.5...1.3.6)

> 9 August 2024

- chore(deps-dev): bump black from 24.4.2 to 24.8.0 [`828bfa4`](https://me.github.com/ivdatahub/api-to-dataframe/commit/828bfa430731e138e49e9755f54b18cad06ea7f4)
- Update pyproject.toml [`7cc8943`](https://me.github.com/ivdatahub/api-to-dataframe/commit/7cc8943e94131aed315393d92f744e052055d382)
- Merge pull request #57 from IvanildoBarauna/dependabot/pip/pytest-8.3.2 [`16238c9`](https://me.github.com/ivdatahub/api-to-dataframe/commit/16238c934a54382a4ae231e7bd2003907b0181ce)

#### [1.3.5](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.4...1.3.5)

> 29 July 2024

- feature: env setup on workflow [`#56`](https://me.github.com/ivdatahub/api-to-dataframe/pull/56)
- chore(deps-dev): bump pytest from 8.3.1 to 8.3.2 [`586b6c4`](https://me.github.com/ivdatahub/api-to-dataframe/commit/586b6c4266fee69567e92faf6fd228b1dcaafe54)
- chore: bump version [`b7c4356`](https://me.github.com/ivdatahub/api-to-dataframe/commit/b7c43562fc4cd7823ea60b1bdeb209850599bd82)

#### [1.3.4](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.3...1.3.4)

> 24 July 2024

- feature: env setup on workflow [`efe8464`](https://me.github.com/ivdatahub/api-to-dataframe/commit/efe84645806bda0d43242be0f332b68e6ee266a3)
- chore: Update repository on Workflow [`aea6ac9`](https://me.github.com/ivdatahub/api-to-dataframe/commit/aea6ac990476f9967c20e32fc5c537e01b04e565)
- Merge pull request #55 from IvanildoBarauna/dependabot/pip/pylint-3.2.6 [`77558e2`](https://me.github.com/ivdatahub/api-to-dataframe/commit/77558e21a1b453d7688ad9c6faa09462b28d56af)

#### [1.3.3](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.2...1.3.3)

> 22 July 2024

- chore(deps-dev): bump pylint from 3.2.5 to 3.2.6 [`955bc78`](https://me.github.com/ivdatahub/api-to-dataframe/commit/955bc78ff1de5d250fe1d5bf3ce83bd56744e9d1)
- Update pyproject.toml [`7041393`](https://me.github.com/ivdatahub/api-to-dataframe/commit/704139378e4cde53eba160c138cf98f30393d63e)
- Merge pull request #54 from IvanildoBarauna/dependabot/pip/pytest-8.3.1 [`cfd1a87`](https://me.github.com/ivdatahub/api-to-dataframe/commit/cfd1a87d079fd4881249e2e9d71cf2502715bc68)

#### [1.3.2](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.1...1.3.2)

> 22 July 2024

- fix: remove logs for test [`#52`](https://me.github.com/ivdatahub/api-to-dataframe/pull/52)
- chore(deps-dev): bump pytest from 8.2.2 to 8.3.1 [`0ee32d5`](https://me.github.com/ivdatahub/api-to-dataframe/commit/0ee32d5e521729899d37a8c2954a5786f8bce93c)
- Update pyproject.toml [`677937c`](https://me.github.com/ivdatahub/api-to-dataframe/commit/677937cfdd949d0919419789255024b0f0418b8e)

#### [1.3.1](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.3.0...1.3.1)

> 8 July 2024

- feat: Improve Docs, fix level logger to INFO and remove _get_response_data [`28f13c8`](https://me.github.com/ivdatahub/api-to-dataframe/commit/28f13c86907dac76250e16a54bb017521014e4fd)

#### [1.3.0](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.2.3...1.3.0)

> 8 July 2024

- feat-StableVersion [`#50`](https://me.github.com/ivdatahub/api-to-dataframe/pull/50)
- [NEWS] Evoluted to Beta Pypi Version [`#48`](https://me.github.com/ivdatahub/api-to-dataframe/pull/48)
- chore: black + pylint conventions [`fa342e0`](https://me.github.com/ivdatahub/api-to-dataframe/commit/fa342e016bfcc1adb2f9665a21ecf4eed3f60d8d)
- chore: Added dev deps + added .pre-commits [`a0d73cc`](https://me.github.com/ivdatahub/api-to-dataframe/commit/a0d73ccf3bb4f2873c916b5780062813e4cdbe16)
- feature: implement logger [`43cfabd`](https://me.github.com/ivdatahub/api-to-dataframe/commit/43cfabde823d3de837a020a1b97813e5bea95fef)

#### [1.2.3](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.2.2...1.2.3)

> 23 June 2024

- FEATURE: Improve Development Experience for use api-to-dataframe [`#47`](https://me.github.com/ivdatahub/api-to-dataframe/pull/47)
- feature [`18106dd`](https://me.github.com/ivdatahub/api-to-dataframe/commit/18106dd2dc85f5042a81a389c14f110d98c20bbd)

#### [1.2.2](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.2.1...1.2.2)

> 23 June 2024

- chore: Update Notebook [`#45`](https://me.github.com/ivdatahub/api-to-dataframe/pull/45)
- feat: Update name param to initial_delay [`1f75da0`](https://me.github.com/ivdatahub/api-to-dataframe/commit/1f75da0bd31b8f127cc68200ac2486f07ad1903a)
- docs: Update Code Guide [`f656362`](https://me.github.com/ivdatahub/api-to-dataframe/commit/f656362f7052c415cdb2b4100c0f3c8306a2dff0)

#### [1.2.1](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.2.0...1.2.1)

> 23 June 2024

- feat: Initial development of Retry Strategies [`#44`](https://me.github.com/ivdatahub/api-to-dataframe/pull/44)
- chore: Update Notebook [`274fad5`](https://me.github.com/ivdatahub/api-to-dataframe/commit/274fad59c04b5b1ebbaf72a3e6e3a3ed15b138f7)
- Update pyproject.toml [`c36956a`](https://me.github.com/ivdatahub/api-to-dataframe/commit/c36956a5b38369191b10527afb8eabafd63f5715)

#### [1.2.0](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.1.0...1.2.0)

> 21 June 2024

- FEATURE/Added Timeout and raises in Exceptions case for GetApiData [`#43`](https://me.github.com/ivdatahub/api-to-dataframe/pull/43)
- feat: added functional tests on jupyter notebook [`af8462b`](https://me.github.com/ivdatahub/api-to-dataframe/commit/af8462bfc966c4796939977d3646dce9bf322c95)
- Update notebooks and evoluted project for Alpha phase [`7011b6d`](https://me.github.com/ivdatahub/api-to-dataframe/commit/7011b6de2fa78c3fe2f31cc176e38268ad2a1453)
- chore: Update Documentation + set quantity of retry to 3 [`291b47a`](https://me.github.com/ivdatahub/api-to-dataframe/commit/291b47a8a4ea5e4b24042b19126d4e3d6cca1b8d)

#### [1.1.0](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.0.3...1.1.0)

> 16 June 2024

- 💻 FEATURE/Remove Unecessary Packages for better development experience [`#42`](https://me.github.com/ivdatahub/api-to-dataframe/pull/42)
- testes: increase coverage for +90% [`8d21675`](https://me.github.com/ivdatahub/api-to-dataframe/commit/8d21675bc2b51893340f8489039aa815a9eb421c)
- feat: Added timeout param [`04e3034`](https://me.github.com/ivdatahub/api-to-dataframe/commit/04e30348db0ae529c53f08f158112c25d63cbd1e)
- docs: Added headers in Code Guide [`bc515a6`](https://me.github.com/ivdatahub/api-to-dataframe/commit/bc515a6a0fa0c7b6ab380c80c60dbe99f3370ec8)

#### [1.0.3](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.0.2...1.0.3)

> 15 June 2024

- docs: Update Readme + Added Docs Strings + Include only constructor [`#41`](https://me.github.com/ivdatahub/api-to-dataframe/pull/41)
- chore: remove unecessary packages for better dev experience [`a9608a6`](https://me.github.com/ivdatahub/api-to-dataframe/commit/a9608a6b06d06f7ebc40fbd5ee48220a2aec9343)

#### [1.0.2](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.0.1...1.0.2)

> 15 June 2024

- chore: flexibilized version of dependencies [`#36`](https://me.github.com/ivdatahub/api-to-dataframe/pull/36)
- docs: Update Readme + Added Docs Strings + Include only constructor [`ff00acb`](https://me.github.com/ivdatahub/api-to-dataframe/commit/ff00acb07fa04ef54c995143316e39f7cef5b78b)

#### [1.0.1](https://me.github.com/ivdatahub/api-to-dataframe/compare/1.0.0...1.0.1)

> 13 June 2024

- feat: change entrypoint of lib + split responsabilites in components [`#29`](https://me.github.com/ivdatahub/api-to-dataframe/pull/29)
- chore: flexibilized version of dependencies [`222b371`](https://me.github.com/ivdatahub/api-to-dataframe/commit/222b37149f20a29f3753a31b5e24c9bee03b5024)

### [1.0.0](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.1.0...1.0.0)

> 13 June 2024

- chore: rename step for generate tag [`8e72c3b`](https://me.github.com/ivdatahub/api-to-dataframe/commit/8e72c3b42ef6dfd338e9ec7f6fa9e25a0d28ac91)
- chore: increment major version [`9e53660`](https://me.github.com/ivdatahub/api-to-dataframe/commit/9e536605d524f592e745cb95e11201f8606dec6e)

#### [0.1.0](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.11...0.1.0)

> 13 June 2024

- FEATURE-EntrypointDefinition [`#28`](https://me.github.com/ivdatahub/api-to-dataframe/pull/28)
- FEATURE-Update Badges [`#27`](https://me.github.com/ivdatahub/api-to-dataframe/pull/27)
- feat: change entrypoint of lib + split responsabilites in components [`7b53bc0`](https://me.github.com/ivdatahub/api-to-dataframe/commit/7b53bc0424a707cf05691c04ae33e663d3065897)
- feat: Class Methods Define + write tests [`fbbf03b`](https://me.github.com/ivdatahub/api-to-dataframe/commit/fbbf03b81221f28b7a7d338ce50dc2edb3330027)
- tests: remove src from imports for tests [`ff88f57`](https://me.github.com/ivdatahub/api-to-dataframe/commit/ff88f576a6856dfc0887b36bab06a1dd5075793f)

#### [0.0.11](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.10...0.0.11)

> 11 June 2024

- UpdateBadges [`#26`](https://me.github.com/ivdatahub/api-to-dataframe/pull/26)
- Added link to repo in README [`8df9697`](https://me.github.com/ivdatahub/api-to-dataframe/commit/8df9697f631755b625b9c0f9bcb9cdf8800dac6a)
- Update pyproject.toml [`f8c46d3`](https://me.github.com/ivdatahub/api-to-dataframe/commit/f8c46d3668f95c1d942df104457d61c45e8dd6a0)

#### [0.0.10](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.9...0.0.10)

> 11 June 2024

- UpdateReadme [`#25`](https://me.github.com/ivdatahub/api-to-dataframe/pull/25)
- Update Readme [`#23`](https://me.github.com/ivdatahub/api-to-dataframe/pull/23)
- feat VersionControlOnCd [`#22`](https://me.github.com/ivdatahub/api-to-dataframe/pull/22)
- UpdateBadges [`52f548d`](https://me.github.com/ivdatahub/api-to-dataframe/commit/52f548dccb42563fdc8623bf842659c7d5fecd38)
- chore: increment version [`79b83dd`](https://me.github.com/ivdatahub/api-to-dataframe/commit/79b83ddd400a7f0598e3d450253702567eae7ad6)

#### [0.0.9](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.8...0.0.9)

> 11 June 2024

- chore: added generate tags version [`#21`](https://me.github.com/ivdatahub/api-to-dataframe/pull/21)
- chore: .pre-commit config + version increment shell script added [`b831fe8`](https://me.github.com/ivdatahub/api-to-dataframe/commit/b831fe8e7e33057662f6aa07425b8e2f8ef4c7c4)
- fix: remove poetry version patch from CI [`2d54e7c`](https://me.github.com/ivdatahub/api-to-dataframe/commit/2d54e7c6a102f7952b77e8abfda44cd91f2ac7a0)
- chore: increment version [`48dfd07`](https://me.github.com/ivdatahub/api-to-dataframe/commit/48dfd07be26f798b57cb1f284b033bf397eace5e)

#### [0.0.8](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.7...0.0.8)

> 11 June 2024

- chore: Added Version Control on CD [`#20`](https://me.github.com/ivdatahub/api-to-dataframe/pull/20)
- fix: workflow formatting file [`8a219ed`](https://me.github.com/ivdatahub/api-to-dataframe/commit/8a219eddc5386366553294ae7dc1ed54498d0c65)
- chore: Join CI with CD [`a7afdd5`](https://me.github.com/ivdatahub/api-to-dataframe/commit/a7afdd5fe943f65a91339fee2e5c1db429df46ad)
- chore: added generate tags version [`9b1295f`](https://me.github.com/ivdatahub/api-to-dataframe/commit/9b1295f476ec842e7fd01d5720c5817abc64894a)

#### [0.0.7](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.6...0.0.7)

> 11 June 2024

- chore: increment version [`2186a17`](https://me.github.com/ivdatahub/api-to-dataframe/commit/2186a1722a945e9e384336777bba9d4a7c730d82)
- chore: remove gitactions user from CD [`aefdded`](https://me.github.com/ivdatahub/api-to-dataframe/commit/aefddedd0eb88329ace99088bf667008f4e8793e)

#### [0.0.6](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.5...0.0.6)

> 11 June 2024

- build(deps): bump packaging from 24.0 to 24.1 [`#5`](https://me.github.com/ivdatahub/api-to-dataframe/pull/5)
- feat AutoRelease [`#18`](https://me.github.com/ivdatahub/api-to-dataframe/pull/18)
- chore: added auto-release [`a94c79c`](https://me.github.com/ivdatahub/api-to-dataframe/commit/a94c79c7c4cca8cbc059ed2fcdeb8a62a910eaec)
- chore: Added Version Control on CD [`3ae2ec9`](https://me.github.com/ivdatahub/api-to-dataframe/commit/3ae2ec9c2d6b85f4bf193036c84d16504dbd587c)
- chore: increment version [`5d37d60`](https://me.github.com/ivdatahub/api-to-dataframe/commit/5d37d6090dc68b0103b366ac046f967ff7cd3110)

#### [0.0.5](https://me.github.com/ivdatahub/api-to-dataframe/compare/0.0.4...0.0.5)

> 11 June 2024

- feat AutoRelease [`#17`](https://me.github.com/ivdatahub/api-to-dataframe/pull/17)
- feat AutoRelease [`#16`](https://me.github.com/ivdatahub/api-to-dataframe/pull/16)
- feat AutoRelease [`#15`](https://me.github.com/ivdatahub/api-to-dataframe/pull/15)
- feat AutoRelease [`#14`](https://me.github.com/ivdatahub/api-to-dataframe/pull/14)
- feat AutoRelease [`#13`](https://me.github.com/ivdatahub/api-to-dataframe/pull/13)
- feat AutoRelease [`#12`](https://me.github.com/ivdatahub/api-to-dataframe/pull/12)
- Feature-AutoRelease [`#11`](https://me.github.com/ivdatahub/api-to-dataframe/pull/11)
- Feature-AutoReleases [`#10`](https://me.github.com/ivdatahub/api-to-dataframe/pull/10)
- chore: added auto-release [`3a78e8c`](https://me.github.com/ivdatahub/api-to-dataframe/commit/3a78e8cb3149f1a0de66b78e70e54b6708339d47)
- chore: added auto-release [`ae1a8eb`](https://me.github.com/ivdatahub/api-to-dataframe/commit/ae1a8ebad7bc6215300ee8bfef92d0b6f7b54342)
- chore: added auto-release [`62cbdab`](https://me.github.com/ivdatahub/api-to-dataframe/commit/62cbdabc1405abed50f404868f9f66776e18bd34)

#### [0.0.4](https://me.github.com/ivdatahub/api-to-dataframe/compare/v0.0.3...0.0.4)

> 11 June 2024

- FEATURES-Devops [`#9`](https://me.github.com/ivdatahub/api-to-dataframe/pull/9)
- HotFix: Setups and Initial Class [`#8`](https://me.github.com/ivdatahub/api-to-dataframe/pull/8)
- chore: Added dev-dependencies [`de95347`](https://me.github.com/ivdatahub/api-to-dataframe/commit/de953471beed22dc9a40a8a0dae9791722695d2d)
- chore: added auto-versioning [`54c4a34`](https://me.github.com/ivdatahub/api-to-dataframe/commit/54c4a34f320ac8350ae8ab0520140720219fc3c7)
- chore: added .idea [`702452d`](https://me.github.com/ivdatahub/api-to-dataframe/commit/702452d4c1c16787f83b38ac034161e26416ce7a)

#### [v0.0.3](https://me.github.com/ivdatahub/api-to-dataframe/compare/v0.0.2...v0.0.3)

> 10 June 2024

- chore: Remove OLD Setup format [`#7`](https://me.github.com/ivdatahub/api-to-dataframe/pull/7)
- Feature first build [`#6`](https://me.github.com/ivdatahub/api-to-dataframe/pull/6)
- feat: Add pip installation instructions to example notebook [`44a3eb7`](https://me.github.com/ivdatahub/api-to-dataframe/commit/44a3eb7f3856058bb9fbd77ae4258ac35e3c227d)
- chore: Bump version to v0.0.3 in pyproject.toml [`19a0f0a`](https://me.github.com/ivdatahub/api-to-dataframe/commit/19a0f0a9f66de8bbbdaeded80250552b9962eff4)
- chore: Update pyproject.toml to include "src" directory in packages [`7d36096`](https://me.github.com/ivdatahub/api-to-dataframe/commit/7d360968f8dc50f2b66f7ac7e855b3fb2e55183b)

#### [v0.0.2](https://me.github.com/ivdatahub/api-to-dataframe/compare/v0.0.1...v0.0.2)

> 10 June 2024

- Update Coverage [`#4`](https://me.github.com/ivdatahub/api-to-dataframe/pull/4)
- Update Readme [`#3`](https://me.github.com/ivdatahub/api-to-dataframe/pull/3)
- FEATURE: Initial SDK Setup [`#2`](https://me.github.com/ivdatahub/api-to-dataframe/pull/2)
- Setup PreBuild [`b771b8e`](https://me.github.com/ivdatahub/api-to-dataframe/commit/b771b8e71ca5d196c2b0771cfb4139fddc92c520)
- chore: Add pre-commit configuration file [`588178d`](https://me.github.com/ivdatahub/api-to-dataframe/commit/588178defc7df068a10a677e6d0d3691598e529d)

#### v0.0.1

> 7 June 2024

- Initial commit [`9259146`](https://me.github.com/ivdatahub/api-to-dataframe/commit/9259146d2dec1ec5e01cc0b709c825458ab3c9fe)
- chore: do not build [`6035295`](https://me.github.com/ivdatahub/api-to-dataframe/commit/6035295ff4954025c9c621157248953303355067)
- build: initial setup tests [`84ef25e`](https://me.github.com/ivdatahub/api-to-dataframe/commit/84ef25e824e527fbd7efa598fe7e3c031504c0c6)
