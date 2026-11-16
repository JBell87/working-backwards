#!/usr/bin/env bash
# Prints a short reminder when a build-from-prfaq build is in progress.
# Claude Code adds a SessionStart hook's output to the session's context, so
# after compaction the orchestrator is pointed back at its state on disk.
# Prints nothing, and exits 0, when there is no build in progress.

dir="${CLAUDE_PROJECT_DIR:-$PWD}"
found=0
for state in "$dir"/docs/build/*/state.md; do
  [ -f "$state" ] || continue
  stage=$(grep -m1 -i '^| *Stage *|' "$state" | cut -d'|' -f3 | sed 's/^ *//; s/ *$//')
  case "$(printf '%s' "$stage" | tr '[:upper:]' '[:lower:]')" in
    done|"") continue ;;
  esac
  if [ "$found" -eq 0 ]; then
    echo "A build-from-prfaq build is in progress in this repository, and earlier conversation may have been compacted."
    echo "Before doing anything else: load the build-from-prfaq skill again, then read the state file and the last 30 lines of the ledger below, and check them against git."
    echo "You are the orchestrator: do not implement or fix code yourself. Continue from the recorded point."
    found=1
  fi
  build=$(dirname "$state")
  echo "- ${build#"$dir"/}: stage \"$stage\" (state: ${state#"$dir"/}, ledger: ${build#"$dir"/}/ledger.md)"
done
exit 0
