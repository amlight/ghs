<div align="center">
  <h1><code>ghs</code></h1>

  <strong>GitHub Scripts</strong>
</div>

## Overview

This repository contains a CLI application `ghs` (GitHub Scripts), that you can use for day-to-day filtering and operations that you might need to do as a contributor or developer at AmLight. This tool and the GitHub related information on this repository are meant to facilitate dealing with the following points:

- Provide progress visibility for a specific GitHub label of an organization
- Manage GitHub label creation of an organization and its repositories
- Filter issues and pull requests of repositories given a label and available states such as open/closed
- Standardize certain labels that our team should typically use to facilitate scope planning and prioritization

## GitHub Labels

This [labels.md document](./docs/labels.md) provides information about how labels are being used for overall organization, planning, version releases, prioritization, and how to search issues using GitHub web search. 

## `ghs`

If you need to do bulk operations on GitHub such as creating labels or if you need to search or perform other operations from a terminal `ghs` can help with that, by interfacing with GitHub API. If you need a new functionality that will be used periodically, it's worth adding a function and command for it.

## How to install `ghs`

Pre requisites:

- Make sure you have Python 3.9 (this is the current version being supported)
- Activate your virtualenv

To install `ghs`:

- `pip install -e .`

After that, you should have `ghs` available in your PATH once you source your shell.

## How to use

### Authentication

GitHub API is public, it doesn't require authentication, but for certain operations like creating and deleting resources like labels you'll [need to use and create a personal authentication token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token). Once you have the token, export this `GH_TOKEN` environment variable with your token value.

### Getting help

`ghs --help` 

### Examples

#### Listing labels of an organization

- List all labels of all repositories of an organization:

```
ghs org_repos_labels kytos-ng
```
- List specific labels of certain repositories (`flow_manager`, `mef_eline`) of an organization:

```
ghs org_repos_labels kytos-ng --included_repos="['flow_manager', 'mef_eline']" --included_labels="['documentation']"
```

#### Creating labels

- Create a label on all repositories of an organization (`kytos-ng`):

```
ghs org_repos_labels_create kytos-ng 2022.2 --description="Kytos-ng 2022.2"
```

- Create a label on specific repositories (`flow_manager`, `topology`) of an organization (`kytos-ng`):

```
ghs org_repos_labels_create kytos-ng 2022.2 --description="Kytos-ng 2022.2" --included_repos="['flow_manager', 'topology']"
```

#### Deleting labels

When deleting a resource, `ghs` will always require explicit values to avoid unexpected deletions but there aren't any confirmations, so if you're going to delete, make sure to make a get operation first to confirm the values that would be targeted.

- Delete label `xyz` on all repositories of an organization (`kytos-ng`):

```
ghs org_repos_labels_delete kytos-ng "['xyz']"
```

- Delete label `xyz` on specific repositories (`flow_manager`) of an organization (`kytos-ng`):

```
ghs org_repos_labels_delete kytos-ng "['xyz']" --included_repos="['flow_manager']"
```

#### Searching

The search functionality accepts and passes all parameters to [GitHub GET /search/issues](https://docs.github.com/en/rest/reference/search#search-issues-and-pull-requests), [so all upstream query parameters are supported](https://docs.github.com/en/search-github/searching-on-github/searching-issues-and-pull-requests). Keep in mind that GitHub search API returns at most `1000` results, so if you have a broad search expression it'll return partial results.

- Search `kytos-ng` `2022.2` labelled issues:

```
ghs search 'org:kytos-ng label:2022.2 is:issue'
```

To check progress of the number of issues, the response will have a `stats` property that shows the number of open and closed issues and the progress (closed/open), so any progress that you are interested in checking you can have it when you narrow down the filter accordingly.

```
  "stats": {
      "closed": 1,
      "open": 3,
      "progress": 0.3333333333333333
  }
```
