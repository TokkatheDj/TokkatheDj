# The Check That Deleted Everything

*A safety check ran inside the thing it was guarding, and recorded 1,794 files as deleted. Twice.*

Amigo, my local home assistant, lives in a private git repository. Next to it sits a
"ship kit": a one-page list of deploy steps I run from my phone, each one checked
against the live result. The ship kit has its own tests, and since early October a
**pre-commit hook** runs them before any commit that touches it. If the tests fail,
the commit is refused. It's the kind of safety net I'd recommend to anyone.

This is about the week that safety net became the danger, and what it took to fix it
properly rather than twice.

As with the rest of my projects, I built this with heavy AI assistance: an assistant
did the work in the repository, including the commits described here, working from my
direction. My part was deciding what counted as proof, and refusing to merge until we
had it.

---

## 1. The commit that "worked"

Changes to Amigo are made in **worktrees**: separate folders, one per change, each on
its own branch, so that several pieces of work can happen at once without trampling
each other. When a change is ready, a single fast-forward merge brings it into the main
branch.

On 16 October a small change to the health check was committed from one of those
worktrees. The hook ran the tests and refused the commit: two of them failed, with an
error about a commit inside a temporary folder. That looked like a flaky test, so the
test was investigated, given clearer error messages, fixed, and the commit tried again.
This time the hook ran the tests, they passed, and the commit went through. Every
signal said success.

Then `git status` in that folder came back looking wrong. It listed a file called
`first.txt` that had never existed in the project, and almost every real file in
Amigo showed as *untracked*, as if git had never heard of them.

`git show --stat` on the new commit settled it:

> 1795 files changed, 13 insertions(+), **66606 deletions(-)**

The commit kept two files. It recorded the other **1,794** as deleted. Had that branch
been merged, the main copy of the project would have been emptied in one step, by a
commit whose every check had passed.

It was caught before anything was merged. The commit lived only on its side branch, the
main branch was untouched, and so was every file on disk. Resetting the branch to main
and re-committing the three files that were actually meant to change took a minute.
Working out *why* took longer.

## 2. Git hands a hook its repository

When git runs a hook, it tells the hook where it is. It exports environment variables:
`GIT_DIR` (which repository) and `GIT_INDEX_FILE` (which staging area). From a worktree,
that staging area is the worktree's own.

The ship kit's tests build **throwaway repositories** in a temporary folder and run real
git commands inside them, to prove the deploy runner behaves on real repos. One test's
first move is to create a file, `first.txt`, and commit it.

Every one of those git commands **inherited the hook's variables**. So "commit
`first.txt` in my throwaway repo" really meant "make `first.txt` the entire contents of
the worktree's staging area". That happened during the *refused* attempts: the hook said
no, but its tests had already rewritten the staging area, and a refused commit doesn't
undo that. The commit that later went through was built from what they left behind. The
damage was in the world the tests had been handed, and nothing was looking there.

That's the part worth remembering. **A safety net runs inside the thing it protects, and
it inherits that thing's context.** Nobody wrote code to touch the real repository. The
environment did it quietly, because it was there.

The fix was three lines at the top of the test file: drop every `GIT_*` variable before
any test runs. A note went into the assistant's working memory: *any test that starts
git must clear these first.*

## 3. It came back through a different door

Two days later, on 18 October, it happened again.

Another session working on the same project had, in the meantime, added new tests to the
*other* test file, the health check's. They also built throwaway repositories with real
git. They didn't have the three lines. Committing from a worktree, the hook ran them, and
this time the staging area was rewritten as **1,892 deletions**.

The only reason nothing was recorded the second time is luck in how it failed. The nested
commit tripped over the hook itself, the tests failed, and the hook refused the commit.
Again nothing had reached main, and resetting the staging area put it right.

The lesson of the first fix was *each test file must protect itself*. The second
incident showed what that lesson is worth: it holds until somebody writes the next test
file. A fix that has to be remembered in every new place isn't a fix. It's a habit, and
habits don't transfer between sessions or between people.

## 4. Fixing it where it enters

So the third fix went to the boundary, the one place every test passes through: the hook.

- **The hook is now under version control.** It had only ever existed inside `.git/`,
  where git doesn't track it, so it couldn't be reviewed, tested or restored. It now
  lives in the repository and is installed by one ship-kit step that checks the
  installed copy is byte-for-byte identical.
- **It reads what's staged first, then forgets which repository it's in.** It unsets
  every `GIT_*` variable *before* any test runs. No test file, existing or future, can
  inherit the repository again.
- **A test pins that order.** It checks the hook reads the staged files before clearing
  anything, and clears before running anything. Then it runs the clearing line in Git's
  own shell with fake variables set, and proves they're gone.
- **Every merge step now counts the files.** After merging, it checks the main branch
  still holds the whole project (1,790 or more), not just that the merge "succeeded".

## What I took from it

**Succeeded is not correct, and refused is not harmless.** The refused attempts did the
damage; the bad commit passed every check and exited cleanly. What caught it was looking
at what the commit *contained*. A file count and a
`--stat` line are cheap, and now they run on every merge.

**Fix the boundary, not the instance.** The per-file guard was right and not enough. The
leak entered in exactly one place, and that's the place the fix belongs.

**Watch the context your checks run in.** Tests are usually trusted because they're
isolated. These weren't, and nothing in their output could have said so.

This carries into teaching. When a student gets a problem wrong in a new way, I can
correct that answer, and they'll make the same mistake on the next problem that looks
different. Or I can find the step in their method where the error got in, and fix it
there. The second takes longer and is the only one that lasts.

---

*Amigo's code is private; the ship kit and its health check are described in
[Shipping on a teacher's schedule](shipping-on-a-teachers-schedule.md). Every number
here comes from git's own output at the time.*
