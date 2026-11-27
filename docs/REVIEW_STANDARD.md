# Review standard

Every change that touches code is reviewed by someone other than its author before it merges. This is the standard the reviewer follows and the record they leave. A repository can replace it with its own by pointing `standard:` in `factory.yml` at another file.

## Who reviews

A reviewer who did not write the change. When agents do the work, the reviewer is a fresh agent that is given the diff and this standard, not the author's reasoning or conclusions.

## What the reviewer checks

1. **It does what it says.** Read the diff against the pull request's description. Anything the description does not mention is a finding.
2. **It is correct.** Follow the changed code through its callers and its failure paths. Run the tests that cover it.
3. **It is safe in the risk areas it touches.** The gate's summary lists each risk area and why it matters. Check that reason specifically.
4. **It can be undone.** Say how the change would be reversed if it turned out wrong. If it cannot be, say so.

A finding is blocking when the change would do harm, lose data, or not do what it claims. Anything else is a remark and does not block.

## The record

The reviewer posts a comment on the pull request. Its first line is the marker, with the full 40-character head commit that was reviewed:

```
<!-- independent-review sha=<head commit> verdict=pass -->
```

or

```
<!-- independent-review sha=<head commit> verdict=findings -->
```

Below the marker, in plain words: what was checked, and each blocking finding with the file and line.

Rules the gate enforces:

- **A record is for one commit.** A new commit needs a new review.
- **Every review is a new comment.** Never edit or replace an earlier record. A send-back is part of the change's history.
- **The newest record for the head commit wins.** Findings posted after a pass block again; a pass posted after findings clears them.
- **Only accounts that can write to the repository count.** The gate looks up what each account may do; being a member of the organisation is not enough. This is checked each time the gate runs, so a record from someone who has since lost write access stops counting, findings included. A record posted by a GitHub App does not count, with one exception: the automatic reviewer that `factory.yml` names (`automatic.account`), and only when the record carries the reviewer's signature. Its findings count at every level; its pass counts only for the levels `factory.yml` lists, and never clears findings a person recorded for the same commit. A repeat of a signed record it has already made is ignored.

## What this is and is not

It is a process control. It makes a second look the default and leaves a dated trail of what was found. It is not proof that a review happened: when the author and the reviewer share one login, that login can post the marker without one.
