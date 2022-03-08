### Labels

This section describes some GitHub labels (markers that can be associated in an issue) to be used on `kytos-ng` and `amlight` organizations, in order to facilitate when it comes to searching, planning, filtering, and prioritizing issues and features.

#### `priority_[critical|major|medium|low]`

Priority of the issue (or enhancement) in the following order: 

- `priority_critical` 
- `priority_major`
- `priority_medium`
- `priority_low`.

The critical level is recommended to be be used when an issue or feature needs absolute priority and immediate attention.

#### `[version]`

A `[version]` label is meant for planning the current issues and enhancements. For example, `2022.2` could be used on any of the repositories, that way, it is expected to be delivered in this version. If the scope changes, then the label version is supposed to be updated accordingly (removed or set a new future version). 

Kytos-ng and NApps use this version pattern `[year].[number].[patch]`, the number of releases depend on what is being planned for every year. The `[patch]` number should only be incremented when a patch is indeed needed, for instance, when a major bug fix is needed after a version has been released. 

Contributors should prioritize issues and enhancements that have a planned version and based on their priority value, if there is no version set yet, then a `future_release` (string) label should be used, and then replaced as soon as the team is done planning the scope of the upcoming version.

#### Epic

A label `epic_[.*]` can also be used to represent an epic, which represents an objective or major functionality that is expected to be delivered. Depending on the scope of an epic, it can span across multiple repositories.

##### Examples

- `epic_INT`: An epic for supporting serializing, installing, and pushing INT entries via OpenFlow on NoviFlow switches.
- `epic_fast_convergence`: An epic for fast convergence in the network by having more parallel events events and related optimizations
- `epic_liveness_detection_lldp`: An epic for link liveness detection, a first iteration, via LLDP.
- `epic_liveness_detection_bfd`: An epic for link liveness detection, a second iteration, via BFD on switches that support it, expected to be less CPU intensive.

#### `in_progress`

A label `in_progress` should be added when a developer starts to work on an issue or feature, and when its gets closed the label should be removed. This workflow ideally should be automated by GitHub actions, whenever a PR closes an associated issue then the `in_progress` label should be removed.

Also, one GitHub Kanban board with epics that are planned for the current year will be used to provide a high level view of the progress. Every card on this board will move in the board as progress is made, and on each card there will be links for the filters to find out more information about the features and issues associated with an epic. In the long term, automation might be added to facilitate adding cards.

#### `blocked`

If you are working on an issue or feature and you can't make progress because of an unexpected issue then the `blocked` label should be added, and it's encouraged to add comments in the issue explaining why it's blocked.

#### `enhancement`

The `enhancement` label should be used for new features or improvements.

#### `bug`

This a label is for defects and problems.

#### `documentation`

This label should be used for `documentation` related tasks.

#### `duplicate`

This is a label to mark if an issue is duplicate.

#### `good first issue`

The `good first issue` label is meant to be used for issues that are good for new contributors.

### GitHub Search

This subsection illustrates practical queries examples using [GitHub Search `[1]`](https://github.com/search).

##### Examples

* All `kytos-ng` `2022.2` open issues:
  * [org:kytos-ng is:issue state:open label:2022.2](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+state%3Aopen+label%3A2022.2)
* All `kytos-ng` `2022.2` `in_progress` issues:
  * [org:kytos-ng is:issue state:open label:2022.2 label:in_progress](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+state%3Aopen+label%3A2022.2+label%3Ain_progress)
* All `kytos-ng` `2022.2` `in_progress` issues of an epic `xyz`:
  * [org:kytos-ng is:issue state:open label:2022.2 label:in_progress label:epic_xyz](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+state%3Aopen+label%3A2022.2+label%3Ain_progress+label%3Aepic_xyz)
* All `kytos-ng` `2022.2` closed issues:
  * [org:kytos-ng is:issue state:closed label:2022.2](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+state%3Aclosed+label%3A2022.2)
* All `kytos-ng` `2022.2` `priority_critical` open issues:
  * [org:kytos-ng is:issue state:open label:2022.2 label:priority_critical](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+state%3Aopen+label%3A2022.2+label%3Apriority_critical)
* All `kytos-ng` closed issues between two dates, for instance, `2022-02-01` and `2022-02-10`:
  * [org:kytos-ng is:issue state:closed closed:2022-02-01..2022-02-10](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+state%3Aclosed+closed%3A2022-02-01..2022-02-10)
* All `kytos-ng` `2022.2` issues that don't have an assignee yet:
  * [org:kytos-ng is:issue no:assignee label:2022.2](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+no%3Aassignee+label%3A2022.2)
* All PRs (Pull Requests) that were merged between `2022-02-01` and `2022-02-10`:
  * [org:kytos-ng is:pr merged:2022-02-01..2022-02-10](https://github.com/search?q=org%3Akytos-ng+is%3Apr+merged%3A2022-02-01..2022-02-10)

You can adapt any of these filters directly on the GitHub Search webpage in left upper corner of the toolbar. For more information on how to use other query parameters and values, [check out this documentation `[2]`](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests).

### References

- `[1]` GitHub Search. https://github.com/search.
- `[2]` GitHub Searching issues and PRs. https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests
