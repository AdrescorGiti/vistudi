# ViStudi revision summary

- Updated the existing ViStudi skill and its production contract.
- Added exactly five permanent role README files under `agents/`, each with clear ownership, boundaries, inputs, workflows, handoff schemas, interfaces, completion criteria, and conflict/token-efficiency rules.
- Defined the coordinator as a separate director role, outside the fixed five-subagent count.
- Required dispatch to all five subagents for each ViStudi task; if the runtime cannot do that, the skill must report the limitation rather than simulate roles.
- Added orchestration, sequencing, handoff, and conflict-resolution rules; updated the root README to match.

The archive contains the revised existing skill, not a replacement project.
