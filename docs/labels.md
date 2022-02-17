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

#### Epics

A label `epic_[.*]` can also be used to represent an epic, which represents an objective or major functionality that is expected to be delivered. Depending on the scope on an epic, it can span across multiple repositories. For instance:

- `epic_INT`: An epic for supporting serializing, installing, and pushing INT entries via OpenFlow on NoviFlow switches.
- `epic_fast_convergence`: An epic for fast convergence in the network by having more parallel events events and related optimizations
- `epic_liveness_detection_lldp`: An epic for link liveness detection, a first iteration, via LLDP.
- `epic_liveness_detection_bfd`: An epic for link liveness detection, a second iteration, via BFD on switches that support it, expected to be less CPU intensive.

### Examples

This section illustrates practical queries examples using GitHub Search `[1]`:

* All `kytos-ng` `2022.2` open issues:
  * [org:kytos-ng is:issue state:open label:2022.2](https://github.com/search?q=org%3Akytos-ng+is%3Aissue+state%3Aopen+label%3A2022.2)
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


### References

`[1]` GitHub Search. https://github.com/search.
